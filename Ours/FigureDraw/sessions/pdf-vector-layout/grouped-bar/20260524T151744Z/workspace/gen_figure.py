import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.size"] = 8

with open("data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]
methods = data["methods"]
values = data["values"]

n_benchmarks = len(benchmarks)
n_methods = len(methods)

# Palette: colorblind-friendly + hatches for B&W
colors = ["#999999", "#4477AA", "#EE6677", "#228833"]
hatches = ["", "//", "xx", ".."]
labels = methods  # Baseline, Method-A, Method-B, OursModel

bar_width = 0.18
group_gap = 0.08
group_width = n_methods * bar_width + group_gap
x_centers = np.arange(n_benchmarks) * group_width

fig, ax = plt.subplots(figsize=(3.5, 2.6))

for i, method in enumerate(methods):
    means = [values[method][b]["mean"] for b in benchmarks]
    stds  = [values[method][b]["std"]  for b in benchmarks]
    offsets = x_centers + (i - (n_methods - 1) / 2) * bar_width
    bars = ax.bar(
        offsets, means,
        width=bar_width * 0.92,
        color=colors[i],
        hatch=hatches[i],
        edgecolor="white",
        linewidth=0.4,
        label=labels[i],
        zorder=3,
    )
    ax.errorbar(
        offsets, means, yerr=stds,
        fmt="none",
        ecolor="black",
        elinewidth=0.8,
        capsize=2.0,
        capthick=0.8,
        zorder=4,
    )
    # Bold outline on OursModel bars
    if method == "OursModel":
        for bar in bars:
            bar.set_edgecolor("#228833")
            bar.set_linewidth(1.2)

# y-axis: don't start at 0 since min ~31
all_means = [values[m][b]["mean"] for m in methods for b in benchmarks]
all_stds  = [values[m][b]["std"]  for m in methods for b in benchmarks]
y_min = min(v - s for v, s in zip(all_means, all_stds))
y_max = max(v + s for v, s in zip(all_means, all_stds))
pad = (y_max - y_min) * 0.08
ax.set_ylim(max(0, y_min - pad - 2), y_max + pad + 2)

ax.set_xticks(x_centers)
ax.set_xticklabels(benchmarks, fontsize=7.5)
ax.set_ylabel("Accuracy (%)", fontsize=8)
ax.yaxis.grid(True, linestyle="--", linewidth=0.4, alpha=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend_handles = [
    Patch(facecolor=colors[i], hatch=hatches[i], edgecolor="#555555",
          linewidth=0.5, label=labels[i])
    for i in range(n_methods)
]
ax.legend(
    handles=legend_handles,
    fontsize=6.5,
    frameon=False,
    ncol=2,
    loc="upper left",
    handlelength=1.4,
    handleheight=0.9,
    columnspacing=0.8,
    labelspacing=0.3,
)

fig.tight_layout(pad=0.4)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
