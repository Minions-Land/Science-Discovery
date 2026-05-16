\subsection{Pipeline}

The pipeline of \texttt{OurNet} comprises four sequential steps.

\paragraph{Step 1.}
Raw images are preprocessed using contrast-limited histogram equalization.

\paragraph{Step 2.}
Preprocessed images are partitioned into non-overlapping patches of $256 \times 256$ pixels.

\paragraph{Step 3.}
Patches are fed to \texttt{OurNet}, which outputs a per-patch classification score.

\paragraph{Step 4.}
Per-patch scores are aggregated via logistic regression to obtain a whole-image prediction.

The full architecture of \texttt{OurNet} is shown in Figure~2.