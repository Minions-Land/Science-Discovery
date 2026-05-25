import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from scipy.stats import gaussian_kde
from matplotlib.backends.backend_pdf import PdfPages

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# Color palette: sequential blues/purples from bottom to top
colors = [
    "#4e79a7",
    "#59a14f",
    "#f28e2b",
    "#e15759",
    "#b07aa1",
    "#76b7b2",
]

x_min = min(v for vals in samples.values() for v in vals) - 0.3
x_max = max(v for vals in samples.values() for v in vals) + 0.3
x_grid = np.linspace(x_min, x_max, 500)

overlap = 1.8  # vertical overlap factor

fig, ax = plt.subplots(figsize=(7, 5))

n = len(clusters)
for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method=0.25)
    density = kde(x_grid)
    density = density / density.max()  # normalize to 1

    baseline = i * overlap
    y = density + baseline

    color = colors[i % len(colors)]

    # Fill under the ridge
    ax.fill_between(x_grid, baseline, y, alpha=0.7, color=color, zorder=n - i)
    # Outline
    ax.plot(x_grid, y, color=color, lw=1.2, zorder=n - i + 0.5)
    # Baseline
    ax.plot(x_grid, [baseline] * len(x_grid), color="white", lw=0.5, zorder=n - i + 0.4)

    # Label on the left
    ax.text(
        x_min - 0.05,
        baseline + 0.15,
        cluster,
        ha="right",
        va="bottom",
        fontsize=9,
        color=color,
        fontweight="bold",
    )

ax.set_xlabel(x_label, fontsize=11)
ax.set_xlim(x_min - 0.5, x_max)
ax.set_ylim(-0.3, n * overlap + 0.5)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

ax.set_title("Expression Distributions by Cluster", fontsize=12, pad=10)

plt.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
