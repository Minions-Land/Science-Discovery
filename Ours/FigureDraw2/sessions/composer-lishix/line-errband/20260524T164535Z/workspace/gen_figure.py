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

COLORS = {
    "Baseline":  "#888888",
    "Method-A":  "#4477AA",
    "OursModel": "#EE6677",
}
LINESTYLES = {
    "Baseline":  "--",
    "Method-A":  "-.",
    "OursModel": "-",
}

fig, ax = plt.subplots(figsize=(6, 4))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci   = np.array(curves[method]["ci_half"])
    color = COLORS[method]
    ls    = LINESTYLES[method]
    ax.plot(steps, mean, color=color, linestyle=ls, linewidth=1.8,
            label=method, zorder=3)
    ax.fill_between(steps, mean - ci, mean + ci,
                    color=color, alpha=0.18, zorder=2)

# Highlight gap at final step
final_step = steps[-1]
vals = {m: curves[m]["mean"][-1] for m in methods}
ours_val    = vals["OursModel"]
best_other  = min(vals[m] for m in methods if m != "OursModel")

ax.annotate(
    "",
    xy=(final_step, ours_val),
    xytext=(final_step, best_other),
    arrowprops=dict(arrowstyle="<->", color="#EE6677", lw=1.5),
    zorder=5,
)
gap = best_other - ours_val
ax.text(
    final_step + 0.6, (ours_val + best_other) / 2,
    f"$\\Delta={gap:.3f}$",
    color="#EE6677", fontsize=8, va="center",
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"], fontsize=11)
ax.set_ylabel(data["y_label"], fontsize=11)
ax.set_xlim(steps[0], steps[-1])
ax.legend(fontsize=9, framealpha=0.9)
ax.grid(True, which="both", linestyle=":", linewidth=0.5, alpha=0.6)
ax.set_title("Validation Loss vs. Training Step", fontsize=12)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
