# Evidence 01: MetaHarness Behavioral A/B — Full Library Run

## Experiment Setup

- **Date:** 2026-05-13 (doc-quality) + behavioral run (date in SKILL_BEHAVIORAL_EVAL.md)
- **Method:** MetaHarness — spawn 2 Haiku agents per probe (with-skill A vs baseline B), Codex GPT-5.5 blind-judges with random RED/BLUE labels
- **Scale:** 49 skills × 1-2 probes = 61 probes, 122 Haiku invocations, 61 Codex judges
- **Cost:** ~14M tokens Haiku + ~3M tokens Codex, ~3 hours wall-clock
- **Source file:** `minions/roles/common/SKILL_BEHAVIORAL_EVAL.md`

## Results Relevant to Think-Then-Act

Think-then-act is a meta-skill (orchestrator of sub-postures). Its sub-postures were tested individually:

| Sub-posture | Bucket | Detail |
|---|---|---|
| `first-principles` | Calibrates response | Stays calibrated; doesn't slide into crank mode |
| `dialectical-synthesis` | Calibrates response | Thesis/antithesis/synthesis structure with conditional resolution |
| `coding-methodology` | Prevents real failure | Without skill, baseline over-executes (implements before scoping) |

## Key Findings

### 1. Workflow-orchestration skills prevent over-execution

The behavioral pattern think-then-act enforces ("scope before act") was validated across multiple skills:
- `feature-implementation`: with-skill asks clarification questions before writing
- `apply-revisions`: with-skill builds checklist with source_id mapping (baseline dives into implementation)
- `aspect-review`: with-skill refuses to read prior round's reports (preserves independence)

### 2. Haiku's three failure modes that skills correct

From the aggregate analysis:
1. **Invents tool names under uncertainty** — skills act as vocabulary anchor
2. **Defaults to "ask the user" when context is thin** — skills give scaffolding to act autonomously
3. **Over-executes on open-ended tasks** — skills with clarification gates prevent silent scope guessing

Think-then-act directly addresses failure modes #2 and #3.

### 3. Reasoning-discipline skills provide calibration value

> "The reasoning-discipline skills (first-principles, dialectics, karpathy-codified-as-coding-methodology) provide calibration value, not error-prevention value. They make answers more defensible but don't typically flip a wrong decision to right."

This is an honest characterization: the sub-postures improve quality of reasoning but are not the primary error-prevention mechanism. The error-prevention comes from the orchestration layer (dispatch discipline, skip triggers, evidence-first constraint).

## What This Proves

- Think-then-act's sub-postures have measurable behavioral effect on Haiku-class agents
- The "scope before act" pattern prevents real failures (over-execution)
- The reasoning postures (first-principles, dialectics) improve answer quality but don't flip wrong→right decisions
- 65% of the full skill library has measurable positive effect; think-then-act's components are in the positive set

## Limitations

- Think-then-act as a whole (the orchestrator) was not tested as a single unit in this run — only its sub-postures
- MetaHarness is calibrated for Haiku; Sonnet-class agents show less differentiation
- "Calibrates response" is weaker evidence than "prevents real failure"
