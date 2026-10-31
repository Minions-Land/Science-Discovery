# Think-Then-Act Skill — Evidence Collection

## What is Think-Then-Act

A structured planning skill that provides five composable "postures" (Unstated Premises, First-Principles, Dialectical Synthesis, Goal-Setting, Plan Persistence) for autonomous agents to reason before acting. The agent decides which postures to use, how many, and in what order. After thinking, it dispatches all execution to subagents — never self-executes.

Core design principle: **context separation** — the thinking context stays clean for coordination; the doing context is disposable.

## Claim (what we want to prove)

Think-then-act improves autonomous agent decision quality by:
1. Preventing premature execution on ambiguous tasks
2. Surfacing unstated constraints before they become bugs
3. Producing verifiable acceptance criteria (not vague "looks good")
4. Surviving context resets without re-deriving plans
5. Adapting to task complexity (skip on trivial, full pipeline on ambiguous)

## Competitors / Baselines

| Baseline | Source | What it does |
|---|---|---|
| No skill (raw Haiku) | MetaHarness control | Agent reasons from training alone |
| Superpowers `brainstorming` | Claude Code built-in | Divergent idea generation |
| Superpowers `writing-plans` | Claude Code built-in | Structured plan with no-placeholder rule |
| `ultrathink` | Extended thinking prompt | More compute on reasoning, no structure |

## Evidence Summary

See individual evidence files for details:
- [evidence-01-metaharness-behavioral-ab.md](evidence-01-metaharness-behavioral-ab.md) — Full library A/B showing sub-postures prevent real failures
- [evidence-02-competitor-eval-2026-05-17.md](evidence-02-competitor-eval-2026-05-17.md) — 3-probe × 4-variant A/B against competitor prompts
- [evidence-03-self-assessment-removal.md](evidence-03-self-assessment-removal.md) — Negative result: in-skill self-assessment hurts
- [evidence-04-posture4-drift-fix.md](evidence-04-posture4-drift-fix.md) — Observed failure mode and iterative fix

## Strengths (supported by evidence)

1. **Sub-postures prevent API hallucination** — first-principles and dialectics scored "calibrates response" in MetaHarness; the EACN3 cluster skills (which TTA dispatches into) scored "prevents real failure" in 13/13 cases
2. **Adaptive complexity** — skip-trigger prevents ceremony on trivial tasks (validated by competitor eval P1 fix)
3. **Evidence-first constraint** — forces repo-evidence before messaging offline roles (validated by competitor eval P2 fix)
4. **Verbatim goal passing** — eliminates threshold softening in handoff (validated by competitor eval P3 fix)
5. **Iterative self-improvement** — v3→v6 evolution driven by empirical A/B, not intuition
6. **Context separation** — thinking agent never self-executes, keeping coordination context clean across multi-task sessions

## Weaknesses (honest assessment)

1. **Text-only rules don't override Haiku defaults** — prose instructions alone failed to change behavior on P2; required a concrete worked example (+9 lines). This is a fundamental limitation of prompt-based skills on smaller models.
2. **Ceremony risk on trivial tasks** — even with skip-trigger, Haiku still occasionally runs unnecessary postures on well-specified tasks (P1 failure in v3)
3. **No measurable effect on Sonnet-class models** — MetaHarness explicitly notes "Sonnet already does most of what skills prescribe; differences vanish in the noise." The skill is calibrated for Haiku-class executors.
4. **Goal-Setting drift** — Posture 4 tends to collapse into engineering conclusions instead of producing the canonical 5-element Goal block (observed 2026-05-19, required explicit failure-mode callout)
5. **Self-assessment is counterproductive** — adding reflection prompts made Haiku write defensive restatements and over-execute on trivial tasks (5-probe A/B, 2/5 wins with confounds)

## Comparison Dimensions

| Dimension | Think-Then-Act | brainstorming | writing-plans | ultrathink |
|---|---|---|---|---|
| Handles trivial tasks | Skip trigger (v6) | Natural anti-pattern | No skip mechanism | Wastes compute |
| Evidence-first | Explicit constraint | No | No | No |
| Verbatim thresholds | Explicit rule | No | Yes (no-placeholders) | No |
| Context separation | Hard rule | No | No | No |
| Survives resets | Plan persistence | No | No | No |
| Composable | 5 independent postures | Monolithic | Monolithic | Monolithic |
| Calibrated for model class | Haiku-optimized | General | General | General |
