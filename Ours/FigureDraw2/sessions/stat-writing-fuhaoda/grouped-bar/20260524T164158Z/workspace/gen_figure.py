import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

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

# Palette: colorblind-friendly + hatches for B&W readers
colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
hatches = ["", "//", "..", "xx"]
labels = methods

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

bar_width = 0.18
group_gap = 0.08
x = np.arange(n_benchmarks)

fig, ax = plt.subplots(figsize=(3.5, 2.6))

offsets = np.linspace(
    -(n_methods - 1) / 2 * (bar_width + group_gap / n_methods),
     (n_methods - 1) / 2 * (bar_width + group_gap / n_methods),
    n_methods,
)

for i, (method, color, hatch, offset) in enumerate(zip(methods, colors, hatches, offsets)):
    xs = x + offset
    highlight = method == data["winner_overall"]
    edge_color = "black" if highlight else "0.3"
    lw = 1.2 if highlight else 0.6
    ax.bar(
        xs, means[i], width=bar_width,
        color=color, hatch=hatch,
        edgecolor=edge_color, linewidth=lw,
        yerr=stds[i], error_kw=dict(elinewidth=0.8, capsize=2.0, capthick=0.8, ecolor="0.2"),
        label=method + (" ★" if highlight else ""),
        zorder=3,
    )

# y-range: all values are above ~31, so don't start at 0
all_means = means.flatten()
all_stds = stds.flatten()
ymin = max(0, np.min(all_means - all_stds) - 5)
ymax = np.max(all_means + all_stds) + 5
ax.set_ylim(ymin, ymax)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7.5)
ax.set_ylabel("Accuracy (%)", fontsize=8)
ax.yaxis.grid(True, linestyle="--", linewidth=0.4, alpha=0.7, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(
    fontsize=6.5, ncol=2, frameon=True,
    framealpha=0.9, edgecolor="0.7",
    loc="upper left", handlelength=1.4,
    borderpad=0.5, labelspacing=0.3,
)

fig.tight_layout(pad=0.4)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
