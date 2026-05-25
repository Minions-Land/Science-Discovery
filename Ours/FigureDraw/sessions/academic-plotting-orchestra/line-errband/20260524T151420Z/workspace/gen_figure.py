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

colors = {
    "Baseline": "#888888",
    "Method-A": "#2196F3",
    "OursModel": "#E53935",
}
linestyles = {
    "Baseline": "--",
    "Method-A": "-.",
    "OursModel": "-",
}
linewidths = {
    "Baseline": 1.4,
    "Method-A": 1.4,
    "OursModel": 2.0,
}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    color = colors[method]
    label = method if method != "OursModel" else "OursModel (ours)"
    ax.plot(steps, mean, color=color, linestyle=linestyles[method],
            linewidth=linewidths[method], label=label, zorder=3)
    ax.fill_between(steps, mean - ci, mean + ci, color=color, alpha=0.15, zorder=2)

# Highlight gap at final step (step 49)
final_step = steps[-1]
final_vals = {m: curves[m]["mean"][-1] for m in methods}
ours_val = final_vals["OursModel"]

# Draw bracket between OursModel and Method-A at final step
method_a_val = final_vals["Method-A"]
baseline_val = final_vals["Baseline"]

ax.annotate(
    "",
    xy=(final_step + 0.5, ours_val),
    xytext=(final_step + 0.5, method_a_val),
    arrowprops=dict(arrowstyle="<->", color=colors["OursModel"], lw=1.5),
    zorder=5,
)
gap = method_a_val - ours_val
ax.text(
    final_step + 1.2, (ours_val + method_a_val) / 2,
    f"$\\Delta={gap:.3f}$",
    va="center", ha="left", fontsize=7.5, color=colors["OursModel"],
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"].capitalize(), fontsize=10)
ax.set_ylabel(data["y_label"].capitalize(), fontsize=10)
ax.set_xlim(-1, 54)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda y, _: f"{y:g}"
))

ax.legend(framealpha=0.9, fontsize=8.5, loc="upper right")
ax.grid(True, which="both", linestyle=":", linewidth=0.5, alpha=0.6)
ax.tick_params(labelsize=8)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
