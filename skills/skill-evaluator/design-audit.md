# Design Audit

Is this skill well-made? What should be fixed?

## When to use

- You want structural quality signal beyond pass/fail.
- Refining a skill and need a scorecard to guide iteration.
- Comparing two skills that solve the same problem.

## Skip when

- User says "just run the A/B".
- Design hasn't changed since last audit.
- You only need a binary "helps or doesn't" answer (use Behavioral A/B).

## Procedure

Read the full skill (SKILL.md + all referenced files) and score 12 dimensions, 1–10 each:

| # | Dimension | Core question |
|---|---|---|
| 1 | Positioning | Trigger condition specific? Distinguishable from peers? |
| 2 | Structure | Logical flow? One job done well? |
| 3 | Granularity | Right scope — not three skills in one, not too narrow? |
| 4 | Context engineering | Token-efficient? References modular and on-demand? |
| 5 | Usefulness | Would an agent without it make a worse decision? |
| 6 | Reusability | Works across projects and teams? |
| 7 | Composability | No conflicts with common peer skills? |
| 8 | Maintainability | Easy to update without rewrite? |
| 9 | Safety | No dangerous defaults? |
| 10 | Transferability | Portable across agents (Claude Code / Cursor / Codex)? |
| 11 | Team-friendliness | Understandable by someone who didn't write it? |
| 12 | Evolution | Room to grow? |

## Output

1. **Overall score** — mean of 12 dimensions.
2. **Most overrated aspect** — where perception exceeds reality.
3. **Most underrated aspect** — where reality exceeds perception.
4. **Top 3 refinement actions** — specific, actionable, ordered by impact.
5. **Four-way extraction:**

| Category | Criterion |
|---|---|
| Adopt as-is | Score ≥7, no redesign needed. |
| Adopt after redesign | Good idea, wrong form or scope. |
| Pattern only | Learn from it, don't copy it. |
| Reject | Fundamentally misaligned or unsafe. |

## Scoring guidance

- 9–10: Exemplary. Teaching example.
- 7–8: Strong. Minor improvements.
- 5–6: Adequate. Clear gaps.
- 3–4: Weak. Needs significant rework.
- 1–2: Broken or missing.

Be specific. Cite actual content from the skill as evidence. "Good structure" is not a score justification; "procedure section has 7 steps in logical dependency order with clear skip conditions" is.

## Cost

~8k tokens (one sonnet call reading the full skill + producing the scorecard).
