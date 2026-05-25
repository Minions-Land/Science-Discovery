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

x_min = min(v for vals in samples.values() for v in vals) - 0.5
x_max = max(v for vals in samples.values() for v in vals) + 0.5
x_grid = np.linspace(x_min, x_max, 500)

n = len(clusters)
overlap = 0.6
colors = plt.cm.viridis(np.linspace(0.15, 0.85, n))

fig, ax = plt.subplots(figsize=(7, 5))

for i, cluster in enumerate(clusters):
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method=0.3)
    density = kde(x_grid)
    density = density / density.max()

    baseline = i * (1 - overlap)
    y = baseline + density

    ax.fill_between(x_grid, baseline, y, alpha=0.75, color=colors[i], zorder=n - i)
    ax.plot(x_grid, y, color=colors[i] * np.array([0.6, 0.6, 0.6, 1.0]), lw=1.0, zorder=n - i)

    ax.text(
        x_min - 0.05, baseline + 0.02,
        cluster,
        ha="right", va="bottom",
        fontsize=9, color="0.2",
        zorder=n + 1,
    )

ax.set_xlabel(x_label, fontsize=11)
ax.set_xlim(x_min - 1.2, x_max)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)
ax.tick_params(axis="x", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
