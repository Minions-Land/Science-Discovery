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

# Color palette (sequential, light to dark)
colors = ["#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#084594"]

fig, ax = plt.subplots(figsize=(7, 5))

x_min = min(v for vals in samples.values() for v in vals)
x_max = max(v for vals in samples.values() for v in vals)
x_grid = np.linspace(x_min - 0.3, x_max + 0.3, 500)

overlap = 0.55  # fraction of spacing used for ridge height
n = len(clusters)

for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method=0.25)
    density = kde(x_grid)
    density = density / density.max()  # normalize to 1

    baseline = i
    scale = overlap

    ax.fill_between(x_grid, baseline, baseline + density * scale,
                    color=colors[i], alpha=0.85, linewidth=0)
    ax.plot(x_grid, baseline + density * scale,
            color=colors[i], linewidth=1.2,
            solid_capstyle="round")
    # baseline rule
    ax.axhline(baseline, color="white", linewidth=0.6, zorder=3)

# Y-axis labels
ax.set_yticks(range(n))
ax.set_yticklabels(clusters, fontsize=10)
ax.set_ylim(-0.15, n - 1 + overlap + 0.1)

ax.set_xlabel(x_label, fontsize=11)
ax.set_xlim(x_grid[0], x_grid[-1])

# Clean up spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(left=False)

ax.set_title("Expression distributions by cluster", fontsize=12, pad=10)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
