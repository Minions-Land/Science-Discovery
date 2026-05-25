import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Embed editable text
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["svg.fonttype"] = "none"

with open("data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]
methods = data["methods"]
values = data["values"]

n_benchmarks = len(benchmarks)
n_methods = len(methods)

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# Palette distinguishable in B&W and color; winner gets a star accent
palette = ["#9e9e9e", "#4e9cd9", "#f4a835", "#d94e4e"]  # grey, blue, amber, red
hatches = ["", "//", "..", "xx"]  # distinct for B&W
winner_idx = methods.index(data["winner_overall"])

bar_width = 0.18
group_gap = 0.08
x = np.arange(n_benchmarks)

fig, ax = plt.subplots(figsize=(3.5, 2.6))

for i, (method, color, hatch) in enumerate(zip(methods, palette, hatches)):
    offset = (i - (n_methods - 1) / 2) * bar_width
    bars = ax.bar(
        x + offset, means[i], bar_width,
        yerr=stds[i], capsize=2.5,
        color=color, hatch=hatch,
        edgecolor="white" if hatch == "" else color,
        linewidth=0.5,
        error_kw=dict(elinewidth=0.8, ecolor="#333333", capthick=0.8),
        label=method,
        zorder=3,
    )
    # Outline winner bars to make them pop
    if i == winner_idx:
        for bar in bars:
            bar.set_edgecolor("#222222")
            bar.set_linewidth(1.2)

# Y range: data spans ~31-84; floor at 25 avoids wasted space
all_means = means.flatten()
y_min = max(0, np.floor((all_means.min() - 8) / 5) * 5)
y_max = np.ceil((all_means.max() + stds.max() + 4) / 5) * 5
ax.set_ylim(y_min, y_max)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=7)
ax.tick_params(axis="y", labelsize=7)
ax.tick_params(axis="x", length=0)

ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
ax.grid(axis="y", which="major", linestyle="--", linewidth=0.4, alpha=0.6, zorder=0)
ax.grid(axis="y", which="minor", linestyle=":", linewidth=0.3, alpha=0.4, zorder=0)
ax.set_axisbelow(True)

# Spine cleanup
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.6)
ax.spines["bottom"].set_linewidth(0.6)

# Legend inside upper-left; winner label bolded
handles, labels = ax.get_legend_handles_bars() if hasattr(ax, "get_legend_handles_bars") else (None, None)
legend_patches = []
for i, (method, color, hatch) in enumerate(zip(methods, palette, hatches)):
    patch = mpatches.Patch(
        facecolor=color, hatch=hatch,
        edgecolor="#222222" if i == winner_idx else ("white" if hatch == "" else color),
        linewidth=1.2 if i == winner_idx else 0.5,
        label=(r"$\mathbf{" + method.replace("-", r"\text{-}") + r"}$" if i == winner_idx else method),
    )
    legend_patches.append(patch)

leg = ax.legend(
    handles=legend_patches,
    fontsize=6,
    loc="upper left",
    frameon=True,
    framealpha=0.9,
    edgecolor="#cccccc",
    handlelength=1.6,
    handleheight=0.9,
    borderpad=0.5,
    labelspacing=0.35,
    ncol=2,
)

fig.tight_layout(pad=0.4)

fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
