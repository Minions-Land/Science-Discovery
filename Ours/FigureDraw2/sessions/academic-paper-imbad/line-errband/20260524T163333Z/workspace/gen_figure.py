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

colors = {"Baseline": "#4878CF", "Method-A": "#6ACC65", "OursModel": "#D65F5F"}
labels = {"Baseline": "Baseline", "Method-A": "Method-A", "OursModel": "Ours"}

fig, ax = plt.subplots(figsize=(5.5, 3.8))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    c = colors[method]
    lw = 2.2 if method == "OursModel" else 1.5
    ax.plot(steps, mean, color=c, linewidth=lw, label=labels[method],
            zorder=3 if method == "OursModel" else 2)
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.15, linewidth=0)

# Highlight gap at final step
final_step = steps[-1]
ours_final = curves["OursModel"]["mean"][-1]
baseline_final = curves["Baseline"]["mean"][-1]
methoda_final = curves["Method-A"]["mean"][-1]

ax.annotate(
    "",
    xy=(final_step + 0.5, ours_final),
    xytext=(final_step + 0.5, baseline_final),
    arrowprops=dict(arrowstyle="<->", color="#888888", lw=1.2),
    annotation_clip=False,
)
gap = baseline_final - ours_final
ax.text(
    final_step + 1.2, (ours_final + baseline_final) / 2,
    f"Δ={gap:.2f}",
    va="center", ha="left", fontsize=8, color="#555555",
    clip_on=False,
)

ax.set_yscale("log")
ax.set_xlabel(d["x_label"].capitalize(), fontsize=11)
ax.set_ylabel(d["y_label"].capitalize(), fontsize=11)
ax.set_xlim(steps[0], steps[-1] + 4)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda v, _: f"{v:g}" if v >= 0.5 else f"{v:.2f}"
))
ax.yaxis.set_minor_formatter(ticker.NullFormatter())

ax.legend(frameon=True, framealpha=0.9, edgecolor="#cccccc", fontsize=9,
          loc="upper right")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
