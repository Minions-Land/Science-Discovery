#!/usr/bin/env python3
"""regression-core diff: compare a freshly-graded arm against FD3 baseline.

Usage:
    python3 regression_core_diff.py <arm_grader_dir>

Where <arm_grader_dir> is a directory containing per-fig grader JSONs
(e.g. FigureDraw4/grader/minionsos-v4/). Reads the 5-cell list from
FigureDraw4/evals/regression-core.txt, loads each cell, sums the 8-axis
score, and diffs vs FigureDraw3/grader/_aggregate.json::v3_per_fig.

Exit code 0 if all 5 cells are within -2 of baseline; 1 otherwise.
Prints a markdown table summary.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
FD3 = REPO / "FigureDraw3"
FD4 = REPO / "FigureDraw4"

REGRESSION_CORE = (FD4 / "evals" / "regression-core.txt")
FD3_AGGREGATE = (FD3 / "grader" / "_aggregate.json")
AXES = [
    "scientific_clarity", "typography", "palette", "layout_density",
    "reviewer_readiness", "vector_fidelity", "file_format", "caption_quality",
]


def load_cells():
    cells = []
    for line in REGRESSION_CORE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cells.append(line)
    return cells


def load_baseline():
    if not FD3_AGGREGATE.exists():
        print(f"ERROR: FD3 baseline missing at {FD3_AGGREGATE}", file=sys.stderr)
        sys.exit(2)
    return json.loads(FD3_AGGREGATE.read_text(encoding="utf-8")).get("v3_per_fig", {})


def total_for(arm_dir: pathlib.Path, fig: str):
    p = arm_dir / f"{fig}.json"
    if not p.exists():
        return None
    body = json.loads(p.read_text(encoding="utf-8"))
    scores = body.get("scores")
    if not scores or not all(a in scores for a in AXES):
        return None
    return sum(scores[a] for a in AXES)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    arm_dir = pathlib.Path(sys.argv[1]).resolve()
    if not arm_dir.is_dir():
        print(f"ERROR: arm grader dir does not exist: {arm_dir}", file=sys.stderr)
        sys.exit(2)

    cells = load_cells()
    baseline = load_baseline()

    rows = []
    failed = 0
    for fig in cells:
        new_t = total_for(arm_dir, fig)
        base_t = baseline.get(fig)
        if new_t is None:
            rows.append((fig, base_t, None, None, "MISSING"))
            failed += 1
            continue
        if base_t is None:
            rows.append((fig, None, new_t, None, "no-baseline"))
            continue
        delta = new_t - base_t
        verdict = "OK" if delta >= -2 else "REGRESS"
        if delta < -2:
            failed += 1
        rows.append((fig, base_t, new_t, delta, verdict))

    print("# regression-core diff")
    print(f"baseline: {FD3_AGGREGATE}")
    print(f"new arm:  {arm_dir}\n")
    print(f"| {'fig_type':16s} | {'fd3':>4s} | {'new':>4s} | {'Δ':>5s} | verdict |")
    print(f"|{'-'*18}|{'-'*6}|{'-'*6}|{'-'*7}|{'-'*9}|")
    for fig, base_t, new_t, delta, verdict in rows:
        b = f"{base_t}" if base_t is not None else "  -"
        n = f"{new_t}" if new_t is not None else "  -"
        d = f"{delta:+d}" if delta is not None else "   -"
        print(f"| {fig:16s} | {b:>4s} | {n:>4s} | {d:>5s} | {verdict:7s} |")
    print()
    if failed:
        print(f"FAIL — {failed} cell(s) regressed by ≥ 3 OR missing.")
        sys.exit(1)
    print("PASS — all cells within tolerance.")


if __name__ == "__main__":
    main()
