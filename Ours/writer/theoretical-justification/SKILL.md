---
slug: theoretical-justification
summary: Theoretical Analysis section uses theorem-proof structure; proof sketch in main text, complete proof in appendix; each theorem followed by a Remark explaining practical implications.
layer: logical
tools:
version: 2
status: active
supersedes:
references: preliminary-problem-definition
provenance: R7-evolved
---

# Skill — Theoretical Justification

This section convinces the reader that the method has formal guarantees. The structure follows a statement → sketch → interpretation pattern: state the result formally, give enough proof for intuition, then explain what it means in practice.

## When to invoke

- Drafting the Theoretical Analysis / Theory section.
- When the paper includes convergence guarantees / bounds / complexity analysis.

## Procedure

State core conclusions using `\begin{theorem}` environments. Each theorem explicitly references the assumptions from Preliminaries — the reader should be able to trace exactly which conditions are required.

Provide a proof sketch in the main text (~0.5 page) covering the key steps and intuition. The complete proof goes in the Appendix. Reviewers want to understand the proof strategy without reading every algebraic step inline.

Follow each theorem with a Remark explaining its practical meaning ("This implies that convergence is guaranteed when…"). Non-theory reviewers cannot extract practical significance from a formal statement alone; the Remark bridges that gap.

If prior bounds exist for the same problem, provide a comparison table (our bound vs. prior bounds) so the improvement is immediately visible.

## Pitfalls

- Placing a 2-page complete proof in the main text (reviewers do not want to read this inline).
- Theorem without referencing its assumptions (reader does not know the preconditions).
- No Remark (non-theory reviewers cannot understand the practical significance of the theorem).
