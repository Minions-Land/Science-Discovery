## Abstract

Protein structure prediction and design remain computationally expensive, with large generative models requiring substantial GPU resources. Here we show that retrieval-augmented generation can achieve competitive accuracy while dramatically reducing computational cost. We present RetroDiff, a method that combines a learned diffusion prior over protein backbones with retrieval-augmented decoding from a curated structural database. The retrieval module supplies fragment-level priors that guide the diffusion process toward physically plausible backbones, enabling the generative model to focus on high-confidence regions of the search space. On CASP15 free-modelling targets, RetroDiff achieves a TM-score of 0.71, comparable to AlphaFold-2's 0.73, while requiring 30-fold less GPU time at inference. These results demonstrate that retrieval can effectively substitute for very large generative models in structural biology, reducing the computational barrier to entry for protein design applications.

---

## Introduction

Protein structure prediction has undergone a revolution with the emergence of deep learning approaches, particularly those leveraging multiple sequence alignments and covariance information. AlphaFold-2 and related methods have achieved remarkable accuracy on diverse protein targets, yet their computational demands—requiring hours of GPU time per prediction—create a practical bottleneck for large-scale design applications. This computational cost stems from the need to search a vast conformational space with minimal structural priors, forcing the model to learn both the general principles of protein folding and the specific constraints of individual sequences simultaneously.

Retrieval-based approaches offer a complementary strategy: by conditioning on structurally similar fragments from known proteins, a generative model can focus on the regions where sequence-specific information is most critical. Fragment-based methods have a long history in structure prediction, yet they have been largely superseded by end-to-end learning. However, the rise of efficient diffusion models suggests that retrieval and generation need not be mutually exclusive—a retrieval module could provide strong inductive biases that allow a smaller generative model to achieve comparable accuracy with far less computation.

We developed RetroDiff to test this hypothesis. The method combines a diffusion prior trained on protein backbone coordinates with a retrieval module that identifies structurally similar fragments from a curated subset of the Protein Data Bank. During inference, the retrieval module supplies fragment-level constraints that guide the diffusion sampling process, effectively reducing the effective dimensionality of the search space. This hybrid approach preserves the flexibility of generative modeling while leveraging the specificity of retrieval.

We evaluated RetroDiff on CASP15 free-modelling targets, a challenging benchmark of recently released protein sequences with no close homologs in the training data. On this benchmark, RetroDiff achieves a TM-score of 0.71, within 2.7% of AlphaFold-2's 0.73, while requiring 30-fold less GPU time at inference. These results suggest that retrieval-augmented generation can substantially reduce the computational requirements for structure prediction without sacrificing accuracy.

The remainder of this paper describes the RetroDiff method, presents experimental validation on CASP15 targets, and discusses the implications for protein design and structural biology more broadly.

---

## Conclusion

This work demonstrates that retrieval-augmented diffusion models can achieve near state-of-the-art accuracy in protein structure prediction with dramatically reduced computational cost. By combining learned generative priors with fragment-level constraints from a structural database, RetroDiff shows that large monolithic models are not strictly necessary for competitive performance. The method is currently limited to single-chain backbones; extending it to multi-chain complexes and incorporating side-chain information remain important directions for future work. More broadly, these findings suggest that retrieval can serve as a powerful alternative to scaling up generative models, potentially democratizing access to accurate structure prediction and design tools.
