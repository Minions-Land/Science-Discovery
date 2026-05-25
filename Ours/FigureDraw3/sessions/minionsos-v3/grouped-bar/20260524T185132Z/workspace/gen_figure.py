"""
gen_figure.py — Grouped bar chart: 4 methods × 5 benchmarks
Source data: data.json (same directory)
"""

import json
import pathlib
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "xtick.major.size": 0,
    "ytick.major.size": 2.5,
    "ytick.major.width": 0.6,
})

# ── Load data ─────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]   # 5 items
methods    = data["methods"]       # 4 items: Baseline, Method-A, Method-B, OursModel
values     = data["values"]
n_seeds    = data["n_seeds"]
winner     = data["winner_overall"]

# ── Palette — cool-family pastels with one warm accent for OursModel ──────────
# 4 hues from the same family (cool-warm pastel), distinguishable per P1-corrected rule.
# OursModel gets the deepest accent (it wins).
PALETTE = {
    "Baseline":  "#b0b8c8",   # cool grey-blue  (~20% sat)
    "Method-A":  "#7bafd4",   # medium blue     (~55% sat)
    "Method-B":  "#5c9ec4",   # deeper blue-teal (~65% sat)
    "OursModel": "#1a6fa8",   # strong signal blue (~80% sat, the winner)
}

HATCH = {
    "Baseline":  "///",
    "Method-A":  "...",
    "Method-B":  "xxx",
    "OursModel": "",
}

EDGE = {
    "Baseline":  "#8898b0",
    "Method-A":  "#5888b8",
    "Method-B":  "#3a7898",
    "OursModel": "#0d4f78",
}

# ── Layout ────────────────────────────────────────────────────────────────────
n_benchmarks = len(benchmarks)
n_methods    = len(methods)
bar_width    = 0.18
group_gap    = 0.25   # extra gap between benchmark groups (fraction of bar width)
x_positions  = np.arange(n_benchmarks)

fig, ax = plt.subplots(figsize=(7.2, 4.2))

# ── Draw bars ─────────────────────────────────────────────────────────────────
offsets = np.linspace(
    -(n_methods - 1) / 2 * (bar_width + 0.01),
     (n_methods - 1) / 2 * (bar_width + 0.01),
    n_methods,
)

bar_handles = []
for i, method in enumerate(methods):
    means = np.array([values[method][b]["mean"] for b in benchmarks])
    stds  = np.array([values[method][b]["std"]  for b in benchmarks])
    xpos  = x_positions + offsets[i]

    bars = ax.bar(
        xpos,
        means,
        width=bar_width,
        color=PALETTE[method],
        edgecolor=EDGE[method],
        linewidth=0.6,
        hatch=HATCH[method],
        hatch_linewidth=0.4,
        zorder=3,
        label=method,
    )
    ax.errorbar(
        xpos,
        means,
        yerr=stds,
        fmt="none",
        ecolor="#444444",
        elinewidth=0.8,
        capsize=2.2,
        capthick=0.7,
        zorder=4,
    )
    bar_handles.append(bars)

# ── Y-axis range tuned to data (not 0-100) ────────────────────────────────────
all_means = np.array([values[m][b]["mean"] for m in methods for b in benchmarks])
all_stds  = np.array([values[m][b]["std"]  for m in methods for b in benchmarks])
data_min  = (all_means - all_stds).min()
data_max  = (all_means + all_stds).max()
span      = data_max - data_min
ax.set_ylim(data_min - 0.10 * span, data_max + 0.18 * span)

# ── Axes labels & ticks ───────────────────────────────────────────────────────
ax.set_xticks(x_positions)
ax.set_xticklabels(benchmarks, fontsize=8.5)
ax.set_ylabel("Accuracy (%)", fontsize=9)
ax.tick_params(axis="y", direction="out", labelsize=8)
ax.tick_params(axis="x", bottom=False)

# ── Horizontal grid lines (subtle) ────────────────────────────────────────────
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.5, zorder=0)
ax.set_axisbelow(True)

# ── Legend — inside axes, top-right, away from the bars ──────────────────────
# Ablation grouped-bars: legend inside, no frame (ML-paper idiom)
legend_patches = [
    mpatches.Patch(
        facecolor=PALETTE[m],
        edgecolor=EDGE[m],
        linewidth=0.6,
        hatch=HATCH[m],
        label="OursModel (*)" if m == winner else m,
    )
    for m in methods
]
ax.legend(
    handles=legend_patches,
    fontsize=8.5,
    loc="upper left",
    ncol=2,
    handlelength=1.4,
    handletextpad=0.5,
    columnspacing=1.0,
    borderpad=0.6,
)

# ── Spine cleanup ─────────────────────────────────────────────────────────────
ax.spines["left"].set_linewidth(0.8)
ax.spines["bottom"].set_linewidth(0.8)

fig.tight_layout(pad=0.8)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig(cwd / "figure.pdf", bbox_inches="tight")
fig.savefig(cwd / "figure.png", dpi=300, bbox_inches="tight")
fig.savefig(cwd / "figure.svg", bbox_inches="tight")

print("Saved: figure.pdf, figure.png, figure.svg")
