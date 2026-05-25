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

# Palette: sequential blue-to-red through 6 clusters
colors = plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, len(clusters)))

x_min = min(min(v) for v in samples.values()) - 0.3
x_max = max(max(v) for v in samples.values()) + 0.3
x_grid = np.linspace(x_min, x_max, 400)

fig_w, fig_h = 6.5, 5.5
fig, ax = plt.subplots(figsize=(fig_w, fig_h))

overlap = 0.55  # fraction of row height that ridges overlap
n = len(clusters)
row_height = 1.0

for i, name in enumerate(reversed(clusters)):
    vals = np.array(samples[name])
    kde = gaussian_kde(vals, bw_method=0.25)
    density = kde(x_grid)
    density = density / density.max()  # normalise peak to 1

    y_base = i * row_height * (1 - overlap)
    y_top = y_base + density * row_height

    color = colors[n - 1 - i]

    # filled ridge
    ax.fill_between(x_grid, y_base, y_top, color=color, alpha=0.85, lw=0)
    # top line
    ax.plot(x_grid, y_top, color=color * np.array([0.6, 0.6, 0.6, 1.0]), lw=0.8)
    # baseline
    ax.axhline(y_base, color="white", lw=0.4, alpha=0.6)

    # cluster label on left
    ax.text(
        x_min - 0.05, y_base + row_height * 0.35,
        name,
        ha="right", va="center",
        fontsize=8.5, color="#222222"
    )

ax.set_xlim(x_min - 0.1, x_max)
ax.set_xlabel(x_label, fontsize=10)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_color("#888888")
ax.tick_params(axis="x", labelsize=8.5, color="#888888")

fig.tight_layout(rect=[0.14, 0.0, 1.0, 1.0])

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
