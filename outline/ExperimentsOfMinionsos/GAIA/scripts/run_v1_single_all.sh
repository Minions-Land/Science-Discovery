#!/usr/bin/env bash
# Run all single-question sessions for one model in parallel.
# Usage: ./scripts/run_v1_single_all.sh <model> [parallelism]
set -euo pipefail

MODEL="${1:?usage: run_v1_single_all.sh <model> [parallelism]}"
PAR="${2:-12}"
ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GAIA"
cd "$ROOT"

LOG_DIR="$ROOT/sessions/v1-baseline-pull/_parallel_logs/single-$MODEL-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$LOG_DIR"

QIDS=()
for f in "$ROOT/data/prompts/single/"*.md; do
  QIDS+=("$(basename "${f%.md}")")
done
N=${#QIDS[@]}

echo "[parallel] model=$MODEL  N=$N  parallelism=$PAR  log_dir=$LOG_DIR" >&2

pids=()
launched=0

for qid in "${QIDS[@]}"; do
  # If at capacity, wait for ANY child to finish.
  while [[ ${#pids[@]} -ge $PAR ]]; do
    wait -n || true
    new=()
    for p in "${pids[@]}"; do kill -0 "$p" 2>/dev/null && new+=("$p"); done
    pids=("${new[@]}")
  done
  bash "$ROOT/scripts/run_v1.sh" "$MODEL" single "$qid" \
    > "$LOG_DIR/$qid.stdout" 2> "$LOG_DIR/$qid.stderr" &
  pids+=($!)
  launched=$((launched+1))
  echo "[parallel] launched $launched/$N: $qid" >&2
done

# Wait for stragglers
fail=0
for p in "${pids[@]}"; do
  if ! wait "$p"; then fail=$((fail+1)); fi
done

echo "[parallel] complete — $((N-fail))/$N succeeded, $fail failed" >&2
echo "[parallel] log_dir: $LOG_DIR" >&2
exit $fail
