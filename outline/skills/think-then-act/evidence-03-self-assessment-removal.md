# Evidence 03: Self-Assessment Removal — Negative Result

## Experiment Setup

- **Date:** 2026-05-16
- **Method:** 5-probe Haiku A/B (4 hard + 1 trivial)
- **Hypothesis:** Adding "recommended self-assessment" (reflect on which postures were load-bearing) would improve calibration
- **Session ID:** af901ee2-d3d2-45bd-9cc7-3c3398fe2525

## Results

| Metric | Value |
|---|---|
| With-assessment wins | 2/5 |
| Confounds | Yes — wins were not clearly attributable to self-assessment |

## Failure Modes Observed

### 1. Defensive restatement instead of honest reflection
Codex flagged 3/5 reflections as "adding no new insight." Haiku writes what looks like reflection but is actually defensive restatement of what it already did — not genuine calibration.

### 2. Over-execution on trivial tasks
P5 (version bump 0.5.2→0.5.3): with-assessment variant auto-committed beyond scope, while baseline correctly just edited the file. The prompt to reflect pushed Haiku toward "doing more" to justify the reflection.

### 3. Wasted on larger models
Sonnet/Opus self-assess naturally (observed in MoE simulation transcripts). The explicit prompt is redundant for capable models and harmful for smaller ones.

## Decision

**Removed self-assessment from think-then-act.** If calibration data is needed, build it as an external audit:
- Gru-log sampler → Opus reviewer of N recent think-then-act applications
- Report on which postures fired on which task types and how often each was load-bearing
- Trigger only on multi-step planning wakes, not trivial ones

## What This Proves

1. **Not all additions to a skill are improvements** — empirical testing caught a harmful feature before it shipped to production
2. **Haiku's reflection is performative, not genuine** — smaller models produce the form of self-assessment without the substance
3. **The skill design process is evidence-driven** — features are added AND removed based on A/B results

## Why This Matters for the Paper

This is a **negative result that strengthens the methodology claim**. It shows:
- The skill evolution process has a removal mechanism, not just accretion
- We test hypotheses and accept negative results
- The system is calibrated to its target model class (Haiku), not designed for an idealized agent
