#!/usr/bin/env bash
# Run a per-domain batch (all questions of one domain) in ONE Claude Code session.
# Usage: ./scripts/run_domain.sh <model> <domain-key>
#   domain-key: phys_physics | chem_chemistry | bio_biology
set -euo pipefail

MODEL="${1:?usage: run_domain.sh <model> <domain-key>}"
DOMAIN="${2:?usage: run_domain.sh <model> <domain-key>}"

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
PROMPT_FILE="$ROOT/data/prompts/domain/$DOMAIN.md"
[[ -f "$PROMPT_FILE" ]] || { echo "missing prompt: $PROMPT_FILE" >&2; exit 1; }

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$DOMAIN"
OUT_DIR="$ROOT/sessions/domain/$MODEL/$RUN_ID"
mkdir -p "$OUT_DIR"
cp "$PROMPT_FILE" "$OUT_DIR/prompt.md"

PROMPT="Answer all questions, stop only after emitting all final answer lines.

$(cat "$PROMPT_FILE")"

printf '{"run_id":"%s","mode":"domain","model":"%s","domain":"%s","started_utc":"%s"}\n' \
  "$RUN_ID" "$MODEL" "$DOMAIN" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUT_DIR/meta.json"

echo "[run_domain] model=$MODEL domain=$DOMAIN run_id=$RUN_ID" >&2

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

echo "[run_domain] done -> $OUT_DIR" >&2
