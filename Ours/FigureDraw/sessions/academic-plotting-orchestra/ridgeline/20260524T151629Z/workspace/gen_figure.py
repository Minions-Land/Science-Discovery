import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.stats import gaussian_kde

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# Color palette — sequential purples/blues per ridge
colors = [
    "#4e4695", "#5a7fc4", "#4aa5a0", "#5dbe6b", "#d4c03a", "#e07b3a"
]

x_min = min(v for vals in samples.values() for v in vals) - 0.3
x_max = max(v for vals in samples.values() for v in vals) + 0.3
x_grid = np.linspace(x_min, x_max, 512)

fig, ax = plt.subplots(figsize=(7, 5.5))

n = len(clusters)
overlap = 0.55  # ridge vertical overlap factor

# Compute per-cluster KDE and plot bottom → top (Cluster 1 at bottom)
for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method="scott")
    density = kde(x_grid)
    # Normalise so peak height = 1 for visual consistency
    density = density / density.max()

    baseline = i * (1.0 - overlap)
    y = baseline + density

    color = colors[i % len(colors)]
    ax.fill_between(x_grid, baseline, y, alpha=0.75, color=color, linewidth=0)
    ax.plot(x_grid, y, color=color, linewidth=1.2)
    # Baseline rule
    ax.axhline(baseline, color="white", linewidth=0.5, zorder=3)

    # Label on the left
    ax.text(
        x_min - 0.05, baseline + 0.12,
        cluster,
        ha="right", va="bottom",
        fontsize=9, color="0.2",
    )

ax.set_xlabel(x_label, fontsize=11)
ax.set_xlim(x_min - 0.8, x_max)
ax.set_ylim(-0.05, n * (1.0 - overlap) + 1.1)
ax.set_yticks([])
ax.spines[["left", "top", "right"]].set_visible(False)
ax.spines["bottom"].set_color("0.5")
ax.tick_params(axis="x", colors="0.4", labelsize=9)
ax.set_title("Expression distributions by cluster", fontsize=12, pad=10)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
