\subsection{Pipeline}

The pipeline of \texttt{OurNet} has four steps.

\paragraph{Step 1.}
We preprocess the raw images.

\paragraph{Step 2.}
We extract patches.

\paragraph{Step 3.}
We feed the patches to \texttt{OurNet}.

\paragraph{Step 4.}
We aggregate the patch-level predictions to obtain a whole-image prediction.

\begin{itemize}
  \item Preprocessing uses contrast-limited histogram equalization.
  \item Patches are $256 \times 256$.
  \item \texttt{OurNet} outputs a per-patch score.
  \item Aggregation uses logistic regression.
\end{itemize}

The full architecture of \texttt{OurNet} is shown in Figure~\ref{fig:architecture}.
