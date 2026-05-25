import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import mannwhitneyu

with open("data.json") as f:
    data = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
samples = [np.array(data["samples"][c]) for c in order]

colors = ["#4C9BE8", "#F4A460", "#E86060", "#7B68EE"]
rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(7, 5))

positions = np.arange(1, len(order) + 1)

# Violin plots
vp = ax.violinplot(samples, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for body, color in zip(vp["bodies"], colors):
    body.set_facecolor(color)
    body.set_edgecolor("none")
    body.set_alpha(0.45)

# Box plots (no fliers; we plot points manually)
bp = ax.boxplot(samples, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="black", linewidth=2.0),
                boxprops=dict(facecolor="white", edgecolor="black", linewidth=1.2),
                whiskerprops=dict(color="black", linewidth=1.2),
                capprops=dict(color="black", linewidth=1.2))

# Jittered individual points
for i, (pos, vals, color) in enumerate(zip(positions, samples, colors)):
    jitter = rng.uniform(-0.12, 0.12, size=len(vals))
    ax.scatter(pos + jitter, vals, color=color, alpha=0.35, s=14,
               zorder=3, linewidths=0)

# Significance brackets (Mann-Whitney U vs Control)
def bracket(ax, x1, x2, y, color="black", lw=1.1):
    h = 0.03
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=lw, color=color)

ctrl = samples[0]
y_top = max(np.max(s) for s in samples)
offsets = [0.12, 0.22, 0.32]
pval_labels = []
for i, s in enumerate(samples[1:], start=1):
    stat, p = mannwhitneyu(ctrl, s, alternative="two-sided")
    if p < 0.001:
        label = "***"
    elif p < 0.01:
        label = "**"
    elif p < 0.05:
        label = "*"
    else:
        label = "ns"
    y_br = y_top + offsets[i - 1]
    bracket(ax, 1, i + 1, y_br)
    ax.text((1 + i + 1) / 2, y_br + 0.04, label,
            ha="center", va="bottom", fontsize=10)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=11)
ax.set_ylabel("Relative cell viability", fontsize=12)
ax.set_xlim(0.4, len(order) + 0.6)
ax.set_ylim(-0.05, y_top + 0.62)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=10)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done: figure.pdf, figure.png, figure.svg")
