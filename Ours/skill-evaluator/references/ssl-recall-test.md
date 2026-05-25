# Stage 0 — SSL Recall Test

This file specifies the recall protocol referenced from `SKILL.md`. Run it before behavioural A/B (Stage 1) on any full-library evaluation.

## What it measures

Whether a skill is **discoverable**: given a probe scenario, does the agent's skill-selection step return the target skill in its top-K choices?

This is a different question from "does the skill help when loaded". A skill can be perfectly written and behaviourally useful and still never get picked, because:

- Its `summary` is too generic ("Procedural discipline for X").
- Two skills' summaries describe the same trigger and the agent picks the wrong one.
- The summary uses internal vocabulary the agent doesn't map back to the situation.
- The summary is buried in jargon and the keyword that should match the probe never appears.

If recall fails, behaviour testing is moot — the skill won't reach the agent in production.

## Inputs

- The full skill library — frontmatter `summary` fields only, **bodies excluded**. Format as a plain numbered list, one line per skill: `[1] slug-name: summary text`.
- A set of probe scenarios — one per skill being tested. Each probe is a 1–3 sentence situation prompt and identifies a target skill (the one that should be selected).

You can reuse the Stage-1 probes here — same scenarios, different question.

## Protocol

For each probe:

1. Render the prompt: situation + numbered skill list + "Pick the top-3 skills you would open here. Return their numbers in order, comma-separated."
2. Send it to a single LLM (haiku is fine; recall is a triage task, not deep reasoning).
3. Parse the returned ranking.
4. Record:
   - **Recall@1** — was the target skill at rank 1?
   - **Recall@3** — was it in the top 3?
   - **MRR** — reciprocal rank of the target if present, else 0.
   - **Distractors** — which non-target skills appeared in top-3? (these are the recall-overlap risks.)

Aggregate per-skill into a recall report:

| Skill | Recall@1 | Recall@3 | MRR | Top distractor |
|---|---|---|---|---|
| target-a | ✓ | ✓ | 1.00 | — |
| target-b | ✗ | ✓ | 0.50 | sibling-skill |
| target-c | ✗ | ✗ | 0.00 | three other skills |

## Decision rules

- **Recall@3 = 1, MRR ≥ 0.5** — recall is healthy. Proceed to Stage 1.
- **Recall@3 = 1, MRR < 0.5** — target is in top-3 but consistently outranked. Note the top distractor; sometimes it's fine (peer skill is genuinely a near-substitute), sometimes the target's summary needs to surface a more specific keyword. Proceed to Stage 1, but flag the distractor for review.
- **Recall@3 = 0** — target is unreachable. **Do not run Stage 1**. Rewrite the summary first. Common fixes:
  - Lead with the trigger condition, not the description ("Open when X happens" beats "A skill for X").
  - Include the noun the probe scenario uses (if probes mention "rebuttal", the summary should too).
  - Distinguish from sibling skills explicitly — if two skills both touch citations, name the difference up-front.
- **Recall@3 = 0 across many skills** — the library has a structural problem (overlapping summaries, missing taxonomy). Fix at the library level before running per-skill A/B.

## When to skip Stage 0

Two legitimate cases:

1. **Single-skill test.** You're testing one skill in isolation, and your test setup hand-loads it. Recall is irrelevant.
2. **Regression run.** You already ran Stage 0 in the previous evaluation cycle and the summaries haven't changed. Re-running is wasted compute.

Otherwise, always do Stage 0. It's cheap (one LLM call per probe, no spawning) and catches the most expensive failure mode in skill libraries: writing a great skill nobody can find.

## Cost

A 60-skill recall test is ~60 haiku calls × ~3000 token prompt = ~180k tokens. Roughly 5 minutes wall clock with no batching needed. Stage 0 is the cheap stage; Stage 1 is the expensive one. Doing Stage 0 first lets you skip Stage 1 on skills that fail recall — saving the bulk of the budget on skills that wouldn't have produced reliable signal anyway.
