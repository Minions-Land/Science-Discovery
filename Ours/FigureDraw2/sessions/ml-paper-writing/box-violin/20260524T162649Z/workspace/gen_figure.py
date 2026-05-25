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

ORDER = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
LABELS = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
COLORS = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

samples = [np.array(data["samples"][c]) for c in ORDER]

fig, ax = plt.subplots(figsize=(6.5, 4.5))

# Violin plots
vparts = ax.violinplot(samples, positions=range(1, 5), widths=0.6,
                       showmeans=False, showmedians=False, showextrema=False)
for i, pc in enumerate(vparts["bodies"]):
    pc.set_facecolor(COLORS[i])
    pc.set_alpha(0.35)
    pc.set_edgecolor(COLORS[i])
    pc.set_linewidth(1.2)

# Box plots overlaid
bp = ax.boxplot(samples, positions=range(1, 5), widths=0.22,
                patch_artist=True, notch=False,
                medianprops=dict(color="white", linewidth=2.5),
                whiskerprops=dict(color="#333333", linewidth=1.2),
                capprops=dict(color="#333333", linewidth=1.2),
                flierprops=dict(marker="", linestyle="none"))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(COLORS[i])
    patch.set_alpha(0.85)
    patch.set_edgecolor(COLORS[i])

# Jittered individual points
rng = np.random.default_rng(42)
for i, s in enumerate(samples):
    x = rng.uniform(-0.13, 0.13, size=len(s)) + (i + 1)
    ax.scatter(x, s, color=COLORS[i], s=12, alpha=0.35, linewidths=0,
               zorder=3)

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
bracket_y_base = max(max(s) for s in samples) * 1.04
step = bracket_y_base * 0.08

for i, cond_idx in enumerate([2, 3, 4]):
    if cond_idx - 1 >= len(samples):
        break
    test_s = samples[cond_idx - 1]
    _, p = stats.mannwhitneyu(ctrl, test_s, alternative="two-sided")
    label = sig_label(p)
    y = bracket_y_base + i * step
    x1, x2 = 1, cond_idx
    # draw bracket
    ax.plot([x1, x1, x2, x2], [y - step * 0.25, y, y, y - step * 0.25],
            lw=1.2, color="#555555")
    ax.text((x1 + x2) / 2, y + step * 0.05, label,
            ha="center", va="bottom", fontsize=9, color="#333333")

ax.set_xticks(range(1, 5))
ax.set_xticklabels(LABELS, fontsize=10)
ax.set_ylabel("Relative cell viability", fontsize=11)
ax.set_xlim(0.3, 4.7)
ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
