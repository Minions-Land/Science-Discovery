import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from scipy import stats

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

ORDER = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
LABELS = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
data = [np.array(d["samples"][c]) for c in ORDER]
metric = d.get("metric", "relative cell viability")

# ── colours ───────────────────────────────────────────────────────────────────
PALETTE = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

# ── figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.8))

positions = np.arange(1, len(ORDER) + 1)

# violin
vp = ax.violinplot(data, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for body, col in zip(vp["bodies"], PALETTE):
    body.set_facecolor(col)
    body.set_alpha(0.35)
    body.set_edgecolor(col)
    body.set_linewidth(0.8)

# box (no fliers — points drawn separately)
bp = ax.boxplot(data, positions=positions, widths=0.22,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="white", linewidth=2.2),
                whiskerprops=dict(color="#333333", linewidth=1.0),
                capprops=dict(color="#333333", linewidth=1.0),
                boxprops=dict(linewidth=0.8))
for patch, col in zip(bp["boxes"], PALETTE):
    patch.set_facecolor(col)
    patch.set_alpha(0.85)

# jittered points
rng = np.random.default_rng(42)
for i, (arr, col) in enumerate(zip(data, PALETTE)):
    jitter = rng.uniform(-0.18, 0.18, size=len(arr))
    ax.scatter(positions[i] + jitter, arr,
               color=col, s=14, alpha=0.35, linewidths=0, zorder=3)

# median diamonds
for i, arr in enumerate(data):
    med = np.median(arr)
    ax.scatter(positions[i], med, marker="D", s=40,
               color="white", edgecolors="#333333", linewidths=0.8, zorder=5)

# ── significance brackets (Mann-Whitney U vs Control) ─────────────────────────
def sig_label(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    return "ns"

ctrl = data[0]
y_top = max(np.max(arr) for arr in data)
bracket_base = y_top + 0.08
step = 0.18

for j, arr in enumerate(data[1:], start=1):
    _, p = stats.mannwhitneyu(ctrl, arr, alternative="two-sided")
    label = sig_label(p)
    x1, x2 = positions[0], positions[j]
    y = bracket_base + (j - 1) * step
    ax.plot([x1, x1, x2, x2], [y - 0.04, y, y, y - 0.04],
            color="#555555", linewidth=0.9)
    ax.text((x1 + x2) / 2, y + 0.01, label,
            ha="center", va="bottom", fontsize=8.5, color="#333333")

# ── axes cosmetics ─────────────────────────────────────────────────────────────
ax.set_xticks(positions)
ax.set_xticklabels(LABELS, fontsize=9)
ax.set_ylabel(metric.capitalize(), fontsize=10)
ax.set_xlim(0.4, len(ORDER) + 0.6)
ax.set_ylim(-0.05, bracket_base + len(data) * step + 0.1)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="both", labelsize=9)
ax.axhline(1.0, color="#aaaaaa", linewidth=0.7, linestyle="--", zorder=0)

legend_elements = [
    mpatches.Patch(facecolor=PALETTE[i], alpha=0.6, label=LABELS[i].replace("\n", " "))
    for i in range(len(ORDER))
]
legend_elements.append(
    Line2D([0], [0], marker="D", color="w", markerfacecolor="white",
           markeredgecolor="#333333", markersize=6, label="Median")
)
ax.legend(handles=legend_elements, fontsize=7.5, frameon=False,
          loc="upper right", ncol=1)

fig.tight_layout()

# ── save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
