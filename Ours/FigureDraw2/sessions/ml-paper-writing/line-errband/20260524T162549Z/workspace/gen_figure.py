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
    "Baseline": "#888888",
    "Method-A": "#4477AA",
    "OursModel": "#EE6677",
}
linestyles = {
    "Baseline": "--",
    "Method-A": "-.",
    "OursModel": "-",
}
zorders = {"Baseline": 1, "Method-A": 2, "OursModel": 3}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    c = colors[method]
    ls = linestyles[method]
    z = zorders[method]
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.18, zorder=z)
    ax.plot(steps, mean, color=c, linestyle=ls, linewidth=1.8,
            label=method, zorder=z)

# Highlight gap at final step
final_step = steps[-1]
final_vals = {m: curves[m]["mean"][-1] for m in methods}
ours_final = final_vals["OursModel"]
baseline_final = final_vals["Baseline"]
method_a_final = final_vals["Method-A"]

# Draw bracket between OursModel and Baseline at final step
x_ann = final_step + 1.2
ax.annotate(
    "",
    xy=(x_ann, ours_final),
    xytext=(x_ann, baseline_final),
    arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2),
)
gap = baseline_final - ours_final
ax.text(
    x_ann + 0.6, (ours_final + baseline_final) / 2,
    f"$\\Delta={gap:.2f}$",
    va="center", ha="left", fontsize=7.5, color="#555555",
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"], fontsize=10)
ax.set_ylabel(data["y_label"], fontsize=10)
ax.set_xlim(steps[0], steps[-1] + 4)
ax.legend(fontsize=9, framealpha=0.9, loc="upper right")
ax.grid(True, which="both", linestyle=":", linewidth=0.5, alpha=0.6)
ax.tick_params(labelsize=8)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
