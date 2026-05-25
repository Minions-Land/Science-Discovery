import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import mannwhitneyu

# Load data
with open("data.json") as f:
    d = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10μM", "Drug-A\n50μM", "Combo"]
data = [d["samples"][c] for c in order]
metric = d["metric"]

# Colors
palette = ["#4c78a8", "#72b7b2", "#f58518", "#e45756"]

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(6.5, 4.5))

positions = np.arange(1, len(order) + 1)

# Violin plots
vp = ax.violinplot(data, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for body, color in zip(vp["bodies"], palette):
    body.set_facecolor(color)
    body.set_alpha(0.45)
    body.set_edgecolor("none")

# Box plots (thin, no fliers)
bp = ax.boxplot(data, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="black", linewidth=2),
                whiskerprops=dict(color="#333333", linewidth=1),
                capprops=dict(color="#333333", linewidth=1),
                boxprops=dict(linewidth=1))
for patch, color in zip(bp["boxes"], palette):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

# Jittered individual points
for i, (vals, pos) in enumerate(zip(data, positions)):
    jitter = rng.uniform(-0.22, 0.22, size=len(vals))
    ax.scatter(pos + jitter, vals, color=palette[i],
               alpha=0.35, s=14, linewidths=0, zorder=3)

# Significance brackets (Mann-Whitney U vs Control)
control = data[0]
sig_pairs = []
for j in range(1, len(order)):
    stat, p = mannwhitneyu(control, data[j], alternative="two-sided")
    sig_pairs.append((j, p))

def pval_label(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "ns"

y_max = max(max(v) for v in data)
bracket_base = y_max * 1.06
step = y_max * 0.07

for k, (j, p) in enumerate(sig_pairs):
    y = bracket_base + k * step
    x1, x2 = positions[0], positions[j]
    ax.plot([x1, x1, x2, x2], [y - step * 0.3, y, y, y - step * 0.3],
            color="#444444", linewidth=1)
    ax.text((x1 + x2) / 2, y + step * 0.05, pval_label(p),
            ha="center", va="bottom", fontsize=9)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel(metric.capitalize(), fontsize=10)
ax.set_xlim(0.35, len(order) + 0.65)
ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
