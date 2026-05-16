from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures/figures-novel-form/radar/data/method-metric-comparison.csv"
OUT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "Arial",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 7,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.6,
})

df = pd.read_csv(DATA).set_index("method")
metrics = list(df.columns)
x = np.arange(len(metrics))
width = 0.15
colors = plt.get_cmap("tab10").colors[: len(df)]

fig, ax = plt.subplots(figsize=(5.8, 3.6))

for i, (method, row) in enumerate(df.iterrows()):
    ax.bar(
        x + (i - 2) * width,
        row.values,
        width,
        label=method,
        color=colors[i],
        alpha=0.86,
        linewidth=0,
    )

ax.set_title("Method comparison across evaluation metrics", fontsize=8, pad=6)
ax.set_ylabel("Normalised score")
ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=25, ha="right")
ax.set_ylim(0, 1.04)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#d8d8d8", linewidth=0.5)
ax.legend(frameon=False, ncol=2, loc="lower left", bbox_to_anchor=(0, 1.01), borderaxespad=0)

fig.tight_layout(pad=0.45)
for ext in ("svg", "pdf", "png"):
    kwargs = {"dpi": 300} if ext == "png" else {}
    fig.savefig(OUT / f"baseline.{ext}", bbox_inches="tight", **kwargs)
