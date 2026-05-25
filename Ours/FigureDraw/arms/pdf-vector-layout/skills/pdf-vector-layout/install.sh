#!/bin/bash
# Install pdf-vector-layout skill to Codex and/or Claude Code
#
# Usage:
#   ./install.sh codex     # install only to Codex
#   ./install.sh claude    # install only to Claude Code
#   ./install.sh both      # install to both (default)

set -e

SKILL_NAME="pdf-vector-layout"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-both}"

install_to() {
    local target_dir="$1"
    local target_name="$2"
    if [ ! -d "$target_dir" ]; then
        echo "Creating $target_dir"
        mkdir -p "$target_dir"
    fi
    if [ -d "$target_dir/$SKILL_NAME" ]; then
        echo "Removing existing $target_name skill at $target_dir/$SKILL_NAME"
        rm -rf "$target_dir/$SKILL_NAME"
    fi
    cp -r "$SCRIPT_DIR" "$target_dir/$SKILL_NAME"
    # Remove the install scripts from the installed copy
    rm -f "$target_dir/$SKILL_NAME/install.sh"
    rm -f "$target_dir/$SKILL_NAME/install.bat"
    rm -f "$target_dir/$SKILL_NAME/INSTALL.md"
    echo "[OK] Installed to $target_name: $target_dir/$SKILL_NAME"
}

case "$TARGET" in
    codex)
        install_to "$HOME/.codex/skills" "Codex"
        ;;
    claude)
        install_to "$HOME/.claude/skills" "Claude Code"
        ;;
    both)
        install_to "$HOME/.codex/skills" "Codex"
        install_to "$HOME/.claude/skills" "Claude Code"
        ;;
    *)
        echo "Usage: $0 [codex|claude|both]"
        exit 1
        ;;
esac

echo ""
echo "Done. Try invoking the skill by asking:"
echo "  '请帮我移动 PDF 中的图到页面下方，保持矢量可编辑'"
