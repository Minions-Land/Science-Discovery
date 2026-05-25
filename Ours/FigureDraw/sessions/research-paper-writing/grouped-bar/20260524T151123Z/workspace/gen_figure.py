import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── reproducibility ──────────────────────────────────────────────────────────
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.size"] = 8

# ── data ─────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]
methods    = data["methods"]
values     = data["values"]

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# ── layout ───────────────────────────────────────────────────────────────────
n_benchmarks = len(benchmarks)
n_methods    = len(methods)
bar_w        = 0.18
group_gap    = 0.08          # extra gap between benchmark groups
x_centers    = np.arange(n_benchmarks) * (n_methods * bar_w + group_gap + 0.10)

# colourblind-friendly palette (Okabe–Ito subset)
colors  = ["#999999", "#56B4E9", "#E69F00", "#D55E00"]
hatches = ["",        "//",      "..",       "xx"]
winner_idx = methods.index(data["winner_overall"])

fig, ax = plt.subplots(figsize=(3.5, 2.6))  # single-column friendly

for i, (method, color, hatch) in enumerate(zip(methods, colors, hatches)):
    offsets = x_centers + (i - (n_methods - 1) / 2) * bar_w
    lw = 1.2 if i == winner_idx else 0.6
    ec = "#1a1a1a" if i == winner_idx else "#555555"
    bars = ax.bar(
        offsets, means[i],
        width=bar_w,
        color=color,
        edgecolor=ec,
        linewidth=lw,
        hatch=hatch,
        alpha=0.92,
        zorder=3,
        label=method,
    )
    ax.errorbar(
        offsets, means[i], yerr=stds[i],
        fmt="none",
        ecolor="#222222",
        elinewidth=0.8,
        capsize=2.0,
        capthick=0.8,
        zorder=4,
    )

# ── axes dressing ─────────────────────────────────────────────────────────────
all_vals = means - stds
y_min = max(0, np.floor(all_vals.min() / 5) * 5 - 5)   # no zero-waste if >60
y_max = np.ceil((means + stds).max() / 5) * 5 + 2

ax.set_ylim(y_min, y_max)
ax.set_xticks(x_centers)
ax.set_xticklabels(benchmarks, fontsize=7.5)
ax.set_ylabel("Accuracy (%)", fontsize=8)
ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)

# legend — place outside so bars aren't obscured
legend = ax.legend(
    loc="upper left",
    fontsize=6.5,
    framealpha=0.85,
    edgecolor="#cccccc",
    borderpad=0.5,
    labelspacing=0.3,
    handlelength=1.4,
    handleheight=0.9,
)
# bold the winner's legend entry
for text, method in zip(legend.get_texts(), methods):
    if method == data["winner_overall"]:
        text.set_fontweight("bold")

fig.tight_layout(pad=0.4)

# ── save ─────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
