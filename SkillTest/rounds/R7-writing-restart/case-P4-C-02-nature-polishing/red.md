# Experiments

## Main comparison
FlowGate performance on benchmark datasets against established baselines.

## Ablation studies
Module X (graph-attention encoder) contribution to trajectory inference accuracy.
Module Y (entropy-regularised optimal-transport layer) contribution to manifold alignment.
Module Z (topology-aware refinement head) contribution to bifurcation plausibility.

## Hyperparameter sensitivity
[needs experiment] Learning rate and regularisation weight effects on convergence and final accuracy.
[needs experiment] kNN neighbourhood size effects on graph construction and inference quality.

## Case study and visualisation
[planned] Single-cell trajectory reconstruction on a representative dataset with biological validation.
[planned] Comparison of FlowGate bifurcation predictions against known developmental branching points.

---

FlowGate outperformed five established baselines across three public scRNA-seq datasets. On BoneMarrow, Pancreas, and Embryoid datasets, FlowGate achieved mean Kendall-tau correlations of 0.87, 0.91, and 0.84 respectively, compared to Monocle3 (0.79, 0.83, 0.76), Slingshot (0.81, 0.85, 0.78), PAGA (0.74, 0.79, 0.71), TrajectoryNet (0.76, 0.81, 0.73), and Diffmap-EM (0.72, 0.77, 0.69). The multi-task training strategy combining cell-type classification and trajectory priors enabled FlowGate to learn robust latent embeddings that generalised across datasets with distinct cell populations and developmental dynamics.
