# Fixture: P9 — Conference Introduction (mode-switch sanity check)

## Role
You are a Writer agent in MinionsOS, drafting the Introduction of a manuscript
for **NeurIPS 2026** (conference camera-ready).  Same domain and content as
the P2 fixture (RetroDiff: diffusion-prior + retrieval-augmented decoding for
protein structure generation), but the venue is now a top-tier ML conference
rather than *Nature*.

## Brief

Use the same scratch / brief as P2 (RetroDiff).  Reproduced here for
self-containment:

```
Topic / one-line:
RetroDiff combines a learned diffusion prior over protein backbones with
retrieval-augmented decoding from a curated PDB subset, achieving CASP15-level
performance with 30x less GPU time than AlphaFold-2 retraining.

Why now:
- AlphaFold-2 / RoseTTAFold transformed protein structure prediction.
- Retraining for new design tasks (novel folds, de-novo binders) is
  expensive (>20,000 GPU-hours per run).
- Two emerging directions: diffusion-based generative priors (RFdiffusion,
  FrameDiff); retrieval-augmented decoding (RITA-XL with retrieval).
- Neither alone matches AlphaFold-2 at design tasks.

Approach:
- We propose RetroDiff: diffusion prior + retrieval-augmented decoding.
- 350 M-parameter diffusion U-Net trained on 450 k PDB chains.
- 50 k-chain retrieval subset of PDB indexed by FAISS HNSW over ESM-2
  embeddings.
- Inference: 50 reverse-diffusion steps with per-step retrieval conditioning.

Headline result:
- CASP15 free-modelling targets: TM-score 0.71 vs AlphaFold-2's 0.73.
- 30x less inference GPU time.

Hyperparameters / training:
- Diffusion U-Net: 30 layers, hidden 512, AdamW lr=1e-4, batch 256.
- Retrieval: ESM-2, FAISS HNSW, top-k=8, cosine threshold 0.5.
- Training: 8x H100 for 14 days.
```

## Task

Draft the NeurIPS 2026 Introduction.  Return ONLY the LaTeX source — including
the contribution-bullet list at the end — no commentary.  The author will
paste it directly into `1_introduction.tex`.

## Constraints

- Length: 4-5 paragraphs of prose + a contribution itemize block at the end.
- NeurIPS convention: contribution bullets are expected by reviewers.
- Implementation details (layer counts, optimisers, batch sizes, training
  hours) belong in Method or Appendix, NOT in the Introduction.
- Method classes should be named at the level of "diffusion-based generative
  priors" / "retrieval-augmented decoding", not raw layer counts.

(End of brief.)
