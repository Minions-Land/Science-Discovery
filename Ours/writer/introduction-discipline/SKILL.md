---
slug: introduction-discipline
summary: Introduction covers only background + method-class overview + contribution bullets; no implementation details. 4–6 paragraph hourglass structure ending with contribution itemize.
layer: logical
tools:
version: 2
status: active
supersedes:
references: abstract-writing, end-to-end-paper-workflow
provenance: R7-evolved
---

# Skill — Introduction Discipline

The Introduction sells the problem and positions the contribution. It operates at the class level — what type of method, what type of result — never at the implementation level. The reader finishes the Introduction knowing WHY this work matters and WHAT it contributes, then turns to the Method section for HOW.

## When to invoke

- Drafting or polishing the Introduction section.
- Checking whether the Introduction leaks Method-level implementation details.

## Overall structure (4–6 paragraph hourglass)

1. Broad context (1 paragraph)
2. Gap / problem (1 paragraph)
3. Our approach (1–2 paragraphs)
4. Contribution bullets
5. (Optional) Roadmap

Three paragraphs is too short to develop the argument adequately.

## Content boundary

The Introduction describes the method at the class level only. Parameter counts, optimizers, index structures, specific layer counts, and training configurations belong in the Method section.

Replacement examples:
- `350M-parameter diffusion U-Net` → `a learned diffusion prior`
- `FAISS HNSW over ESM-2 embeddings` → `retrieval over structural embeddings`

Boundary case: quantitative facts about prior work (e.g., "AlphaFold-2 requires ~20,000 GPU-hours") constitute background information and may be retained.

After reading the Introduction, the reader should know WHAT TYPE of method is used, without needing to know HOW it is implemented.

## Argumentation

The Introduction must specifically explain why prior work is insufficient. Generic statements such as "no one has done this" or "prior work has limitations" are unacceptable — name the specific failure mode or gap that motivates this work.

## Closing format

The Introduction ends with 2–4 noun-phrase contribution bullets (`\begin{itemize}`). This is the only location in the paper where itemize is permitted. Contribution bullets are noun-phrases, not full sentences.

## Pitfalls

- Pulling Method content into the Introduction (parameter counts, optimizers, batch size).
- Writing contribution bullets as full sentences rather than noun-phrases.
- Only 3 paragraphs (too short, insufficient substance).
- Why-not analysis too vague ("neither approach alone achieves satisfactory performance").
