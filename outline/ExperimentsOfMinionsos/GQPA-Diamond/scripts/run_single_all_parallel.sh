#!/usr/bin/env bash
# Run all 12 single-question sessions IN PARALLEL for one model.
# Usage: ./scripts/run_single_all_parallel.sh <model>
set -euo pipefail

MODEL="${1:?usage: run_single_all_parallel.sh <model>}"
ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
cd "$ROOT"

QIDS=(pg-01 pg-02 pg-03 pg-04 pg-05 pg-06 pg-07 pg-08 pg-09 pg-10 pg-11 pg-12)
LOG_DIR="$ROOT/sessions/_parallel_logs/$MODEL-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$LOG_DIR"

echo "[parallel] launching ${#QIDS[@]} sessions for model=$MODEL" >&2
pids=()
for qid in "${QIDS[@]}"; do
  bash scripts/run_single.sh "$MODEL" "$qid" \
    > "$LOG_DIR/$qid.stdout" 2> "$LOG_DIR/$qid.stderr" &
  pids+=($!)
  echo "[parallel] spawned $qid pid=${pids[-1]}" >&2
done

fail=0
for i in "${!pids[@]}"; do
  qid="${QIDS[$i]}"
  if wait "${pids[$i]}"; then
    echo "[parallel] done $qid" >&2
  else
    echo "[parallel] FAIL $qid (see $LOG_DIR/$qid.stderr)" >&2
    fail=$((fail+1))
  fi
done

echo "[parallel] complete — $((${#QIDS[@]}-fail))/${#QIDS[@]} succeeded" >&2
exit $fail
