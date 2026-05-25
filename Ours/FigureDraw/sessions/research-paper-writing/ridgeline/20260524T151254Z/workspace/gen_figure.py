import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from scipy.stats import gaussian_kde
from matplotlib.backends.backend_pdf import PdfPages

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# Color palette: sequential blue-to-red
colors = ["#4575b4", "#74add1", "#abd9e9", "#fdae61", "#f46d43", "#d73027"]

fig, ax = plt.subplots(figsize=(7, 5))

x_min = min(v for vals in samples.values() for v in vals) - 0.3
x_max = max(v for vals in samples.values() for v in vals) + 0.3
x_grid = np.linspace(x_min, x_max, 500)

n = len(clusters)
overlap = 0.6  # vertical overlap factor

# Compute per-cluster KDE max for normalisation
kde_peaks = []
for cl in clusters:
    kde = gaussian_kde(samples[cl], bw_method=0.25)
    y = kde(x_grid)
    kde_peaks.append(y.max())

row_height = 1.0  # spacing between baselines

for i, cl in enumerate(reversed(clusters)):
    color = colors[n - 1 - i]
    baseline = i * row_height
    kde = gaussian_kde(samples[cl], bw_method=0.25)
    y = kde(x_grid)
    y_scaled = y / kde_peaks[n - 1 - i] * row_height * (1 + overlap)

    ax.fill_between(x_grid, baseline, baseline + y_scaled,
                    color=color, alpha=0.85, linewidth=0)
    ax.plot(x_grid, baseline + y_scaled,
            color="white", linewidth=0.8, alpha=0.6)
    ax.plot(x_grid, baseline + y_scaled,
            color=color, linewidth=1.2, alpha=0.9)

    # Baseline rule
    ax.axhline(baseline, color="white", linewidth=0.5, alpha=0.4,
               xmin=0.0, xmax=1.0)

    # Label on the left
    ax.text(x_min - 0.05, baseline + row_height * 0.25,
            cl, ha="right", va="center", fontsize=9,
            color="#333333", fontweight="medium")

ax.set_xlim(x_min - 0.5, x_max)
ax.set_ylim(-0.15, n * row_height + row_height * overlap)
ax.set_xlabel(x_label, fontsize=10)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)
ax.tick_params(axis="x", labelsize=9)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
