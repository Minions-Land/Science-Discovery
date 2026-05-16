# Fixture: P6 — LaTeX typography polish (CNS style)

## Role
You are a Writer agent in MinionsOS, polishing the LaTeX source of a Methods
subsection for submission to *Cell*.  The user is the corresponding author.

## Brief

The author has handed you the following LaTeX snippet describing the 4-step data
pipeline of their model, called "OurNet" in some places, "\texttt{OurNet}" in
others, and "\textsf{OurNet}" in a third place.

```latex
\subsection{Pipeline}

The pipeline of OurNet has four steps.

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
  \item Patches are 256x256.
  \item OurNet outputs a per-patch score.
  \item Aggregation uses logistic regression.
\end{itemize}

The full architecture of \textsf{OurNet} is shown in Figure 2.
```

## Task

Polish this LaTeX snippet for *Cell* (CNS-grade typography). Return ONLY the
polished LaTeX source — no commentary. The author will paste your output
directly into the manuscript.

## Constraints

- The model name (`OurNet`) must be typeset consistently throughout.
- Polished output must compile under standard `article` class with `amsmath`,
  `amssymb`, `graphicx`, `xcolor` loaded.

(End of brief.)
