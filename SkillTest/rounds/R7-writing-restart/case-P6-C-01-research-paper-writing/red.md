\subsection{Pipeline}

The pipeline of \texttt{OurNet} comprises four sequential steps: preprocessing, patch extraction, model inference, and aggregation.

\paragraph{Step 1: Preprocessing}
Raw images undergo contrast-limited histogram equalization to enhance local contrast and improve feature visibility.

\paragraph{Step 2: Patch Extraction}
Images are divided into non-overlapping patches of size $256 \times 256$ pixels.

\paragraph{Step 3: Model Inference}
Each patch is processed by \texttt{OurNet}, which outputs a per-patch prediction score.

\paragraph{Step 4: Aggregation}
Per-patch scores are aggregated via logistic regression to produce a whole-image prediction.

The full architecture of \texttt{OurNet} is shown in Figure~2.
