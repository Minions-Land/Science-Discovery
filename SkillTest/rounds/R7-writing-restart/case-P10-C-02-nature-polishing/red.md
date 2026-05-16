## Abstract

Protein structure prediction has been transformed by large generative models, yet their computational cost limits accessibility for many researchers. Here we show that retrieval-augmented diffusion can match the accuracy of these models while reducing inference time substantially. We developed RetroDiff, which combines a learned diffusion prior over protein backbones with retrieval-augmented decoding from a curated PDB subset. On CASP15 free-modelling targets, RetroDiff achieves a TM-score of 0.71 compared to AlphaFold-2's 0.73, while requiring 30-fold less GPU time. The retrieval module supplies fragment-level priors that guide the diffusion process toward physically plausible backbones, reducing the search space the generative model must cover. RetroDiff is currently restricted to single-chain backbones; multi-chain complexes and side-chain-aware design remain out of scope. Our results demonstrate that retrieval can substitute for very large generative models in structural-biology problems, lowering the computational barrier to protein design.

---

## Introduction

Protein structure prediction has long been a central challenge in computational biology. Traditional physics-based approaches rely on energy minimization and conformational sampling, but these methods scale poorly with protein size and complexity. Recent advances in deep learning, particularly AlphaFold-2, have achieved remarkable accuracy by learning patterns from evolutionary and structural databases. However, these large models demand substantial computational resources, creating a barrier for researchers with limited access to high-performance computing infrastructure.

Generative models offer an alternative path to structure prediction by learning the distribution of natural protein backbones. Diffusion-based approaches have shown particular promise, as they can generate diverse, physically plausible structures through iterative refinement. Yet scaling these models to match AlphaFold-2's accuracy typically requires training on massive datasets and deploying models with billions of parameters, further increasing computational demands.

Retrieval-augmented methods provide a complementary strategy. Rather than relying solely on learned priors, these approaches leverage existing structural knowledge by retrieving similar fragments from curated databases. Fragment-based methods have a long history in protein structure prediction, but they have been largely overshadowed by end-to-end learning. Recent work suggests that combining retrieval with generative models may offer a more efficient path to accurate predictions.

We hypothesized that retrieval-augmented diffusion could achieve competitive accuracy while dramatically reducing inference time. The key insight is that retrieval supplies fragment-level priors that constrain the search space, allowing a smaller generative model to focus on refinement rather than exploration. Here we show that this approach succeeds: RetroDiff combines a learned diffusion prior over protein backbones with retrieval-augmented decoding from a curated PDB subset, achieving performance comparable to AlphaFold-2 at a fraction of the computational cost.

---

## Conclusion

RetroDiff demonstrates that retrieval-augmented diffusion can achieve near-state-of-the-art accuracy in protein structure prediction while substantially reducing computational requirements. By coupling a learned generative model with fragment-level priors from a curated database, we show that retrieval can effectively substitute for the scale of large end-to-end models. This approach lowers the computational barrier to entry for protein design and structure prediction, making these capabilities more accessible to the broader research community. Future work should extend the method to multi-chain complexes and incorporate side-chain information, broadening its applicability to more complex biological systems.
