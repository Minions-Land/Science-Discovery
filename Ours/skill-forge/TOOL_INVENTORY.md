# Official Skill-Creator Tool Inventory

## Primary Location: ~/.codex/skills/.system/skill-creator/scripts/

**Available tools (3 scripts):**
- ✅ `init_skill.py` (14,602 bytes) — Initialize new skills from templates
- ✅ `generate_openai_yaml.py` (6,619 bytes) — Generate UI metadata
- ✅ `quick_validate.py` (3,293 bytes) — Validate skill structure

**Missing tools:**
- ❌ `run_eval.py` — Run skill evaluations
- ❌ `run_loop.py` — Iterative improvement loop
- ❌ `improve_description.py` — Improve skill descriptions
- ❌ `aggregate_benchmark.py` — Aggregate benchmark results
- ❌ `generate_report.py` — Generate evaluation reports
- ❌ `package_skill.py` — Package skills

---

## Secondary Location: ~/.claude/plugins/cache/claude-plugins-official/skill-creator/

**Latest version: 6cc16f4b16e8 (2026-05-21 14:41)**

**Complete script set (8 scripts):**
- ✅ `run_eval.py` (11,464 bytes)
- ✅ `run_loop.py` (13,605 bytes)
- ✅ `improve_description.py` (11,116 bytes)
- ✅ `aggregate_benchmark.py` (14,386 bytes)
- ✅ `generate_report.py` (12,847 bytes)
- ✅ `package_skill.py` (4,234 bytes)
- ✅ `quick_validate.py` (3,972 bytes)
- ✅ `utils.py` (1,661 bytes)

**Additional resources:**
- ✅ `eval-viewer/generate_review.py` — HTML viewer for benchmark results
- ✅ `agents/` — Evaluation agents (grader.md, comparator.md, analyzer.md)
- ✅ `references/schemas.md` — JSON schema documentation

---

## Recommendation: Consolidate Tools

The plugin cache has the complete set, but they're scattered across 18 versions. The ~/.codex location only has 3 scripts.

**Action needed:**
1. Copy missing scripts from plugin cache to ~/.codex/skills/.system/skill-creator/scripts/
2. Update skill-forge SKILL.md to reference both locations as fallbacks
3. Test all scripts are executable and have correct dependencies

---

## Script Dependency Map

```
Stage 1 (Creation):
  └─ init_skill.py (✅ in ~/.codex)

Stage 2 (Form Validation):
  └─ quick_validate.py (✅ in both locations)

Stage 3 (Behavioral Validation):
  ├─ run_eval.py (❌ only in plugin cache)
  ├─ aggregate_benchmark.py (❌ only in plugin cache)
  └─ generate_report.py (❌ only in plugin cache)

Stage 4 (Iteration):
  └─ run_loop.py (❌ only in plugin cache)

Stage 5 (Description Optimization):
  └─ improve_description.py (❌ only in plugin cache)

Stage 6 (Packaging):
  ├─ package_skill.py (❌ only in plugin cache)
  └─ generate_openai_yaml.py (✅ in ~/.codex)
```

---

## Path Strategy for skill-forge

Use this fallback chain:

```python
# Primary path (stable, user-controlled)
PRIMARY = "~/.codex/skills/.system/skill-creator/scripts/"

# Secondary path (latest, auto-updated)
SECONDARY = "~/.claude/plugins/cache/claude-plugins-official/skill-creator/6cc16f4b16e8/skills/skill-creator/scripts/"

# Fallback: search all cache versions
FALLBACK = "~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/"
```

For each script, check PRIMARY first, then SECONDARY, then FALLBACK.
