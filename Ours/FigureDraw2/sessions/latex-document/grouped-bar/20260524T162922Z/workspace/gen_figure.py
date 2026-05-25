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

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# Colorblind-friendly palette (Okabe-Ito subset)
colors = ["#999999", "#56B4E9", "#E69F00", "#D55E00"]
hatches = ["", "///", "...", "xxx"]
labels = methods

bar_width = 0.18
group_gap = 0.1
x = np.arange(n_benchmarks) * (n_methods * bar_width + group_gap)

fig, ax = plt.subplots(figsize=(3.5, 2.6))  # single-column width

for i, (method, color, hatch) in enumerate(zip(methods, colors, hatches)):
    offsets = x + i * bar_width - (n_methods - 1) * bar_width / 2
    bars = ax.bar(
        offsets,
        means[i],
        bar_width,
        yerr=stds[i],
        label=method,
        color=color,
        hatch=hatch,
        edgecolor="white" if hatch == "" else "black",
        linewidth=0.5,
        error_kw=dict(elinewidth=0.8, capsize=2, ecolor="black", capthick=0.8),
        zorder=3,
    )
    # Bold outline for OursModel
    if method == "OursModel":
        for bar in bars:
            bar.set_edgecolor("#D55E00")
            bar.set_linewidth(1.2)

# Y-axis: data spans ~31 to ~85; start just below min
ymin = max(0, np.min(means - stds) - 5)
ymax = np.max(means + stds) + 5
ax.set_ylim(ymin, ymax)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=8)
ax.yaxis.grid(True, linestyle="--", linewidth=0.4, alpha=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(
    fontsize=6.5,
    ncol=2,
    frameon=True,
    framealpha=0.9,
    edgecolor="#cccccc",
    loc="upper left",
    handlelength=1.4,
    handleheight=0.9,
)

fig.tight_layout(pad=0.4)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
