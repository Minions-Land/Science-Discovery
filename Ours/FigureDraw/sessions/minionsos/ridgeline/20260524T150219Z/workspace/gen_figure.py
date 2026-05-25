import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def gaussian_kde(data, bw_method=0.25):
    """Minimal KDE using Gaussian kernel."""
    n = len(data)
    std = np.std(data, ddof=1)
    # Silverman's rule scaled by bw_method factor
    bw = bw_method * std * n ** (-0.2)

    def evaluate(x_grid):
        diff = (x_grid[:, None] - data[None, :]) / bw
        return np.exp(-0.5 * diff ** 2).sum(axis=1) / (n * bw * np.sqrt(2 * np.pi))

    evaluate.max = lambda: None  # placeholder, computed after call
    return evaluate

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

colors = [
    "#4e79a7",
    "#59a14f",
    "#f28e2b",
    "#e15759",
    "#b07aa1",
    "#76b7b2",
]

fig, ax = plt.subplots(figsize=(7, 6))

x_min = min(min(v) for v in samples.values())
x_max = max(max(v) for v in samples.values())
x_grid = np.linspace(x_min - 0.3, x_max + 0.3, 500)

n = len(clusters)

# Pre-compute densities
densities = {}
for cl in clusters:
    vals = np.array(samples[cl])
    kde_fn = gaussian_kde(vals, bw_method=0.25)
    densities[cl] = kde_fn(x_grid)

max_peak = max(d.max() for d in densities.values())
row_height = max_peak * 0.6

for i, cl in enumerate(reversed(clusters)):
    y_base = i * row_height
    density = densities[cl]
    color = colors[n - 1 - i]

    ax.fill_between(x_grid, y_base, y_base + density,
                    alpha=0.75, color=color, linewidth=0)
    ax.plot(x_grid, y_base + density, color=color, linewidth=1.2)

    ax.text(x_min - 0.35, y_base + density.max() * 0.45,
            cl, ha="right", va="center", fontsize=9,
            fontweight="bold", color=color)

ax.set_xlabel(x_label, fontsize=11)
ax.set_yticks([])
ax.set_xlim(x_min - 1.2, x_max + 0.4)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

ax.set_title("Expression Distributions by Cluster", fontsize=12, pad=10)

plt.tight_layout()
plt.savefig("figure.pdf", dpi=150, bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
