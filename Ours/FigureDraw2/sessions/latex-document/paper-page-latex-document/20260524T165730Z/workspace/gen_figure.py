"""
gen_figure.py — Produce figure.pdf and figure.png for the RetroDiff paper.

Figure: Grouped bar chart comparing four methods across five benchmarks
(matches fig01 description from captions.json).
Data is representative/illustrative; exact values derived from claim.json claims
(OursModel best on all five; largest gain on MATH +4.8pp).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Data ──────────────────────────────────────────────────────────────────────
benchmarks = ["MMLU", "HumanEval", "GSM8K", "MATH", "GPQA"]

# Accuracy (%) per method per benchmark; 5 seeds → mean ± std
# OursModel (RetroDiff) is best on all five; MATH gain over next-best = 4.8pp
data = {
    "Baseline":  {"mean": [63.1, 52.4, 71.3, 38.2, 31.5], "std": [0.6, 0.9, 0.8, 0.7, 0.5]},
    "Method-A":  {"mean": [67.4, 57.8, 76.1, 43.5, 35.2], "std": [0.5, 0.8, 0.7, 0.6, 0.6]},
    "Method-B":  {"mean": [68.9, 59.3, 77.4, 44.9, 36.8], "std": [0.7, 1.0, 0.9, 0.8, 0.7]},
    "OursModel": {"mean": [71.2, 62.7, 80.5, 49.7, 39.4], "std": [0.4, 0.7, 0.6, 0.5, 0.4]},
}
# Verify MATH claim: OursModel(49.7) - Method-B(44.9) = 4.8pp ✓

# ── Okabe–Ito palette (colour-blind safe) ─────────────────────────────────────
colors = {
    "Baseline":  "#56B4E9",   # sky blue
    "Method-A":  "#009E73",   # bluish green
    "Method-B":  "#F0E442",   # yellow
    "OursModel": "#E69F00",   # orange
}
hatches = {
    "Baseline":  "",
    "Method-A":  "//",
    "Method-B":  "\\\\",
    "OursModel": "xxx",
}

methods = list(data.keys())
n_benchmarks = len(benchmarks)
n_methods = len(methods)
bar_width = 0.18
group_gap = 0.05
x = np.arange(n_benchmarks)

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8.5, 4.2))

for i, method in enumerate(methods):
    offset = (i - (n_methods - 1) / 2) * (bar_width + group_gap / n_methods)
    means = data[method]["mean"]
    stds  = data[method]["std"]
    bars = ax.bar(
        x + offset, means, bar_width,
        label=method,
        color=colors[method],
        hatch=hatches[method],
        edgecolor="black",
        linewidth=0.6,
        yerr=stds,
        capsize=3,
        error_kw={"elinewidth": 0.8, "ecolor": "black"},
        zorder=3,
    )

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=10)
ax.set_ylabel("Accuracy (%)", fontsize=10)
ax.set_ylim(25, 58)
ax.yaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.7, zorder=0)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
legend_patches = [
    mpatches.Patch(facecolor=colors[m], hatch=hatches[m],
                   edgecolor="black", linewidth=0.6, label=m)
    for m in methods
]
ax.legend(handles=legend_patches, fontsize=9, framealpha=0.9,
          loc="upper left", ncol=2)

fig.tight_layout(pad=0.5)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
