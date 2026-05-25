---
name: skill-forge
description: Complete skill lifecycle orchestration — from initial concept through creation, validation, testing, iteration, optimization, and packaging. Delegates to specialized subskills (skill-edit for form, skill-evaluator for behavior, official skill-creator tools for description optimization and packaging). Use when the user wants to create a new skill, improve an existing one, or run the full development pipeline. Trigger phrases include "create a skill", "forge a skill", "skill lifecycle", "develop a skill end-to-end", "optimize this skill", "package this skill".
metadata:
  version: 1.1.0
  layer: meta-orchestration
  references: [skill-edit, skill-evaluator, skill-curator, codex]
allowed-tools: [Agent, Bash, Read, Write, Edit, Skill]
---

# skill-forge — Complete Skill Lifecycle Orchestration

**What this does:** Orchestrates the entire skill development lifecycle from concept to deployment. Acts as a conductor that delegates to specialized subskills and tools at each stage.

**When to invoke:**
- User types `/skill-forge`
- User asks to "create a new skill", "forge a skill", "develop a skill end-to-end"
- User wants to "improve/optimize/iterate on this skill"
- User asks to "test this skill thoroughly", "run the full pipeline"
- User wants to "package this skill for distribution"
- User says "take this skill through the full lifecycle"

**Core philosophy:** Don't duplicate what exists. Orchestrate specialized tools in the right sequence with the right handoffs.

---

## Stage 0: Intake & Scoping

**Goal:** Understand what the user wants to build or improve.

**Step 0.1 — Detect mode:**
- **Create mode:** User wants a new skill from scratch
- **Improve mode:** User has an existing skill to optimize
- **Validate mode:** User wants to test an existing skill
- **Package mode:** User wants to ship a finished skill

**Step 0.2 — Gather context:**

*(Context questions vary by mode — some modes need more detail than others.)*

For **Create mode:**
- What should this skill make Claude do?
- When should it trigger? (user phrases, scenarios)
- What's the expected output format?
- Are there objective success criteria? (if yes → testable; if no → subjective, skip quantitative eval)
- Any similar skills to reference?

For **Improve mode:**
- Which skill? (path to SKILL.md)
- What's wrong with it? (form issues, behavior issues, trigger issues, or "not sure, just make it better")
- Do you have test cases already? (evals.json)

For **Validate mode:**
- Which skill?
- What scenarios should it handle?
- What's the baseline? (no skill, or old version)

For **Package mode:**
- Which skill?
- Any dependencies? (scripts, references, assets)

**Step 0.3 — Route to appropriate stage:**
- Create mode → Stage 1 (Creation)
- Improve mode → Stage 2 (Form) or Stage 3 (Behavior) depending on issue type
- Validate mode → Stage 3 (Behavior)
- Package mode → Stage 6 (Packaging)

---

## Stage 1: Creation (Create mode only)

**Goal:** Generate initial SKILL.md from user requirements.

**Step 1.1 — Research:**
- Check for similar skills in `~/.claude/skills/`
- Look for relevant MCP tools that might be useful
- Search for best practices in existing high-quality skills

**Step 1.2 — Draft SKILL.md:**
Use the official skill-creator's `init_skill.py` if available, otherwise write manually following this structure:

```yaml
---
name: skill-name
description: <500 chars, must match trigger phrases>
---

# skill-name — One-line summary

**What this does:** ...

**When to invoke:**
- User types `/skill-name`
- User asks to "..." (natural trigger phrases)

## Step 1: ...
## Step 2: ...
## Decision rules
## Pitfalls
```

**Step 1.3 — Write initial test cases:**
If the skill is objectively testable, create `evals/evals.json`:

```json
{
  "skill_name": "skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "realistic user request",
      "expected_output": "what success looks like",
      "files": ["optional-test-file.txt"]
    }
  ]
}
```

**Step 1.4 — Proceed to Stage 2 (Form validation).**

---

## Stage 2: Form Validation

**Goal:** Ensure SKILL.md is structurally sound before behavioral testing.

**Step 2.1 — Run quick validation:**
If official skill-creator's `quick_validate.py` is available:
```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-path>
```

Otherwise, check manually:
- YAML frontmatter present and valid
- `name` and `description` fields present
- Description < 500 chars
- Trigger phrases listed
- Steps are numbered and sequential
- No forward references (Step 3 mentioned in Step 2)

**Step 2.2 — Run skill-edit:**
Invoke `/skill-edit` on the SKILL.md to catch:
- Description/body mismatch
- List-shape drift
- Format inconsistency
- Duplication
- Vague pitfalls
- Section ordering issues

**Step 2.3 — Review and apply fixes:**
Read the appraisal report from skill-edit. Apply recommended changes.

**Step 2.4 — Route to next stage:**
- If test cases exist → Stage 3 (Behavioral validation — verify skill changes agent behavior)
- If no test cases → Stage 5 (Description optimization — tune trigger accuracy)

---

## Stage 3: Behavioral Validation

**Goal:** Verify the skill actually changes agent behavior.

**Step 3.1 — Choose validation approach:**

**Option A: Use skill-evaluator** (recommended for single-skill deep dive):
- Invoke `/skill-evaluator` with the skill path
- This runs:
  - **Stage 0 (SSL Recall):** Can the skill be discovered from its description?
  - **Stage 1 (Behavioral A/B):** Does it change behavior? (Haiku with/without skill, Codex blind-judges)
  - **Stage 2 (Iteration):** Hill-climbing with eval set (if requested)

**Option B: Use official skill-creator eval pipeline** (recommended for multi-skill benchmarking):
- Run `run_eval.py` to execute with_skill vs baseline in parallel
- Run `aggregate_benchmark.py` to generate quantitative comparison
- Run `generate_report.py` to launch eval-viewer HTML interface

**Step 3.2 — Interpret results:**

From skill-evaluator:
- **Prevents real failure:** Skill is load-bearing, keep it
- **Calibrates response:** Skill improves quality, keep it
- **Matches baseline:** Either probe is too easy, or skill is redundant → investigate
- **Overreaches:** Skill makes things worse → debug

From official eval pipeline:
- Check pass rate (% of evals where skill met expected output)
- Check token efficiency (with_skill vs baseline token consumption)
- Check timing (with_skill vs baseline duration)

**Step 3.3 — Decision point:**
- If skill passes validation → proceed to Stage 4 (Iteration) or Stage 5 (Description optimization)
- If skill fails → return to Stage 1 (rewrite) or Stage 2 (fix form issues)
- If "matches baseline" → write harder test cases and re-run

---

## Stage 4: Iteration (Optional, for continuous improvement)

**Goal:** Hill-climb the skill using eval sets as learning signals.

**Step 4.1 — Split eval set:**
- 60% optimization set (used for tuning)
- 40% holdout set (used for validation)
- Keep a small regression core (3-5 cases that must never break)

**Step 4.2 — Run iteration loop:**

**Option A: Use skill-evaluator Stage 2:**
- Make one explainable change per cycle
- Re-run on optimization set
- Check for score gain + no regression on holdout
- Human reviews winning traces before merge

**Option B: Use official skill-creator's `run_loop.py`:**
- Runs 5 rounds of description optimization
- Uses 20-query test set (10 should-trigger + 10 should-not-trigger)
- Automatically selects best-performing description

**Step 4.3 — Proceed to Stage 5 (Description optimization).**

---

## Stage 5: Description Optimization

**Goal:** Maximize trigger accuracy — skill fires when it should, stays silent when it shouldn't.

**Step 5.1 — Generate test queries:**
Create 20 test queries:
- 10 that **should** trigger the skill (positive cases)
- 10 that **should not** trigger the skill (negative cases, especially near-misses)

**Step 5.2 — Human review:**
Present queries in HTML template (if available) or as markdown list. User adjusts any that are ambiguous or wrong.

**Step 5.3 — Run optimization loop:**
If official skill-creator's `improve_description.py` is available:
```bash
python ~/.codex/skills/.system/skill-creator/scripts/improve_description.py \
  --skill-path <path> \
  --queries <queries.json> \
  --rounds 5
```

This iterates on the `description` field to maximize trigger accuracy.

**Step 5.4 — Select best description:**
Choose the description with highest F1 score (balancing precision and recall).

**Step 5.5 — Update SKILL.md:**
Replace the `description` field in frontmatter with the optimized version.

**Step 5.6 — Proceed to Stage 6 (Packaging).**

---

## Stage 6: Packaging

**Goal:** Prepare skill for distribution.

**Step 6.1 — Gather dependencies:**
Check if skill references:
- Scripts in `scripts/` subdirectory
- Reference docs in `references/` subdirectory
- Assets (icons, templates) in `assets/` subdirectory

**Step 6.2 — Generate metadata:**
If official skill-creator's `generate_openai_yaml.py` is available:
```bash
python ~/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py <skill-path>
```

This creates `agents/openai.yaml` with UI metadata.

**Step 6.3 — Package:**
If official skill-creator's `package_skill.py` is available:
```bash
python ~/.codex/skills/.system/skill-creator/scripts/package_skill.py <skill-folder>
```

This generates a `.skill` file that users can install directly.

Otherwise, create a tarball manually:
```bash
cd ~/.claude/skills/
tar -czf skill-name.skill skill-name/
```

**Step 6.4 — Final checklist:**
- [ ] SKILL.md has valid frontmatter
- [ ] Description < 500 chars
- [ ] Trigger phrases documented
- [ ] Test cases pass (if applicable)
- [ ] No broken references
- [ ] Dependencies included
- [ ] Version number set

**Step 6.5 — Report completion:**
Provide:
- Path to packaged .skill file
- Installation instructions
- Summary of validation results (pass rate, token efficiency, timing)
- Known limitations or edge cases

---

## Decision Rules

| Situation | Action |
|-----------|--------|
| User wants to create a new skill | Start at Stage 1 (Creation) |
| User wants to improve existing skill's structure | Start at Stage 2 (Form validation) |
| User wants to test if skill works | Start at Stage 3 (Behavioral validation) |
| User wants to optimize trigger accuracy | Start at Stage 5 (Description optimization) |
| User wants to ship a skill | Start at Stage 6 (Packaging) |
| Skill fails form validation | Fix issues, re-run Stage 2 |
| Skill fails behavioral validation | Return to Stage 1 (rewrite) or Stage 2 (fix form) |
| Skill "matches baseline" | Write harder test cases, re-run Stage 3 |
| User wants continuous improvement | Run Stage 4 (Iteration loop) |
| Official skill-creator tools unavailable | Fall back to manual equivalents |
| Skill is subjective (writing style, tone) | Skip quantitative eval (Stage 3), go straight to Stage 5 |

---

## Pitfalls

**Skipping form validation before behavioral testing:**
If SKILL.md has description/body mismatch, the recall stage will fail. Always run Stage 2 before Stage 3.

**Running behavioral validation without test cases:**
Stage 3 requires concrete test scenarios. If user hasn't provided them, ask for 2-3 realistic prompts first.

**Treating "matches baseline" as deletion signal:**
This often means the test case is too easy, not that the skill is useless. Write a harder probe and re-test.

**Optimizing description before validating behavior:**
Description optimization (Stage 5) assumes the skill's behavior is already correct. Don't tune triggers for a broken skill.

**Packaging without final validation:**
Always re-run quick_validate.py (or manual checks) before packaging. Catch broken references early.

**Mixing multiple changes in one iteration cycle:**
In Stage 4, make one explainable change per cycle. Otherwise you can't tell which change caused the score to move.

**Reward hacking in iteration:**
Watch for token bloat (skill adds unnecessary verbosity), universal hedging (skill makes agent overly cautious), or verbatim eval phrasing (skill memorizes test cases). These inflate scores without improving real-world performance.

**Ignoring the holdout set:**
In Stage 4, always check holdout set performance. Optimization set scores can be gamed; holdout set catches overfitting.

**Skipping human review of winning traces:**
Before merging an iteration, read the actual agent outputs. Scores can lie; traces don't.

**Using Sonnet-class agents for behavioral validation:**
skill-evaluator is calibrated for Haiku. Using Sonnet wastes compute and produces different baseline metrics, making it impossible to compare against the Haiku-calibrated benchmarks.

---

## Related Skills

- [[skill-edit]] — Form validation (Stage 2)
- [[skill-evaluator]] — Behavioral validation (Stage 3, Option A)
- [[codex]] — Subagent dispatch for expensive operations
- [[dev-log]] — Record design decisions and dead ends during skill development

---

## Operational Notes

**Tool availability:**
- Official skill-creator tools live in `~/.codex/skills/.system/skill-creator/scripts/`
- If unavailable, fall back to manual equivalents (documented in each stage)

**Subagent dispatch:**
- Use Haiku for trivial operations (file validation, quick checks)
- Use Codex (via `/codex`) for expensive operations (behavioral A/B testing, blind judging)
- Use Sonnet only as degraded fallback

**Reporting format:**
Emit appraisal-style reports at each stage:
```
Stage: <stage-name>
Diagnosis: <what was found>
Actions taken: <what was done>
Results: <quantitative + qualitative>
Next: <recommended next stage>
```

**Chaining:**
Stages can be run independently or chained:
- Full pipeline: Stage 1 → 2 → 3 → 4 → 5 → 6
- Quick validation: Stage 2 → 3
- Optimization only: Stage 5
- Packaging only: Stage 6

**Context preservation:**
Between stages, preserve:
- Skill path
- Eval set path (if exists)
- Validation results (pass rate, token efficiency, timing)
- Iteration history (if Stage 4 was run)

This allows resuming from any stage without re-running earlier work.
