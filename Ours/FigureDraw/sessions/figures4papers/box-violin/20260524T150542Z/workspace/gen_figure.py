import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# Load data
with open("data.json") as f:
    d = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
data = [d["samples"][c] for c in order]
metric = d["metric"]

rng = np.random.default_rng(42)

palette = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]

fig, ax = plt.subplots(figsize=(6, 4.5))

positions = np.arange(1, len(order) + 1)

# Violin plots
parts = ax.violinplot(data, positions=positions, widths=0.6,
                      showmeans=False, showmedians=False, showextrema=False)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(palette[i])
    pc.set_alpha(0.35)
    pc.set_edgecolor(palette[i])
    pc.set_linewidth(0.8)

# Box plots (no fliers — points shown separately)
bp = ax.boxplot(data, positions=positions, widths=0.22,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="white", linewidth=2.5),
                whiskerprops=dict(color="black", linewidth=1.2),
                capprops=dict(color="black", linewidth=1.2),
                boxprops=dict(linewidth=1.0))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(palette[i])
    patch.set_alpha(0.8)

# Jittered individual points
for i, (pos, vals) in enumerate(zip(positions, data)):
    jitter = rng.uniform(-0.22, 0.22, size=len(vals))
    ax.scatter(pos + jitter, vals, s=10, color=palette[i],
               alpha=0.35, zorder=3, linewidths=0)

# Significance brackets (Mann-Whitney U vs Control)
def bracket(ax, x1, x2, y, h, p):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.0, color="black")
    if p < 0.001:
        label = "***"
    elif p < 0.01:
        label = "**"
    elif p < 0.05:
        label = "*"
    else:
        label = "ns"
    ax.text((x1 + x2) / 2, y + h + 0.01, label, ha="center", va="bottom",
            fontsize=9)

ctrl = data[0]
y_max = max(max(v) for v in data)
bracket_base = y_max + 0.08

for i in range(1, len(order)):
    _, p = stats.mannwhitneyu(ctrl, data[i], alternative="two-sided")
    h = 0.07
    y = bracket_base + (i - 1) * 0.20
    bracket(ax, 1, positions[i], y, h, p)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel(f"Relative cell viability", fontsize=11)
ax.set_xlim(0.4, len(order) + 0.6)
ax.set_ylim(-0.05, bracket_base + (len(order) - 1) * 0.20 + 0.25)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
