#!/usr/bin/env python3
"""Summarize v2-minionsos cell results into one row per (model, stem, run_id).

Usage:
  scripts/summarize_v2_minionsos.py [--out RESULTS.md]

Walks outline/.../sessions/v2-minionsos/<cell>/<run_id>/ and reads each cell's
eval.json + meta.json. Emits a markdown table:

| cell | model | stem | accuracy | answered/total | wall-clock | port | run_id |

If --out is given, writes the table to that path. Otherwise prints to stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond/sessions/v2-minionsos")


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _row(run_dir: Path) -> dict | None:
    meta = run_dir / "meta.json"
    eval_ = run_dir / "eval.json"
    if not meta.exists():
        return None
    m = json.loads(meta.read_text(encoding="utf-8"))
    e = json.loads(eval_.read_text(encoding="utf-8")) if eval_.exists() else {}
    started = _parse_iso(m.get("started_utc"))
    finished = _parse_iso(m.get("finished_utc"))
    duration = (finished - started).total_seconds() if started and finished else None

    details = e.get("details") or {}
    return {
        "cell": run_dir.parent.name,
        "model": m.get("model"),
        "stem": m.get("stem"),
        "score": e.get("score"),
        "verdict": e.get("verdict"),
        "answered": details.get("answered"),
        "correct": details.get("correct"),
        "total": details.get("total"),
        "duration_s": duration,
        "port": m.get("port"),
        "run_id": m.get("run_id"),
        "hit_timeout": m.get("hit_timeout"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows: list[dict] = []
    for cell_dir in sorted(ROOT.glob("*")):
        if not cell_dir.is_dir():
            continue
        for run_dir in sorted(cell_dir.glob("*")):
            r = _row(run_dir)
            if r:
                rows.append(r)

    lines: list[str] = []
    lines.append(
        "| cell | model | stem | acc | corr/total | dur(s) | verdict | timeout | port | run_id |"
    )
    lines.append(
        "|------|-------|------|-----|------------|--------|---------|---------|------|--------|"
    )
    for r in rows:
        score = r["score"]
        score_str = f"{score:.3f}" if isinstance(score, (int, float)) else "—"
        ct = (
            f"{r['correct']}/{r['total']}"
            if r["correct"] is not None and r["total"] is not None
            else "—"
        )
        dur = f"{r['duration_s']:.0f}" if isinstance(r["duration_s"], (int, float)) else "—"
        timeout = "Y" if r.get("hit_timeout") else ""
        lines.append(
            f"| {r['cell']} | {r['model']} | {r['stem']} | {score_str} | {ct} "
            f"| {dur} | {r['verdict'] or '—'} | {timeout} | {r['port']} | {r['run_id']} |"
        )

    out_str = "\n".join(lines) + "\n"
    if args.out:
        args.out.write_text(out_str, encoding="utf-8")
        print(f"wrote {args.out} ({len(rows)} rows)")
    else:
        sys.stdout.write(out_str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
