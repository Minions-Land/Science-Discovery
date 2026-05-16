# Fixture: P3 — Related Work depth (CNS, methods paper)

## Role
You are a Writer agent in MinionsOS, drafting the Related Work section of a
manuscript intended for *Nature Methods*.  The methods paper is the same one
introduced in P2 — RetroDiff, a diffusion-prior + retrieval-augmented decoding
recipe for protein structure generation.

## Brief

The Introduction of this paper has already mentioned three method classes
that RetroDiff builds on or compares against:

1. **AlphaFold-2 family** (folding-based prediction): Jumper et al., 2021;
   Baek et al., 2021 (RoseTTAFold).
2. **Diffusion-based generative priors** for protein backbones: Watson et al.,
   2023 (RFdiffusion); Yim et al., 2023 (FrameDiff); Anand & Achim, 2022
   (denoising-diffusion folding).
3. **Retrieval-augmented decoding** for protein language models: Notin et al.,
   2024 (RITA-XL with retrieval); Lin et al., 2023 (ESM-Retrieve).

The Introduction did NOT discuss the specific architectures, training data,
or implementation details of any of these works — the Introduction stayed at
the method-class level.  That Detail is the Related Work section's job.

You also have author scratch notes from a prior literature scan:

```
- AlphaFold-2: 48-layer Evoformer, MSA + template input, structure module
  with invariant point attention.  Trained on PDB clustered at 30% sequence ID.
  RoseTTAFold uses a three-track architecture (1D sequence + 2D pairwise +
  3D coordinates) with SE(3)-Transformer-style equivariance.
- RFdiffusion: backbone-only diffusion using SE(3)-equivariant noise,
  conditional on a target hot-spot residue.  Trained on PDB with 200 k chains.
- FrameDiff: same family but with a frame-based parameterisation; reports
  better designability than RFdiffusion on de novo binders.
- RITA-XL with retrieval: 7B-parameter protein language model with an
  external KNN database of 50 M sequences; kNN logits are mixed into the
  decoder's softmax.
- ESM-Retrieve: ESM-2 backbone with retrieval over UniRef50 clusters;
  improves zero-shot variant fitness by 3-5 Spearman points.
```

## Task

Draft the Related Work section. Return ONLY the prose text — no headings,
no commentary, no bullet lists. The author will paste it directly into the
manuscript as the "Related Work" section body.

## Constraints

- Target length: 3 paragraphs (one per method class).
- *Nature Methods* expects: each method-class paragraph names the model used,
  the algorithm or training data, and the architectural / implementation
  property that distinguishes it.  The Related Work section is where
  implementation detail is appropriate.
- ≤ 600 words total.
- Methods-class organisation, not chronological.

(End of brief.)
