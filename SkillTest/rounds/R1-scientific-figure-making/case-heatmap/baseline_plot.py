import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt


OUT = "rounds/R1-scientific-figure-making/case-heatmap/baseline"
DATA = "fixtures/figures/data/heatmap-zscore.csv"


df = pd.read_csv(DATA)
values = df.drop(columns=["gene", "cluster"]).to_numpy()
genes = df["gene"].tolist()
conditions = [c for c in df.columns if c not in ("gene", "cluster")]

fig, ax = plt.subplots(figsize=(4.53, 5.0))
im = ax.imshow(values)
ax.set_xticks(range(len(conditions)))
ax.set_xticklabels(conditions, rotation=45, ha="right")
ax.set_yticks(range(len(genes)))
ax.set_yticklabels(genes)
fig.colorbar(im, ax=ax, label="z-score")
ax.set_title("Expression z-score")
fig.tight_layout()
fig.savefig(f"{OUT}.svg")
fig.savefig(f"{OUT}.pdf")
fig.savefig(f"{OUT}.png", dpi=300)
