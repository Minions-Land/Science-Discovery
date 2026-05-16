\newcommand{\methodname}{\textsc{DeepMIMO}\xspace}

\noindent\textbf{Channel Estimation Module.}
We use a \methodname network for channel estimation. The network takes the received pilot signal $\mathbf{y} \in \mathbb{C}^{N_p}$ as input.

\noindent\textbf{Beamforming Module.}
The beamforming vectors are computed by \methodname's second stage. The module takes the estimated channel $\hat{\mathbf{H}}$ as input, processes it through a 3-layer MLP with ReLU activation, and outputs the beamforming vector $\mathbf{w} \in \mathbb{C}^{N_t}$.

\noindent\textbf{Loss Function.}
We minimize the sum-rate loss:
$$\mathcal{L} = -\sum_{k=1}^{K} \log_2(1 + \text{SINR}_k)$$

The overall \methodname framework achieves 2.3 dB gain over conventional MMSE estimation with lower computational complexity.
