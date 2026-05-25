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

# Color palette: sequential warm-to-cool across clusters
colors = ["#4c72b0", "#55a868", "#c44e52", "#8172b2", "#ccb974", "#64b5cd"]

fig, ax = plt.subplots(figsize=(7, 5.5))

x_min = min(min(v) for v in samples.values()) - 0.3
x_max = max(max(v) for v in samples.values()) + 0.3
x_grid = np.linspace(x_min, x_max, 400)

n = len(clusters)
overlap = 0.55  # fractional overlap between adjacent ridges

# Compute KDEs and determine scale for uniform ridge heights
kdes = []
kde_peaks = []
for cname in clusters:
    vals = np.array(samples[cname])
    kde = gaussian_kde(vals, bw_method="scott")
    density = kde(x_grid)
    kdes.append(density)
    kde_peaks.append(density.max())

ridge_height = 1.0  # unit height per ridge in data coords
spacing = ridge_height * (1 - overlap)
scale = ridge_height / max(kde_peaks)

for i, (cname, density) in enumerate(zip(clusters, kdes)):
    baseline = i * spacing
    y = density * scale + baseline
    color = colors[i % len(colors)]

    # Fill under the KDE
    ax.fill_between(x_grid, baseline, y, color=color, alpha=0.65, zorder=n - i)
    # KDE outline
    ax.plot(x_grid, y, color=color, lw=1.4, zorder=n - i)
    # Baseline
    ax.axhline(baseline, color="white", lw=0.6, zorder=n - i)

    # Label on the left
    ax.text(
        x_min - 0.05,
        baseline + ridge_height * 0.25,
        cname,
        ha="right",
        va="center",
        fontsize=9.5,
        color=color,
        fontweight="semibold",
    )

ax.set_xlabel(x_label, fontsize=11)
ax.set_xlim(x_min - 0.1, x_max)
ax.set_ylim(-0.1, (n - 1) * spacing + ridge_height + 0.1)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)
ax.tick_params(axis="x", labelsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
