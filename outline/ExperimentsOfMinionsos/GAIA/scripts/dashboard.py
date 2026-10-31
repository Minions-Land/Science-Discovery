#!/usr/bin/env python3
"""Quick status dashboard for all GAIA baseline runs."""
import json, os, time
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GAIA")
SESSIONS = ROOT / "sessions" / "v1-baseline-pull"

def scan_cell(mode, model):
    base = SESSIONS / mode / model
    if not base.exists():
        return []
    rows = []
    for d in base.iterdir():
        if not d.is_dir(): continue
        if d.name.startswith("_FAILED"): continue
        ans = d / "answers.txt"
        tr = d / "transcript.jsonl"
        trans_mb = round(tr.stat().st_size / 1024 / 1024, 2) if tr.exists() else 0
        ans_lines = 0
        if ans.exists() and ans.stat().st_size > 0:
            with open(ans) as f:
                ans_lines = sum(1 for _ in f)
        # detect running: transcript modified within last 2 min
        running = False
        if tr.exists():
            mtime = tr.stat().st_mtime
            running = (time.time() - mtime) < 120
        rows.append({"name": d.name, "ans_lines": ans_lines, "trans_mb": trans_mb, "running": running})
    return rows

def render():
    print(f"\n=== GAIA Baseline Dashboard ({time.strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
    print(f"{'Cell':<20s} {'Done':>5s} {'Running':>8s} {'Empty':>6s} {'Total':>6s}")
    print("-" * 50)
    cells = [
        ("haiku","batch"), ("sonnet","batch"),
        ("haiku","level"), ("sonnet","level"),
        ("haiku","full"), ("sonnet","full"),
        ("haiku","single"), ("sonnet","single"),
    ]
    for model, mode in cells:
        rows = scan_cell(mode, model)
        n_total = len(rows)
        n_running = sum(1 for r in rows if r["running"])
        n_done = sum(1 for r in rows if r["ans_lines"] > 0 and not r["running"])
        n_empty = n_total - n_done - n_running
        flag = ""
        # Check for any runaway-sized transcript
        big = [r for r in rows if r["trans_mb"] > 6 and r["running"]]
        if big: flag = f"  <BIG {[r['trans_mb'] for r in big]}>"
        print(f"{model}-{mode:<13s} {n_done:>5d} {n_running:>8d} {n_empty:>6d} {n_total:>6d}{flag}")
    # Watchdog process count
    import subprocess
    wd = subprocess.check_output(["pgrep", "-f", "watchdog_runner.py"]).decode().strip().splitlines()
    cl = subprocess.run(["pgrep", "-f", "claude --print"], capture_output=True, text=True).stdout.strip().splitlines()
    print(f"\nActive watchdogs: {len(wd)}")
    print(f"Active claude --print: {len(cl)}")

if __name__ == "__main__":
    render()
