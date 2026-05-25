import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from itertools import combinations

# Load data
with open("data.json") as f:
    d = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
data = [np.array(d["samples"][c]) for c in order]
metric = d.get("metric", "relative cell viability")

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(7, 5))

palette = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

positions = np.arange(1, len(order) + 1)

# Violin plots
vp = ax.violinplot(data, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for i, body in enumerate(vp["bodies"]):
    body.set_facecolor(palette[i])
    body.set_alpha(0.35)
    body.set_edgecolor(palette[i])
    body.set_linewidth(1.2)

# Box plots (no fliers — we draw points ourselves)
bp = ax.boxplot(data, positions=positions, widths=0.22,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="white", linewidth=2.5),
                whiskerprops=dict(color="#333333", linewidth=1.2),
                capprops=dict(color="#333333", linewidth=1.2),
                boxprops=dict(linewidth=1.2))
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(palette[i])
    patch.set_alpha(0.75)

# Jittered individual points
for i, (pos, vals) in enumerate(zip(positions, data)):
    jitter = rng.uniform(-0.18, 0.18, size=len(vals))
    ax.scatter(pos + jitter, vals, color=palette[i], alpha=0.35,
               s=14, zorder=3, linewidths=0)

# Significance brackets (Mann-Whitney U, Bonferroni-corrected)
pairs = [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]
n_tests = len(pairs)
y_top = max(np.max(v) for v in data)
bracket_gap = 0.12
bracket_h = 0.05
y_start = y_top + 0.15

def sig_label(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "ns"

drawn = 0
for (i, j) in pairs:
    _, p_raw = stats.mannwhitneyu(data[i], data[j], alternative="two-sided")
    p = min(p_raw * n_tests, 1.0)  # Bonferroni
    label = sig_label(p)
    if label == "ns":
        continue
    y = y_start + drawn * (bracket_gap + bracket_h)
    x1, x2 = positions[i], positions[j]
    ax.plot([x1, x1, x2, x2],
            [y, y + bracket_h, y + bracket_h, y],
            lw=1.0, color="#333333")
    ax.text((x1 + x2) / 2, y + bracket_h + 0.01, label,
            ha="center", va="bottom", fontsize=9, color="#333333")
    drawn += 1

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel(metric.capitalize(), fontsize=11)
ax.set_xlim(0.4, len(order) + 0.6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", which="both", length=3)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
