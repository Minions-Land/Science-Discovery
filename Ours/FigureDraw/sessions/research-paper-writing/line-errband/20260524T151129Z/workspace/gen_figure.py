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
    "Baseline":  "#4878CF",
    "Method-A":  "#6ACC65",
    "OursModel": "#D65F5F",
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
    c    = colors[method]
    lw   = 2.2 if method == "OursModel" else 1.6
    ax.plot(steps, mean, color=c, linewidth=lw, label=labels[method], zorder=3)
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.18, zorder=2)

# Highlight gap at final step
final = steps[-1]
vals = {m: curves[m]["mean"][-1] for m in methods}
y_ours   = vals["OursModel"]
y_best_other = min(vals["Baseline"], vals["Method-A"])

ax.annotate(
    "",
    xy=(final + 0.5, y_ours),
    xytext=(final + 0.5, y_best_other),
    arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2),
    zorder=5,
)
gap = y_best_other - y_ours
ax.text(
    final + 1.2, (y_ours + y_best_other) / 2,
    f"$\\Delta={gap:.2f}$",
    va="center", ha="left", fontsize=8, color="#555555",
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"], fontsize=10)
ax.set_ylabel(data["y_label"], fontsize=10)
ax.set_xlim(steps[0], steps[-1] + 3)
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.tick_params(axis="both", labelsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
