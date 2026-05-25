import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter1d

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# Color palette — sequential from cool to warm to show progression
colors = [
    "#4C72B0",  # C1
    "#55A868",  # C2
    "#C44E52",  # C3
    "#8172B2",  # C4
    "#CCB974",  # C5
    "#64B5CD",  # C6
]

fig, ax = plt.subplots(figsize=(7, 6))

# Determine common x range
all_vals = [v for cl in clusters for v in samples[cl]]
x_min, x_max = min(all_vals) - 0.3, max(all_vals) + 0.3
x_grid = np.linspace(x_min, x_max, 400)

# Vertical spacing and overlap
n = len(clusters)
spacing = 1.0
overlap = 0.6  # fraction of spacing that ridges can overlap

y_offsets = [(n - 1 - i) * spacing for i in range(n)]

for i, (cluster, color, y0) in enumerate(zip(clusters, colors, y_offsets)):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method="scott")
    density = kde(x_grid)
    scale = overlap * spacing / density.max()
    density_scaled = density * scale

    y_top = y0 + density_scaled
    y_bottom = np.full_like(y_top, y0)

    # Filled area
    verts = [(x_grid[0], y0)] + list(zip(x_grid, y_top)) + [(x_grid[-1], y0)]
    poly = Polygon(verts, facecolor=color, alpha=0.75, edgecolor="none")
    ax.add_patch(poly)
    # Ridge outline
    ax.plot(x_grid, y_top, color=color, lw=1.5, alpha=0.95)
    # Baseline
    ax.axhline(y0, color="white", lw=0.6, alpha=0.5)

    # Label on left
    ax.text(
        x_min - 0.05,
        y0 + 0.05,
        cluster,
        ha="right",
        va="bottom",
        fontsize=9,
        color="black",
    )

ax.set_xlim(x_min, x_max)
ax.set_ylim(-0.2, (n - 1) * spacing + overlap * spacing + 0.1)
ax.set_yticks([])
ax.set_xlabel(x_label, fontsize=11)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

fig.suptitle("Expression Distributions by Cluster", fontsize=12, y=0.97)
plt.tight_layout(rect=[0.12, 0.0, 1.0, 0.97])

fig.savefig("figure.pdf", dpi=150)
fig.savefig("figure.png", dpi=150)
fig.savefig("figure.svg")
print("Saved figure.pdf, figure.png, figure.svg")
