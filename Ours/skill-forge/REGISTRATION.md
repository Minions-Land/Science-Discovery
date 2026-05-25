# skill-forge Registration Entry for CLAUDE.md

Add this to `~/.claude/CLAUDE.md`:

```markdown
# skill-forge
- **skill-forge** (`~/.claude/skills/skill-forge/SKILL.md`) - complete skill lifecycle orchestration from concept to deployment. Orchestrates creation, form validation (skill-edit), behavioral validation (skill-evaluator), iteration, description optimization, and packaging. Trigger: `/skill-forge`
When the user types `/skill-forge`, invoke the Skill tool with `skill: "skill-forge"` before doing anything else.
Also invoke proactively when the user asks to "create a new skill", "forge a skill", "develop a skill end-to-end", "optimize this skill", "improve this skill", "test this skill thoroughly", "run the full pipeline", "package this skill for distribution", or "take this skill through the full lifecycle".
```

---

# Architecture Overview

## The Unified Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                          skill-forge                              │
│                    (Meta-Orchestrator)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ├─ Stage 0: Intake & Scoping
                              │  └─ Detect mode, gather context, route
                              │
                              ├─ Stage 1: Creation
                              │  ├─ Research similar skills
                              │  ├─ Draft SKILL.md (init_skill.py or manual)
                              │  └─ Write initial test cases (evals.json)
                              │
                              ├─ Stage 2: Form Validation
                              │  ├─ quick_validate.py (official)
                              │  └─ /skill-edit (your custom)
                              │     └─ Catches: description/body mismatch,
                              │        list-shape drift, format issues
                              │
                              ├─ Stage 3: Behavioral Validation
                              │  ├─ Option A: /skill-evaluator
                              │  │  ├─ Stage 0: SSL Recall (can it be found?)
                              │  │  ├─ Stage 1: A/B (Haiku ± skill, Codex judges)
                              │  │  └─ Stage 2: Iteration (hill-climbing)
                              │  │
                              │  └─ Option B: Official eval pipeline
                              │     ├─ run_eval.py (parallel with/without)
                              │     ├─ aggregate_benchmark.py (quantitative)
                              │     └─ generate_report.py (HTML viewer)
                              │
                              ├─ Stage 4: Iteration (Optional)
                              │  ├─ Split: 60% optimization, 40% holdout
                              │  ├─ One change per cycle
                              │  └─ Guard against reward hacking
                              │
                              ├─ Stage 5: Description Optimization
                              │  ├─ Generate 20 test queries (10+/10-)
                              │  ├─ Human review in HTML template
                              │  ├─ improve_description.py (5 rounds)
                              │  └─ Select best F1 score
                              │
                              └─ Stage 6: Packaging
                                 ├─ Gather dependencies
                                 ├─ generate_openai_yaml.py (metadata)
                                 ├─ package_skill.py → .skill file
                                 └─ Final checklist
```

## Tool Ecosystem

```
┌──────────────────────────────────────────────────────────────────┐
│                     Your Existing Tools                           │
├──────────────────────────────────────────────────────────────────┤
│ skill-edit                    │ Form validation (150 lines)      │
│ skill-evaluator│ Behavioral validation (215 lines)│
│ codex                         │ Subagent dispatch (Tier 1/2/3)   │
│ 35 other skills               │ Domain-specific capabilities     │
└──────────────────────────────────────────────────────────────────┘
                              ▲
                              │ delegates to
                              │
┌──────────────────────────────────────────────────────────────────┐
│                  Official skill-creator Tools                     │
├──────────────────────────────────────────────────────────────────┤
│ init_skill.py                 │ Template-based creation          │
│ quick_validate.py             │ Format validation                │
│ run_eval.py                   │ Parallel A/B testing             │
│ run_loop.py                   │ Description optimization loop    │
│ improve_description.py        │ Trigger accuracy tuning          │
│ aggregate_benchmark.py        │ Quantitative comparison          │
│ generate_report.py            │ HTML eval viewer                 │
│ package_skill.py              │ .skill file generation           │
│ generate_openai_yaml.py       │ UI metadata                      │
└──────────────────────────────────────────────────────────────────┘
                              ▲
                              │ orchestrated by
                              │
┌──────────────────────────────────────────────────────────────────┐
│                          skill-forge                               │
│                    (This Meta-Skill)                              │
└──────────────────────────────────────────────────────────────────┘
```

## What Makes skill-forge Different?

### Before skill-forge:
- ❌ Manual workflow: write → test → fix → repeat
- ❌ No standardized pipeline
- ❌ Tools used in isolation
- ❌ No quantitative benchmarking
- ❌ No description optimization
- ❌ Manual packaging

### After skill-forge:
- ✅ Automated orchestration: one command, full pipeline
- ✅ Six-stage lifecycle with clear handoffs
- ✅ Integrated tool ecosystem
- ✅ Quantitative + qualitative validation
- ✅ Trigger accuracy optimization (20-query test set)
- ✅ One-click packaging (.skill files)

## Comparison Matrix

| Feature | skill-edit | skill-evaluator | Official skill-creator | skill-forge |
|---------|-----------|-----------------|----------------------|-----------|
| **Form validation** | ✅ Core | ❌ | ✅ Basic | ✅ Integrated |
| **Behavioral validation** | ❌ | ✅ Core (3 stages) | ✅ Basic | ✅ Integrated (both options) |
| **Description optimization** | ❌ | ❌ | ✅ Core (20-query) | ✅ Integrated |
| **Iteration loop** | ❌ | ✅ Stage 2 | ✅ run_loop.py | ✅ Integrated (both options) |
| **Packaging** | ❌ | ❌ | ✅ Core | ✅ Integrated |
| **Quantitative benchmarking** | ❌ | ✅ Token/timing | ✅ Pass rate/token/timing | ✅ Both |
| **HTML viewer** | ❌ | ❌ | ✅ eval-viewer | ✅ Integrated |
| **End-to-end pipeline** | ❌ | ❌ | ❌ | ✅ Core |
| **Flexible entry points** | ❌ | ❌ | ❌ | ✅ Core |
| **Appraisal reporting** | ✅ | ✅ | ❌ | ✅ Unified |

## Usage Patterns

### Pattern 1: Full Pipeline (New Skill)
```
User: "Create a skill that analyzes git commit patterns"
skill-forge: Stage 1 → 2 → 3 → 5 → 6
Output: Packaged .skill file, validation report
```

### Pattern 2: Optimization Only (Existing Skill)
```
User: "This skill isn't triggering when it should"
skill-forge: Stage 5 (description optimization)
Output: Optimized description, F1 score report
```

### Pattern 3: Deep Validation (Quality Check)
```
User: "Test this skill thoroughly before I ship it"
skill-forge: Stage 2 → 3 (Option A + B) → 4
Output: Form report, behavioral report, iteration history
```

### Pattern 4: Quick Package (Ready to Ship)
```
User: "Package this skill for distribution"
skill-forge: Stage 6 (with final validation)
Output: .skill file, installation instructions
```

## Subskill Architecture

skill-forge uses **delegation, not inheritance**:

```
skill-forge (orchestrator)
    │
    ├─ Delegates to: skill-edit
    │  └─ Returns: appraisal report (Diagnosis/Repaired/Left alone/Open)
    │
    ├─ Delegates to: skill-evaluator
    │  └─ Returns: validation report (Stage 0/1/2 results)
    │
    ├─ Delegates to: codex (for expensive ops)
    │  └─ Returns: subagent summary
    │
    └─ Invokes: official skill-creator scripts
       └─ Returns: script output (JSON, HTML, .skill file)
```

**Key principle:** skill-forge never duplicates logic. It routes, sequences, and reports.

## File Structure

```
~/.claude/skills/skill-forge/
├── SKILL.md              # Main orchestration logic (this file)
├── README.md             # Documentation (what you're reading)
└── REGISTRATION.md       # CLAUDE.md entry + architecture diagrams
```

No scripts, no agents, no assets — pure orchestration.

## Next Steps

1. **Add to CLAUDE.md** — Copy the registration entry above
2. **Test on existing skill** — Run `/skill-forge` on a skill you want to improve
3. **Create new skill** — Try the full pipeline: "Create a skill that..."
4. **Iterate** — Refine stage transitions based on real usage
5. **Document patterns** — Add successful workflows to this README

## Related Documentation

- **Your tools:**
  - `~/.claude/skills/skill-edit/SKILL.md`
  - `~/.claude/skills/skill-evaluator/SKILL.md`
  - `~/.claude/skills/codex/SKILL.md`

- **Official tools:**
  - `~/.codex/skills/.system/skill-creator/SKILL.md`
  - `~/.codex/skills/.system/skill-creator/scripts/`

- **Examples:**
  - `minions/roles/common/SKILL_BEHAVIORAL_EVAL.md`

---

**Why "skill-forge"?**

A forge is where raw material becomes refined tools through iterative cycles of heating, hammering, and cooling. The metaphor captures:
- **Creation** (forging from raw ideas)
- **Testing** (tempering under heat)
- **Refinement** (hammering out imperfections)
- **Iteration** (multiple heating cycles)
- **Mastery** (craftsmanship, not automation)

The name evokes the full lifecycle — 从诞生到成熟的完整生命周期 — while staying memorable and action-oriented.
