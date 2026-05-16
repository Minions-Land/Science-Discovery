\section{Introduction}

Large language models have improved rapidly, yet their reasoning ability remains brittle.
Despite scaling, models still fail on multi-step arithmetic and logical inference, as documented by recent benchmarks.
Chain-of-thought prompting \citep{Wei2022} and tool use \citep{Schick2023} have partially closed this gap, but performance plateaus on problems requiring more than five reasoning steps.

In this paper, we introduce \textsc{OurNet}, a new training recipe that combines verifier feedback with synthetic data generation.
\textsc{OurNet} is trained on a curated reasoning corpus and substantially outperforms prior work across three benchmarks.

\paragraph{Contributions.}
\begin{itemize}
  \item We propose \textsc{OurNet}, a verifier-augmented training recipe for reasoning-intensive large language models.
  \item We curate a 1.2M-example synthetic reasoning corpus.
  \item We demonstrate that \textsc{OurNet} improves accuracy on GSM8K, MATH, and BIG-Bench Hard by 8--15 absolute percentage points over the strongest baseline.
  \item We release training code, data, and model checkpoints.
\end{itemize}

The remainder of the paper is organized as follows.
Section~\ref{sec:related} reviews related work\ldots
