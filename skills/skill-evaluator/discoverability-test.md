# Discoverability Test

Will agents find this skill at the right moment?

## When to use

- Full-library evaluation (check all skills' descriptions compete fairly).
- A skill "should fire but doesn't" in production.
- After rewriting a skill's description.

## Skip when

- Single-skill test where you hand-load the skill into the prompt.
- Regression run where descriptions haven't changed since last pass.

## Procedure

1. **Assemble the skill list.** Collect the `description` field from every skill in the library (or a representative 15–30 including distractors). Format as a numbered list — descriptions only, no bodies.

2. **Write a probe scenario.** 1–3 sentences describing a concrete situation where the target skill should activate. Reuse the Behavioral A/B probe if you have one.

3. **Ask a haiku-class model:** "Given this situation, pick the top-3 skills from the list. Return their numbers, comma-separated."

4. **Record:**
   - Recall@1 — target at rank 1?
   - Recall@3 — target in top 3?
   - MRR — reciprocal rank (0 if absent).
   - Top distractor — which non-target skill ranked highest?

## Decision

| Result | Action |
|---|---|
| Recall@3 = 1, MRR ≥ 0.5 | Healthy. Proceed. |
| Recall@3 = 1, MRR < 0.5 | Outranked by a peer. Flag the distractor, but proceed. |
| Recall@3 = 0 | **Unreachable.** Rewrite description before any further evaluation. |

## Common fixes for Recall@3 = 0

- Lead with the trigger condition ("Use when X happens" beats "A skill for X").
- Include the noun the probe uses (if probes say "rebuttal", description should say "rebuttal").
- Distinguish from sibling skills explicitly in the first sentence.

## Cost

~3k tokens per probe (one haiku call). A 60-skill library test ≈ 180k tokens total, ~5 minutes.
