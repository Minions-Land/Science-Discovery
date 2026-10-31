#!/bin/bash
# Run by-level mode for GAIA baseline
#
# Usage:
#   ./scripts/run_level.sh <model> <level>
#
# Example:
#   ./scripts/run_level.sh sonnet 1
#   ./scripts/run_level.sh haiku 3

set -euo pipefail

MODEL="${1:-sonnet}"
LEVEL="${2:-1}"

# Resolve model name
case "$MODEL" in
    sonnet) MODEL_NAME="claude-sonnet-4-6" ;;
    haiku)  MODEL_NAME="claude-haiku-4-5" ;;
    *)
        echo "Error: unknown model '$MODEL' (use 'sonnet' or 'haiku')"
        exit 1
        ;;
esac

# Validate level
if [[ ! "$LEVEL" =~ ^[123]$ ]]; then
    echo "Error: level must be 1, 2, or 3"
    exit 1
fi

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$ROOT_DIR/data"
PROMPTS_DIR="$DATA_DIR/prompts/level"
ATTACHMENTS_DIR="$DATA_DIR/attachments"
SESSIONS_DIR="$ROOT_DIR/sessions/v1-baseline-pull/level${LEVEL}/$MODEL"

QUESTIONS_FILE="$PROMPTS_DIR/level${LEVEL}.md"

if [[ ! -f "$QUESTIONS_FILE" ]]; then
    echo "Error: questions file not found: $QUESTIONS_FILE"
    echo "Run 'python scripts/build_prompts.py' first"
    exit 1
fi

# Create run directory
RUN_ID="$(date +%Y%m%d_%H%M%S)_level${LEVEL}"
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
echo "GAIA Baseline - By-Level Mode"
echo "========================================="
echo "Model:    $MODEL_NAME"
echo "Level:    $LEVEL"
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
    echo "Answers (first 10 lines):"
    head -10 "$SANDBOX_DIR/answers.txt"
    cp "$SANDBOX_DIR/answers.txt" "$RUN_DIR/answers.txt"
else
    echo "Warning: answers.txt not found"
fi

echo ""
echo "Next: python scripts/grade.py --run-dir $RUN_DIR --mode level"
