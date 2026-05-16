# Fixture: P10 — End-to-end Abstract + Intro + Conclusion (CNS coordination)

## Role
You are a Writer agent in MinionsOS, drafting the front-matter and back-matter
of a manuscript for *Nature Methods*.  Same domain as P2 (RetroDiff:
diffusion-prior + retrieval-augmented decoding for protein structure
generation).

## Brief

Methods and Results sections of the paper are already drafted.  You have only
the following compressed summary:

```
Method (1 sentence):
RetroDiff combines a learned diffusion prior over protein backbones with
retrieval-augmented decoding from a curated PDB subset.

Headline result (1 sentence):
On CASP15 free-modelling targets, RetroDiff achieves TM-score 0.71 vs
AlphaFold-2's 0.73, while using 30x less GPU time at inference.

Mechanism (1 sentence):
The retrieval module supplies fragment-level priors that guide the diffusion
process toward physically plausible backbones, reducing the search-space
size that the generative model has to cover.

Limitation (1 sentence):
RetroDiff is currently restricted to single-chain backbones; multi-chain
complexes and side-chain-aware design are out of scope.

Implication (1 sentence):
RetroDiff demonstrates that retrieval can substitute for very large
generative models in structural-biology problems, reducing the GPU-time
barrier to entry for protein design.
```

## Task

Draft THREE sections in one shot:

1. **Abstract** (≤ 200 words, single paragraph, *Nature Methods* style).
2. **Introduction** (4-5 paragraphs, *Nature Methods* style — same constraints
   as P2: no contribution bullets, no implementation detail).
3. **Conclusion** (≤ 150 words, single paragraph, *Nature Methods* style — no
   citations, no specific numbers, no dataset names).

Return all three sections, separated by `\n---\n` lines.  No commentary,
no headings beyond the section labels `## Abstract`, `## Introduction`,
`## Conclusion`.

## Constraints

- The same main-result claim must be made in Abstract, Introduction's last
  paragraph, and Conclusion.  No contradictions in scope or hedging.
- The "Here we show" / "we developed" anchor should appear in both Abstract
  and the closing paragraph of Introduction.
- Conclusion must NOT reuse Abstract's exact wording verbatim.
- No `\cite{}` calls in Abstract or Conclusion.

(End of brief.)
