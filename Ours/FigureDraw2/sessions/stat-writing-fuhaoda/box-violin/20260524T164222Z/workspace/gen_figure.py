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
metric = data.get("metric", "value")
samples = [np.array(data["samples"][c]) for c in order]

palette = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]

fig, ax = plt.subplots(figsize=(6.5, 4.5))

positions = np.arange(1, len(order) + 1)

# Violin plots
vparts = ax.violinplot(
    samples,
    positions=positions,
    widths=0.6,
    showmeans=False,
    showmedians=False,
    showextrema=False,
)
for i, pc in enumerate(vparts["bodies"]):
    pc.set_facecolor(palette[i])
    pc.set_alpha(0.35)
    pc.set_edgecolor(palette[i])
    pc.set_linewidth(1.0)

# Box plots (no fliers — points shown separately)
bp = ax.boxplot(
    samples,
    positions=positions,
    widths=0.22,
    patch_artist=True,
    showfliers=False,
    medianprops=dict(color="white", linewidth=2.0),
    whiskerprops=dict(color="0.3", linewidth=1.0),
    capprops=dict(color="0.3", linewidth=1.0),
    boxprops=dict(linewidth=0),
)
for i, patch in enumerate(bp["boxes"]):
    patch.set_facecolor(palette[i])
    patch.set_alpha(0.85)

# Jittered individual points
rng = np.random.default_rng(42)
for i, s in enumerate(samples):
    jitter = rng.uniform(-0.18, 0.18, size=len(s))
    ax.scatter(
        positions[i] + jitter,
        s,
        s=10,
        color=palette[i],
        alpha=0.35,
        zorder=3,
        linewidths=0,
    )

# Median markers
for i, s in enumerate(samples):
    ax.scatter(positions[i], np.median(s), s=40, color="white",
               zorder=5, linewidths=1.0, edgecolors=palette[i])

# --- Significance brackets (Mann-Whitney U vs Control) ---
def bracket(ax, x1, x2, y, h, color="0.3", lw=1.0, label=""):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=lw, color=color)
    if label:
        ax.text((x1 + x2) / 2, y + h * 1.1, label,
                ha="center", va="bottom", fontsize=7.5, color=color)

ctrl = samples[0]
comparisons = [(1, 2), (1, 3), (1, 4)]  # 1-indexed positions
all_vals = np.concatenate(samples)
y_max = np.max(all_vals)
gap = (np.max(all_vals) - np.min(all_vals)) * 0.05
h_step = gap * 1.2

sig_labels = []
for x1, x2 in comparisons:
    s2 = samples[x2 - 1]
    _, p = stats.mannwhitneyu(ctrl, s2, alternative="two-sided")
    if p < 0.001:
        lbl = "***"
    elif p < 0.01:
        lbl = "**"
    elif p < 0.05:
        lbl = "*"
    else:
        lbl = "ns"
    sig_labels.append((x1, x2, lbl, p))

bracket_base = y_max + gap
for idx, (x1, x2, lbl, _) in enumerate(sig_labels):
    y = bracket_base + idx * h_step
    bracket(ax, x1, x2, y, gap * 0.6, label=lbl)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel(metric.capitalize(), fontsize=11)
ax.set_xlim(0.35, len(order) + 0.65)
top_pad = bracket_base + len(sig_labels) * h_step + gap * 2
ax.set_ylim(bottom=np.min(all_vals) - gap, top=top_pad)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
