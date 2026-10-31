---
slug: writing-style
summary: Eliminate AI-generated tone and translationese; ensure academic prose is natural, precise, and free of redundancy. Blacklist high-frequency AI words such as delve/pivotal/landscape.
layer: logical
tools:
version: 2
status: active
supersedes:
references: cn-en-academic-polish
provenance: R7-evolved
---

# Skill — Writing Style

Academic prose should be invisible — the reader sees the argument, not the writing. AI-generated text and translationese both fail this test because they introduce recognizable patterns that distract from content. This skill operates at three levels: word choice, sentence structure, and paragraph rhythm.

## When to invoke

- Polishing prose style in any section.
- Checking for AI writing artifacts or literal-translation structures.

## Word choice

**Blacklisted AI markers.** Remove: delve, pivotal, landscape, tapestry, underscore, noteworthy, intriguingly, harness, leverage, utilize, multifaceted, paradigm shift, holistic. Replacements: delve → examine; pivotal → key; leverage → use; utilize → use.

**Translationese patterns.** These survive from Chinese-source drafts or AI generation:
- "With the rapid development of…" → start from the concrete problem
- "plays an important role" → "enables" / "is central to"
- "has attracted wide attention" → "is widely studied" or remove entirely

**Prefer verbs over nominalizations.** "perform an analysis" → "analyze"; "make a comparison" → "compare".

**Use specific nouns.** "this result" → "the 30× speedup" / "the convergence guarantee". Vague referents force the reader to backtrack.

## Sentence structure

**Keep subject and verb adjacent.** Do not insert long relative clauses between subject and verb.

**Given-before-new information order.** Each sentence: familiar context first → new information later. Place the most important new information at sentence end.

**Remove redundant openings.** Delete "It is worth noting that" / "Importantly," / "Notably," / "In this section, we…". These add no information.

## Paragraph rhythm

**Avoid consecutive This/We sentence openings.** Do not begin two consecutive sentences with "This" or "We".

**Avoid rule-of-three patterns.** Do not repeatedly use "X, Y, and Z" tricolon structures — this is a hallmark of AI-generated prose that reviewers recognize.

## Pitfalls

- Opening with "delve into" (the single most recognizable AI marker).
- Three consecutive sentences beginning with "We".
- Every paragraph containing an "X, Y, and Z" tricolon enumeration.
- "this approach" with unclear antecedent (forces the reader to backtrack).
