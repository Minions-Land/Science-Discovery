#!/usr/bin/env bash
# Run all 8 arms' paper-page cells in parallel.
set -uo pipefail
ROOT=/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2
CONC="${1:-4}"
LOG=$ROOT/sessions/_batch/paper-page-$(date -u +%Y%m%dT%H%M%SZ).log
mkdir -p "$(dirname "$LOG")"

ARMS=(minionsos ml-paper-writing latex-document academic-paper-imbad scientific-writing-kdense stat-writing-fuhaoda composer-lishix awesome-writing-prompts)
TODO_FILE="$LOG.todo"
: > "$TODO_FILE"
for a in "${ARMS[@]}"; do
  echo "$a paper-page-$a" >> "$TODO_FILE"
done

echo "[ppbatch] running ${#ARMS[@]} cells, conc=$CONC" | tee -a "$LOG"

xargs -P "$CONC" -n 2 bash -c '
  arm="$1"; fig="$2"
  echo "[ppbatch] START $arm/$fig $(date -u +%H:%M:%SZ)"
  bash '"$ROOT"'/scripts/run_cell.sh "$arm" "$fig" >>'"$LOG"' 2>&1
  echo "[ppbatch] DONE  $arm/$fig exit=$? $(date -u +%H:%M:%SZ)"
' _ < "$TODO_FILE" 2>&1 | tee -a "$LOG"

echo "[ppbatch] complete -> $LOG"
