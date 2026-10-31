#!/usr/bin/env python3
"""Run the full sweep: 3 policies x 2 streams x 3 seeds = 18 runs.

Mixed stream is 16 problems, drift is 13. Plus router calls for static-N
and dynamic. Sequential to avoid hammering the proxy.

Writes JSON per run under results/, then prints a summary table.
"""
from __future__ import annotations
import json
import os
import sys
import time
import traceback

import outline.experiments.expert_split_merge.run as R


POLICIES = ["static-1", "static-N", "dynamic"]
STREAMS = ["mixed", "drift"]
SEEDS = [0, 1, 2]


def main():
    os.makedirs("results", exist_ok=True)
    log_path = "results/sweep.log"
    log = open(log_path, "w")
    started = time.time()

    runs = []
    for policy in POLICIES:
        for stream in STREAMS:
            for seed in SEEDS:
                tag = f"{policy}_{stream}_s{seed}"
                out = f"results/{tag}.json"
                if os.path.exists(out):
                    log.write(f"[skip-existing] {tag}\n")
                    log.flush()
                    with open(out) as f:
                        runs.append((policy, stream, seed, json.load(f)))
                    continue
                t0 = time.time()
                log.write(f"[start] {tag}\n"); log.flush()
                try:
                    rec = R.run_once(policy, stream, seed=seed, out_path=out)
                    dt = time.time() - t0
                    log.write(
                        f"[done]  {tag} acc={rec.n_correct}/{rec.n} "
                        f"in={rec.total_in} out={rec.total_out} "
                        f"latency_calls={rec.total_latency:.1f}s wall={dt:.1f}s "
                        f"final={rec.final_roster} dec={len(rec.decisions)}\n"
                    )
                    log.flush()
                    with open(out) as f:
                        runs.append((policy, stream, seed, json.load(f)))
                except Exception:
                    log.write(f"[FAIL] {tag}\n{traceback.format_exc()}\n")
                    log.flush()

    # Aggregate
    by_key: dict[tuple[str, str], list[dict]] = {}
    for policy, stream, seed, d in runs:
        by_key.setdefault((policy, stream), []).append(d)

    log.write("\n=== SUMMARY ===\n")
    log.write(
        f"{'policy':12s} {'stream':8s} {'n_runs':>6s} {'acc_mean':>9s} "
        f"{'in_tok_mean':>12s} {'out_tok_mean':>13s} {'lat_s_mean':>11s} "
        f"{'split_n':>8s} {'merge_n':>8s}\n"
    )
    rows = []
    for (policy, stream), ds in sorted(by_key.items()):
        if not ds:
            continue
        accs = [d["n_correct"] / d["n"] for d in ds]
        ins = [d["total_in_tok"] for d in ds]
        outs = [d["total_out_tok"] for d in ds]
        lat = [d["total_latency_s"] for d in ds]
        sp = [sum(1 for x in d["decisions"] if x["type"] == "split") for d in ds]
        mg = [sum(1 for x in d["decisions"] if x["type"] == "merge") for d in ds]
        row = (
            f"{policy:12s} {stream:8s} {len(ds):6d} "
            f"{sum(accs)/len(accs):9.3f} "
            f"{sum(ins)/len(ins):12.0f} {sum(outs)/len(outs):13.0f} "
            f"{sum(lat)/len(lat):11.1f} "
            f"{sum(sp)/len(sp):8.2f} {sum(mg)/len(mg):8.2f}\n"
        )
        rows.append(row)
        log.write(row)
    log.write(f"\nTotal wall: {time.time() - started:.1f}s\n")
    log.close()
    sys.stdout.write(open(log_path).read())


if __name__ == "__main__":
    main()
