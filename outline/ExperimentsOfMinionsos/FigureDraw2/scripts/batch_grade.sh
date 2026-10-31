#!/usr/bin/env bash
# Grade every (arm, fig_type) cell that has a figure.pdf and no grade .json yet.
set -uo pipefail

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2"
SCRIPT_DIR="$ROOT/scripts"
CONC="${1:-4}"

LOG_DIR="$ROOT/grader/_batch"
mkdir -p "$LOG_DIR"
BATCH_ID="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$LOG_DIR/$BATCH_ID.log"
TODO="$LOG_DIR/$BATCH_ID.todo"
> "$TODO"

for arm_dir in "$ROOT/sessions"/*; do
  arm=$(basename "$arm_dir")
  [[ "$arm" == "_batch" ]] && continue
  for fig_dir in "$arm_dir"/*; do
    fig=$(basename "$fig_dir")
    if compgen -G "$fig_dir/*/workspace/figure.pdf" > /dev/null; then
      grade="$ROOT/grader/$arm/$fig.json"
      if [[ ! -s "$grade" ]] || ! grep -q '"scores"' "$grade" 2>/dev/null; then
        echo "$arm $fig" >> "$TODO"
      fi
    fi
  done
done

N=$(wc -l < "$TODO" | tr -d ' ')
echo "[gbatch] $BATCH_ID -- $N cells to grade, conc=$CONC" | tee -a "$LOG"
[[ "$N" -eq 0 ]] && exit 0

xargs -P "$CONC" -n 2 bash -c '
  arm="$1"; fig="$2"
  echo "[gbatch] START $arm/$fig $(date -u +%H:%M:%SZ)"
  bash "'"$SCRIPT_DIR"'/grade_cell.sh" "$arm" "$fig" >>"'"$LOG"'" 2>&1
  ec=$?
  echo "[gbatch] DONE  $arm/$fig exit=$ec $(date -u +%H:%M:%SZ)"
' _ < "$TODO" 2>&1 | tee -a "$LOG"

echo "[gbatch] $BATCH_ID complete -> $LOG"
