#!/usr/bin/env bash
# FigureDraw cell runner -- sandboxed Sonnet 4.6 with one arm's Skills loaded.
#
# Usage: scripts/run_cell.sh <arm> <fig_type>
#
# Boundary conditions mirror GQPA-Diamond v2-baseline-pull:
# env -i, --strict-mcp-config, --setting-sources "", --disallowedTools WebSearch WebFetch,
# --model claude-sonnet-4-6 --effort max, no host hooks, no host CLAUDE.md.

set -euo pipefail

ARM="${1:?usage: run_cell.sh <arm> <fig_type>}"
FIG_TYPE="${2:?usage: run_cell.sh <arm> <fig_type>}"

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw"
ARM_DIR="$ROOT/arms/$ARM"
FIX_DIR="$ROOT/fixtures/$FIG_TYPE"
SCRIPT_DIR="$ROOT/scripts"

[[ -d "$ARM_DIR/skills" ]] || { echo "missing arm skills dir: $ARM_DIR/skills" >&2; exit 1; }
[[ -d "$FIX_DIR" ]] || { echo "missing fixture dir: $FIX_DIR" >&2; exit 1; }

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="$ROOT/sessions/$ARM/$FIG_TYPE/$RUN_ID"
mkdir -p "$OUT_DIR/workspace"

SANDBOX_HOME="$(mktemp -d -t figdraw-XXXXXX)"
mkdir -p "$SANDBOX_HOME/.claude/skills"
cp -R "$ARM_DIR/skills/." "$SANDBOX_HOME/.claude/skills/"
if [[ -d "$ARM_DIR/references_demos" ]]; then
  cp -R "$ARM_DIR/references_demos" "$SANDBOX_HOME/references_demos"
fi
trap 'rm -rf "$SANDBOX_HOME"' EXIT

cp -R "$FIX_DIR/." "$OUT_DIR/workspace/"

PROMPT="/goal
You are a research-figure agent. Read brief.md and data.json (or data.csv) in your current working directory.
Produce ONE figure that matches the brief, plus a short caption.tex (LaTeX figure caption text only --
e.g. \\caption{...} on its own; no \\begin{figure}).

Hard requirements:
- Output figure as figure.pdf AND figure.png (in the cwd). figure.svg is optional but encouraged.
- Save your generation script as gen_figure.py (or gen_figure.R) so the result is reproducible.
- No web access. Use only the data provided. If data is insufficient or you must mock anything, note it in caption.tex.
- Use the Skills available under your sandbox HOME (~/.claude/skills/). Read each SKILL.md file when relevant.
- Stop only when figure.pdf, figure.png, caption.tex, and gen_figure.py all exist.

Begin."

# Persist start metadata
START_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$OUT_DIR/meta.json" <<META
{
  "run_id": "$RUN_ID",
  "arm": "$ARM",
  "fig_type": "$FIG_TYPE",
  "model": "claude-sonnet-4-6",
  "effort": "max",
  "started_utc": "$START_ISO",
  "fixture_dir": "$FIX_DIR",
  "out_dir": "$OUT_DIR"
}
META

echo "[run_cell] arm=$ARM fig=$FIG_TYPE run_id=$RUN_ID" >&2
echo "[run_cell] workspace=$OUT_DIR/workspace" >&2

set +e
env -i \
  HOME="$SANDBOX_HOME" \
  PATH="$PATH" \
  ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-}" \
  ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL:-}" \
  ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}" \
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS="1" \
  TERM="${TERM:-xterm-256color}" \
  LANG="${LANG:-en_US.UTF-8}" \
  bash -c '
    cd "$1"
    printf %s "$2" | claude \
      --print \
      --output-format stream-json --include-partial-messages --verbose \
      --model claude-sonnet-4-6 --effort max \
      --strict-mcp-config \
      --setting-sources "" \
      --disallowedTools WebSearch WebFetch \
      --no-session-persistence --permission-mode bypassPermissions \
      --add-dir "$3"
  ' _ "$OUT_DIR/workspace" "$PROMPT" "$SANDBOX_HOME" \
  > "$OUT_DIR/transcript.jsonl" 2> "$OUT_DIR/stderr.log"
EXIT_CODE=$?
set -e

python3 "$SCRIPT_DIR/finalize_cell.py" "$OUT_DIR" "$EXIT_CODE"
echo "[run_cell] done -> $OUT_DIR  exit=$EXIT_CODE" >&2
