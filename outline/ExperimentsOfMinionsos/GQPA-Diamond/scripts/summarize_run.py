"""Compute per-run summary from a session's transcript.jsonl.

Usage:
  python3 scripts/summarize_run.py <run_dir>
  python3 scripts/summarize_run.py --all   # every run under sessions/

Writes <run_dir>/summary.json. Grades against:
  - data/ground_truth.json       for postgrad-12 modes (single, batch)
  - data/ground_truth_full.json  for full / domain modes (198-question pool)

Duplicates: when a model emits the same FINAL ANSWER <id> twice, the LAST one wins.
Thinking density: thinking_chars / n_questions is recorded so we can spot the
"model declined to think" runs (compare with single-question reasoning baseline).
"""
import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond")
sys.path.insert(0, str(ROOT / "scripts"))
from pricing import compute_cost_usd  # noqa

GT_PG   = json.loads((ROOT / "data" / "ground_truth.json").read_text())
GT_FULL_PATH = ROOT / "data" / "ground_truth_full.json"
GT_FULL = json.loads(GT_FULL_PATH.read_text()) if GT_FULL_PATH.exists() else {}

# Match "FINAL ANSWER <id>: <letter>" where id is pg-NN, phys-NNN, chem-NNN, bio-NNN.
FINAL_RE_KEYED = re.compile(
    r"FINAL\s+ANSWER\s+((?:pg|phys|chem|bio)-\d{2,3})\s*:\s*([A-D])",
    re.IGNORECASE,
)
# Single-question mode: "FINAL ANSWER: <letter>" (no id).
FINAL_RE_BARE = re.compile(r"FINAL\s+ANSWER\s*:\s*([A-D])", re.IGNORECASE)

MODE_EXPECT = {
    "single": 1,
    "batch": 12,
    "domain": None,   # set per-run from prompt domain
    "full": 198,
}

DOMAIN_EXPECT = {
    "phys_physics":   86,
    "chem_chemistry": 93,
    "bio_biology":    19,
}


def pick_truth(qid: str) -> str | None:
    if qid.startswith("pg-"): return GT_PG.get(qid)
    return GT_FULL.get(qid)


def extract_answers(result_text: str, mode: str, qid: str | None) -> dict:
    """Returns {qid -> letter}. Last duplicate wins."""
    if mode == "single":
        m = None
        for m in FINAL_RE_BARE.finditer(result_text): pass
        return {qid: m.group(1).upper()} if (m and qid) else {}
    out: dict[str, str] = {}
    for m in FINAL_RE_KEYED.finditer(result_text):
        out[m.group(1).lower()] = m.group(2).upper()  # last wins
    return out


def summarize_run(run_dir: Path) -> dict | None:
    transcript = run_dir / "transcript.jsonl"
    meta = json.loads((run_dir / "meta.json").read_text())
    events = [json.loads(l) for l in transcript.open()]

    result = next((e for e in reversed(events) if e.get("type") == "result"), None)
    if not result or result.get("num_turns", 0) == 0:
        print(f"[skip] no usable result in {transcript}", file=sys.stderr)
        return None

    # Walk assistant blocks for tool calls + thinking density.
    tool_counter: Counter = Counter()
    thinking_chars = 0
    text_chars = 0
    n_thinking_blocks = 0
    for e in events:
        if e.get("type") != "assistant": continue
        for b in e.get("message", {}).get("content", []) or []:
            t = b.get("type")
            if t == "tool_use":
                tool_counter[b.get("name", "?")] += 1
            elif t == "thinking":
                thinking_chars += len(b.get("thinking", "") or "")
                n_thinking_blocks += 1
            elif t == "text":
                text_chars += len(b.get("text", "") or "")

    usage = result.get("usage", {}) or {}
    model_usage = result.get("modelUsage", {}) or {}
    model_id = next(iter(model_usage), None) or result.get("model")
    computed = compute_cost_usd(model_id or "", usage)

    mode = meta["mode"]
    answers = extract_answers(result.get("result", ""), mode, meta.get("question_id"))

    if mode == "single":
        expected = 1
    elif mode == "batch":
        expected = 12
    elif mode == "domain":
        expected = DOMAIN_EXPECT.get(meta.get("domain", ""), 0)
    elif mode == "full":
        expected = 198
    else:
        expected = 0

    grading = []
    correct = 0
    wrong = []
    for qid in sorted(answers.keys()):
        letter = answers[qid]
        truth = pick_truth(qid)
        ok = (truth == letter)
        grading.append({"qid": qid, "answered": letter, "truth": truth, "correct": ok})
        if ok: correct += 1
        else:  wrong.append(qid)

    summary = {
        "run_id": meta["run_id"],
        "mode": mode,
        "model": meta["model"],
        "model_id": model_id,
        "question_id": meta.get("question_id"),
        "domain": meta.get("domain"),
        "n_questions_expected": expected,
        "n_questions_answered": len(answers),
        "n_correct": correct,
        "n_wrong": len(wrong),
        "n_unanswered": max(expected - len(answers), 0),
        "accuracy_over_expected": (correct / expected) if expected else None,
        "accuracy_over_answered": (correct / len(answers)) if answers else None,
        "wrong_qids": wrong,
        "grading": grading,
        "timing": {
            "duration_ms": result.get("duration_ms"),
            "duration_api_ms": result.get("duration_api_ms"),
            "ttft_ms": result.get("ttft_ms"),
            "num_turns": result.get("num_turns"),
        },
        "tokens": {
            "input": usage.get("input_tokens"),
            "output": usage.get("output_tokens"),
            "cache_read": usage.get("cache_read_input_tokens"),
            "cache_creation_total": usage.get("cache_creation_input_tokens"),
            "cache_creation_5m": usage.get("cache_creation", {}).get("ephemeral_5m_input_tokens"),
            "cache_creation_1h": usage.get("cache_creation", {}).get("ephemeral_1h_input_tokens"),
        },
        "thinking": {
            "n_blocks": n_thinking_blocks,
            "total_chars": thinking_chars,
            "text_chars": text_chars,
            "chars_per_question": (thinking_chars / expected) if expected else None,
        },
        "tools": {
            "total_calls": sum(tool_counter.values()),
            "by_name": dict(tool_counter),
        },
        "cost": {
            "reported_usd": result.get("total_cost_usd"),
            "computed_usd": computed["cost_usd"],
            "computed_breakdown": computed["breakdown"],
            "price_model": computed["price_model"],
        },
        "stop_reason": result.get("stop_reason"),
        "terminal_reason": result.get("terminal_reason"),
        "permission_denials": result.get("permission_denials"),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def main(argv):
    if argv[1:2] == ["--all"]:
        run_dirs = sorted((ROOT / "sessions").glob("*/*/*/"))
    else:
        run_dirs = [Path(argv[1])]
    for d in run_dirs:
        if not (d / "transcript.jsonl").exists(): continue
        s = summarize_run(d)
        if s is None: continue
        cost = s["cost"]["computed_usd"]
        cost_str = f"${cost:.4f}" if cost else "n/a"
        thn = s["thinking"]["chars_per_question"]
        thn_str = f"{thn:.0f}" if thn else "-"
        print(
            f"{s['mode']:<6} {s['model']:<7} {(s.get('domain') or s.get('question_id') or '-'):<16} "
            f"acc={s['n_correct']:>3}/{s['n_questions_expected']:<3} "
            f"answered={s['n_questions_answered']:>3}  "
            f"think_cpq={thn_str:>5}  "
            f"cost={cost_str:>9}  "
            f"tools={s['tools']['total_calls']}"
        )

if __name__ == "__main__":
    main(sys.argv)
