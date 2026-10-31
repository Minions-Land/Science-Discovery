#!/usr/bin/env bash
# v2-skills runner: Same /goal prompt, same model, same effort=max, same flags
# as run_v2.sh, with ONE addition: --plugin-dir loads a freshly-built plugin
# bundle that wraps the 7 QA-relevant skills from minionsos-fork.
#
# Single-variable A/B against run_v2.sh:
#   v2-baseline-pull  : no --plugin-dir; sandbox sees only built-in skills
#   v2-skills         : --plugin-dir <bundle>; bundle's skills appear in
#                       system/init.skills next to the built-in ones
#
# The plugin.json schema is the same one Claude Code uses for marketplaces.
# Skills under test:
#   think-then-act, first-principles, unstated-premises, dialectical-synthesis,
#   think-in-parallel, evidence-driven-proposal, goal-setting
#
# Usage: ./scripts/run_v2_skills.sh <model> <mode> <stem>
set -euo pipefail

MODEL="${1:?usage: run_v2_skills.sh <model> <mode> <stem>}"
MODE="${2:?usage: run_v2_skills.sh <model> <mode> <stem>}"
STEM="${3:?usage: run_v2_skills.sh <model> <mode> <stem>}"

ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
FORK_SKILLS="$ROOT/minionsos-fork/minions/roles/common/skills"
Q_FILE="$ROOT/data/v2/questions/$MODE/$STEM.md"
[[ -f "$Q_FILE" ]] || { echo "missing question file: $Q_FILE" >&2; exit 1; }

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$STEM"
OUT_DIR="$ROOT/sessions/v2-skills/$MODE/$MODEL/$RUN_ID"
mkdir -p "$OUT_DIR"
A_FILE="$OUT_DIR/answers.md"
: > "$A_FILE"

PROMPT="/goal Answer every question in @$Q_FILE and append a 'FINAL ANSWER <id>: <letter>' line for each to @$A_FILE. Stop only when @$A_FILE contains a line for every question.

Begin."

SKILLS=(think-then-act first-principles unstated-premises dialectical-synthesis think-in-parallel evidence-driven-proposal goal-setting)

for s in "${SKILLS[@]}"; do
  if [[ ! -f "$FORK_SKILLS/$s.md" ]]; then
    echo "fork is missing skill: $FORK_SKILLS/$s.md" >&2
    exit 2
  fi
done

printf '{"run_id":"%s","variant":"v2-skills","skills_source":"minionsos-fork","mode":"%s","model":"%s","stem":"%s","questions_file":"%s","answers_file":"%s","skills":%s,"started_utc":"%s"}\n' \
  "$RUN_ID" "$MODE" "$MODEL" "$STEM" "$Q_FILE" "$A_FILE" \
  "$(printf '%s\n' "${SKILLS[@]}" | python3 -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')" \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUT_DIR/meta.json"

echo "[run_v2_skills] model=$MODEL mode=$MODE stem=$STEM run_id=$RUN_ID skills=${#SKILLS[@]}" >&2

SANDBOX_HOME="$(mktemp -d -t gpqa-v2-skills-XXXXXX)"
mkdir -p "$SANDBOX_HOME/.claude"
PLUGIN_DIR="$SANDBOX_HOME/plugin"
mkdir -p "$PLUGIN_DIR/.claude-plugin" "$PLUGIN_DIR/skills"

# Build the plugin.json that registers our 7 skills.
python3 - "$FORK_SKILLS" "$PLUGIN_DIR" "${SKILLS[@]}" <<'INNER_PY_END'
import sys, pathlib, re, json

src_root = pathlib.Path(sys.argv[1])
plugin_root = pathlib.Path(sys.argv[2])
slugs = sys.argv[3:]

FM_RE = re.compile(r'^---\n(.*?)\n---\n?', re.DOTALL)

def parse_fm(text):
    m = FM_RE.match(text)
    if not m: return {}, text
    fields = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fields[k.strip()] = v.strip().strip('"').strip("'")
    return fields, text[m.end():]

# Convert each fork skill (single .md) into <plugin>/skills/<slug>/SKILL.md.
for slug in slugs:
    src = src_root / f"{slug}.md"
    fields, body = parse_fm(src.read_text(encoding="utf-8"))
    name = fields.get("slug") or fields.get("name") or slug
    desc = fields.get("summary") or fields.get("description") or ""
    desc_q = desc.replace('"', '\\"')
    new_fm = f'---\nname: {name}\ndescription: "{desc_q}"\n---\n'
    out_dir = plugin_root / "skills" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "SKILL.md").write_text(new_fm + body, encoding="utf-8")

# think-then-act references plan-persistence; copy the helper file alongside.
pp = src_root / "plan-persistence.md"
if pp.exists():
    (plugin_root / "skills" / "think-then-act" / "plan-persistence.md").write_text(
        pp.read_text(encoding="utf-8"), encoding="utf-8"
    )

# Top-level marketplace.json is what --plugin-dir <path> consumes when path
# contains a .claude-plugin/ directory.
plugin_manifest = {
    "name": "gpqa-skills-bundle",
    "owner": {"name": "gpqa-experiment", "email": "noreply@local"},
    "metadata": {
        "description": "QA-relevant skills extracted from minionsos-fork for v2-skills A/B",
        "version": "0.1.0",
    },
    "plugins": [
        {
            "name": "qa-skills",
            "description": "7 QA-relevant reasoning skills (think-then-act + 6 referenced postures).",
            "source": "./",
            "strict": False,
            "skills": [f"./skills/{s}" for s in slugs],
        }
    ],
}
(plugin_root / ".claude-plugin" / "marketplace.json").write_text(
    json.dumps(plugin_manifest, indent=2), encoding="utf-8"
)

# Some claude versions expect plugin.json (single-plugin form). Write both.
single_plugin = {
    "name": "qa-skills",
    "description": "7 QA-relevant reasoning skills.",
    "version": "0.1.0",
    "skills": [f"./skills/{s}" for s in slugs],
}
(plugin_root / ".claude-plugin" / "plugin.json").write_text(
    json.dumps(single_plugin, indent=2), encoding="utf-8"
)

print(f"[skills-install] plugin built at {plugin_root} with {len(slugs)} skills", file=sys.stderr)
INNER_PY_END

trap 'rm -rf "$SANDBOX_HOME"' EXIT

echo "[run_v2_skills] plugin layout: $(find "$PLUGIN_DIR" -maxdepth 4 | wc -l | tr -d ' ') paths" >&2

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
    --plugin-dir "'"$PLUGIN_DIR"'" \
    --disallowedTools WebSearch WebFetch \
    --no-session-persistence --permission-mode bypassPermissions \
    --add-dir "'"$ROOT/data/v2"'" \
    --add-dir "'"$OUT_DIR"'"' _ "$PROMPT" \
    > "$OUT_DIR/transcript.jsonl" 2> "$OUT_DIR/stderr.log"

echo "[run_v2_skills] done -> $OUT_DIR  (answers: $(wc -l < "$A_FILE" | tr -d ' ') lines)" >&2
