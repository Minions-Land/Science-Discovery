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
samples = [np.array(data["samples"][c]) for c in order]

palette = ["#4878CF", "#6ACC65", "#D65F5F", "#B47CC7"]

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(6.5, 4.8))

positions = np.arange(1, len(order) + 1)

# Violin plots
vp = ax.violinplot(samples, positions=positions, widths=0.55,
                   showmeans=False, showmedians=False, showextrema=False)
for body, color in zip(vp["bodies"], palette):
    body.set_facecolor(color)
    body.set_edgecolor("none")
    body.set_alpha(0.45)

# Box plots (no fliers; we draw points ourselves)
bp = ax.boxplot(samples, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="black", linewidth=2),
                whiskerprops=dict(color="#333333", linewidth=1.2),
                capprops=dict(color="#333333", linewidth=1.2),
                boxprops=dict(linewidth=1.2))
for patch, color in zip(bp["boxes"], palette):
    patch.set_facecolor("white")
    patch.set_alpha(0.85)
    patch.set_edgecolor(color)
    patch.set_linewidth(1.8)

# Jittered individual points
for i, (pos, vals, color) in enumerate(zip(positions, samples, palette)):
    jitter = rng.uniform(-0.14, 0.14, size=len(vals))
    ax.scatter(pos + jitter, vals, color=color, s=14, alpha=0.35,
               linewidths=0, zorder=3)

# Median markers
for pos, vals, color in zip(positions, samples, palette):
    med = np.median(vals)
    ax.scatter(pos, med, color="white", s=40, zorder=5,
               edgecolors=color, linewidths=1.8)

# Significance brackets (Mann-Whitney U vs Control)
def bracket(ax, x1, x2, y, text, dy=0.04):
    ax.plot([x1, x1, x2, x2], [y, y + dy, y + dy, y], lw=1.1, color="#444444")
    ax.text((x1 + x2) / 2, y + dy + 0.01, text, ha="center", va="bottom",
            fontsize=8, color="#333333")

y_base = max(max(s) for s in samples) + 0.08
ctrl = samples[0]
step = 0.22
for idx, (pos, cond_vals) in enumerate(zip(positions[1:], samples[1:]), start=1):
    _, p = stats.mannwhitneyu(ctrl, cond_vals, alternative="two-sided")
    if p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    else:
        sig = "ns"
    bracket(ax, 1, pos, y_base + (idx - 1) * step, sig)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Relative cell viability", fontsize=11)
ax.set_xlim(0.4, len(order) + 0.6)
ax.set_ylim(bottom=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
