import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

benchmarks = d["benchmarks"]
methods    = d["methods"]
values     = d["values"]

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# ── style ──────────────────────────────────────────────────────────────────
matplotlib.rcParams.update({
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
    "font.family":  "sans-serif",
    "font.size":    7,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
})

# Nature single-column: 89 mm wide
FIG_W = 89 / 25.4
FIG_H = FIG_W * 0.72

# Colour-blind-safe palette (Wong 2011) + hatch for B&W readers
COLORS  = ["#999999", "#56B4E9", "#E69F00", "#D55E00"]
HATCHES = ["",        "///",     "...",     "xxx"]
LABELS  = methods   # ["Baseline", "Method-A", "Method-B", "OursModel"]

n_bench  = len(benchmarks)
n_method = len(methods)
group_w  = 0.72          # total width occupied by one benchmark group
bar_w    = group_w / n_method
x_centers = np.arange(n_bench)

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))

for i, (label, color, hatch) in enumerate(zip(LABELS, COLORS, HATCHES)):
    offsets = x_centers - group_w / 2 + bar_w * (i + 0.5)
    bars = ax.bar(
        offsets, means[i], bar_w * 0.92,
        yerr=stds[i],
        color=color, hatch=hatch,
        edgecolor="white" if hatch == "" else color,
        linewidth=0.4,
        error_kw=dict(elinewidth=0.7, capsize=1.8, capthick=0.7, ecolor="#333333"),
        label=label,
        zorder=3,
    )
    # bold outline for OursModel
    if label == "OursModel":
        for bar in bars:
            bar.set_edgecolor("#D55E00")
            bar.set_linewidth(1.0)

# ── axes formatting ────────────────────────────────────────────────────────
ymin = max(0, np.floor((means - stds).min() / 5) * 5 - 5)
ymax = np.ceil((means + stds).max() / 5) * 5 + 3
ax.set_ylim(ymin, ymax)

ax.set_xticks(x_centers)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=7)
ax.yaxis.set_tick_params(labelsize=6.5)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linewidth=0.4, linestyle="--", color="#cccccc", zorder=0)
ax.set_axisbelow(True)

# ── legend ─────────────────────────────────────────────────────────────────
legend_patches = [
    mpatches.Patch(facecolor=c, hatch=h, edgecolor="#555555", linewidth=0.4, label=l)
    for c, h, l in zip(COLORS, HATCHES, LABELS)
]
ax.legend(
    handles=legend_patches,
    fontsize=6,
    frameon=False,
    ncol=2,
    loc="upper left",
    handlelength=1.6,
    handleheight=0.9,
    borderpad=0,
    labelspacing=0.3,
    columnspacing=0.8,
)

fig.tight_layout(pad=0.4)

# ── save ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
