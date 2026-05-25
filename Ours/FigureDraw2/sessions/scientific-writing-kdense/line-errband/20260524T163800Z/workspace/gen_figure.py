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
    "Baseline": "#4878CF",
    "Method-A": "#6ACC65",
    "OursModel": "#D65F5F",
}
labels = {
    "Baseline": "Baseline",
    "Method-A": "Method-A",
    "OursModel": "Ours",
}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    c = colors[method]
    lw = 2.2 if method == "OursModel" else 1.6
    ax.plot(steps, mean, color=c, linewidth=lw, label=labels[method], zorder=3)
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.18, zorder=2)

# Highlight gap at final step
final = steps[-1]
ours_final = curves["OursModel"]["mean"][-1]
baseline_final = curves["Baseline"]["mean"][-1]
methoda_final = curves["Method-A"]["mean"][-1]

ax.annotate(
    "",
    xy=(final + 0.4, ours_final),
    xytext=(final + 0.4, methoda_final),
    arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2),
    zorder=5,
)
gap = methoda_final - ours_final
ax.text(
    final + 1.2,
    (ours_final + methoda_final) / 2,
    f"$\\Delta={gap:.3f}$",
    va="center",
    ha="left",
    fontsize=7.5,
    color="#555555",
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"].capitalize(), fontsize=10)
ax.set_ylabel(data["y_label"].capitalize(), fontsize=10)
ax.set_xlim(steps[0], steps[-1] + 3)
ax.tick_params(axis="both", labelsize=8.5)
ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.yaxis.get_major_formatter().set_scientific(False)

legend = ax.legend(fontsize=8.5, framealpha=0.9, loc="upper right")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
