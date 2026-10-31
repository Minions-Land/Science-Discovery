#!/usr/bin/env bash
# Run all 12 postgrad GPQA Diamond questions in ONE Claude Code session.
# Usage: ./scripts/run_batch.sh <model>
set -euo pipefail

MODEL="${1:?usage: run_batch.sh <model>}"

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
PROMPT_FILE="$ROOT/data/prompts/batch.md"
[[ -f "$PROMPT_FILE" ]] || { echo "missing prompt: $PROMPT_FILE" >&2; exit 1; }

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-batch12"
OUT_DIR="$ROOT/sessions/batch/$MODEL/$RUN_ID"
mkdir -p "$OUT_DIR"
cp "$PROMPT_FILE" "$OUT_DIR/prompt.md"

PROMPT="Answer all questions, stop only after emitting all final answer lines.

$(cat "$PROMPT_FILE")"

printf '{"run_id":"%s","mode":"batch","model":"%s","n_questions":12,"started_utc":"%s"}\n' \
  "$RUN_ID" "$MODEL" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUT_DIR/meta.json"

echo "[run_batch] model=$MODEL run_id=$RUN_ID" >&2

SANDBOX_HOME="$(mktemp -d -t gpqa-sandbox-XXXXXX)"
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
  claude \
    --print \
    --output-format stream-json --include-partial-messages --verbose \
    --model "$MODEL" --effort max \
    --strict-mcp-config \
    --setting-sources "" \
    --disallowedTools WebSearch WebFetch \
    --no-session-persistence --permission-mode bypassPermissions \
    "$PROMPT" \
    > "$OUT_DIR/transcript.jsonl" 2> "$OUT_DIR/stderr.log"
echo "[run_batch] done -> $OUT_DIR" >&2
