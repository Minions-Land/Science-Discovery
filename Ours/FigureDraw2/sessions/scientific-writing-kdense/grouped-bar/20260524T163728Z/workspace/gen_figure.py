import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Embed editable text in PDF/SVG
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 7

with open("data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]
methods = data["methods"]
values = data["values"]
winner = data["winner_overall"]

# Palette: colorblind-friendly (Wong 2011)
colors = {
    "Baseline":  "#999999",
    "Method-A":  "#56B4E9",
    "Method-B":  "#E69F00",
    "OursModel": "#009E73",
}
hatches = {
    "Baseline":  "",
    "Method-A":  "///",
    "Method-B":  "...",
    "OursModel": "xxx",
}

n_benchmarks = len(benchmarks)
n_methods = len(methods)
bar_width = 0.18
group_gap = 0.08
group_width = n_methods * bar_width + group_gap
x = np.arange(n_benchmarks) * group_width

fig, ax = plt.subplots(figsize=(3.5, 2.4))  # single-column width ~3.5 in

for i, method in enumerate(methods):
    means = [values[method][b]["mean"] for b in benchmarks]
    stds  = [values[method][b]["std"]  for b in benchmarks]
    offset = (i - (n_methods - 1) / 2) * bar_width
    bars = ax.bar(
        x + offset, means, bar_width,
        yerr=stds, capsize=2,
        color=colors[method],
        hatch=hatches[method],
        edgecolor="white" if method != winner else "black",
        linewidth=0.6 if method != winner else 1.0,
        error_kw=dict(elinewidth=0.8, ecolor="black", capthick=0.8),
        label=method,
        zorder=3,
    )
    # Bold outline for winner
    if method == winner:
        for bar in bars:
            bar.set_edgecolor("#222222")
            bar.set_linewidth(1.2)

# Axis formatting
all_means = [values[m][b]["mean"] for m in methods for b in benchmarks]
all_stds  = [values[m][b]["std"]  for m in methods for b in benchmarks]
y_min = min(v - s for v, s in zip(all_means, all_stds))
y_max = max(v + s for v, s in zip(all_means, all_stds))
pad = (y_max - y_min) * 0.08
ax.set_ylim(max(0, y_min - pad - 4), y_max + pad + 2)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel("Accuracy (%)", fontsize=7)
ax.yaxis.set_tick_params(labelsize=6)
ax.xaxis.set_tick_params(labelsize=6)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linewidth=0.4, linestyle="--", alpha=0.5, zorder=0)

# Legend — winner starred
legend_labels = [f"{m} ★" if m == winner else m for m in methods]
handles = [
    mpatches.Patch(
        facecolor=colors[m],
        hatch=hatches[m],
        edgecolor="#222222" if m == winner else "white",
        linewidth=1.0 if m == winner else 0.5,
        label=legend_labels[i],
    )
    for i, m in enumerate(methods)
]
ax.legend(
    handles=handles,
    fontsize=6,
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
