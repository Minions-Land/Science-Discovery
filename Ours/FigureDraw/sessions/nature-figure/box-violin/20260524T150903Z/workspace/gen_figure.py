import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# Load data
with open("data.json") as f:
    data = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
samples = [np.array(data["samples"][c]) for c in order]

# Colors (Nature-style palette)
colors = ["#4878CF", "#6ACC65", "#D65F5F", "#B47CC7"]

fig, ax = plt.subplots(figsize=(5.5, 4.5))

rng = np.random.default_rng(42)

for i, (vals, color, label) in enumerate(zip(samples, colors, labels)):
    x = i + 1

    # Violin
    vp = ax.violinplot(vals, positions=[x], widths=0.6,
                       showmeans=False, showmedians=False, showextrema=False)
    for body in vp["bodies"]:
        body.set_facecolor(color)
        body.set_alpha(0.35)
        body.set_edgecolor(color)
        body.set_linewidth(0.8)

    # Box (IQR)
    q1, med, q3 = np.percentile(vals, [25, 50, 75])
    iqr = q3 - q1
    whislo = max(vals.min(), q1 - 1.5 * iqr)
    whishi = min(vals.max(), q3 + 1.5 * iqr)

    box_w = 0.18
    rect = mpatches.FancyBboxPatch(
        (x - box_w / 2, q1), box_w, iqr,
        boxstyle="square,pad=0", linewidth=1.2,
        edgecolor=color, facecolor="white", zorder=3
    )
    ax.add_patch(rect)
    # Whiskers
    ax.plot([x, x], [whislo, q1], color=color, lw=1.2, zorder=3)
    ax.plot([x, x], [q3, whishi], color=color, lw=1.2, zorder=3)
    ax.plot([x - box_w * 0.4, x + box_w * 0.4], [whislo, whislo], color=color, lw=1.2, zorder=3)
    ax.plot([x - box_w * 0.4, x + box_w * 0.4], [whishi, whishi], color=color, lw=1.2, zorder=3)
    # Median line
    ax.plot([x - box_w / 2, x + box_w / 2], [med, med],
            color=color, lw=2.2, zorder=4)

    # Jittered points
    jitter = rng.uniform(-0.12, 0.12, size=len(vals))
    ax.scatter(x + jitter, vals, color=color, alpha=0.35, s=8, zorder=2, linewidths=0)

# Significance brackets (Mann-Whitney U vs Control)
def sig_label(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "ns"

ctrl = samples[0]
bracket_pairs = [(1, 2), (1, 3), (1, 4)]
y_top = max(v.max() for v in samples)
bracket_heights = [y_top + 0.18, y_top + 0.38, y_top + 0.58]

for (xi, xj), bh in zip(bracket_pairs, bracket_heights):
    _, p = stats.mannwhitneyu(ctrl, samples[xj - 1], alternative="two-sided")
    label = sig_label(p)
    ax.plot([xi, xi, xj, xj], [bh - 0.04, bh, bh, bh - 0.04],
            color="#333333", lw=0.9)
    ax.text((xi + xj) / 2, bh + 0.01, label, ha="center", va="bottom",
            fontsize=8, color="#333333")

ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("Relative cell viability", fontsize=10)
ax.set_xlim(0.4, 4.6)
ax.set_ylim(-0.05, bracket_heights[-1] + 0.18)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
