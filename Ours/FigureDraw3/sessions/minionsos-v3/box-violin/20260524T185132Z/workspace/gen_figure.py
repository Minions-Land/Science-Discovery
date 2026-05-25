"""
gen_figure.py — violin + box + jitter overlay for 4-condition cell viability data.
Data source: data.json (conditions x 100 samples, metric: relative cell viability)
"""

import json
import numpy as np
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# ── Palette ─────────────────────────────────────────────────────────────────
# Okabe-Ito colorblind-safe, ordered Control → low → high → Combo
PALETTE = {
    "Control":      "#767676",   # neutral grey
    "Drug-A 10uM":  "#56B4E9",   # light blue
    "Drug-A 50uM":  "#0072B2",   # deep blue
    "Combo":        "#D55E00",   # vermillion accent
}

# ── Data ────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    raw = json.load(f)

ORDER = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
LABELS = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
data = [np.array(raw["samples"][c]) for c in ORDER]
metric = raw.get("metric", "relative cell viability")

# ── Figure ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4.5))

positions = np.arange(len(ORDER))
rng = np.random.default_rng(42)

for i, (cond, vals) in enumerate(zip(ORDER, data)):
    color = PALETTE[cond]

    # Violin
    parts = ax.violinplot(vals, positions=[i], widths=0.55,
                          showmeans=False, showmedians=False, showextrema=False)
    for pc in parts["bodies"]:
        pc.set_facecolor(color)
        pc.set_alpha(0.30)
        pc.set_edgecolor(color)
        pc.set_linewidth(0.8)

    # Box (manual: Q1, median, Q3, whiskers)
    q1, med, q3 = np.percentile(vals, [25, 50, 75])
    iqr = q3 - q1
    lo_wh = max(vals[vals >= q1 - 1.5 * iqr].min(), vals.min())
    hi_wh = min(vals[vals <= q3 + 1.5 * iqr].max(), vals.max())

    box_w = 0.18
    rect = mpatches.FancyBboxPatch(
        (i - box_w / 2, q1), box_w, iqr,
        boxstyle="square,pad=0", linewidth=1.2,
        edgecolor=color, facecolor="white", zorder=3
    )
    ax.add_patch(rect)
    ax.hlines(med, i - box_w / 2, i + box_w / 2,
              colors=color, linewidths=2.0, zorder=4)
    ax.vlines(i, lo_wh, q1, colors=color, linewidths=1.0, zorder=3)
    ax.vlines(i, q3, hi_wh, colors=color, linewidths=1.0, zorder=3)
    ax.hlines([lo_wh, hi_wh], i - box_w / 4, i + box_w / 4,
              colors=color, linewidths=1.0, zorder=3)

    # Jittered points
    jitter = rng.uniform(-0.14, 0.14, size=len(vals))
    ax.scatter(i + jitter, vals, color=color, alpha=0.35,
               s=10, linewidths=0, zorder=2)

# ── Significance brackets (Mann-Whitney U vs Control) ───────────────────────
def bracket(ax, x1, x2, y, h, pval):
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y],
            lw=0.8, color="#272727")
    if pval < 0.001:
        label = "***"
    elif pval < 0.01:
        label = "**"
    elif pval < 0.05:
        label = "*"
    else:
        label = "ns"
    ax.text((x1 + x2) / 2, y + h + 0.01, label,
            ha="center", va="bottom", fontsize=8, color="#272727")

ctrl = data[0]
y_top = max(np.concatenate(data)) + 0.05
bracket_h = 0.06

for i, cond in enumerate(ORDER[1:], start=1):
    _, pval = stats.mannwhitneyu(ctrl, data[i], alternative="two-sided")
    bracket(ax, 0, i, y_top + (i - 1) * (bracket_h + 0.12), bracket_h, pval)

# ── Axes styling ────────────────────────────────────────────────────────────
ax.set_xticks(positions)
ax.set_xticklabels(LABELS, fontsize=9)
ax.set_ylabel(f"Relative cell viability", fontsize=9)
ax.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax.set_xlim(-0.6, len(ORDER) - 0.4)

# y-axis: data-range with headroom for brackets
data_min = min(v.min() for v in data)
data_max = max(v.max() for v in data)
span = data_max - data_min
ax.set_ylim(data_min - 0.05 * span,
            y_top + len(ORDER) * (bracket_h + 0.12) + 0.15)

ax.spines["left"].set_bounds(
    np.floor(data_min * 10) / 10,
    np.ceil(data_max * 10) / 10
)

fig.tight_layout()

# ── Export ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved: figure.pdf, figure.png, figure.svg")
