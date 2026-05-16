# Fixture: S3 — LaTeX Typography polish (Wireless Communications, IEEE)

## Role
You are a Writer agent polishing the LaTeX typography of a manuscript for IEEE Transactions on Wireless Communications.

## Brief
Fix the typography issues in the following LaTeX snippet. This is from the Method section of a paper about "DeepMIMO" — a deep learning framework for massive MIMO channel estimation.

## Draft LaTeX

```latex
\paragraph{Channel Estimation Module.}
We use a \textbf{DeepMIMO} network for channel estimation. The network takes the received pilot signal $\mathbf{y} \in \mathbb{C}^{N_p}$ as input.

\paragraph{Beamforming Module.}
The beamforming vectors are computed by \textbf{DeepMIMO}'s second stage.

\begin{itemize}
\item Input: estimated channel $\hat{\mathbf{H}}$
\item Processing: 3-layer MLP with ReLU
\item Output: beamforming vector $\mathbf{w} \in \mathbb{C}^{N_t}$
\end{itemize}

\paragraph{Loss Function.}
We minimize the sum-rate loss:
$$\mathcal{L} = -\sum_{k=1}^{K} \log_2(1 + \text{SINR}_k)$$

The overall \textbf{DeepMIMO} framework achieves 2.3 dB gain over conventional MMSE estimation with \textit{significantly} lower computational complexity.
```

## Expected output
- Replace `\paragraph{}` with `\noindent\textbf{}` or `\subsection{}`
- Define `\newcommand{\methodname}{\textsc{DeepMIMO}\xspace}` and use it throughout
- Remove the itemize block — integrate into prose
- Remove random bold/italic ("significantly")
- Keep the math environments as-is
