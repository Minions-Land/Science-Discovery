"""Aggregate v2 baseline results from session transcripts.

Reads everything from disk:
  - answers.md (model output)
  - transcript.jsonl (token/cost/turn metadata)
  - meta.json (run identification)
  - data/ground_truth.json + ground_truth_full.json (truth)
  - data/v2/postgrad_subset.json (pg-NN ↔ 198-ID mapping)

Writes:
  - sessions/v2-baseline-pull/results/runs.jsonl
      One line per completed run: model, mode, stem, run_id, answers,
      grading, tokens, cost, timing, thinking density.
  - sessions/v2-baseline-pull/results/master.json
      Per-mode aggregates per model.
  - sessions/v2-baseline-pull/results/cross_mode.json
      Per-question comparison across single / domain / full / batch_pg
      for each model.
  - sessions/v2-baseline-pull/results/SUMMARY.md
      Human-readable report.

No model is consulted; every number is computed from session artifacts.
"""
import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond")
SESS = ROOT / "sessions" / "v2-baseline-pull"
OUT  = SESS / "results"
OUT.mkdir(parents=True, exist_ok=True)

GT_FULL = json.loads((ROOT / "data" / "ground_truth_full.json").read_text())
GT_PG   = json.loads((ROOT / "data" / "ground_truth.json").read_text())
PG_SUBSET = json.loads((ROOT / "data" / "v2" / "postgrad_subset.json").read_text())

# Pricing (USD per Mtok); cache write 5m = 1.25x base, 1h = 2.0x, cache read = 0.10x
PRICING = {
    "claude-haiku-4-5-20251001":  {"in": 1.0,  "out": 5.0,  "name": "haiku-4.5"},
    "claude-sonnet-4-6-20250929": {"in": 3.0,  "out": 15.0, "name": "sonnet-4.6"},
    "claude-sonnet-4-6":          {"in": 3.0,  "out": 15.0, "name": "sonnet-4.6"},
    "claude-haiku-4-5":            {"in": 1.0,  "out": 5.0,  "name": "haiku-4.5"},
}

ANS_RE = re.compile(r"FINAL ANSWER\s+(\S+):\s*([A-D])", re.IGNORECASE)


def truth_for(qid: str) -> str | None:
    if qid.startswith("pg-"): return GT_PG.get(qid)
    return GT_FULL.get(qid)


def parse_answers(answers_path: Path) -> dict:
    """Returns {qid -> letter}. Last duplicate wins."""
    out = {}
    if not answers_path.exists(): return out
    for line in answers_path.read_text().splitlines():
        m = ANS_RE.search(line)
        if m:
            out[m.group(1).lower()] = m.group(2).upper()
    return out


def compute_cost(model_id: str, usage: dict) -> dict:
    p = PRICING.get(model_id)
    if not p:
        return {"cost_usd": None, "breakdown": None, "price_model": None}
    inp = usage.get("input_tokens", 0) or 0
    out = usage.get("output_tokens", 0) or 0
    cr = usage.get("cache_read_input_tokens", 0) or 0
    cc = usage.get("cache_creation", {}) or {}
    cw5 = cc.get("ephemeral_5m_input_tokens", 0) or 0
    cw1 = cc.get("ephemeral_1h_input_tokens", 0) or 0
    bd = {
        "input":          inp * p["in"]      / 1e6,
        "output":         out * p["out"]     / 1e6,
        "cache_read":     cr  * (p["in"] * 0.10) / 1e6,
        "cache_write_5m": cw5 * (p["in"] * 1.25) / 1e6,
        "cache_write_1h": cw1 * (p["in"] * 2.0)  / 1e6,
    }
    return {"cost_usd": sum(bd.values()), "breakdown": bd, "price_model": p["name"]}


def process_run(run_dir: Path) -> dict | None:
    meta_path = run_dir / "meta.json"
    trans_path = run_dir / "transcript.jsonl"
    ans_path   = run_dir / "answers.md"
    if not (meta_path.exists() and trans_path.exists()): return None
    meta = json.loads(meta_path.read_text())

    events = [json.loads(l) for l in trans_path.open()]
    result = next((e for e in reversed(events) if e.get("type") == "result"), None)
    if not result: return None

    # Walk assistant blocks for tool_use + thinking density
    tool_calls = Counter()
    thinking_chars = 0
    text_chars = 0
    n_thinking_blocks = 0
    for e in events:
        if e.get("type") != "assistant": continue
        for b in e.get("message", {}).get("content", []) or []:
            t = b.get("type")
            if t == "tool_use":
                tool_calls[b.get("name", "?")] += 1
            elif t == "thinking":
                thinking_chars += len(b.get("thinking", "") or "")
                n_thinking_blocks += 1
            elif t == "text":
                text_chars += len(b.get("text", "") or "")

    usage = result.get("usage", {}) or {}
    model_usage = result.get("modelUsage", {}) or {}
    model_id = next(iter(model_usage), None) or result.get("model")
    cost_info = compute_cost(model_id or "", usage)

    answers = parse_answers(ans_path)
    grading = []
    n_correct = 0
    n_wrong = 0
    for qid in sorted(answers.keys()):
        letter = answers[qid]
        truth = truth_for(qid)
        ok = (truth == letter)
        grading.append({"qid": qid, "answered": letter, "truth": truth, "correct": ok})
        if ok: n_correct += 1
        else:  n_wrong += 1

    mode = meta["mode"]
    stem = meta.get("stem", "")
    if mode == "single":
        expected = 1
    elif mode == "batch":
        expected = 12
    elif mode == "full":
        expected = 198
    elif mode == "domain":
        expected = {"physics-86": 86, "chemistry-93": 93, "biology-19": 19}.get(stem, 0)
    else:
        expected = 0

    return {
        "run_id": meta.get("run_id"),
        "variant": meta.get("variant"),
        "mode": mode,
        "model": meta.get("model"),
        "model_id": model_id,
        "stem": stem,
        "questions_file": meta.get("questions_file"),
        "answers_file": meta.get("answers_file"),
        "started_utc": meta.get("started_utc"),
        "n_questions_expected": expected,
        "n_questions_answered": len(answers),
        "n_correct": n_correct,
        "n_wrong": n_wrong,
        "n_unanswered": max(expected - len(answers), 0),
        "accuracy_over_expected": (n_correct / expected) if expected else None,
        "answers": answers,
        "grading": grading,
        "wrong_qids": [g["qid"] for g in grading if not g["correct"]],
        "tokens": {
            "input":               usage.get("input_tokens"),
            "output":              usage.get("output_tokens"),
            "cache_read":          usage.get("cache_read_input_tokens"),
            "cache_creation_total": usage.get("cache_creation_input_tokens"),
            "cache_creation_5m":   (usage.get("cache_creation") or {}).get("ephemeral_5m_input_tokens"),
            "cache_creation_1h":   (usage.get("cache_creation") or {}).get("ephemeral_1h_input_tokens"),
        },
        "thinking": {
            "n_blocks": n_thinking_blocks,
            "total_chars": thinking_chars,
            "text_chars": text_chars,
            "chars_per_question": (thinking_chars / expected) if expected else None,
        },
        "tools": {
            "total_calls": sum(tool_calls.values()),
            "by_name": dict(tool_calls),
        },
        "timing": {
            "duration_ms": result.get("duration_ms"),
            "duration_api_ms": result.get("duration_api_ms"),
            "ttft_ms": result.get("ttft_ms"),
            "num_turns": result.get("num_turns"),
        },
        "cost": cost_info,
        "stop_reason": result.get("stop_reason"),
        "terminal_reason": result.get("terminal_reason"),
        "result_subtype": result.get("subtype"),
        "permission_denials": result.get("permission_denials"),
    }


def main():
    runs = []
    for run_dir in sorted(SESS.glob("*/*/*/")):
        if run_dir.parent.parent.name == "results": continue
        if run_dir.parent.parent.name == "_parallel_logs": continue
        if not (run_dir / "transcript.jsonl").exists(): continue
        rec = process_run(run_dir)
        if rec is None:
            print(f"[skip] {run_dir}", file=sys.stderr)
            continue
        runs.append(rec)

    # Write per-run JSONL
    runs_path = OUT / "runs.jsonl"
    with open(runs_path, "w") as f:
        for r in runs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {runs_path} ({len(runs)} runs)", file=sys.stderr)

    # Per-(model, mode) aggregates
    agg = defaultdict(lambda: {
        "n_runs": 0, "n_correct": 0, "n_expected": 0, "n_answered": 0,
        "cost_usd": 0.0, "duration_ms": 0,
        "tokens_in": 0, "tokens_out": 0, "cache_read": 0, "cache_write_5m": 0, "cache_write_1h": 0,
        "tool_calls": 0, "thinking_blocks": 0, "thinking_chars": 0,
    })
    for r in runs:
        # For single mode, roll all 198 per-question runs into one cell.
        stem_key = "" if r["mode"] == "single" else r.get("stem", "")
        key = (r["model"], r["mode"], stem_key)
        a = agg[key]
        a["n_runs"]      += 1
        a["n_correct"]   += r["n_correct"]
        a["n_expected"]  += r["n_questions_expected"]
        a["n_answered"]  += r["n_questions_answered"]
        a["cost_usd"]    += r["cost"].get("cost_usd") or 0
        a["duration_ms"] += r["timing"]["duration_ms"] or 0
        a["tokens_in"]   += r["tokens"]["input"] or 0
        a["tokens_out"]  += r["tokens"]["output"] or 0
        a["cache_read"]  += r["tokens"]["cache_read"] or 0
        a["cache_write_5m"] += r["tokens"]["cache_creation_5m"] or 0
        a["cache_write_1h"] += r["tokens"]["cache_creation_1h"] or 0
        a["tool_calls"]  += r["tools"]["total_calls"]
        a["thinking_blocks"] += r["thinking"]["n_blocks"]
        a["thinking_chars"]  += r["thinking"]["total_chars"]

    master = {}
    for (model, mode, stem), v in agg.items():
        cell = f"{model}/{mode}" + (f"/{stem}" if stem and mode != "single" else "")
        v["accuracy"] = (v["n_correct"] / v["n_expected"]) if v["n_expected"] else None
        v["model"] = model
        v["mode"] = mode
        v["stem"] = stem
        master[cell] = v
    (OUT / "master.json").write_text(json.dumps(master, indent=2, ensure_ascii=False))
    print(f"wrote {OUT / 'master.json'} ({len(master)} cells)", file=sys.stderr)

    # Cross-mode per-question analysis (per model)
    cross = {}
    for model in ["haiku", "sonnet"]:
        # Collect answers across modes for the 198-ID space
        single = {}
        for r in runs:
            if r["model"] != model or r["mode"] != "single": continue
            single.update(r["answers"])
        domain = {}
        for r in runs:
            if r["model"] != model or r["mode"] != "domain": continue
            domain.update(r["answers"])
        full = next((r["answers"] for r in runs if r["model"] == model and r["mode"] == "full"), {})
        batch_pg = next((r["answers"] for r in runs if r["model"] == model and r["mode"] == "batch"), {})

        # Per-qid table for the 198 space
        per_q = {}
        for qid, truth in GT_FULL.items():
            per_q[qid] = {
                "truth": truth,
                "single":  single.get(qid),
                "domain":  domain.get(qid),
                "full":    full.get(qid),
                "single_correct": (single.get(qid) == truth) if qid in single else None,
                "domain_correct": (domain.get(qid) == truth) if qid in domain else None,
                "full_correct":   (full.get(qid)   == truth) if qid in full   else None,
            }

        # Categorize the 197/198 qs that have answers in all 3 modes
        cats = {
            "all_correct": [], "all_wrong": [], "mixed": [],
            "single_only_correct": [], "domain_only_correct": [], "full_only_correct": [],
            "single_only_wrong":  [], "domain_only_wrong":  [], "full_only_wrong":  [],
            "single_missing": [], "domain_missing": [], "full_missing": [],
        }
        for qid, info in per_q.items():
            s, d, f = info["single_correct"], info["domain_correct"], info["full_correct"]
            if s is None: cats["single_missing"].append(qid)
            if d is None: cats["domain_missing"].append(qid)
            if f is None: cats["full_missing"].append(qid)
            if s is None or d is None or f is None: continue
            if s and d and f: cats["all_correct"].append(qid)
            elif not s and not d and not f: cats["all_wrong"].append(qid)
            else:
                cats["mixed"].append(qid)
                if s and not d and not f: cats["single_only_correct"].append(qid)
                if d and not s and not f: cats["domain_only_correct"].append(qid)
                if f and not s and not d: cats["full_only_correct"].append(qid)
                if not s and d and f: cats["single_only_wrong"].append(qid)
                if not d and s and f: cats["domain_only_wrong"].append(qid)
                if not f and s and d: cats["full_only_wrong"].append(qid)

        # Postgrad-12 view (different shuffle, requires per-record comparison)
        pg_view = []
        for i, mapped_id in enumerate(PG_SUBSET):
            pgid = f"pg-{i+1:02d}"
            pg_view.append({
                "pg_id": pgid,
                "mapped_198_id": mapped_id,
                "truth_pg": GT_PG.get(pgid),
                "truth_198": GT_FULL.get(mapped_id),
                "batch_pg":   batch_pg.get(pgid),
                "single":     single.get(mapped_id),
                "domain":     domain.get(mapped_id),
                "full":       full.get(mapped_id),
                "batch_pg_correct": (batch_pg.get(pgid) == GT_PG.get(pgid)) if pgid in batch_pg else None,
                "single_correct":   (single.get(mapped_id) == GT_FULL.get(mapped_id)) if mapped_id in single else None,
                "domain_correct":   (domain.get(mapped_id) == GT_FULL.get(mapped_id)) if mapped_id in domain else None,
                "full_correct":     (full.get(mapped_id)   == GT_FULL.get(mapped_id)) if mapped_id in full else None,
            })

        cross[model] = {
            "per_question": per_q,
            "categories":   {k: sorted(v) for k, v in cats.items()},
            "summary": {
                "total_qids_in_truth": len(GT_FULL),
                "single_n": len(single),
                "domain_n": len(domain),
                "full_n":   len(full),
                "n_with_all_three":  sum(1 for q in per_q.values() if all(q[k] is not None for k in ["single_correct","domain_correct","full_correct"])),
                "all_correct":            len(cats["all_correct"]),
                "all_wrong":              len(cats["all_wrong"]),
                "mixed":                  len(cats["mixed"]),
                "single_only_correct":    len(cats["single_only_correct"]),
                "domain_only_correct":    len(cats["domain_only_correct"]),
                "full_only_correct":      len(cats["full_only_correct"]),
                "single_only_wrong":      len(cats["single_only_wrong"]),
                "domain_only_wrong":      len(cats["domain_only_wrong"]),
                "full_only_wrong":        len(cats["full_only_wrong"]),
            },
            "postgrad_12_view": pg_view,
        }

    (OUT / "cross_mode.json").write_text(json.dumps(cross, indent=2, ensure_ascii=False))
    print(f"wrote {OUT / 'cross_mode.json'}", file=sys.stderr)

    return runs, master, cross


if __name__ == "__main__":
    main()
