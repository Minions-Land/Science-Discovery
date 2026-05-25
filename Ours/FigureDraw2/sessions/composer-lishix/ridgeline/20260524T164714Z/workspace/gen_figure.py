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

# Color palette — soft sequential blues/greens from bottom to top
colors = ["#4e9af1", "#6db8f5", "#91c4e8", "#a8d8a8", "#70c070", "#3a9a3a"]

fig, ax = plt.subplots(figsize=(7, 5.5))

x_min = min(v for vals in samples.values() for v in vals) - 0.3
x_max = max(v for vals in samples.values() for v in vals) + 0.3
x_grid = np.linspace(x_min, x_max, 512)

overlap = 0.55  # fraction of step that ridges overlap

n = len(clusters)
step = 1.0
baselines = [(n - 1 - i) * step for i in range(n)]  # top cluster at highest y

for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method=0.3)
    density = kde(x_grid)
    density = density / density.max() * (step * (1 + overlap))

    baseline = baselines[i]
    color = colors[i]

    # Filled ridge
    verts_x = np.concatenate([[x_grid[0]], x_grid, [x_grid[-1]]])
    verts_y = np.concatenate([[baseline], density + baseline, [baseline]])
    poly = Polygon(list(zip(verts_x, verts_y)), closed=True,
                   facecolor=color, edgecolor="white", alpha=0.85, linewidth=0.8)
    ax.add_patch(poly)

    # KDE line on top
    ax.plot(x_grid, density + baseline, color="white", linewidth=1.2, alpha=0.9)
    ax.plot(x_grid, density + baseline, color=color, linewidth=0.6, alpha=0.6)

    # Label on left
    ax.text(x_min - 0.05, baseline + 0.05, cluster,
            ha="right", va="bottom", fontsize=9, color="#333333", fontweight="medium")

ax.set_xlim(x_min - 0.8, x_max)
ax.set_ylim(-0.3, n * step + 0.3)
ax.set_xlabel(x_label, fontsize=11, labelpad=6)
ax.set_yticks([])
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#cccccc")
ax.tick_params(axis="x", colors="#666666", labelsize=9)

ax.set_title("Expression Distributions by Cluster", fontsize=12, pad=10, color="#222222")

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
