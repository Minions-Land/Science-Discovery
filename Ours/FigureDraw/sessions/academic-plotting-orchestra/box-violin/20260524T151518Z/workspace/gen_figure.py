import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

with open("data.json") as f:
    data = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10μM", "Drug-A\n50μM", "Combo"]
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

groups = [np.array(data["samples"][c]) for c in order]

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(6.5, 4.5))

positions = np.arange(1, len(order) + 1)

# Violin plots
parts = ax.violinplot(groups, positions=positions, widths=0.6,
                      showmeans=False, showmedians=False, showextrema=False)
for pc, color in zip(parts["bodies"], colors):
    pc.set_facecolor(color)
    pc.set_alpha(0.35)
    pc.set_edgecolor("none")

# Box plots (no fliers; we draw jitter instead)
bp = ax.boxplot(groups, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="black", linewidth=2),
                whiskerprops=dict(color="black", linewidth=1),
                capprops=dict(color="black", linewidth=1),
                boxprops=dict(facecolor="white", edgecolor="black", linewidth=1))

# Jittered individual points
for i, (g, color, pos) in enumerate(zip(groups, colors, positions)):
    jitter = rng.uniform(-0.08, 0.08, size=len(g))
    ax.scatter(pos + jitter, g, color=color, alpha=0.35, s=12, zorder=3,
               linewidths=0)

# Significance brackets (Mann-Whitney U vs Control)
ref = groups[0]
y_max = max(g.max() for g in groups)
bracket_base = y_max + 0.08

def pval_label(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "ns"

bracket_y = bracket_base
for i in range(1, len(order)):
    stat, p = stats.mannwhitneyu(ref, groups[i], alternative="two-sided")
    label = pval_label(p)
    x1, x2 = positions[0], positions[i]
    h = 0.05
    ax.plot([x1, x1, x2, x2], [bracket_y, bracket_y + h, bracket_y + h, bracket_y],
            lw=1, color="black")
    ax.text((x1 + x2) / 2, bracket_y + h + 0.01, label, ha="center", va="bottom",
            fontsize=9)
    bracket_y += 0.18

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Relative cell viability", fontsize=11)
ax.set_xlim(0.4, len(order) + 0.6)
ax.set_ylim(-0.05, bracket_y + 0.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", which="both", length=3)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
