---
slug: preliminary-problem-definition
summary: Preliminary / Problem Definition section — formalize definitions clearly, list assumptions explicitly, bridge naturally to the Method section.
layer: logical
tools:
version: 2
status: active
supersedes:
references: methodology-discipline
provenance: R7-evolved
---

# Skill — Preliminary / Problem Definition

This section establishes the formal foundation that the Method section builds upon. The reader should finish Preliminaries knowing every definition and assumption they need, with a clear path into the technical exposition that follows.

## When to invoke

- Drafting the Preliminary / Problem Definition / Setup section.
- When the paper has a theoretical component requiring formal definitions.

## Procedure

Begin with formal definitions of core concepts using `\begin{definition}` environments. Prose definitions are insufficient — reviewers need to locate and verify definitions quickly, and LaTeX environments provide that structure.

Next, state assumptions explicitly using `\begin{assumption}` environments. Implicit assumptions are a primary target for reviewer attacks; making them explicit converts a vulnerability into a strength. When the number of symbols exceeds 10, provide a notation table (in the Appendix or at the beginning of Preliminaries).

Close with a natural transition to the Method section ("Given the above formulation, we now describe…"). The Preliminaries should not end abruptly — the bridge paragraph signals that the formal setup is complete and the technical contribution begins.

Proofs do not belong here. They go in Theoretical Justification or the Appendix.

## Pitfalls

- Defining concepts in prose without using Definition environments.
- Assumptions buried in prose where reviewers cannot locate them.
- Preliminaries ending abruptly without a bridge to the Method section.
