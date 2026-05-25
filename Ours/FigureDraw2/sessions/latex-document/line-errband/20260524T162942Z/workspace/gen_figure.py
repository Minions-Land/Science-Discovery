import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data.json") as f:
    data = json.load(f)

steps = np.array(data["steps"])
methods = data["methods"]
curves = data["curves"]

COLORS = {
    "Baseline": "#4878CF",
    "Method-A": "#6ACC65",
    "OursModel": "#D65F5F",
}
LINESTYLES = {
    "Baseline": "--",
    "Method-A": "-.",
    "OursModel": "-",
}
LABELS = {
    "Baseline": "Baseline",
    "Method-A": "Method-A",
    "OursModel": "Ours",
}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    color = COLORS[method]
    ls = LINESTYLES[method]
    lw = 2.2 if method == "OursModel" else 1.6
    ax.plot(steps, mean, color=color, linestyle=ls, linewidth=lw,
            label=LABELS[method], zorder=3)
    ax.fill_between(steps, mean - ci, mean + ci, color=color, alpha=0.18, zorder=2)

# Highlight gap at final step
final = steps[-1]
vals = {m: curves[m]["mean"][-1] for m in methods}
ours_val = vals["OursModel"]
best_other = min(vals[m] for m in methods if m != "OursModel")

ax.annotate(
    "",
    xy=(final + 0.4, ours_val),
    xytext=(final + 0.4, best_other),
    arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2),
    zorder=5,
)
gap = best_other - ours_val
ax.text(
    final + 1.0, (ours_val + best_other) / 2,
    f"$\\Delta={gap:.3f}$",
    va="center", ha="left", fontsize=7.5, color="#333333",
)

ax.set_yscale("log")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda y, _: f"{y:g}"
))
ax.set_xlabel(data["x_label"].capitalize(), fontsize=10)
ax.set_ylabel(data["y_label"].capitalize(), fontsize=10)
ax.set_xlim(steps[0], steps[-1] + 4)
ax.legend(fontsize=9, framealpha=0.9, loc="upper right")
ax.grid(True, which="both", linestyle=":", linewidth=0.5, alpha=0.6)
ax.tick_params(axis="both", labelsize=8)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
