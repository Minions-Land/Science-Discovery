#!/usr/bin/env bash
# v2 runner: /goal + @file pull-based pattern.
# Usage: ./scripts/run_v2.sh <model> <mode> <stem>
#   <mode>  : single | batch | domain | full
#   <stem>  : the question file stem under data/v2/questions/<mode>/<stem>.md
#             e.g. phys-001  (single), postgrad-12 (batch),
#                  physics-86 (domain), all-198 (full)
set -euo pipefail

MODEL="${1:?usage: run_v2.sh <model> <mode> <stem>}"
MODE="${2:?usage: run_v2.sh <model> <mode> <stem>}"
STEM="${3:?usage: run_v2.sh <model> <mode> <stem>}"

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
Q_FILE="$ROOT/data/v2/questions/$MODE/$STEM.md"
[[ -f "$Q_FILE" ]] || { echo "missing question file: $Q_FILE" >&2; exit 1; }

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$STEM"
OUT_DIR="$ROOT/sessions/v2-baseline-pull/$MODE/$MODEL/$RUN_ID"
mkdir -p "$OUT_DIR"
A_FILE="$OUT_DIR/answers.md"
: > "$A_FILE"   # truncate / create empty answers file

# Goal: short stop-condition referencing both files via @-syntax.
PROMPT="/goal Answer every question in @$Q_FILE and append a 'FINAL ANSWER <id>: <letter>' line for each to @$A_FILE. Stop only when @$A_FILE contains a line for every question.

Begin."

printf '{"run_id":"%s","variant":"v2-baseline-pull","mode":"%s","model":"%s","stem":"%s","questions_file":"%s","answers_file":"%s","started_utc":"%s"}\n' \
  "$RUN_ID" "$MODE" "$MODEL" "$STEM" "$Q_FILE" "$A_FILE" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUT_DIR/meta.json"

echo "[run_v2] model=$MODEL mode=$MODE stem=$STEM run_id=$RUN_ID" >&2

SANDBOX_HOME="$(mktemp -d -t gpqa-v2-XXXXXX)"
mkdir -p "$SANDBOX_HOME/.claude"
trap 'rm -rf "$SANDBOX_HOME"' EXIT

env -i \
  HOME="$SANDBOX_HOME" \
  PATH="$PATH" \
  ANTHROPIC_AUTH_TOKEN="$ANTHROPIC_AUTH_TOKEN" \
  ANTHROPIC_BASE_URL="$ANTHROPIC_BASE_URL" \
  ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}" \
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS="${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-1}" \
  TERM="${TERM:-xterm-256color}" \
  LANG="${LANG:-en_US.UTF-8}" \
  bash -c 'printf %s "$1" | claude \
    --print \
    --output-format stream-json --include-partial-messages --verbose \
    --model "'"$MODEL"'" --effort max \
    --strict-mcp-config \
    --setting-sources "" \
    --disallowedTools WebSearch WebFetch \
    --no-session-persistence --permission-mode bypassPermissions \
    --add-dir "'"$ROOT/data/v2"'" \
    --add-dir "'"$OUT_DIR"'"' _ "$PROMPT" \
    > "$OUT_DIR/transcript.jsonl" 2> "$OUT_DIR/stderr.log"

echo "[run_v2] done -> $OUT_DIR  (answers: $(wc -l < "$A_FILE" | tr -d ' ') lines)" >&2
