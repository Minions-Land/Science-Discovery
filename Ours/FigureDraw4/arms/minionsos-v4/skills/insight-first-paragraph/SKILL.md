---
slug: insight-first-paragraph
summary: Every technical subsection opens with one sentence stating the conceptual move ("the core insight is X"), then formula(numbered)+citation, then implication. Anti-textbook-recap rhythm. Corrections of primary literature welcome.
layer: logical
tools:
version: 1
status: active
references: methodology-discipline, related-work-discipline, paper-quality-contract
provenance: human + LLM-Survey
---

# Skill — Insight-First Paragraph

Survey and method subsections drift into textbook recap by default. The user's contract is the opposite: every subsection opens by stating *the conceptual move that distinguishes this method*, then grounds it with formulas and references, then closes with the implication. Corrections of prior-literature mis-statements are welcomed.

## When to invoke

- Drafting any technical subsection in a survey, related work, or method section.
- Polishing a section that "reads like a Wikipedia entry".
- Editing a Method section that lists facts without a thread.

## The three-beat rhythm

Each technical subsection opens with this pattern:

1. **Insight** — one sentence: *"The core insight of [method class] is [the conceptual move]."*
   Examples from LLM-Survey:
   - 线性注意力的核心 insight 是一个优雅的代数观察 — by reordering Q (K^⊤ V) one drops a dimension from the cost.
   - Hardware-Efficient Attention 的核心 insight 是 — without changing the attention algorithm itself, restructuring memory access yields the speedup.
   - 混合架构的核心 insight 是 — different layers and different tokens have different attention needs; one architecture fits none.
2. **Formula + ref** — the equation realising the insight, with `\eqref{}` and a citation. Anchor at the insight, not after three textbook lines.
3. **Implication** — what this enables (faster, more expressive, more parallel) AND what it costs (lost expressiveness, harder optimisation, special hardware). Both halves required.

## Anti-textbook-recap rule

Avoid:
> "Attention is computed as $QK^\top V$. Several variants have been proposed. We list them below."

Prefer:
> "The core insight of linear attention is reordering the matmul: by computing $K^\top V$ first, the cost drops from $O(n^2 d)$ to $O(n d^2)$ (Eq.~\ref{eq:linear-attn}). This is exact for kernel-feature-map attention and approximate for softmax (Performer, \citet{choromanski2021}); the trade-off is the loss of strict softmax normalisation, which manifests as degraded long-range retrieval on tasks like…"

Textbook recap is what readers can skim a Wikipedia article for. The insight is what they came to your paper for.

## Corrections of primary literature

When a primary paper mis-stated a derivation (e.g. Vaswani's original sinusoidal-PE argument), correct it. The correction earns the section its place; without it the section is paraphrase.

Pattern:
- State the original argument.
- Identify the gap.
- Provide the corrected derivation.
- Cite the original AND state where the correction enters.

This is not aggression. It is the section's reason for existence.

## Procedure

1. **Audit the section opening.** Does the first sentence state an insight, or does it restate notation? If the latter, rewrite.
2. **Audit the formula anchor.** Is the central formula tagged at the insight ("the reorder", "the masking", "the recurrence"), or buried after three textbook lines? Move it up.
3. **Audit the close.** Does the paragraph end with what this *enables and costs*, or does it end with "see [Smith 2020] for details"? Add the implication.

If any answer is wrong, rewrite in three-beat rhythm.

## Pitfalls

- Opening with a citation rather than an insight. "[Vaswani et al., 2017] introduced…" — wrong rhythm.
- "Recently, [X] proposed Y. Y improves Z." This is news, not science.
- Insight stated, then formula buried two paragraphs later. Insight + formula must co-locate.
- Cost not stated. Every method has a cost; if you don't name it, reviewers will.
- Refusing to correct a primary-source mis-statement out of politeness. Politeness is not the standard.
- Bulleting the insights. Survey-style technical sections use *flowing paragraph prose*, not bullet lists. Bullets are reserved for Introduction contributions.
