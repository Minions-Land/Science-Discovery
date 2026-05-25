import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

benchmarks = d["benchmarks"]
methods    = d["methods"]
values     = d["values"]

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# ── style ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype":  42,
    "svg.fonttype": "none",
    "font.family":  "sans-serif",
    "font.size":    8,
    "axes.linewidth": 0.8,
})

COLORS  = ["#9ecae1", "#4292c6", "#08519c", "#e6550d"]   # blue ramp + orange for ours
HATCHES = ["",        "///",     "xxx",     "..."]        # B&W distinguishable

n_bench  = len(benchmarks)
n_method = len(methods)
width    = 0.18
x        = np.arange(n_bench)
offsets  = np.linspace(-(n_method - 1) / 2, (n_method - 1) / 2, n_method) * width

fig, ax = plt.subplots(figsize=(3.5, 2.6))

for i, (method, color, hatch) in enumerate(zip(methods, COLORS, HATCHES)):
    bars = ax.bar(
        x + offsets[i], means[i], width,
        yerr=stds[i],
        color=color, hatch=hatch,
        edgecolor="white" if hatch == "" else "#333333",
        linewidth=0.5,
        error_kw=dict(elinewidth=0.8, capsize=2, ecolor="#333333"),
        label=method,
        zorder=3,
    )
    # bold outline on OursModel bars
    if method == "OursModel":
        for bar in bars:
            bar.set_edgecolor("#b03a00")
            bar.set_linewidth(1.2)

# ── axes ───────────────────────────────────────────────────────────────────
ymin = max(0, np.floor((means - stds).min() / 5) * 5 - 5)
ymax = np.ceil((means + stds).max() / 5) * 5 + 2
ax.set_ylim(ymin, ymax)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=8)
ax.yaxis.set_tick_params(labelsize=7)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linewidth=0.4, linestyle="--", color="#cccccc", zorder=0)
ax.set_axisbelow(True)

# ── legend ─────────────────────────────────────────────────────────────────
legend_handles = [
    Patch(facecolor=COLORS[i], hatch=HATCHES[i],
          edgecolor="#333333" if HATCHES[i] else "white",
          linewidth=0.5, label=methods[i])
    for i in range(n_method)
]
ax.legend(
    handles=legend_handles,
    fontsize=6.5, frameon=False,
    ncol=2, loc="upper left",
    handlelength=1.4, handleheight=0.9,
    columnspacing=0.8, labelspacing=0.3,
)

fig.tight_layout(pad=0.4)

# ── save ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg",           bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
