## Abstract

Computational protein structure prediction has been transformed by large generative models, yet their computational cost remains a barrier to widespread adoption. Here we show that retrieval-augmented decoding can substantially reduce the inference burden while maintaining competitive accuracy. We developed RetroDiff, a method that combines a learned diffusion prior over protein backbones with retrieval-augmented decoding from a curated PDB subset. On CASP15 free-modelling targets, RetroDiff achieves performance comparable to AlphaFold-2 while requiring substantially less GPU time at inference. The key insight is that retrieval-based fragment priors can guide the diffusion process toward physically plausible backbones, effectively reducing the search space that the generative model must explore. This approach demonstrates that retrieval can substitute for very large generative models in structural-biology problems, lowering the computational barrier to entry for protein design applications. RetroDiff is currently restricted to single-chain backbones; multi-chain complexes and side-chain-aware design remain out of scope.

---

## Introduction

Protein structure prediction has long been a central challenge in computational biology. Traditional physics-based approaches rely on energy minimization and molecular dynamics, but these methods scale poorly with protein size and complexity. Recent advances in deep learning have dramatically improved prediction accuracy, particularly through large-scale generative models trained on sequence and structure databases. However, these models demand substantial computational resources, limiting their accessibility for many research groups and applications.

The success of large generative models in protein structure prediction raises a fundamental question: can we achieve comparable performance with lower computational cost? One promising direction is to leverage the wealth of structural information already available in curated databases. Fragment-based methods have a long history in structure prediction, providing local structural constraints that guide global folding. Yet these approaches have largely been superseded by end-to-end learning, which treats the entire prediction problem as a single optimization task.

Recent work has explored hybrid approaches that combine retrieval with generative models in other domains, showing that retrieved examples can provide valuable inductive biases. In protein structure prediction, this suggests an alternative strategy: use retrieval to supply fragment-level priors that constrain the generative process, rather than relying entirely on learned representations. Such an approach could reduce the effective complexity of the prediction problem, allowing smaller models to achieve competitive results.

The computational efficiency of protein design methods has practical implications. Reducing inference time expands access to structure prediction for researchers with limited computational budgets and enables new applications in high-throughput design. At the same time, maintaining accuracy is essential for practical utility. A method that trades accuracy for speed may be of limited value if the predictions are unreliable.

Here we show that retrieval-augmented decoding can achieve this balance. We developed RetroDiff, which combines a learned diffusion prior over protein backbones with retrieval-augmented decoding from a curated PDB subset. On CASP15 free-modelling targets, RetroDiff achieves performance comparable to AlphaFold-2 while requiring substantially less GPU time at inference.

---

## Conclusion

RetroDiff demonstrates that retrieval-augmented decoding offers a practical path toward more efficient protein structure prediction. By combining learned diffusion priors with fragment-level guidance from curated structural databases, the method achieves competitive accuracy while substantially reducing computational demands. This result suggests that retrieval can serve as an effective substitute for very large generative models in structural-biology problems, democratizing access to high-quality structure prediction. The approach opens new directions for computationally efficient design and suggests that hybrid retrieval-generative methods may be broadly applicable across domains where large reference databases exist. Future work should explore extensions to multi-chain complexes and side-chain-aware design, as well as applications to structure-based drug discovery and protein engineering.
