#!/usr/bin/env bash
# Run all 198 v2 single-question sessions for one model, in parallel batches.
# Usage: ./scripts/run_v2_single_all.sh <model> [parallelism]
set -euo pipefail

MODEL="${1:?usage: run_v2_single_all.sh <model> [parallelism]}"
PAR="${2:-16}"
ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
cd "$ROOT"

LOG_DIR="$ROOT/sessions/v2-baseline-pull/_parallel_logs/$MODEL-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$LOG_DIR"

QIDS=()
for f in "$ROOT/data/v2/questions/single/"*.md; do
  QIDS+=("$(basename "${f%.md}")")
done
N=${#QIDS[@]}

echo "[parallel] model=$MODEL  N=$N  parallelism=$PAR  log_dir=$LOG_DIR" >&2

pids=()
launched=0
done_count=0
fail=0

for qid in "${QIDS[@]}"; do
  # If we are at capacity, wait for ANY child to finish.
  while [[ ${#pids[@]} -ge $PAR ]]; do
    if ! wait -n; then fail=$((fail+1)); fi
    # purge finished pids from array
    new=()
    for p in "${pids[@]}"; do kill -0 "$p" 2>/dev/null && new+=("$p"); done
    pids=("${new[@]}")
    done_count=$((launched - ${#pids[@]}))
  done
  bash scripts/run_v2.sh "$MODEL" single "$qid" \
    > "$LOG_DIR/$qid.stdout" 2> "$LOG_DIR/$qid.stderr" &
  pids+=($!)
  launched=$((launched+1))
  if (( launched % 20 == 0 )); then
    echo "[parallel] launched=$launched/$N (currently running: ${#pids[@]})" >&2
  fi
done

# Wait for the remaining stragglers.
for p in "${pids[@]}"; do
  if ! wait "$p"; then fail=$((fail+1)); fi
done

echo "[parallel] complete — $((N-fail))/$N succeeded, $fail failed" >&2
exit $fail
