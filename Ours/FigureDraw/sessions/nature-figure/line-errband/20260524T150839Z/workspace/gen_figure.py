import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data.json") as f:
    d = json.load(f)

steps = np.array(d["steps"])
methods = d["methods"]
curves = d["curves"]

# Nature-style palette
colors = {
    "Baseline":  "#555555",
    "Method-A":  "#0072B2",
    "OursModel": "#D55E00",
}
labels = {
    "Baseline":  "Baseline",
    "Method-A":  "Method-A",
    "OursModel": "Ours",
}

fig, ax = plt.subplots(figsize=(4.5, 3.2))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci   = np.array(curves[method]["ci_half"])
    c = colors[method]
    lw = 2.0 if method == "OursModel" else 1.4
    ax.plot(steps, mean, color=c, linewidth=lw, label=labels[method], zorder=3)
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.18, linewidth=0)

# Highlight final-step gap between OursModel and next-best (Method-A)
final_step = steps[-1]
ours_final = curves["OursModel"]["mean"][-1]
methodA_final = curves["Method-A"]["mean"][-1]

ax.annotate(
    "",
    xy=(final_step, ours_final),
    xytext=(final_step, methodA_final),
    arrowprops=dict(arrowstyle="<->", color="#D55E00", lw=1.4),
    zorder=4,
)
gap = methodA_final - ours_final
ax.text(
    final_step + 0.8, (ours_final + methodA_final) / 2,
    f"$\\Delta={gap:.2f}$",
    va="center", ha="left", fontsize=7, color="#D55E00",
)

ax.set_yscale("log")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:g}"))
ax.set_xlabel(d["x_label"].title(), fontsize=9)
ax.set_ylabel(d["y_label"].title(), fontsize=9)
ax.tick_params(labelsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(fontsize=8, frameon=False, loc="upper right")
ax.set_xlim(steps[0], steps[-1])

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
