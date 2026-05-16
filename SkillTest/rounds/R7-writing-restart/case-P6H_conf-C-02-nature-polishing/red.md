\section{Introduction}

Large language models have improved rapidly, yet their reasoning ability remains brittle.

\paragraph{The reasoning gap.}
Despite scaling, models still fail on multi-step arithmetic and logical inference, as documented by recent benchmarks.

\paragraph{Prior approaches.}
Chain-of-thought prompting (Wei et al., 2022) and tool use (Schick et al., 2023) have partially closed this gap, but performance plateaus on problems requiring more than five reasoning steps.

In this paper, we introduce \texttt{OurNet}, a new training recipe that combines verifier feedback with synthetic data generation. \texttt{OurNet} is trained on a curated reasoning corpus and substantially outperforms prior work across three benchmarks.

\begin{itemize}
  \item We propose \texttt{OurNet}, a verifier-augmented training recipe for reasoning-intensive language models.
  \item We curate a 1.2 million-example synthetic reasoning corpus.
  \item We show that \texttt{OurNet} improves accuracy on GSM8K, MATH, and BIG-Bench Hard by 8--15 absolute percentage points over the strongest baseline.
  \item We release training code, data, and checkpoints.
\end{itemize}

The remainder of the paper is organized as follows. Section~\ref{sec:related} reviews related work\ldots
