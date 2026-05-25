import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

with open("data.json") as f:
    data = json.load(f)

ORDER = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
LABELS = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
COLORS = ["#4878CF", "#6ACC65", "#D65F5F", "#B47CC7"]

samples = [np.array(data["samples"][c]) for c in ORDER]

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(6.5, 4.5))

positions = np.arange(1, len(ORDER) + 1)

# Violin plots
parts = ax.violinplot(samples, positions=positions, widths=0.6,
                      showmeans=False, showmedians=False, showextrema=False)
for pc, color in zip(parts["bodies"], COLORS):
    pc.set_facecolor(color)
    pc.set_alpha(0.35)
    pc.set_edgecolor("none")

# Box plots (no fliers — we plot points manually)
bp = ax.boxplot(samples, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="white", linewidth=2.5),
                whiskerprops=dict(color="#444444", linewidth=1.2),
                capprops=dict(color="#444444", linewidth=1.2),
                boxprops=dict(linewidth=0))
for patch, color in zip(bp["boxes"], COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

# Jittered individual points
for i, (pos, samp, color) in enumerate(zip(positions, samples, COLORS)):
    jitter = rng.uniform(-0.22, 0.22, size=len(samp))
    ax.scatter(pos + jitter, samp, color=color, alpha=0.35,
               s=14, linewidths=0, zorder=3)

# Significance brackets (Mann-Whitney U vs Control)
ctrl = samples[0]
sig_pairs = []
for i in range(1, len(ORDER)):
    stat, p = stats.mannwhitneyu(ctrl, samples[i], alternative="two-sided")
    sig_pairs.append((i + 1, p))

def pval_label(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "ns"

y_max = max(np.max(s) for s in samples)
bracket_base = y_max * 1.05
step = y_max * 0.08

for idx, (pos, p) in enumerate(sig_pairs):
    label = pval_label(p)
    y = bracket_base + idx * step
    x1, x2 = 1, pos
    ax.plot([x1, x1, x2, x2], [y - step * 0.3, y, y, y - step * 0.3],
            color="#333333", linewidth=1.0)
    ax.text((x1 + x2) / 2, y + step * 0.05, label,
            ha="center", va="bottom", fontsize=9, color="#333333")

ax.set_xticks(positions)
ax.set_xticklabels(LABELS, fontsize=10)
ax.set_ylabel("Relative cell viability", fontsize=11)
ax.set_xlim(0.35, len(ORDER) + 0.65)
ax.set_ylim(-0.05, bracket_base + step * len(sig_pairs) + step * 0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

ax.axhline(1.0, color="#888888", linewidth=0.8, linestyle="--", zorder=0)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
