You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

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


## Expected-behaviour signature

3 paragraphs by method class. Each paragraph names the model + algorithm + at least one architectural/implementation property (Evoformer + SE(3)-Transformer for AlphaFold/RoseTTAFold; SE(3)-equivariant noise + 200k chains for RFdiffusion; KNN over 50M sequences for RITA-XL retrieval). Methods-class organisation, not chronological.

## Wrong patterns to watch for

Bibliography dump (just citations, no method description); chronological order; failure to name model + algorithm + implementation property per class.

## RED response (verbatim)

Structure prediction has been revolutionized by folding-based approaches, most notably AlphaFold-2 and RoseTTAFold. AlphaFold-2 employs a 48-layer Evoformer architecture that processes multiple sequence alignments and structural templates as input, with a dedicated structure module using invariant point attention to generate 3D coordinates. The model was trained on PDB structures clustered at 30% sequence identity, enabling strong generalization to novel sequences. RoseTTAFold takes a complementary approach with a three-track architecture that jointly processes 1D sequence information, 2D pairwise residue relationships, and 3D coordinate predictions, incorporating SE(3)-Transformer-style equivariance to respect rotational and translational symmetries. While these methods excel at predicting native structures from sequence alone, they are less suited to generative tasks where the goal is to design novel sequences or backbones with specified functional properties.

Diffusion-based generative models have emerged as a powerful alternative for protein design, offering explicit control over the generation process through conditioning. RFdiffusion pioneered this approach by applying SE(3)-equivariant noise schedules to protein backbones, conditioning generation on target hotspot residues to guide functional design. The model was trained on approximately 200,000 PDB chains and has demonstrated strong performance in de novo binder design. FrameDiff extends this framework with a frame-based parameterization of protein geometry, reporting improved designability metrics compared to RFdiffusion on de novo binder benchmarks. Both methods leverage equivariance to the 3D rotation and translation group, ensuring that generated structures respect physical constraints and symmetries inherent to protein geometry.

Retrieval-augmented decoding has proven effective for improving protein language model predictions by incorporating information from large sequence databases. RITA-XL combines a 7-billion-parameter protein language model with an external k-nearest-neighbor database of 50 million sequences, integrating retrieved sequence logits directly into the decoder's softmax computation. ESM-Retrieve similarly augments the ESM-2 backbone with retrieval over UniRef50 clusters, achieving 3–5 Spearman point improvements in zero-shot variant fitness prediction. These methods demonstrate that explicit access to similar sequences at inference time can substantially enhance model predictions, particularly in low-data regimes where the training distribution may not cover the target sequence space.

## BLUE response (verbatim)

Structure prediction has been revolutionized by deep learning approaches that leverage evolutionary information and geometric constraints. AlphaFold-2 (Jumper et al., 2021) pioneered this direction with a 48-layer Evoformer architecture that processes multiple sequence alignments (MSA) and structural templates as input, using invariant point attention in its structure module to maintain SE(3) equivariance. RoseTTAFold (Baek et al., 2021) extended this paradigm with a three-track architecture that jointly models 1D sequence information, 2D pairwise residue interactions, and 3D coordinates, employing SE(3)-Transformer-style equivariance to ensure geometric consistency. Both methods were trained on PDB structures clustered at 30% sequence identity, establishing a foundation for structure-aware learning that RetroDiff builds upon. However, these folding-based approaches are fundamentally constrained to predicting structures from sequence alone, limiting their applicability to generative tasks where novel sequences must be designed de novo.

Diffusion-based generative models have emerged as a powerful alternative for protein backbone generation, offering greater flexibility than folding-based methods. RFdiffusion (Watson et al., 2023) introduced backbone-only diffusion using SE(3)-equivariant noise schedules, conditioning generation on target hotspot residues to enable functional design. FrameDiff (Yim et al., 2023) adopted a similar diffusion framework but parameterizes protein backbones using frame-based representations, reporting improved designability compared to RFdiffusion on de novo binder design tasks. Both methods were trained on large-scale PDB datasets (RFdiffusion on ~200k chains), demonstrating that diffusion priors can capture the manifold of natural protein structures. Anand & Achim (2022) further explored denoising-diffusion approaches for folding, showing that diffusion-based priors can be combined with structure prediction objectives. These works establish diffusion as a principled generative framework for proteins, though they do not leverage external sequence databases to guide generation.

Retrieval-augmented decoding has proven effective for improving protein language model predictions by incorporating similarity to known sequences. RITA-XL with retrieval (Notin et al., 2024) augments a 7-billion-parameter protein language model with an external k-nearest-neighbor database of 50 million sequences, mixing retrieved sequence logits into the decoder's softmax to bias predictions toward natural variants. ESM-Retrieve (Lin et al., 2023) applies retrieval over UniRef50 clusters to the ESM-2 backbone, improving zero-shot variant fitness prediction by 3–5 Spearman correlation points. These methods demonstrate that retrieval can effectively ground language model predictions in empirical data, reducing hallucination and improving generalization. However, existing retrieval-augmented approaches operate at the sequence level and have not been systematically combined with diffusion-based structure generation, which is the core contribution of RetroDiff.

## Your output (STRICT JSON, no other text, write to ./verdict.json in cwd)

Save your verdict to `verdict.json` in the current working directory:

```json
{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Overreaches",
  "confidence": "high" | "medium" | "low"
}
```
