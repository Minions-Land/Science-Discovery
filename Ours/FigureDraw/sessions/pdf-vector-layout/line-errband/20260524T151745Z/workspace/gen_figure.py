import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    data = json.load(f)

steps = np.array(data["steps"])
methods = data["methods"]
curves = data["curves"]

colors = {
    "Baseline":  "#6c757d",
    "Method-A":  "#2196F3",
    "OursModel": "#E53935",
}
labels = {
    "Baseline":  "Baseline",
    "Method-A":  "Method-A",
    "OursModel": "Ours",
}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci   = np.array(curves[method]["ci_half"])
    c = colors[method]
    lw = 2.2 if method == "OursModel" else 1.5
    zorder = 3 if method == "OursModel" else 2
    ax.fill_between(steps, mean - ci, mean + ci, alpha=0.18, color=c, linewidth=0)
    ax.plot(steps, mean, color=c, linewidth=lw, label=labels[method], zorder=zorder)

# Highlight gap at final step (step 49)
final_step = steps[-1]
vals = {m: curves[m]["mean"][-1] for m in methods}
ours_val = vals["OursModel"]
best_baseline = min(vals["Baseline"], vals["Method-A"])

ax.annotate(
    "",
    xy=(final_step + 0.5, ours_val),
    xytext=(final_step + 0.5, best_baseline),
    arrowprops=dict(arrowstyle="<->", color="#555", lw=1.2),
)
gap = best_baseline - ours_val
ax.text(
    final_step + 1.2, (ours_val + best_baseline) / 2,
    f"$\\Delta={gap:.3f}$",
    va="center", fontsize=7.5, color="#333",
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"].capitalize(), fontsize=10)
ax.set_ylabel(data["y_label"].capitalize(), fontsize=10)
ax.set_xlim(steps[0], steps[-1] + 5)
ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.tick_params(axis="both", labelsize=8.5)
ax.legend(fontsize=8.5, framealpha=0.85, edgecolor="#ccc", loc="upper right")
ax.set_title("Validation Loss over Training (95% CI, $n=5$)", fontsize=9.5, pad=6)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
