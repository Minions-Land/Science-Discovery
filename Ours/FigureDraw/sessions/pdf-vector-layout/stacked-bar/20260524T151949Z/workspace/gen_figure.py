import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

with open("data.json") as f:
    data = json.load(f)

classes = data["classes"]
conditions = data["conditions"]
proportions = data["proportions"]

# Okabe-Ito colorblind-safe palette (4 colors)
colors = ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"]

matplotlib.rcParams.update({
    "font.family": "Arial",
    "font.size": 7,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})

fig, ax = plt.subplots(figsize=(3.46, 2.6))  # ~88 mm wide (single column)

x = np.arange(len(conditions))
bar_width = 0.6
bottoms = np.zeros(len(conditions))

bars = []
for i, cls in enumerate(classes):
    vals = [proportions[c][i] for c in conditions]
    b = ax.bar(x, vals, bar_width, bottom=bottoms, color=colors[i], label=cls,
               linewidth=0)
    bars.append(b)
    bottoms += np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=7)
ax.set_ylabel("Proportion", fontsize=7)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.5)
ax.spines["bottom"].set_linewidth(0.5)

legend = ax.legend(
    fontsize=6,
    frameon=False,
    loc="upper right",
    ncol=1,
    handlelength=1.0,
    handleheight=0.8,
    handletextpad=0.4,
    borderpad=0,
    labelspacing=0.3,
)

fig.tight_layout(pad=0.4)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", dpi=300, bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
