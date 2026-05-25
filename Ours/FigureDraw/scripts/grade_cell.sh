#!/usr/bin/env bash
# Grade one (arm, fig_type) cell with a fresh sandboxed Sonnet judge.
# The judge has NO Skill mounts, NO inherited settings, and only sees:
#   brief.md (the original task)
#   figure.png (rasterized figure)
#   figure.pdf (vector original)
#   caption.tex
#   gen_figure.py (the script)
#
# It does NOT see the arm name, the data.json, or any other arm's output.
# Output: grader/<arm>/<fig_type>.json with an 8-dim rubric.

set -uo pipefail

ARM="${1:?usage: grade_cell.sh <arm> <fig_type>}"
FIG="${2:?usage: grade_cell.sh <arm> <fig_type>}"

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw"
OUT_FILE="$ROOT/grader/$ARM/$FIG.json"
mkdir -p "$(dirname "$OUT_FILE")"

# Find the latest run directory for this (arm, fig)
LATEST=$(ls -1d "$ROOT/sessions/$ARM/$FIG"/*/ 2>/dev/null | sort | tail -1)
if [[ -z "$LATEST" ]]; then
  echo "{\"error\": \"no run found\", \"arm\": \"$ARM\", \"fig_type\": \"$FIG\"}" > "$OUT_FILE"
  echo "[grade] no run for $ARM/$FIG -> wrote error stub" >&2
  exit 1
fi
WS="${LATEST}workspace"
if [[ ! -f "$WS/figure.pdf" ]]; then
  echo "{\"error\": \"no figure.pdf\", \"arm\": \"$ARM\", \"fig_type\": \"$FIG\", \"workspace\": \"$WS\"}" > "$OUT_FILE"
  echo "[grade] no figure.pdf for $ARM/$FIG -> wrote error stub" >&2
  exit 1
fi

# Stage a tiny sandbox HOME (no skills) and a workspace with brief + outputs only
SBX="$(mktemp -d -t figgrade-XXXXXX)"
mkdir -p "$SBX/.claude" "$SBX/work"
trap 'rm -rf "$SBX"' EXIT

cp "$WS/figure.pdf"     "$SBX/work/figure.pdf"     2>/dev/null
cp "$WS/figure.png"     "$SBX/work/figure.png"     2>/dev/null
cp "$WS/figure.svg"     "$SBX/work/figure.svg"     2>/dev/null
cp "$WS/caption.tex"    "$SBX/work/caption.tex"    2>/dev/null
cp "$WS/gen_figure.py"  "$SBX/work/gen_figure.py"  2>/dev/null
cp "$WS/gen_figure.R"   "$SBX/work/gen_figure.R"   2>/dev/null
cp "$WS/brief.md"       "$SBX/work/brief.md"       2>/dev/null

PROMPT='You are an independent figure reviewer. The current directory contains:
- brief.md  (the original task brief)
- figure.png and/or figure.pdf (the produced figure)
- caption.tex (the LaTeX figure caption)
- gen_figure.py or gen_figure.R (the generation script)

Read the figure (use Read tool on figure.png), the brief, the caption, and the gen script.
Score on the rubric below. Each axis is 0-3 integers, with brief evidence per axis.

RUBRIC (0-3 each):
1. scientific_clarity: does the figure carry the brief'\''s scientific claim? Is it readable?
2. typography: editable text (pdf.fonttype=42 / svg.fonttype=none), font choice, text sizes, no DejaVu Sans defaults.
3. palette: ColorBlind-safe? Is there directional vs categorical discipline (e.g. green/red reserved for direction)?
4. layout_density: panel space used, no gaping whitespace, no overlapping labels, sensible y-range.
5. reviewer_readiness: would Reviewer 2 ask for changes? caption matches figure? legend placement?
6. vector_fidelity: figure.pdf is real vector with selectable text? script uses fonttype=42?
7. file_format: figure.pdf, figure.png, caption.tex, gen_figure.* all exist and are non-trivial?
8. caption_quality: does caption explain what the reader sees, with a numerical claim or specific finding?

OUTPUT FORMAT (write your final answer to ./grade.json as exactly this JSON shape):

{
  "scores": {
    "scientific_clarity":   <0-3>,
    "typography":            <0-3>,
    "palette":               <0-3>,
    "layout_density":        <0-3>,
    "reviewer_readiness":    <0-3>,
    "vector_fidelity":       <0-3>,
    "file_format":           <0-3>,
    "caption_quality":       <0-3>
  },
  "evidence": {
    "scientific_clarity":   "<one line>",
    "typography":            "<one line>",
    "palette":               "<one line>",
    "layout_density":        "<one line>",
    "reviewer_readiness":    "<one line>",
    "vector_fidelity":       "<one line>",
    "file_format":           "<one line>",
    "caption_quality":       "<one line>"
  },
  "overall_strengths": ["<bullet>", "<bullet>"],
  "overall_weaknesses": ["<bullet>", "<bullet>"]
}

Stop only when grade.json is written. Do not modify any other file. No web access.'

set +e
env -i \
  HOME="$SBX" \
  PATH="$PATH" \
  ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-}" \
  ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL:-}" \
  ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}" \
  TERM="${TERM:-xterm-256color}" \
  LANG="${LANG:-en_US.UTF-8}" \
  bash -c '
    cd "$1"
    printf %s "$2" | claude \
      --print \
      --model claude-sonnet-4-6 --effort max \
      --strict-mcp-config \
      --setting-sources "" \
      --disallowedTools WebSearch WebFetch \
      --no-session-persistence --permission-mode bypassPermissions
  ' _ "$SBX/work" "$PROMPT" \
  > "$SBX/work/grade.stdout.log" 2> "$SBX/work/grade.stderr.log"
EC=$?
set -e

if [[ -f "$SBX/work/grade.json" ]]; then
  cp "$SBX/work/grade.json" "$OUT_FILE"
  echo "[grade] $ARM/$FIG -> $OUT_FILE  (exit $EC)" >&2
else
  # Fallback: produce empty stub with the stdout for debugging
  python3 - <<EOF_PY
import json, pathlib
p = pathlib.Path("$OUT_FILE")
p.write_text(json.dumps({
  "error": "judge did not write grade.json",
  "exit_code": $EC,
  "arm": "$ARM",
  "fig_type": "$FIG",
  "stdout_tail": pathlib.Path("$SBX/work/grade.stdout.log").read_text(encoding="utf-8")[-2000:] if pathlib.Path("$SBX/work/grade.stdout.log").exists() else ""
}, indent=2), encoding="utf-8")
EOF_PY
  echo "[grade] $ARM/$FIG FAILED -- stub written" >&2
fi
