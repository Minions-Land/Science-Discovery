# Fixture: P6H — LaTeX typography polish (conference mode-switch variant)

## Role
You are a Writer agent in MinionsOS, polishing the LaTeX source of an
Introduction section for submission to **NeurIPS 2026** (machine-learning
conference). The user is the corresponding author.

## Brief

The author has handed you the following LaTeX snippet — an Introduction draft
that contains a "Contributions" list at the bottom, inconsistent model-name
typography, and several \paragraph{} headers in the middle.

```latex
\section{Introduction}

Large language models have improved rapidly.  However, their reasoning ability
remains brittle.

\paragraph{The reasoning gap.}
Despite scaling, models still fail on multi-step arithmetic and logical
inference, as documented by recent benchmarks.

\paragraph{Prior approaches.}
Chain-of-thought prompting (Wei et al., 2022) and tool use (Schick et al.,
2023) have partially closed this gap, but performance plateaus on problems
requiring more than 5 reasoning steps.

In this paper, we introduce OurNet, a new training recipe that combines
\texttt{OurNet}-style verifier feedback with synthetic data generation.
\textsf{OurNet} is trained on a curated reasoning corpus and substantially
outperforms prior work across three benchmarks.

\begin{itemize}
  \item We propose OurNet, a verifier-augmented training recipe for
        reasoning-intensive LLMs.
  \item We curate a 1.2 M-example synthetic reasoning corpus.
  \item We show that OurNet improves accuracy on GSM8K, MATH, and BIG-Bench
        Hard by 8-15 absolute percentage points over the strongest baseline.
  \item We release training code, data, and checkpoints.
\end{itemize}

The remainder of the paper is organised as follows.  Section~\ref{sec:related}
reviews related work...
```

## Task

Polish this LaTeX snippet for **NeurIPS 2026 camera-ready**. Return ONLY the
polished LaTeX source — no commentary. The author will paste your output
directly into the manuscript.

## Constraints

- Output must compile under `neurips_2026` style.
- The contribution-bullet list at the bottom is conference-standard and the
  reviewers expect it; do NOT silently delete it.
- The model name `OurNet` must be typeset consistently throughout.

(End of brief.)
