import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


OUT = "rounds/R1-scientific-figure-making/case-bar/baseline"
DATA = "fixtures/figures/data/bar-ablation.csv"
ORDER = ["Full", "-A", "-B", "-C"]


df = pd.read_csv(DATA)
summary = df.groupby(["dataset", "method"])["accuracy"].agg(["mean", "std"]).reset_index()
datasets = list(df["dataset"].drop_duplicates())
x = np.arange(len(datasets))
width = 0.2

fig, ax = plt.subplots(figsize=(3.35, 2.7))
for i, method in enumerate(ORDER):
    rows = summary[summary["method"] == method].set_index("dataset").loc[datasets]
    ax.bar(
        x + (i - 1.5) * width,
        rows["mean"],
        width,
        yerr=rows["std"],
        capsize=3,
        label=method,
    )

for j, dataset in enumerate(datasets):
    base = float(df[df["dataset"] == dataset]["external_baseline"].iloc[0])
    ax.hlines(base, j - 0.42, j + 0.42, linestyles="dashed", colors="black")
    full = df[(df["dataset"] == dataset) & (df["method"] == "Full")]["accuracy"]
    minus_c = df[(df["dataset"] == dataset) & (df["method"] == "-C")]["accuracy"]
    p = stats.ttest_ind(full, minus_c, equal_var=False).pvalue
    mark = "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
    y = max(full.mean() + full.std(), minus_c.mean() + minus_c.std()) + 0.025
    ax.text(j, y, mark, ha="center", va="bottom")

ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.set_ylabel("Accuracy")
ax.set_ylim(0, 1.0)
ax.legend()
ax.set_title("Ablation accuracy")
fig.tight_layout()
fig.savefig(f"{OUT}.svg")
fig.savefig(f"{OUT}.pdf")
fig.savefig(f"{OUT}.png", dpi=300)
