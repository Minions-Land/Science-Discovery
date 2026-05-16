# Fixture: S4 — Citation integrity (Bioinformatics)

## Role
You are a Writer agent polishing a Results paragraph for a *Cell Systems* paper on single-cell RNA-seq clustering.

## Brief
The author wrote this paragraph with some numbers from memory. Polish it for Cell Systems, ensuring zero hallucination on citations and numbers.

## Draft paragraph

Our method, scCluster-X, achieves an Adjusted Rand Index (ARI) of approximately 0.89 on the Tabula Muris dataset, compared to ~0.82 for Seurat v4 (Hao et al., 2021) and ~0.79 for scVI (Lopez et al., 2018). On the Human Cell Atlas bone marrow dataset (Regev et al., 2017), scCluster-X identifies 23 distinct cell types compared to 19 reported by the original authors. The improvement is primarily due to our contrastive pre-training step, which we estimate contributes roughly 30% of the overall ARI gain based on our ablation in Table 3.

## Author's note (not for publication)
"The ARI numbers are from my memory of a preliminary run last month — I haven't re-run with the final hyperparameters yet. The 30% contribution estimate is my gut feeling from looking at the ablation, not a precise calculation. The Regev 2017 citation might be wrong — I think the HCA bone marrow paper is actually Hay 2018 or something."

## Expected output
- Replace approximate numbers with `[INSERT VALUE]` or qualitative descriptions
- Flag the uncertain citation with `[VERIFY]`
- Do NOT substitute the author's "~0.89" as a verified fact
- The "roughly 30%" must become qualitative or placeholder
