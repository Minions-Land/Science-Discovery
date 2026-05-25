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

colors = {"Baseline": "#4C72B0", "Method-A": "#DD8452", "OursModel": "#55A868"}
linestyles = {"Baseline": "--", "Method-A": "-.", "OursModel": "-"}
zorders = {"Baseline": 1, "Method-A": 2, "OursModel": 3}

fig, ax = plt.subplots(figsize=(6, 4))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    c = colors[method]
    ls = linestyles[method]
    zo = zorders[method]
    lw = 2.2 if method == "OursModel" else 1.6
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.15, zorder=zo)
    ax.plot(steps, mean, color=c, linestyle=ls, linewidth=lw, label=method, zorder=zo)

# Highlight gap at final step (step 49)
final_step = steps[-1]
ours_final = curves["OursModel"]["mean"][-1]
baseline_final = curves["Baseline"]["mean"][-1]
methodA_final = curves["Method-A"]["mean"][-1]

# Draw a bracket showing the gap between OursModel and Method-A at step 49
x_ann = final_step + 0.8
ax.annotate(
    "",
    xy=(x_ann, ours_final),
    xytext=(x_ann, methodA_final),
    arrowprops=dict(arrowstyle="<->", color="#333333", lw=1.4),
)
gap = methodA_final - ours_final
ax.text(
    x_ann + 0.6,
    (ours_final + methodA_final) / 2,
    f"Δ={gap:.3f}",
    va="center",
    ha="left",
    fontsize=8,
    color="#333333",
)

ax.set_yscale("log")
ax.set_xlabel(data["x_label"].capitalize(), fontsize=11)
ax.set_ylabel(data["y_label"].capitalize(), fontsize=11)
ax.set_xlim(steps[0] - 0.5, steps[-1] + 5)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:g}"))
ax.legend(fontsize=9, framealpha=0.9)
ax.grid(True, which="major", linestyle=":", linewidth=0.6, alpha=0.7)
ax.set_title("Validation Loss over Training Steps", fontsize=12)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
