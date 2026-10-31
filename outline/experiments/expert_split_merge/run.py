"""Run a single problem stream under one of three policies.

Policies
--------
- static-1   : one general mathematician handles every problem
- static-N   : two specialists (algebraist + geometer); router picks per-problem
- dynamic    : start with one mathematician; supervisor may SPLIT after a window
               and MERGE if a specialist starves; route to current roster

Outputs per run: a JSON file with per-problem records and aggregate metrics.
"""
from __future__ import annotations
import argparse
import json
import os
import time
from dataclasses import asdict, dataclass, field
from typing import Optional

import outline.experiments.expert_split_merge.client as ai
import outline.experiments.expert_split_merge.prompts as P
import outline.experiments.expert_split_merge.tasks as T


# ----------------------------- data classes -----------------------------

@dataclass
class Role:
    name: str
    charter: str
    pitfalls: str

    def system_prompt(self) -> str:
        return P.build_specialist_prompt(self.charter, self.pitfalls)


@dataclass
class StepRec:
    step: int
    pid: str
    domain_true: str
    routed_to: str
    response: str
    correct: bool
    in_tok: int
    out_tok: int
    latency_s: float
    event: str = ""  # "split", "merge", or ""


@dataclass
class RunRec:
    policy: str
    stream: str
    seed: int
    model: str
    steps: list[StepRec] = field(default_factory=list)
    decisions: list[dict] = field(default_factory=list)
    final_roster: list[str] = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.steps)

    @property
    def n_correct(self) -> int:
        return sum(1 for s in self.steps if s.correct)

    @property
    def total_in(self) -> int:
        return sum(s.in_tok for s in self.steps)

    @property
    def total_out(self) -> int:
        return sum(s.out_tok for s in self.steps)

    @property
    def total_latency(self) -> float:
        return sum(s.latency_s for s in self.steps)


# ----------------------------- helpers -----------------------------

def role_mathematician() -> Role:
    return Role(
        name="mathematician",
        charter="Solve any algebra, geometry, or arithmetic problem.",
        pitfalls="Read carefully — distinguish sum vs. product of roots; "
                 "distinguish radius vs. diameter; check units.",
    )


def role_generalist_probe() -> Role:
    """Bland generalist for the combo/prob probe — does NOT pre-encode the trap."""
    return Role(
        name="mathematician",
        charter="Solve any word problem in mathematics.",
        pitfalls="Read carefully and ignore irrelevant preamble before computing.",
    )


def static_two_probe() -> list[Role]:
    return [
        Role(
            name="combo",
            charter="Counting problems: arrangements, selections, subsets, "
                    "divisibility-counts.",
            pitfalls="'How many' means a COUNT, never a fraction. Distinguish "
                     "ordered vs. unordered, with vs. without repetition.",
        ),
        Role(
            name="prob",
            charter="Probability problems: fractions of favorable to total outcomes.",
            pitfalls="With vs. without replacement changes the denominator. "
                     "Reduce a/b to lowest terms before reporting a+b.",
        ),
    ]


def static_three_xhard() -> list[Role]:
    return [
        Role(
            name="combo",
            charter="Counting problems: arrangements, selections, distributions, "
                    "inclusion-exclusion, surjective maps, circular arrangements.",
            pitfalls="Distinguish ordered vs. unordered, with vs. without "
                     "repetition. For surjections: 3^n - C(3,1)2^n + C(3,2)1^n. "
                     "For circular: divide by rotations, not reflections, unless "
                     "stated otherwise.",
        ),
        Role(
            name="prob",
            charter="Probability problems: ratio of favorable to total outcomes; "
                    "report a+b for reduced fraction a/b.",
            pitfalls="With vs. without replacement changes the denominator. "
                     "Reduce a/b to LOWEST terms before reporting a+b. "
                     "Conditional probability: numerator and denominator both "
                     "restrict to the conditioning event.",
        ),
        Role(
            name="numth",
            charter="Number theory: divisor sums, Euler phi, modular exponentiation, "
                    "GCD, primes, Fermat's little theorem.",
            pitfalls="For sigma(N) = product over primes (p^(k+1)-1)/(p-1). "
                     "For phi(N) = N * product (1 - 1/p). For modular exponent "
                     "cycles: find the cycle length first.",
        ),
    ]


def role_generalist_xhard() -> Role:
    return Role(
        name="mathematician",
        charter="Solve any word problem in mathematics: combinatorics, "
                "probability, number theory.",
        pitfalls="Read carefully and ignore irrelevant preamble.",
    )


def static_two_ord_inv() -> list[Role]:
    return [
        Role(
            name="ordinal",
            charter="Position / sequence problems: 'k-th from front/back', "
                    "step-counting, wrap-around indexing.",
            pitfalls="Whether the starting position is itself counted; "
                     "1-indexed vs 0-indexed; symmetric formulas like "
                     "kth_from_front + kth_from_back = total + 1.",
        ),
        Role(
            name="inventory",
            charter="Cumulative inventory / depletion / arithmetic-of-amounts.",
            pitfalls="Maintain running balance step-by-step; deposits add and "
                     "withdrawals subtract; do not confuse 'first hour' with "
                     "'after the first hour'.",
        ),
    ]


def static_two() -> list[Role]:
    return [
        Role(
            name="algebraist",
            charter="Equation manipulation, polynomial roots, systems of equations, "
                    "function values.",
            pitfalls="When asked SUM of solutions of x^2=k for k>0, the answer is 0 "
                     "(roots are +/-sqrt(k)). Do not return only the positive root.",
        ),
        Role(
            name="geometer",
            charter="Lengths, areas, volumes, angles, Pythagorean reasoning.",
            pitfalls="Distinguish radius vs. diameter; if diameter d is given, "
                     "radius is d/2; area = pi r^2.",
        ),
    ]


def route(client: ai.Client, problem: T.Problem, roles: list[Role]) -> Role:
    """Use the model to pick a role. Falls back to roles[0] on parse failure."""
    if len(roles) == 1:
        return roles[0]
    domain_list = "\n".join(f"- {r.name}: {r.charter}" for r in roles)
    rprompt = P.ROUTER.format(domain_list=domain_list, problem=problem.question)
    rep = client.call(
        system="You are a careful router. Reply with the slug only.",
        user=rprompt,
        max_tokens=8,
    )
    pick = rep.text.strip().lower().split()[0] if rep.text.strip() else roles[0].name
    pick = pick.strip(".,:")
    for r in roles:
        if r.name.lower() == pick:
            return r
    # partial match fallback
    for r in roles:
        if pick.startswith(r.name.lower()) or r.name.lower().startswith(pick):
            return r
    return roles[0]


def supervisor_split(
    client: ai.Client,
    transcript_window: list[StepRec],
) -> Optional[list[Role]]:
    """Returns a new role list if SPLIT, else None."""
    summary = []
    for s in transcript_window:
        summary.append({
            "pid": s.pid,
            "domain_hint": s.domain_true,
            "response_excerpt": s.response[:280],
            "correct": s.correct,
        })
    user = (
        "Recent transcript window (last "
        f"{len(transcript_window)} problems):\n"
        + json.dumps(summary, indent=2)
    )
    rep = client.call(P.SUPERVISOR_SPLIT, user, max_tokens=600)
    try:
        obj = _extract_json(rep.text)
    except Exception:
        return None
    if obj.get("decision") != "SPLIT":
        return None
    out = []
    for r in obj.get("roles", []):
        if not all(k in r for k in ("name", "charter", "pitfalls")):
            continue
        out.append(Role(name=r["name"].lower().strip(), charter=r["charter"],
                        pitfalls=r["pitfalls"]))
    if len(out) >= 2:
        return out
    return None


def supervisor_merge(
    client: ai.Client,
    role_stats: dict[str, dict],
) -> Optional[Role]:
    user = "Specialist stats over the last window:\n" + json.dumps(role_stats, indent=2)
    rep = client.call(P.SUPERVISOR_MERGE, user, max_tokens=400)
    try:
        obj = _extract_json(rep.text)
    except Exception:
        return None
    if obj.get("decision") != "MERGE":
        return None
    r = obj.get("into_role", {})
    if not all(k in r for k in ("name", "charter", "pitfalls")):
        return None
    return Role(name=r["name"].lower().strip(), charter=r["charter"], pitfalls=r["pitfalls"])


def _extract_json(text: str) -> dict:
    """Tolerant JSON extractor — finds first {...} block."""
    start = text.find("{")
    if start < 0:
        raise ValueError("no json")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unterminated json")


# ----------------------------- runners -----------------------------

def run_once(
    policy: str,
    stream_name: str = "mixed",
    seed: int = 0,
    model: str = "claude-haiku-4-5",
    out_path: Optional[str] = None,
    split_window: int = 6,
    merge_window: int = 6,
    split_min_errors_in_window: int = 1,
    merge_min_starve: int = 2,
) -> RunRec:
    client = ai.Client(model=model)
    if stream_name == "mixed":
        stream = T.stream_mixed(seed=seed)
    elif stream_name == "drift":
        stream = T.stream_drift(seed=seed)
    elif stream_name == "hard":
        import outline.experiments.expert_split_merge.tasks_hard as TH
        stream = TH.stream_hard(seed=seed)
    elif stream_name == "noisy":
        import outline.experiments.expert_split_merge.tasks_hard as TH
        stream = TH.stream_noisy(seed=seed)
    elif stream_name == "probe":
        import outline.experiments.expert_split_merge.tasks_probe as TP
        stream = TP.stream_probe(seed=seed)
    elif stream_name == "ord_inv":
        import outline.experiments.expert_split_merge.tasks_ord_inv as TO
        stream = TO.stream_ord_inv(seed=seed)
    elif stream_name == "xhard":
        import outline.experiments.expert_split_merge.tasks_xhard as TX
        stream = TX.stream_xhard(seed=seed)
    else:
        raise ValueError(stream_name)

    if policy == "static-1":
        if stream_name == "xhard":
            roles = [role_generalist_xhard()]
        elif stream_name in ("probe", "ord_inv"):
            roles = [role_generalist_probe()]
        else:
            roles = [role_mathematician()]
    elif policy == "static-N":
        if stream_name == "probe":
            roles = static_two_probe()
        elif stream_name == "ord_inv":
            roles = static_two_ord_inv()
        elif stream_name == "xhard":
            roles = static_three_xhard()
        else:
            roles = static_two()
    elif policy == "dynamic":
        if stream_name == "xhard":
            roles = [role_generalist_xhard()]
        elif stream_name in ("probe", "ord_inv"):
            roles = [role_generalist_probe()]
        else:
            roles = [role_mathematician()]
    else:
        raise ValueError(policy)

    rec = RunRec(policy=policy, stream=stream_name, seed=seed, model=model)
    decision_offset = 0  # last index after which we evaluated supervisor

    for i, prob in enumerate(stream):
        chosen = route(client, prob, roles) if len(roles) > 1 else roles[0]
        sys_prompt = chosen.system_prompt()
        rep = client.call(sys_prompt, prob.question, max_tokens=400)
        ok = T.grade(rep.text, prob.answer)
        rec.steps.append(StepRec(
            step=i,
            pid=prob.pid,
            domain_true=prob.domain,
            routed_to=chosen.name,
            response=rep.text,
            correct=ok,
            in_tok=rep.input_tokens,
            out_tok=rep.output_tokens,
            latency_s=rep.latency_s,
        ))

        if policy == "dynamic":
            window = rec.steps[decision_offset:]
            # Try SPLIT only when we currently have a generalist
            if len(roles) == 1 and len(window) >= split_window:
                errs = sum(1 for s in window if not s.correct)
                # heterogeneity check: at least 2 distinct domains, each with >=2 tasks
                from collections import Counter as _C
                dom_counts = _C(s.domain_true for s in window)
                hetero_domains = sum(1 for v in dom_counts.values() if v >= 2)
                if hetero_domains >= 2 and errs >= split_min_errors_in_window:
                    new_roles = supervisor_split(client, window)
                    if new_roles is not None:
                        rec.decisions.append({
                            "step": i,
                            "type": "split",
                            "from": [r.name for r in roles],
                            "to": [r.name for r in new_roles],
                        })
                        roles = new_roles
                        rec.steps[-1].event = "split"
                        decision_offset = i + 1
                        continue
            # Try MERGE only when we currently have multiple specialists
            if len(roles) > 1 and len(window) >= merge_window:
                stats: dict[str, dict] = {r.name: {"n": 0, "correct": 0} for r in roles}
                for s in window:
                    if s.routed_to in stats:
                        stats[s.routed_to]["n"] += 1
                        stats[s.routed_to]["correct"] += int(s.correct)
                starving = [name for name, s in stats.items() if s["n"] < merge_min_starve]
                if starving:
                    merged = supervisor_merge(client, stats)
                    if merged is not None:
                        rec.decisions.append({
                            "step": i,
                            "type": "merge",
                            "from": [r.name for r in roles],
                            "to": [merged.name],
                            "stats": stats,
                        })
                        roles = [merged]
                        rec.steps[-1].event = "merge"
                        decision_offset = i + 1
                        continue

    rec.final_roster = [r.name for r in roles]
    if out_path:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w") as f:
            json.dump({
                "policy": rec.policy,
                "stream": rec.stream,
                "seed": rec.seed,
                "model": rec.model,
                "n": rec.n,
                "n_correct": rec.n_correct,
                "accuracy": rec.n_correct / max(rec.n, 1),
                "total_in_tok": rec.total_in,
                "total_out_tok": rec.total_out,
                "total_latency_s": rec.total_latency,
                "final_roster": rec.final_roster,
                "decisions": rec.decisions,
                "steps": [asdict(s) for s in rec.steps],
            }, f, indent=2)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", required=True, choices=["static-1", "static-N", "dynamic"])
    ap.add_argument("--stream", default="mixed",
                    choices=["mixed", "drift", "hard", "noisy", "probe"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--model", default="claude-haiku-4-5")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    out = args.out or f"results/{args.policy}_{args.stream}_s{args.seed}.json"
    t0 = time.time()
    rec = run_once(args.policy, args.stream, args.seed, args.model, out)
    dt = time.time() - t0
    print(f"{args.policy} {args.stream} seed={args.seed}: "
          f"acc={rec.n_correct}/{rec.n} = {rec.n_correct/rec.n:.2%}  "
          f"tok in/out={rec.total_in}/{rec.total_out}  "
          f"latency_calls={rec.total_latency:.1f}s  wall={dt:.1f}s  "
          f"final={rec.final_roster}  decisions={len(rec.decisions)}")


if __name__ == "__main__":
    main()
