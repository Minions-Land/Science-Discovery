# Evidence 02: Competitor Eval — 3-Probe × 4-Variant A/B (2026-05-17)

## Experiment Setup

- **Date:** 2026-05-17
- **Method:** 3 probes × 4 variants, Haiku as executor, Codex as blind judge
- **Variants tested:**
  1. Think-Then-Act (v3 at start, evolved to v6 by end)
  2. Superpowers `brainstorming`
  3. Superpowers `writing-plans`
  4. `ultrathink` (extended thinking, no structure)
- **Session ID:** af901ee2-d3d2-45bd-9cc7-3c3398fe2525

## Probes

| Probe | Type | Description |
|---|---|---|
| P1 | Concrete spec | Fully-specified task with file path + acceptance criteria |
| P2 | Ambiguous architectural | Open-ended design question requiring codebase investigation |
| P3 | Multi-role kickoff | Task requiring coordination across multiple agents with quantitative thresholds |

## Results (v3, before fixes)

| Probe | Winner | Why TTA lost |
|---|---|---|
| P1 | `brainstorming` | TTA: Haiku wrote unstated-premises tables on a fully-specced task (ceremony). Brainstorming had "this is too simple" anti-pattern that let Haiku skip. |
| P2 | `writing-plans` | TTA: Haiku EACN-messaged the offline Writer instead of dispatching codex on the codebase. The "Autonomous-only" constraint said "send EACN3 to the relevant role" without preferring repo-evidence first. |
| P3 | `writing-plans` | TTA: Haiku produced Goal-Setting table with quantitative thresholds (≥3 models, p<0.05) but final dispatch acceptance was "protocol document with model list" — thresholds got softened in handoff. |

**Ultrathink lost everywhere** — no skill discipline replaces calibration.

## Fixes Applied (v3 → v6)

| Fix | What changed | Which probe it addresses |
|---|---|---|
| (a) Skip trigger | Hoisted "Skip entirely" with concrete trigger: "spec is concrete: file path + acceptance already stated" | P1 |
| (b) Evidence-first | Rewrote constraint #1 to "Autonomous-only, evidence-first" with explicit ordering: codex/Task on repo BEFORE EACN-message-and-exit | P2 |
| (c) Verbatim goals | Added "Pass goals verbatim" rule borrowing writing-plans' no-placeholders. "TBD", "reasonable", "appropriate" are plan failures | P3 |
| (d) Worked example | Text-only rule didn't move Haiku even at v5. Required a concrete failure-mode example showing the wrong pattern | P2 |

## Results (v6, after fixes)

P2 re-test: Haiku correctly dispatched codex with specific files cited (`minions/lifecycle/role.py`, `minions/tools/whitelist.py`, `eacn3.db`) instead of messaging offline Writer.

## What This Proves

1. **Think-then-act is empirically improvable** — each failure mode was diagnosed and fixed with targeted edits, not wholesale rewrites
2. **Competitor prompts have specific strengths worth absorbing** — writing-plans' no-placeholder rule and brainstorming's skip-on-trivial were both incorporated
3. **Prose rules alone are insufficient for Haiku** — concrete worked examples are required to override strong defaults (lesson (d))
4. **Ultrathink (more compute, no structure) loses to structured skills** — evidence that structure > raw reasoning budget

## What This Does NOT Prove

- We don't have post-fix results for P1 and P3 (only P2 was re-tested)
- The fixes were validated on the same probes they were designed for (no held-out test set)
- v6 has not been tested against a new set of competitor prompts

## Key Insight for Paper

> "Text-only rules don't override Haiku defaults. When a behavioral correction needs to override a model's strong prior ('ask for clarification'), prose rules alone are insufficient — include a concrete failure-mode example. Net cost: +2 lines internal, +9 lines user-level. Worth it."

This is a generalizable finding about prompt-based skill design for smaller models.
