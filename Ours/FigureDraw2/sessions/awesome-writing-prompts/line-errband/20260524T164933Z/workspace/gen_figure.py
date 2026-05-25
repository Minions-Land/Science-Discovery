import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    d = json.load(f)

steps = np.array(d["steps"])
methods = d["methods"]
curves = d["curves"]

colors = {"Baseline": "#4878CF", "Method-A": "#6ACC65", "OursModel": "#D65F5F"}
labels = {"Baseline": "Baseline", "Method-A": "Method-A", "OursModel": "OursModel (ours)"}

fig, ax = plt.subplots(figsize=(6, 4))

for method in methods:
    mean = np.array(curves[method]["mean"])
    ci = np.array(curves[method]["ci_half"])
    c = colors[method]
    ax.plot(steps, mean, color=c, linewidth=1.8, label=labels[method])
    ax.fill_between(steps, mean - ci, mean + ci, color=c, alpha=0.18)

# Highlight gap at final step
final = steps[-1]
vals = {m: curves[m]["mean"][-1] for m in methods}
y_ours = vals["OursModel"]
y_baseline = vals["Baseline"]
y_methoda = vals["Method-A"]

# Draw bracket between OursModel and Method-A (closest competitor) at final step
x_ann = final + 1.2
ax.annotate(
    "",
    xy=(x_ann, y_ours),
    xytext=(x_ann, y_methoda),
    arrowprops=dict(arrowstyle="<->", color="black", lw=1.2),
)
gap = y_methoda - y_ours
ax.text(
    x_ann + 0.6,
    (y_ours + y_methoda) / 2,
    f"$\\Delta={gap:.3f}$",
    va="center",
    ha="left",
    fontsize=8,
)

ax.set_yscale("log")
ax.set_xlabel(d["x_label"].capitalize(), fontsize=11)
ax.set_ylabel(d["y_label"].capitalize(), fontsize=11)
ax.set_title("Validation Loss over Training Steps", fontsize=12)
ax.legend(fontsize=9, loc="upper right")
ax.set_xlim(steps[0], steps[-1] + 4)
ax.tick_params(axis="both", which="both", labelsize=9)
ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.yaxis.get_major_formatter().set_scientific(False)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
