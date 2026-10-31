#!/usr/bin/env bash
# Batch-run every arm x fig_type cell that has not yet produced figure.pdf.
#
# Usage:
#   scripts/batch_run.sh [--concurrency N] [--arms a,b,c] [--figs f1,f2,...]
#
# Writes a per-batch log under sessions/_batch/<batch_id>.log.
# Skips any (arm, fig) where sessions/<arm>/<fig> already has at least one run with figure.pdf.

set -uo pipefail

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2"
SCRIPT_DIR="$ROOT/scripts"

CONC=4
ARMS_FILTER=""
FIGS_FILTER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --concurrency) CONC="$2"; shift 2;;
    --arms) ARMS_FILTER="$2"; shift 2;;
    --figs) FIGS_FILTER="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

ALL_ARMS=(minionsos ml-paper-writing latex-document academic-paper-imbad scientific-writing-kdense stat-writing-fuhaoda composer-lishix awesome-writing-prompts)
ALL_FIGS=(grouped-bar line-errband scatter-fit heatmap box-violin 4panel-hero architecture roc-prc ridgeline dual-axis-time stacked-bar forest-plot sankey volcano network-graph latex-table equation-block)

if [[ -n "$ARMS_FILTER" ]]; then IFS=',' read -ra ALL_ARMS <<< "$ARMS_FILTER"; fi
if [[ -n "$FIGS_FILTER" ]]; then IFS=',' read -ra ALL_FIGS <<< "$FIGS_FILTER"; fi

BATCH_ID="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_DIR="$ROOT/sessions/_batch"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$BATCH_ID.log"
TODO="$LOG_DIR/$BATCH_ID.todo"

# Build TODO list of (arm, fig) cells without an existing figure.pdf
> "$TODO"
for arm in "${ALL_ARMS[@]}"; do
  for fig in "${ALL_FIGS[@]}"; do
    found_pdf=0
    if compgen -G "$ROOT/sessions/$arm/$fig/*/workspace/figure.pdf" > /dev/null; then
      found_pdf=1
    fi
    if [[ "$found_pdf" -eq 0 ]]; then
      echo "$arm $fig" >> "$TODO"
    fi
  done
done

N=$(wc -l < "$TODO" | tr -d ' ')
echo "[batch] $BATCH_ID -- $N cells to run, concurrency=$CONC" | tee -a "$LOG"

if [[ "$N" -eq 0 ]]; then
  echo "[batch] nothing to do" | tee -a "$LOG"
  exit 0
fi

# Use xargs -P for parallel dispatch. Each line "arm fig" -> one run_cell.sh
xargs -P "$CONC" -n 2 bash -c '
  arm="$1"; fig="$2"
  echo "[batch] START $arm/$fig $(date -u +%H:%M:%SZ)"
  bash "'"$SCRIPT_DIR"'/run_cell.sh" "$arm" "$fig" >>"'"$LOG"'" 2>&1
  ec=$?
  echo "[batch] DONE  $arm/$fig exit=$ec $(date -u +%H:%M:%SZ)"
' _ < "$TODO" 2>&1 | tee -a "$LOG"

echo "[batch] $BATCH_ID complete -> $LOG"
