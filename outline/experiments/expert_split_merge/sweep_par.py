#!/usr/bin/env python3
"""Parallel sweep across (policy, stream, seed). Each run is independent of
the others, so we use a small thread pool. The Anthropic proxy is the
bottleneck — concurrency 4 is empirically OK and well below normal rate
limits for short Haiku calls.
"""
from __future__ import annotations
import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import outline.experiments.expert_split_merge.run as R


# Job sets ---------------------------------------------------------------

# Easy/sanity: 2 seeds is enough since first seed already showed ceiling
EASY_JOBS = [
    (policy, stream, seed)
    for policy in ["static-1", "static-N", "dynamic"]
    for stream in ["mixed", "drift"]
    for seed in [0, 1]
]

# Hard: 3 seeds, wider design — this is where split is hypothesised to help
HARD_JOBS = [
    (policy, stream, seed)
    for policy in ["static-1", "static-N", "dynamic"]
    for stream in ["hard", "noisy"]
    for seed in [0, 1, 2]
]

ALL_JOBS = EASY_JOBS + HARD_JOBS


def one(job):
    policy, stream, seed = job
    tag = f"{policy}_{stream}_s{seed}"
    out = f"results/{tag}.json"
    if os.path.exists(out):
        return tag, "skip", 0.0, None
    t0 = time.time()
    try:
        rec = R.run_once(policy, stream, seed=seed, out_path=out)
        return tag, "ok", time.time() - t0, {
            "n": rec.n, "acc": rec.n_correct / max(rec.n, 1),
            "in_tok": rec.total_in, "out_tok": rec.total_out,
            "latency_calls": rec.total_latency,
            "decisions": len(rec.decisions),
            "final_roster": rec.final_roster,
        }
    except Exception:
        return tag, "fail", time.time() - t0, traceback.format_exc()


def main():
    os.makedirs("results", exist_ok=True)
    log = open("results/sweep_par.log", "w")
    log.write(f"jobs={len(ALL_JOBS)}\n"); log.flush()
    started = time.time()
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(one, j): j for j in ALL_JOBS}
        for f in as_completed(futs):
            tag, status, dt, info = f.result()
            log.write(f"[{status}] {tag} {dt:.1f}s {info}\n"); log.flush()
            print(f"[{status}] {tag} {dt:.1f}s")
    log.write(f"\nTOTAL wall: {time.time()-started:.1f}s\n")
    log.close()
    print(open("results/sweep_par.log").read())


if __name__ == "__main__":
    main()
