import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

# Palette: colorblind-safe + distinct in greyscale
COLORS  = ["#999999", "#4dac26", "#0571b0", "#ca0020"]
HATCHES = ["",        "//",      "xx",      ".."]
LABELS  = methods  # last entry is the winner

bar_width = 0.18
group_gap = 0.08
x = np.arange(n_benchmarks) * (n_methods * bar_width + group_gap)

fig, ax = plt.subplots(figsize=(3.3, 2.6))  # single-column ~3.3 in

for i, (method, color, hatch) in enumerate(zip(methods, COLORS, HATCHES)):
    offset = i * bar_width
    lw = 1.2 if method == "OursModel" else 0.6
    ec = "#000000" if method == "OursModel" else "#444444"
    bars = ax.bar(
        x + offset,
        means[i],
        width=bar_width,
        color=color,
        edgecolor=ec,
        linewidth=lw,
        hatch=hatch,
        label=method,
        zorder=3,
    )
    ax.errorbar(
        x + offset,
        means[i],
        yerr=stds[i],
        fmt="none",
        ecolor="#222222",
        elinewidth=0.8,
        capsize=2.0,
        capthick=0.8,
        zorder=4,
    )

# Highlight winner with a subtle star annotation per benchmark
winner_idx = methods.index("OursModel")
for j in range(n_benchmarks):
    yval = means[winner_idx, j] + stds[winner_idx, j] + 0.8
    ax.text(
        x[j] + winner_idx * bar_width,
        yval,
        "★",
        ha="center", va="bottom",
        fontsize=6, color="#ca0020",
        zorder=5,
    )

# Axis formatting
tick_centers = x + (n_methods - 1) * bar_width / 2
ax.set_xticks(tick_centers)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=7)

all_means = means.flatten()
all_stds  = stds.flatten()
y_min = max(0, (all_means - all_stds).min() - 4)
y_max = (all_means + all_stds).max() + 5
ax.set_ylim(y_min, y_max)

ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
ax.tick_params(axis="y", labelsize=7)
ax.grid(axis="y", which="major", linestyle="--", linewidth=0.5, alpha=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
legend_patches = [
    mpatches.Patch(facecolor=c, edgecolor="#444444", hatch=h, label=m, linewidth=0.6)
    for m, c, h in zip(methods, COLORS, HATCHES)
]
ax.legend(
    handles=legend_patches,
    fontsize=6,
    ncol=2,
    loc="lower right",
    framealpha=0.85,
    edgecolor="#cccccc",
    handlelength=1.4,
    handleheight=0.9,
    borderpad=0.5,
)

fig.tight_layout(pad=0.5)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
