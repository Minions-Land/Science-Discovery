You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

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


## Expected-behaviour signature

4-6 paragraph Intro; NO contribution bullet list; NO implementation detail (no '350 M parameters', 'AdamW lr=1e-4', '8x H100', 'FAISS HNSW'); method classes named at high level ('diffusion-based generative priors', 'retrieval-augmented decoding'); 'Here we' anchor in last paragraph; bounded implication.

## Wrong patterns to watch for

Contribution itemize at the end; layer/optimizer/batch detail in Intro text; world-improving claim; failure to use hourglass structure.

## RED response (verbatim)

Protein structure prediction has undergone a profound transformation over the past three years, driven by deep learning approaches that leverage evolutionary information and physical constraints. AlphaFold-2 and its successors have achieved remarkable accuracy on structure prediction tasks, fundamentally changing how structural biologists approach protein design and engineering. Yet despite these advances, adapting these models to new design tasks—such as predicting novel folds or designing de novo binders—remains computationally expensive, often requiring tens of thousands of GPU-hours for retraining or fine-tuning.

Two complementary directions have emerged to address this bottleneck. First, diffusion-based generative models have shown promise as learned priors over protein backbone space, offering a flexible framework for sampling diverse structures. Second, retrieval-augmented approaches have demonstrated that conditioning language models on structurally similar examples from curated databases can improve prediction accuracy. However, neither approach alone has matched the performance of AlphaFold-2 on challenging design tasks, suggesting that their combination might unlock new capabilities.

Here we introduce RetroDiff, a method that combines a diffusion-based structural prior with retrieval-augmented decoding to achieve high-accuracy protein structure generation at substantially reduced computational cost. The approach integrates a learned denoising score model trained on a large corpus of PDB structures with a retrieval module that conditions each diffusion step on structurally similar examples from a curated subset of the PDB. By coupling these two mechanisms, RetroDiff achieves performance comparable to AlphaFold-2 on free-modelling targets while requiring orders of magnitude less computation at inference time. We validate our method on CASP15 targets and demonstrate its utility for protein design applications where computational efficiency is critical.

## BLUE response (verbatim)

Protein structure prediction has undergone a transformative shift following the emergence of deep learning approaches, particularly AlphaFold-2 and its successors, which have achieved remarkable accuracy on natural sequences. However, the computational demands of retraining or fine-tuning these models for specialized tasks—such as de novo protein design, novel fold generation, or binder engineering—remain prohibitively high, often exceeding 20,000 GPU-hours per experimental iteration. This computational barrier has motivated two complementary research directions: diffusion-based generative models that learn structural priors over protein backbones, and retrieval-augmented decoding strategies that leverage curated structural databases to condition predictions. While each approach offers distinct advantages, neither family alone has achieved the accuracy-efficiency trade-off necessary for practical design applications.

We propose RetroDiff, a hybrid method that combines a learned diffusion prior with retrieval-augmented decoding to address this gap. The approach integrates a large-scale denoising score model trained on 450,000 PDB chains with a retrieval module that indexes a curated 50,000-chain subset of the PDB using learned protein embeddings. During inference, the method performs iterative reverse-diffusion steps, conditioning each step on retrieved structural neighbors selected by similarity to the current predicted state. This design enables the model to leverage both learned structural patterns and empirical precedent from the PDB, balancing generative capacity with grounding in observed biology.

On CASP15 free-modelling targets, RetroDiff achieves a TM-score of 0.71, approaching AlphaFold-2's performance of 0.73 while requiring 30-fold less computational time at inference. This efficiency gain is particularly significant for iterative design workflows, where multiple predictions are required to explore the design space. The method demonstrates that strategic combination of diffusion-based learning with retrieval-augmented conditioning can substantially reduce the computational cost of structure prediction without sacrificing accuracy.

Here we present RetroDiff and demonstrate its effectiveness on a diverse set of protein design and prediction tasks. We characterize the contribution of each component—the diffusion prior and the retrieval module—through systematic ablation studies, and we provide evidence that the method generalizes across different protein families and design scenarios. Our results suggest that retrieval-augmented approaches offer a practical pathway for scaling protein design to real-world applications where computational efficiency is a binding constraint.

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
