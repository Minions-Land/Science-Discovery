import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.size"] = 7

with open("data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]
methods = data["methods"]
values = data["values"]

n_benchmarks = len(benchmarks)
n_methods = len(methods)

# Colors: colorblind-friendly palette
colors = ["#999999", "#56B4E9", "#E69F00", "#D55E00"]
# Hatches for B&W readers
hatches = ["", "///", "...", "xxx"]

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# y-range: all values are above 30; min is ~31.5, max ~84.2
y_min = max(0, np.floor((means - stds).min() / 5) * 5 - 5)
y_max = np.ceil((means + stds).max() / 5) * 5 + 2

bar_width = 0.18
group_gap = 0.08
group_width = n_methods * bar_width + group_gap
x_centers = np.arange(n_benchmarks) * (group_width + 0.15)

fig, ax = plt.subplots(figsize=(3.5, 2.6))

for i, (method, color, hatch) in enumerate(zip(methods, colors, hatches)):
    offsets = x_centers + (i - (n_methods - 1) / 2) * bar_width
    is_ours = method == "OursModel"
    edgecolor = "#222222" if is_ours else "#555555"
    lw = 1.2 if is_ours else 0.6
    ax.bar(
        offsets,
        means[i],
        width=bar_width,
        yerr=stds[i],
        color=color,
        hatch=hatch,
        edgecolor=edgecolor,
        linewidth=lw,
        error_kw=dict(elinewidth=0.8, capsize=2.0, capthick=0.8, ecolor="#333333"),
        label=method,
        zorder=3,
    )

ax.set_xticks(x_centers)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=7)
ax.set_ylim(y_min, y_max)
ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax.tick_params(axis="both", which="major", labelsize=7)
ax.tick_params(axis="y", which="minor", length=2)
ax.grid(axis="y", linestyle="--", linewidth=0.4, alpha=0.6, zorder=0)
ax.set_axisbelow(True)

# Bold "OursModel" in legend to highlight winner
handles = []
for method, color, hatch in zip(methods, colors, hatches):
    patch = mpatches.Patch(
        facecolor=color, hatch=hatch,
        edgecolor="#222222" if method == "OursModel" else "#555555",
        linewidth=1.2 if method == "OursModel" else 0.6,
        label=r"$\mathbf{OursModel}$" if method == "OursModel" else method,
    )
    handles.append(patch)

ax.legend(
    handles=handles,
    fontsize=6,
    frameon=True,
    framealpha=0.9,
    edgecolor="#cccccc",
    loc="upper left",
    ncol=2,
    handlelength=1.4,
    handleheight=0.9,
    columnspacing=0.8,
    labelspacing=0.3,
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout(pad=0.4)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
