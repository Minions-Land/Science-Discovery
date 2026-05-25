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
    "Baseline": "#6c8ebf",
    "Method-A": "#d6a84a",
    "OursModel": "#5aaa72",
}
linestyles = {
    "Baseline": "--",
    "Method-A": "-.",
    "OursModel": "-",
}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    c = colors[method]
    ls = linestyles[method]
    lw = 2.2 if method == "OursModel" else 1.6
    ax.fill_between(steps, mean - ci, mean + ci, alpha=0.18, color=c)
    ax.plot(steps, mean, ls=ls, color=c, linewidth=lw,
            label="Ours" if method == "OursModel" else method)

# Highlight gap at final step between OursModel and the others
final_step = steps[-1]
ours_final = curves["OursModel"]["mean"][-1]
for method in ["Baseline", "Method-A"]:
    other_final = curves[method]["mean"][-1]
    ax.annotate(
        "",
        xy=(final_step + 0.4, ours_final),
        xytext=(final_step + 0.4, other_final),
        arrowprops=dict(arrowstyle="<->", color=colors[method],
                        lw=1.2, shrinkA=0, shrinkB=0),
    )

# Label the gap for the larger one (Baseline)
baseline_final = curves["Baseline"]["mean"][-1]
gap = baseline_final - ours_final
mid_y = (baseline_final + ours_final) / 2
ax.text(final_step + 1.0, mid_y, f"Δ={gap:.2f}", va="center",
        fontsize=7.5, color=colors["Baseline"])

ax.set_yscale("log")
ax.set_xlabel(data["x_label"], fontsize=10)
ax.set_ylabel(data["y_label"], fontsize=10)
ax.set_xlim(steps[0], steps[-1] + 3)
ax.legend(fontsize=9, framealpha=0.85, loc="upper right")
ax.tick_params(axis="both", which="major", labelsize=9)
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

fig.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
