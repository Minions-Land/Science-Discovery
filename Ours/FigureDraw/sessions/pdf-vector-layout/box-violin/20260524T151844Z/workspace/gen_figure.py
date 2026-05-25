import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

rng = np.random.default_rng(42)

with open("data.json") as f:
    d = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
data = [np.array(d["samples"][c]) for c in order]

colors = ["#4878CF", "#6ACC65", "#D65F5F", "#B47CC7"]

fig, ax = plt.subplots(figsize=(6, 4.5))

positions = np.arange(1, len(order) + 1)

# Violin plots
vp = ax.violinplot(data, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for body, color in zip(vp["bodies"], colors):
    body.set_facecolor(color)
    body.set_alpha(0.35)
    body.set_edgecolor("none")

# Box plots (no fliers; we draw points manually)
bp = ax.boxplot(data, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="black", linewidth=2),
                whiskerprops=dict(color="#333333", linewidth=1),
                capprops=dict(color="#333333", linewidth=1),
                boxprops=dict(linewidth=1))
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor("white")
    patch.set_alpha(0.85)
    patch.set_edgecolor("#333333")

# Jittered individual points
for i, (vals, color) in enumerate(zip(data, colors)):
    jitter = rng.uniform(-0.12, 0.12, size=len(vals))
    ax.scatter(positions[i] + jitter, vals, color=color,
               alpha=0.35, s=14, zorder=3, linewidths=0)

# Significance brackets (Mann-Whitney U vs Control)
def bracket(ax, x1, x2, y, h, pval):
    stars = "ns"
    if pval < 0.0001:
        stars = "****"
    elif pval < 0.001:
        stars = "***"
    elif pval < 0.01:
        stars = "**"
    elif pval < 0.05:
        stars = "*"
    if stars == "ns":
        return
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1, color="black")
    ax.text((x1 + x2) / 2, y + h, stars, ha="center", va="bottom",
            fontsize=8, color="black")

ymax = max(np.max(v) for v in data)
gap = 0.12
h = 0.04
ref = data[0]
for i in range(1, len(data)):
    _, p = stats.mannwhitneyu(ref, data[i], alternative="two-sided")
    bracket(ax, positions[0], positions[i], ymax + gap + (i - 1) * 0.22, h, p)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel(d.get("metric", "Relative cell viability").capitalize(), fontsize=10)
ax.set_xlim(0.4, len(order) + 0.6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
