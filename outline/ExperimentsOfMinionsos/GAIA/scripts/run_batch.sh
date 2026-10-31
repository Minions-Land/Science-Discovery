#!/bin/bash
# Run batch mode (mini sample 12 questions) for GAIA baseline
#
# Usage:
#   ./scripts/run_batch.sh <model>
#
# Example:
#   ./scripts/run_batch.sh sonnet
#   ./scripts/run_batch.sh haiku

set -euo pipefail

MODEL="${1:-sonnet}"

# Resolve model name
case "$MODEL" in
    sonnet) MODEL_NAME="claude-sonnet-4-6" ;;
    haiku)  MODEL_NAME="claude-haiku-4-5" ;;
    *)
        echo "Error: unknown model '$MODEL' (use 'sonnet' or 'haiku')"
        exit 1
        ;;
esac

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$ROOT_DIR/data"
PROMPTS_DIR="$DATA_DIR/prompts/batch"
ATTACHMENTS_DIR="$DATA_DIR/attachments"
SESSIONS_DIR="$ROOT_DIR/sessions/v1-baseline-pull/batch/$MODEL"

QUESTIONS_FILE="$PROMPTS_DIR/mini_12.md"

if [[ ! -f "$QUESTIONS_FILE" ]]; then
    echo "Error: questions file not found: $QUESTIONS_FILE"
    echo "Run 'python scripts/build_prompts.py' first"
    exit 1
fi

# Create run directory
RUN_ID="$(date +%Y%m%d_%H%M%S)_mini12"
RUN_DIR="$SESSIONS_DIR/$RUN_ID"
mkdir -p "$RUN_DIR"

# Create sandbox
SANDBOX_DIR="$RUN_DIR/sandbox"
mkdir -p "$SANDBOX_DIR"

# Symlink attachments
ln -sf "$ATTACHMENTS_DIR" "$SANDBOX_DIR/attachments"

# Copy questions file
cp "$QUESTIONS_FILE" "$SANDBOX_DIR/questions.md"

echo "========================================="
echo "GAIA Baseline - Batch Mode (Mini 12)"
echo "========================================="
echo "Model:    $MODEL_NAME"
echo "Run ID:   $RUN_ID"
echo "Sandbox:  $SANDBOX_DIR"
echo "========================================="
echo ""

# Run Claude Code in isolated environment
cd "$SANDBOX_DIR"

env -i \
    HOME="$HOME" \
    PATH="$PATH" \
    TERM="${TERM:-xterm-256color}" \
    claude \
        --model "$MODEL_NAME" \
        --effort max \
        --strict-mcp-config \
        --setting-sources "" \
        --allowedTools "Read" "Write" "Edit" "Bash" "WebSearch" "WebFetch" "mcp__playwright" \
        --print \
        "@questions.md" \
        "/goal 回答所有题目，每题一行 FINAL ANSWER: <task_id> | <answer> append 到 answers.txt" \
    > "$RUN_DIR/transcript.txt" 2>&1

echo ""
echo "========================================="
echo "Run completed: $RUN_DIR"
echo "========================================="
echo ""

# Check if answers.txt exists
if [[ -f "$SANDBOX_DIR/answers.txt" ]]; then
    echo "Answers:"
    cat "$SANDBOX_DIR/answers.txt"
    cp "$SANDBOX_DIR/answers.txt" "$RUN_DIR/answers.txt"
else
    echo "Warning: answers.txt not found"
fi

echo ""
echo "Next: python scripts/grade.py --run-dir $RUN_DIR --mode batch"
