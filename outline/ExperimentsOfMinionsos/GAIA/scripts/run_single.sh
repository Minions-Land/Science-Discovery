#!/bin/bash
# Run single-question mode for GAIA baseline
#
# Usage:
#   ./scripts/run_single.sh <model> <task_id>
#
# Example:
#   ./scripts/run_single.sh sonnet task_001
#   ./scripts/run_single.sh haiku task_042

set -euo pipefail

MODEL="${1:-sonnet}"
TASK_ID="${2:-}"

if [[ -z "$TASK_ID" ]]; then
    echo "Error: task_id required"
    echo "Usage: $0 <model> <task_id>"
    exit 1
fi

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
PROMPTS_DIR="$DATA_DIR/prompts/single"
ATTACHMENTS_DIR="$DATA_DIR/attachments"
SESSIONS_DIR="$ROOT_DIR/sessions/v1-baseline-pull/single/$MODEL"

QUESTION_FILE="$PROMPTS_DIR/${TASK_ID}.md"

if [[ ! -f "$QUESTION_FILE" ]]; then
    echo "Error: question file not found: $QUESTION_FILE"
    echo "Run 'python scripts/build_prompts.py' first"
    exit 1
fi

# Create run directory
RUN_ID="$(date +%Y%m%d_%H%M%S)_${TASK_ID}"
RUN_DIR="$SESSIONS_DIR/$RUN_ID"
mkdir -p "$RUN_DIR"

# Create sandbox
SANDBOX_DIR="$RUN_DIR/sandbox"
mkdir -p "$SANDBOX_DIR"

# Symlink attachments
ln -sf "$ATTACHMENTS_DIR" "$SANDBOX_DIR/attachments"

# Copy question file
cp "$QUESTION_FILE" "$SANDBOX_DIR/question.md"

echo "========================================="
echo "GAIA Baseline - Single Question Mode"
echo "========================================="
echo "Model:    $MODEL_NAME"
echo "Task ID:  $TASK_ID"
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
        "@question.md" \
        "/goal 回答此题，把 FINAL ANSWER: <answer> 写到 answer.txt" \
    > "$RUN_DIR/transcript.txt" 2>&1

echo ""
echo "========================================="
echo "Run completed: $RUN_DIR"
echo "========================================="
echo ""

# Check if answer.txt exists
if [[ -f "$SANDBOX_DIR/answer.txt" ]]; then
    echo "Answer:"
    cat "$SANDBOX_DIR/answer.txt"
    cp "$SANDBOX_DIR/answer.txt" "$RUN_DIR/answer.txt"
else
    echo "Warning: answer.txt not found"
fi

echo ""
echo "Next: python scripts/grade.py --run-dir $RUN_DIR"
