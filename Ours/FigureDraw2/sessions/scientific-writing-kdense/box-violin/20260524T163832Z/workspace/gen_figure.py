import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from scipy import stats

with open("data.json") as f:
    d = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]

data = [d["samples"][c] for c in order]

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(6, 5))

positions = np.arange(1, len(order) + 1)

# Violin plots
vp = ax.violinplot(data, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for body, color in zip(vp["bodies"], colors):
    body.set_facecolor(color)
    body.set_alpha(0.35)
    body.set_edgecolor(color)
    body.set_linewidth(0.8)

# Box plots (no fliers — points shown separately)
bp = ax.boxplot(data, positions=positions, widths=0.22,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="white", linewidth=2.0),
                whiskerprops=dict(color="#333333", linewidth=1.0),
                capprops=dict(color="#333333", linewidth=1.0),
                boxprops=dict(linewidth=0.8))
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

# Jittered individual points
for i, (vals, color) in enumerate(zip(data, colors)):
    x = positions[i] + rng.uniform(-0.22, 0.22, size=len(vals))
    ax.scatter(x, vals, color=color, alpha=0.35, s=12, zorder=3,
               linewidths=0)

# Significance brackets (Mann-Whitney U vs Control)
def bracket(ax, x1, x2, y, h, pval):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.0, color="#333333")
    if pval < 0.001:
        label = "***"
    elif pval < 0.01:
        label = "**"
    elif pval < 0.05:
        label = "*"
    else:
        label = "ns"
    ax.text((x1 + x2) / 2, y + h + 0.02, label, ha="center", va="bottom",
            fontsize=9, color="#333333")

ctrl = data[0]
y_max = max(max(v) for v in data)
gap = 0.12
h = 0.04

comparisons = [(1, 2), (1, 3), (1, 4)]
y_levels = [y_max + gap, y_max + gap + 0.22, y_max + gap + 0.44]

for (i, j), y_base in zip(comparisons, y_levels):
    _, pval = stats.mannwhitneyu(data[i - 1], data[j - 1], alternative="two-sided")
    bracket(ax, i, j, y_base, h, pval)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel(d.get("metric", "Relative cell viability").capitalize(), fontsize=11)
ax.set_xlim(0.4, len(order) + 0.6)
ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
