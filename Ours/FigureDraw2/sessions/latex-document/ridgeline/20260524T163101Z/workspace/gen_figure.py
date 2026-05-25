import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from scipy.stats import gaussian_kde

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# Color palette — one per cluster, top to bottom = C1..C6
colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948"]

fig, ax = plt.subplots(figsize=(7, 5))

x_min = min(min(v) for v in samples.values()) - 0.3
x_max = max(max(v) for v in samples.values()) + 0.3
x_grid = np.linspace(x_min, x_max, 512)

overlap = 0.55  # vertical overlap factor (fraction of row height)
n = len(clusters)
row_height = 1.0

yticks = []
ytick_labels = []

for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method="scott")
    density = kde(x_grid)
    # Normalize so peak == row_height * overlap
    density = density / density.max() * row_height * (1 + overlap)

    base_y = (n - 1 - i) * row_height  # C1 at top

    color = colors[i]
    fill_y = base_y + density

    ax.fill_between(x_grid, base_y, fill_y, alpha=0.75, color=color, linewidth=0)
    ax.plot(x_grid, fill_y, color=color, linewidth=1.2)
    # Baseline
    ax.axhline(base_y, color="white", linewidth=0.4, xmin=0, xmax=1, zorder=0)

    yticks.append(base_y)
    ytick_labels.append(cluster)

ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels, fontsize=9)
ax.set_xlabel(x_label, fontsize=10)
ax.set_xlim(x_min, x_max)
ax.set_ylim(-0.1, n * row_height + 0.2)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(left=False)
ax.set_title("Expression distributions by cluster", fontsize=11, pad=10)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
