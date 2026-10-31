# Evidence 04: Posture-4 Goal-Block Drift — Observed Failure and Fix

## Observation

- **Date:** 2026-05-19
- **Context:** Running think-then-act on a voting-mechanism design question
- **Session ID:** 2eceda9b-d005-4893-ae32-1444c4953044

## The Drift Pattern

When running the default 5-posture sequence:
1. Postures 1-3 (Premises → First-Principles → Synthesis) execute correctly
2. Synthesis ends with "so we should build X"
3. **Posture 4 collapses** — instead of producing the canonical Goal block, agent produces:
   - "Can it be built: yes"
   - "Forced silence: basically no"
   - "MVP scope: Y"
   - Section titled "工程性结论" / "engineering conclusions"

This is a **recommendation**, not a **goal**. No sensor, no threshold, no stop rule, no way to verify the recommendation was right.

## What Posture 4 Must Produce

```
Goal: <one-sentence description>
Sensor: <observable thing to measure>
Metric: <how to quantify>  Threshold: <success value>
Feedback: <when readable>  Stop: <success | failure | timeout rules>
```

## Fix Applied

Added explicit failure-mode callout to think-then-act.md (both locations):

> "If your Posture-4 output reads like an executive summary, a yes/no verdict, or an 'engineering conclusions' list, you skipped Posture 4 — open goal-setting.md and write the actual Goal block before dispatching."

## What This Proves

1. **Skills need anti-drift mechanisms** — even well-designed skills degrade under model tendencies (synthesis → conclusion is a natural language flow that bypasses the structured output requirement)
2. **Failure modes are observable and fixable** — the user caught the drift, diagnosed the root cause, and the fix is a single paragraph
3. **The Goal block is the critical output** — without it, dispatched work has no verifiable acceptance criteria, which defeats the purpose of the entire think-then-act pipeline

## Relationship to Other Evidence

This connects to Evidence 02 (competitor eval P3): the same "threshold softening in handoff" pattern. P3 showed it at the dispatch boundary; this observation shows it at the posture boundary. The fix addresses both: verbatim goals (Evidence 02 fix c) + explicit drift callout (this fix).

## Limitation

- Single observation, not a controlled A/B
- Fix has not been re-tested with a formal probe
- The drift may recur under different task types (the callout is a heuristic, not a guarantee)
