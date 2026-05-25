import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import gaussian_kde

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# x range covering all data
all_vals = [v for c in clusters for v in samples[c]]
x_min, x_max = min(all_vals) - 0.3, max(all_vals) + 0.3
x_grid = np.linspace(x_min, x_max, 512)

n = len(clusters)
overlap = 0.6  # fraction of row height that ridges overlap

fig_h = 1.2 + n * 0.9
fig, ax = plt.subplots(figsize=(7, fig_h))

colors = plt.cm.viridis(np.linspace(0.15, 0.85, n))

row_height = 1.0
y_spacing = row_height * (1 - overlap)

for i, cluster in enumerate(reversed(clusters)):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method="scott")
    density = kde(x_grid)
    density = density / density.max() * row_height * 0.95

    y_base = i * y_spacing
    color = colors[n - 1 - i]

    ax.fill_between(x_grid, y_base, y_base + density,
                    color=color, alpha=0.85, linewidth=0)
    ax.plot(x_grid, y_base + density, color=color * np.array([0.7, 0.7, 0.7, 1.0]),
            linewidth=0.8)
    ax.axhline(y_base, color="white", linewidth=0.5, alpha=0.6)

    ax.text(x_min - 0.05, y_base + row_height * 0.35,
            cluster, ha="right", va="center", fontsize=9,
            fontweight="medium")

ax.set_xlim(x_min - 0.8, x_max)
ax.set_ylim(-0.05, (n - 1) * y_spacing + row_height + 0.1)
ax.set_xlabel(x_label, fontsize=10)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
