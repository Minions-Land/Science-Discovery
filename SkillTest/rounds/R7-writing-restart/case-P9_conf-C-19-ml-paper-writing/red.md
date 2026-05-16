\section{Introduction}

Protein structure prediction has undergone a revolutionary transformation in the past decade. The advent of AlphaFold-2 and RoseTTAFold demonstrated that deep learning could achieve near-experimental accuracy on the CASP benchmarks, fundamentally changing how structural biologists approach protein design and discovery. Yet this success has created a new bottleneck: adapting these models to novel design tasks—such as generating proteins with new folds or engineering de-novo binders—requires expensive retraining campaigns that consume over 20,000 GPU-hours per run. For practitioners, this computational barrier has made structure-based protein engineering inaccessible except to well-resourced institutions.

Two complementary directions have emerged to address this limitation. First, diffusion-based generative models (RFdiffusion, FrameDiff) offer a lightweight alternative to full retraining, learning a prior over protein backbone space that can be conditioned on design constraints. Second, retrieval-augmented decoding—exemplified by systems like RITA-XL—leverages large curated databases to ground predictions in observed structural diversity. However, neither approach alone has matched AlphaFold-2's accuracy on challenging design tasks. Diffusion priors, while efficient, lack the fine-grained structural knowledge encoded in large protein databases. Retrieval-augmented methods, while grounded in real structures, struggle to generalize beyond their training neighborhoods.

We propose \textbf{RetroDiff}, a hybrid approach that combines diffusion-based generative priors with retrieval-augmented decoding. Our key insight is that these two paradigms are complementary: a learned diffusion prior provides a flexible, learnable backbone distribution, while retrieval conditioning at each reverse-diffusion step anchors predictions to the structural diversity of known proteins. We train a 350M-parameter diffusion U-Net on 450k PDB chains and couple it with a retrieval index over a curated 50k-chain PDB subset, indexed by FAISS HNSW over ESM-2 embeddings. During inference, we perform 50 reverse-diffusion steps with per-step retrieval conditioning, achieving CASP15 free-modelling performance (TM-score 0.71) while requiring 30× less GPU time than AlphaFold-2 retraining.

Our contributions are as follows:

\begin{itemize}
  \item A hybrid architecture combining diffusion-based generative priors with retrieval-augmented decoding, demonstrating that these paradigms are synergistic rather than competing.
  \item Empirical validation on CASP15 free-modelling targets, showing competitive accuracy (TM-score 0.71 vs. AlphaFold-2's 0.73) with 30× lower computational cost.
  \item A scalable inference pipeline that enables practical structure-based protein design without expensive retraining, democratizing access to AI-driven protein engineering.
  \item Ablation studies isolating the contributions of diffusion priors, retrieval conditioning, and their interaction, providing insights into when and why hybrid approaches outperform single-paradigm baselines.
\end{itemize}
