# Fixture: P2 — Introduction vs Implementation-detail discipline (CNS)

## Role
You are a Writer agent in MinionsOS, drafting the Introduction section of a
manuscript for *Nature*.  The user is the corresponding author.  This is a
methods paper introducing a new diffusion-prior + retrieval-augmented decoding
recipe called "RetroDiff" for protein-structure generation.

## Brief

The author has handed you a structured brief (high-level + low-level mixed).
Treat the brief as raw material; not all of it belongs in the Introduction.

```
Topic / one-line:
RetroDiff combines a learned diffusion prior over protein backbones with
retrieval-augmented decoding from a curated PDB subset, achieving CASP15-level
performance with 30x less GPU time than AlphaFold-2 retraining.

Why now (background):
- Protein structure prediction has been transformed by AlphaFold-2 and its
  successors (Jumper et al., 2021; Baek et al., 2021).
- However, retraining or fine-tuning AlphaFold for new design tasks (novel
  folds, de-novo binders) remains expensive (>20,000 GPU-hours per run).
- Two emerging directions: (1) diffusion-based generative priors over
  structures (Watson et al., 2023; Yim et al., 2023); (2) retrieval-augmented
  decoding for protein language models (Notin et al., 2024).
- Neither family alone matches AlphaFold-2 accuracy at design tasks.

Approach (one sentence each):
- We propose RetroDiff, combining a diffusion prior with retrieval-augmented
  decoding.
- The diffusion prior is a 350 M-parameter denoising score model trained on
  450 k PDB chains.
- The retrieval module uses a 50 k-chain curated subset of PDB indexed by
  FoamSearch and queried via cosine similarity over ESM-2 embeddings.
- Inference combines 50 reverse-diffusion steps with per-step retrieval
  conditioning.

Headline result:
- On CASP15 free-modelling targets, RetroDiff achieves TM-score 0.71 vs
  AlphaFold-2's 0.73, while using 30x less GPU time at inference.

Contribution bullets (the author wrote these for the conference variant of
this paper; he wants them removed for the Nature version):
- We propose RetroDiff, a diffusion-prior + retrieval-augmented decoding
  recipe.
- We curate a 50 k-chain retrieval subset of PDB.
- We achieve CASP15 performance at 30x less GPU time.

Hyperparameters / architecture detail (for Methods section, NOT for Intro):
- Diffusion: U-Net backbone, 30 layers, hidden dim 512, AdamW lr=1e-4,
  batch 256, 200 epochs.
- Retrieval: ESM-2 embeddings, FAISS HNSW index, top-k=8 per residue,
  cosine similarity threshold 0.5.
- Training: 8x H100 for 14 days.
```

## Task

Draft the Introduction section. Return ONLY the prose text — no headings,
no bullet lists, no commentary. The author will paste it directly into the
manuscript.

## Constraints

- Target length: 4-6 paragraphs.
- *Nature* convention: no contribution bullets, no implementation detail
  (no layer counts, optimisers, batch sizes, training hours).  Mention
  method classes only.
- The hourglass / "Here we" anchor pattern is preferred for the final
  paragraph.

(End of brief.)
