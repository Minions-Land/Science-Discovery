#!/usr/bin/env bash
# GAIA v1 runner — hard-isolated sandbox.
#
# Sandbox guarantees:
#   * sandbox cwd = mktemp -d, NOT inside the GAIA project
#   * --add-dir only points at the sandbox itself
#   * question prompt + needed attachments are COPIED into sandbox
#   * prompt uses sandbox-relative paths (questions.md, attachments/, answers.txt)
#   * GAIA project root never named in prompt or env (no scripts/ access)
#
# Usage:  ./scripts/run_v1.sh <model> <mode> <stem>
#   mode  = single | batch
#   stem  = file stem under data/prompts/<mode>/<stem>.md
#           single: stem == task_id;  batch: stem == mini_12
set -euo pipefail

MODEL_KEY="${1:?usage: run_v1.sh <model> <mode> <stem>}"
MODE="${2:?usage: run_v1.sh <model> <mode> <stem>}"
STEM="${3:?usage: run_v1.sh <model> <mode> <stem>}"

case "$MODEL_KEY" in
    sonnet) MODEL="claude-sonnet-4-6" ;;
    haiku)  MODEL="claude-haiku-4-5" ;;
    *)      MODEL="$MODEL_KEY" ;;
esac

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GAIA"

case "$MODE" in
    single)  Q_FILE="$ROOT/data/prompts/single/$STEM.md" ;;
    batch)   Q_FILE="$ROOT/data/prompts/$STEM.md" ;;
    level)   Q_FILE="$ROOT/data/prompts/level/$STEM.md" ;;
    full)    Q_FILE="$ROOT/data/prompts/full/$STEM.md" ;;
    *)       echo "Error: mode must be single|batch|level|full, got '$MODE'" >&2; exit 1 ;;
esac

[[ -f "$Q_FILE" ]] || { echo "missing question file: $Q_FILE" >&2; exit 1; }

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$STEM"
OUT_DIR="$ROOT/sessions/v1-baseline-pull/$MODE/$MODEL_KEY/$RUN_ID"
mkdir -p "$OUT_DIR"
A_FILE_FINAL="$OUT_DIR/answers.txt"
: > "$A_FILE_FINAL"

# ---- Build hard-isolated sandbox ----
SANDBOX="$(mktemp -d -t gaia-sbox-XXXXXX)"
SANDBOX_HOME="$SANDBOX/home"
SANDBOX_WORK="$SANDBOX/work"
mkdir -p "$SANDBOX_HOME/.claude" "$SANDBOX_WORK"

# Copy question file into sandbox as questions.md
cp "$Q_FILE" "$SANDBOX_WORK/questions.md"

# Copy attachments referenced by this question file into the sandbox
mkdir -p "$SANDBOX_WORK/attachments"
python3 - "$SANDBOX_WORK/questions.md" "$ROOT/data/attachments" "$SANDBOX_WORK/attachments" <<'INNER_PY'
import re, shutil, sys
from pathlib import Path
qfile, src_root, dst_root = map(Path, sys.argv[1:4])
text = qfile.read_text(encoding="utf-8")
for tid, fname in re.findall(r"attachments/([0-9a-f-]{36})/([^\s`)]+)", text):
    src = src_root / tid / fname
    dst = dst_root / tid / fname
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(src, dst)
            print(f"  copied attachment: {tid}/{fname}", file=sys.stderr)
INNER_PY

# Pre-create empty answers.txt inside sandbox so prompt can reference relative path
touch "$SANDBOX_WORK/answers.txt"

trap 'cp -f "$SANDBOX_WORK/answers.txt" "$A_FILE_FINAL" 2>/dev/null || true; rm -rf "$SANDBOX"' EXIT

# Prompt: only sandbox-relative filenames; GAIA project paths NEVER appear here.
PROMPT="/goal Read @questions.md. For every Task ID listed in it, determine the answer and append a single line of the form 'FINAL ANSWER: <task_id> | <answer>' to @answers.txt. For questions with attachments, the file is at attachments/<task_id>/<filename> in the current directory. Use WebSearch / WebFetch / Bash / Read as needed. Stop only when @answers.txt contains a line for every Task ID listed in @questions.md.

Begin."

printf '{"run_id":"%s","variant":"v1-baseline-pull-isolated","mode":"%s","model":"%s","stem":"%s","sandbox":"%s","started_utc":"%s"}\n' \
  "$RUN_ID" "$MODE" "$MODEL" "$STEM" "$SANDBOX_WORK" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUT_DIR/meta.json"

echo "[run_v1] model=$MODEL mode=$MODE stem=$STEM run_id=$RUN_ID sandbox=$SANDBOX_WORK" >&2

cd "$SANDBOX_WORK"

env -i \
  HOME="$SANDBOX_HOME" \
  PATH="$PATH" \
  ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-}" \
  ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL:-}" \
  ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}" \
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS="${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-1}" \
  TERM="${TERM:-xterm-256color}" \
  LANG="${LANG:-en_US.UTF-8}" \
  bash -c 'cd "'"$SANDBOX_WORK"'" && printf %s "$1" | claude \
    --print \
    --output-format stream-json --include-partial-messages --verbose \
    --model "'"$MODEL"'" --effort max \
    --strict-mcp-config \
    --setting-sources "" \
    --no-session-persistence --permission-mode bypassPermissions \
    --add-dir "'"$SANDBOX_WORK"'"' _ "$PROMPT" \
    > "$OUT_DIR/transcript.jsonl" 2> "$OUT_DIR/stderr.log"

cp -f "$SANDBOX_WORK/answers.txt" "$A_FILE_FINAL"
echo "[run_v1] done -> $OUT_DIR  (answers: $(wc -l < "$A_FILE_FINAL" | tr -d ' ') lines)" >&2
