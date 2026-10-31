#!/usr/bin/env python3
"""Grade ALL completed GAIA baseline runs using the official GAIA scorer."""
import json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GAIA")
SESSIONS = ROOT / "sessions" / "v1-baseline-pull"
ADAPTER_DIR = Path("/Users/mjm/MinionsOS/outline/datasets/e2e-general/GAIA")

sys.path.insert(0, str(ADAPTER_DIR))
from adapter import gaia_score, load_rows  # type: ignore

# Load ground truth
rows = load_rows("validation")
GT = {r["task_id"]: {"answer": r["Final answer"], "level": int(r["Level"]), "file_name": r.get("file_name") or ""} for r in rows}

def extract_answers(answers_file):
    """Parse FINAL ANSWER lines from answers.txt."""
    if not answers_file.exists():
        return {}
    out = {}
    for line in answers_file.read_text(encoding="utf-8").splitlines():
        m = re.search(r"FINAL ANSWER:\s*([0-9a-f-]{36})\s*\|\s*(.+)", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
        else:
            m2 = re.search(r"FINAL ANSWER:\s*(.+)", line)
            if m2 and len(out) == 0:
                # single-question mode: just one answer, task_id is in dir name
                out["__single__"] = m2.group(1).strip()
    return out

def grade_run(run_dir, mode):
    """Returns list of {task_id, level, predicted, expected, correct, mode_used}."""
    answers = extract_answers(run_dir / "answers.txt")
    results = []
    if mode == "single":
        # task_id is in dir name: <timestamp>-<task_id>
        base = run_dir.name
        tid = base[base.index("-")+1:] if "-" in base else base
        if tid in GT:
            pred = answers.get("__single__") or answers.get(tid)
            if pred is None:
                results.append({"task_id": tid, "level": GT[tid]["level"], "predicted": None, "expected": GT[tid]["answer"], "correct": False, "has_attachment": bool(GT[tid]["file_name"])})
            else:
                s = gaia_score(pred, GT[tid]["answer"])
                results.append({"task_id": tid, "level": GT[tid]["level"], "predicted": pred, "expected": GT[tid]["answer"], "correct": s["correct"], "mode_used": s["mode"], "has_attachment": bool(GT[tid]["file_name"])})
    else:
        # batch/level/full: answers keyed by task_id
        for tid, pred in answers.items():
            if tid not in GT: continue
            s = gaia_score(pred, GT[tid]["answer"])
            results.append({"task_id": tid, "level": GT[tid]["level"], "predicted": pred, "expected": GT[tid]["answer"], "correct": s["correct"], "mode_used": s["mode"], "has_attachment": bool(GT[tid]["file_name"])})
    return results

def grade_cell(mode, model):
    base = SESSIONS / mode / model
    if not base.exists():
        return None
    all_results = []
    runs_processed = []
    for d in sorted(base.iterdir()):
        if not d.is_dir(): continue
        if d.name.startswith("_"):
            continue  # skip FAILED dirs but note them
        rs = grade_run(d, mode)
        all_results.extend(rs)
        runs_processed.append(d.name)
    return {"runs": runs_processed, "results": all_results}

def summarize(cell_results, model, mode):
    if cell_results is None or not cell_results["results"]:
        return None
    rs = cell_results["results"]
    n = len(rs)
    n_correct = sum(1 for r in rs if r["correct"])
    by_level = defaultdict(lambda: {"n": 0, "correct": 0})
    for r in rs:
        by_level[r["level"]]["n"] += 1
        if r["correct"]:
            by_level[r["level"]]["correct"] += 1
    return {
        "model": model, "mode": mode,
        "n_answered": n, "n_correct": n_correct,
        "accuracy_overall": round(100 * n_correct / n, 1) if n > 0 else 0,
        "by_level": {lv: {**v, "acc": round(100 * v["correct"] / v["n"], 1) if v["n"] else 0} for lv, v in by_level.items()},
    }

def main():
    print(f"\n=== GAIA Baseline Grading ({len(GT)} ground truth answers) ===\n")
    summaries = []
    for model in ["haiku", "sonnet"]:
        for mode in ["batch", "level", "full", "single"]:
            res = grade_cell(mode, model)
            s = summarize(res, model, mode)
            if s is None: continue
            summaries.append(s)
            n_runs = len(res["runs"])
            print(f"{model}-{mode}: {s['n_correct']}/{s['n_answered']} = {s['accuracy_overall']}% ({n_runs} runs)")
            for lv in sorted(s["by_level"].keys()):
                v = s["by_level"][lv]
                print(f"    Level {lv}: {v['correct']}/{v['n']} = {v['acc']}%")
    out_path = SESSIONS / "_summaries" / "ALL_GRADES.json"
    out_path.write_text(json.dumps(summaries, indent=2, ensure_ascii=False))
    print(f"\nWritten to {out_path}")

if __name__ == "__main__":
    main()
