from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures/figures-novel-form/manifold/data/manifold-cells.csv"
OUT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "Arial",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 7,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.6,
})

df = pd.read_csv(DATA)
clusters = ["progenitor", "intermediate", "terminal_A", "terminal_B"]
colors = {
    "progenitor": "#4C78A8",
    "intermediate": "#F58518",
    "terminal_A": "#54A24B",
    "terminal_B": "#E45756",
}

fig, ax = plt.subplots(figsize=(5.7, 3.9))

for cluster in clusters:
    sub = df[df["cluster"] == cluster]
    ax.scatter(
        sub["x"],
        sub["y"],
        s=12,
        color=colors[cluster],
        alpha=0.72,
        edgecolors="white",
        linewidths=0.25,
        label=cluster.replace("_", " "),
    )

ax.set_title("Single-cell differentiation manifold", fontsize=8, pad=6)
ax.set_xlabel("Embedding 1")
ax.set_ylabel("Embedding 2")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=2.5, width=0.6)
ax.legend(frameon=False, loc="upper left", ncol=2, handletextpad=0.3, columnspacing=0.8)
ax.set_aspect("equal", adjustable="box")

fig.tight_layout(pad=0.4)
for ext in ("svg", "pdf", "png"):
    kwargs = {"dpi": 300} if ext == "png" else {}
    fig.savefig(OUT / f"baseline.{ext}", bbox_inches="tight", **kwargs)
