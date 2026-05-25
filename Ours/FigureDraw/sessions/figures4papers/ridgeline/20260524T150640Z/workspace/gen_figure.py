import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import gaussian_kde
from matplotlib.backends.backend_pdf import PdfPages

with open("data.json") as f:
    data = json.load(f)

clusters = data["clusters"]
samples = data["samples"]
x_label = data["x_label"]

# Color palette (one per cluster, top to bottom = C1..C6)
colors = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#76b7b2", "#b07aa1"]

fig, ax = plt.subplots(figsize=(7, 5))

x_min = min(min(v) for v in samples.values()) - 0.3
x_max = max(max(v) for v in samples.values()) + 0.3
xs = np.linspace(x_min, x_max, 500)

n = len(clusters)
overlap = 0.55  # fraction of spacing used for ridge height

# Draw bottom to top so upper ridges paint over lower ones
for i, cluster in enumerate(reversed(clusters)):
    color = colors[n - 1 - i]
    vals = np.array(samples[cluster])
    kde = gaussian_kde(vals, bw_method=0.25)
    ys = kde(xs)
    ys = ys / ys.max()  # normalise to [0,1]

    baseline = i
    ridge = ys * overlap

    ax.fill_between(xs, baseline, baseline + ridge, color=color, alpha=0.85, lw=0)
    ax.plot(xs, baseline + ridge, color=color, lw=1.2)
    ax.axhline(baseline, color="white", lw=0.6, zorder=3)

# Y-axis labels
ax.set_yticks(range(n))
ax.set_yticklabels(list(reversed(clusters)), fontsize=9)
ax.yaxis.set_tick_params(length=0)

ax.set_xlabel(x_label, fontsize=10)
ax.set_xlim(x_min, x_max)
ax.set_ylim(-0.1, n - 1 + overlap + 0.1)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", which="both", left=False)

ax.set_title("Expression distributions by cluster", fontsize=11, pad=8)

plt.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
