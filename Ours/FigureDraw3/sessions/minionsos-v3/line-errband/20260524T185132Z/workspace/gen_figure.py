"""
gen_figure.py — validation loss training curves with 95% CI bands
Data source: data.json (3 methods × 50 steps, n_seeds=5)
"""

import json
import numpy as np
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
import matplotlib.pyplot as plt

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

PALETTE = {
    "Baseline":   "#767676",   # neutral grey
    "Method-A":   "#E69F00",   # Okabe-Ito amber
    "OursModel":  "#0072B2",   # Okabe-Ito blue (signal / accent)
}
BAND_ALPHA = 0.18

with open("data.json") as f:
    data = json.load(f)

steps   = np.array(data["steps"])
methods = data["methods"]
curves  = data["curves"]

fig, ax = plt.subplots(figsize=(6, 4))

for method in methods:
    mean    = np.array(curves[method]["mean"])
    ci_half = np.array(curves[method]["ci_half"])
    color   = PALETTE[method]
    lw      = 2.0 if method == "OursModel" else 1.6
    zorder  = 3 if method == "OursModel" else 2
    label   = method

    ax.fill_between(steps, mean - ci_half, mean + ci_half,
                    color=color, alpha=BAND_ALPHA, linewidth=0, zorder=zorder - 1)
    ax.plot(steps, mean, color=color, linewidth=lw, label=label, zorder=zorder)

# Annotate final-step gap between OursModel and the next-best (Method-A)
ours_final   = curves["OursModel"]["mean"][-1]
methA_final  = curves["Method-A"]["mean"][-1]
gap          = methA_final - ours_final
last_step    = steps[-1]

ax.annotate(
    f"$\\Delta={gap:.3f}$",
    xy=(last_step, ours_final),
    xytext=(-52, 14),
    textcoords="offset points",
    fontsize=8,
    color=PALETTE["OursModel"],
    arrowprops=dict(arrowstyle="-", color=PALETTE["OursModel"],
                    lw=0.8, connectionstyle="arc3,rad=0.0"),
)

ax.set_yscale("log")
ax.set_xlabel("Training step", fontsize=9)
ax.set_ylabel("Validation loss (log scale)", fontsize=9)
ax.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax.legend(loc="upper right", fontsize=9)

# Tight y-range with small headroom
all_means = np.concatenate([curves[m]["mean"] for m in methods])
all_ci    = np.concatenate([curves[m]["ci_half"] for m in methods])
ymin = (all_means - all_ci).min() * 0.95
ymax = (all_means + all_ci).max() * 1.08
ax.set_ylim(ymin, ymax)
ax.set_xlim(steps[0] - 0.5, steps[-1] + 1.5)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
