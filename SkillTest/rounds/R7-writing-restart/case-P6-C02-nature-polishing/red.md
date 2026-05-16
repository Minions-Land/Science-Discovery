\subsection{Pipeline}

\texttt{OurNet} comprises four sequential steps: preprocessing, patch extraction, model inference, and aggregation.

\paragraph{Step 1: Preprocessing.}
Raw images undergo contrast-limited histogram equalization.

\paragraph{Step 2: Patch extraction.}
Preprocessed images are divided into non-overlapping $256 \times 256$ pixel patches.

\paragraph{Step 3: Model inference.}
Each patch is processed by \texttt{OurNet} to generate a per-patch score.

\paragraph{Step 4: Aggregation.}
Per-patch scores are aggregated via logistic regression to produce a whole-image prediction.

The complete architecture of \texttt{OurNet} is illustrated in Figure~2.
