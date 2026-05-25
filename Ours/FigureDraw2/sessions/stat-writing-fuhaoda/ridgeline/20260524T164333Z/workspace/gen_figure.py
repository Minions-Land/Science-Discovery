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

# Color palette: sequential blue-to-red across clusters
colors = [
    "#4e79a7", "#76b7b2", "#59a14f", "#edc948", "#f28e2b", "#e15759"
]

x_min = min(min(v) for v in samples.values())
x_max = max(max(v) for v in samples.values())
x_grid = np.linspace(x_min - 0.3, x_max + 0.3, 500)

overlap = 0.55  # fraction of row height to overlap into row above

fig_width = 6.5
row_height = 1.0
fig_height = row_height * len(clusters) * (1 - overlap) + row_height * overlap + 0.8

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

n = len(clusters)
spacing = 1.0  # vertical unit between baseline centers

for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method=0.25)
    density = kde(x_grid)
    density = density / density.max()  # normalize peak to 1

    baseline = i * spacing * (1 - overlap)
    scale = spacing * (1 + overlap * 0.8)

    y_fill = baseline + density * scale
    color = colors[i % len(colors)]

    # White fill below to mask lower ridges, then colored fill on top
    ax.fill_between(x_grid, baseline, y_fill, color="white", zorder=i * 2)
    ax.fill_between(x_grid, baseline, y_fill, color=color, alpha=0.75, zorder=i * 2 + 1)
    ax.plot(x_grid, y_fill, color=color, lw=1.2, zorder=i * 2 + 2)
    ax.axhline(baseline, color="white", lw=0.6, zorder=i * 2)

    # Label on left
    ax.text(
        x_min - 0.35, baseline + scale * 0.25,
        cluster,
        ha="right", va="center",
        fontsize=9, color="#333333",
        zorder=i * 2 + 3,
    )

ax.set_xlim(x_min - 0.9, x_max + 0.3)
ax.set_ylim(-0.05, (n - 1) * spacing * (1 - overlap) + spacing * (1 + overlap * 0.8) + 0.05)
ax.set_xlabel(x_label, fontsize=10)
ax.set_yticks([])
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
