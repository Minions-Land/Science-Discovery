\section{Introduction}

Protein structure prediction has undergone a paradigm shift following the emergence of AlphaFold-2 and RoseTTAFold, which demonstrated that deep learning can achieve near-experimental accuracy on diverse protein targets. However, the computational cost of retraining these models for new design tasks—such as engineering novel folds or de-novo binders—remains prohibitive, often exceeding 20,000 GPU-hours per run. This computational barrier has motivated two complementary research directions: (1) diffusion-based generative priors that learn the distribution of protein backbones, exemplified by RFdiffusion and FrameDiff, and (2) retrieval-augmented decoding that leverages curated structural databases to condition generation. While each approach offers distinct advantages, neither alone achieves the performance of AlphaFold-2 on challenging design tasks.

We propose \textbf{RetroDiff}, a method that combines diffusion-based generative priors with retrieval-augmented decoding to achieve competitive performance on protein structure prediction with substantially reduced computational requirements. Our approach trains a diffusion U-Net on 450k PDB chains to learn a prior over protein backbone geometries, then conditions the reverse-diffusion process with per-step retrieval from a curated 50k-chain PDB subset indexed by learned protein embeddings. This combination leverages the expressiveness of diffusion models while grounding generation in empirically observed structural patterns.

On CASP15 free-modelling targets, RetroDiff achieves a TM-score of 0.71, approaching AlphaFold-2's 0.73 while requiring 30x less GPU time for inference. This efficiency gain is particularly valuable for applications requiring rapid iteration over design variants or deployment in resource-constrained settings. Beyond computational efficiency, the interpretability of retrieval-augmented generation provides insights into which structural templates most influence the model's predictions.

Our contributions are as follows:

\begin{itemize}
    \item We demonstrate that combining diffusion-based generative priors with retrieval-augmented decoding yields competitive protein structure prediction performance.
    \item We show that this hybrid approach achieves 30x inference speedup compared to AlphaFold-2 retraining while maintaining near-parity on challenging free-modelling targets.
    \item We provide evidence that retrieval-augmented generation improves both performance and interpretability by grounding predictions in empirical structural knowledge.
    \item We establish a practical framework for efficient protein design that balances accuracy, computational cost, and interpretability.
\end{itemize}
