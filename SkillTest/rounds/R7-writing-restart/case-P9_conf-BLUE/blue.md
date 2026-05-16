\section{Introduction}

Protein structure prediction has undergone a paradigm shift with the emergence of deep learning methods, most notably AlphaFold-2 and RoseTTAFold, which achieve near-experimental accuracy on diverse protein targets. However, the computational cost of retraining these models for new design tasks—such as engineering novel folds or designing de-novo binders—remains prohibitive, often requiring tens of thousands of GPU-hours per experiment. This barrier limits the accessibility and iteration speed of structure-guided protein engineering, a critical bottleneck for therapeutic and industrial applications.

Recent advances suggest two complementary directions for reducing this cost. First, diffusion-based generative priors (RFdiffusion, FrameDiff) have emerged as efficient alternatives for sampling protein backbones, offering faster inference and lower training requirements than discriminative models. Second, retrieval-augmented decoding methods (RITA-XL with retrieval) leverage curated structural databases to condition predictions, improving accuracy without retraining. Yet neither approach alone achieves the performance of AlphaFold-2 on challenging design tasks, suggesting that their combination may unlock a new frontier in efficient protein structure generation.

We propose \textbf{RetroDiff}, a method that combines diffusion-based generative priors with retrieval-augmented decoding to achieve competitive structure prediction performance with substantially reduced computational cost. Our approach trains a diffusion U-Net on a large corpus of PDB structures to learn a flexible prior over protein backbones, then conditions the reverse-diffusion process with retrieved examples from a curated PDB subset indexed by learned embeddings. This two-stage design decouples the learning of structural priors from the incorporation of database knowledge, enabling efficient inference through a small number of diffusion steps guided by retrieval.

On CASP15 free-modelling targets, RetroDiff achieves a TM-score of 0.71, approaching AlphaFold-2's 0.73 while requiring 30$\times$ less GPU time for inference. This efficiency gain opens new possibilities for rapid iteration in protein design workflows and democratizes access to structure-guided engineering. We demonstrate the method's robustness across diverse target types and analyze the complementary roles of diffusion priors and retrieval conditioning in the final predictions.

\subsection*{Contributions}

\begin{itemize}
  \item A diffusion-based generative prior trained on large-scale PDB data, providing an efficient backbone sampling mechanism that can be adapted to new design tasks.
  \item A retrieval-augmented decoding framework that conditions diffusion steps with structurally similar examples, improving prediction accuracy without model retraining.
  \item Empirical validation on CASP15 targets, demonstrating competitive performance with AlphaFold-2 at 30$\times$ lower inference cost.
  \item Analysis of the interplay between generative priors and retrieval conditioning, providing insights for future hybrid structure prediction methods.
\end{itemize}
