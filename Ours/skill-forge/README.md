# skill-forge — Complete Skill Lifecycle Management

A unified meta-skill that orchestrates the entire skill development pipeline from concept to deployment.

## What is skill-forge?

**skill-forge** is a conductor, not a monolith. It delegates to specialized tools at each stage of the skill lifecycle:

- **Stage 1: Creation** — Generate initial SKILL.md from requirements
- **Stage 2: Form Validation** — Structural consistency (via `skill-edit`)
- **Stage 3: Behavioral Validation** — Does it change agent behavior? (via `skill-evaluator` or official eval pipeline)
- **Stage 4: Iteration** — Hill-climbing with eval sets
- **Stage 5: Description Optimization** — Maximize trigger accuracy
- **Stage 6: Packaging** — Ship as .skill file

## Architecture

```
skill-forge (orchestrator)
├── Stage 1: Creation
│   └── Uses: init_skill.py (official) or manual drafting
├── Stage 2: Form Validation
│   └── Delegates to: /skill-edit
├── Stage 3: Behavioral Validation
│   ├── Option A: /skill-evaluator (deep dive)
│   └── Option B: official eval pipeline (benchmarking)
├── Stage 4: Iteration
│   ├── Option A: skill-evaluator Stage 2 (hill-climbing)
│   └── Option B: run_loop.py (description optimization)
├── Stage 5: Description Optimization
│   └── Uses: improve_description.py (official) or manual tuning
└── Stage 6: Packaging
    └── Uses: package_skill.py (official) or manual tarball
```

## Key Design Principles

1. **Don't duplicate, orchestrate** — Reuse existing tools (skill-edit, skill-evaluator, official scripts)
2. **Staged pipeline** — Each stage has clear inputs, outputs, and success criteria
3. **Flexible entry points** — Start at any stage depending on user needs
4. **Appraisal reporting** — Consistent format across all stages
5. **Subagent dispatch** — Haiku for trivial ops, Codex for expensive ops

## What's New vs. Existing Tools?

| Capability | Before | After (skill-forge) |
|------------|--------|-------------------|
| **Creation** | Manual drafting | Guided intake + template generation |
| **Form validation** | skill-edit (standalone) | Integrated as Stage 2 |
| **Behavioral validation** | skill-evaluator (standalone) | Integrated as Stage 3, Option A |
| **Benchmarking** | Not available | Stage 3, Option B (official eval pipeline) |
| **Iteration** | skill-evaluator Stage 2 | Integrated as Stage 4, Option A |
| **Description optimization** | Not available | Stage 5 (20-query test set, 5 rounds) |
| **Packaging** | Manual tarball | Stage 6 (official package_skill.py) |
| **End-to-end pipeline** | Manual chaining | Automated orchestration |

## Usage Examples

### Create a new skill from scratch
```
User: "I want to create a skill that converts CSV data to interactive charts"
skill-forge: [Runs Stage 1 → 2 → 3 → 5 → 6]
```

### Improve an existing skill
```
User: "This skill isn't triggering reliably, can you optimize it?"
skill-forge: [Runs Stage 5 (description optimization)]
```

### Validate a skill thoroughly
```
User: "Test this skill end-to-end"
skill-forge: [Runs Stage 2 → 3 → 4]
```

### Package for distribution
```
User: "Package this skill for release"
skill-forge: [Runs Stage 6 (with final validation)]
```

## Tool Locations

**Official skill-creator scripts:**
- Primary: `~/.codex/skills/.system/skill-creator/scripts/`
- Cached: `~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/scripts/`

**Your custom skills:**
- `~/.claude/skills/skill-edit/` — Form validation
- `~/.claude/skills/skill-evaluator/` — Behavioral validation
- `~/.claude/skills/codex/` — Subagent dispatch

## Integration with Existing Infrastructure

skill-forge **preserves** your existing workflow:
- skill-edit still works standalone
- skill-evaluator still works standalone
- Official skill-creator tools still work standalone

skill-forge **adds** orchestration:
- Automatic stage sequencing
- Handoff between tools
- Unified reporting
- Context preservation across stages

## Next Steps

1. **Register in CLAUDE.md** — Add trigger phrases and proactive invocation rules
2. **Test the pipeline** — Run on an existing skill to validate all stages
3. **Write test cases** — Create evals.json for a few skills to enable quantitative validation
4. **Iterate** — Refine stage transitions based on real usage

## Related Documentation

- `~/.claude/skills/skill-edit/SKILL.md` — Form validation details
- `~/.claude/skills/skill-evaluator/SKILL.md` — Behavioral validation details
- `~/.codex/skills/.system/skill-creator/SKILL.md` — Official skill-creator documentation
- `minions/roles/common/SKILL_BEHAVIORAL_EVAL.md` — Full-library eval example

---

**Version:** 1.0.0  
**Created:** 2026-05-21  
**Status:** Ready for testing
