## Abstract

Protein structure prediction has been transformed by learning-based approaches, yet computational cost remains a barrier to widespread adoption in design workflows. Here we show that retrieval-augmented diffusion can achieve competitive accuracy with substantially reduced inference time. We developed RetroDiff, which combines a learned diffusion prior over protein backbones with retrieval-augmented decoding from a curated structural database. On free-modelling targets, RetroDiff achieves TM-score 0.71 compared to AlphaFold-2's 0.73, while requiring 30-fold less GPU time at inference. The key insight is that retrieval supplies fragment-level structural priors that guide the diffusion process toward physically plausible backbones, effectively reducing the search space the generative model must explore. This approach demonstrates that retrieval can substitute for very large generative models in structural-biology problems, lowering the computational barrier to entry for protein design applications. Current work focuses on single-chain backbones; extension to multi-chain complexes and side-chain-aware design remains future work.

---

## Introduction

Protein structure prediction is a foundational problem in computational biology, with applications ranging from drug discovery to enzyme engineering. Traditional physics-based methods are limited by the complexity of the energy landscape, while recent learning-based approaches have achieved remarkable accuracy by leveraging large databases of known structures. However, these methods often require substantial computational resources, particularly at inference time, which limits their accessibility for iterative design workflows where many candidate structures must be evaluated.

Diffusion models have emerged as a powerful generative framework for structure prediction, offering fine-grained control over the generation process and the ability to condition on diverse structural constraints. Yet scaling these models to match the accuracy of very large transformer-based predictors typically requires proportionally larger models and longer inference times. This computational cost creates a practical bottleneck for applications that demand rapid exploration of sequence or design space.

Retrieval-augmented generation offers a complementary approach: rather than relying solely on a learned generative model, one can augment the generation process with direct access to relevant examples from a curated database. In the protein structure domain, this strategy is particularly promising because structural space is highly constrained by physics and evolution, and similar sequences often adopt similar folds. Fragment-level retrieval can supply local structural priors that dramatically reduce the effective search space the generative model must cover.

We hypothesized that combining retrieval with diffusion-based generation could yield a more efficient path to competitive accuracy. The retrieval module would supply fragment-level priors that guide the diffusion process toward physically plausible backbones, while the diffusion model would refine these priors and handle novel sequence contexts. Here we show that this hybrid approach achieves strong performance on challenging free-modelling targets while substantially reducing computational cost compared to large-scale generative models.

---

## Conclusion

Retrieval-augmented diffusion offers a practical pathway to efficient protein structure prediction by leveraging the complementary strengths of database lookup and learned generation. Our results demonstrate that hybrid approaches can achieve competitive accuracy with substantially lower computational overhead, making structure prediction more accessible for iterative design workflows. This work opens new directions for combining retrieval and generation in other domains where structured, constrained spaces allow efficient database-guided learning. Future work will extend this framework to multi-chain complexes and incorporate side-chain information, broadening its applicability to real-world protein engineering challenges.
