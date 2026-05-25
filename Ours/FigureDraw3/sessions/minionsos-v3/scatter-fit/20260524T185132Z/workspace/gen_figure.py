"""
Chinchilla-style scaling law scatter + OLS fit.
Data source: data.json (x=log10(parameters), y=log10(validation loss))
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
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
from scipy import stats

PALETTE = {
    "signal": "#0F4D92",
    "signal_soft": "#B4C0E4",
    "neutral": "#767676",
    "neutral_light": "#D8D8D8",
    "accent": "#E4CCD8",
    "accent_dark": "#9A4D8E",
    "black": "#272727",
    "ours": "#D55E00",
}

with open("data.json") as f:
    data = json.load(f)

x = np.array(data["x"])
y = np.array(data["y"])

slope, intercept, r_value, p_value, se = stats.linregress(x, y)
r2 = r_value ** 2

# Find closest point to (9.4, 0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
ours_idx = int(np.argmin(dists))
ours_x, ours_y = x[ours_idx], y[ours_idx]

fig, ax = plt.subplots(figsize=(6, 4))

# Scatter — all non-ours points
mask = np.ones(len(x), dtype=bool)
mask[ours_idx] = False
ax.scatter(x[mask], y[mask], s=28, color=PALETTE["signal_soft"],
           edgecolors=PALETTE["signal"], linewidths=0.5, zorder=2, alpha=0.85,
           label="Models")

# OLS fit line
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 200)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color=PALETTE["signal"], linewidth=1.5,
        linestyle="--", zorder=3, label="OLS fit")

# OursModel point
ax.scatter([ours_x], [ours_y], s=80, color=PALETTE["ours"],
           edgecolors="white", linewidths=1.0, zorder=5, marker="*",
           label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.35, ours_y + 0.012),
    fontsize=8,
    color=PALETTE["ours"],
    arrowprops=dict(arrowstyle="-", color=PALETTE["ours"], lw=0.8),
    zorder=6,
)

# Annotation box: slope, intercept, R²
stats_text = (
    f"slope = {slope:.3f}\n"
    f"intercept = {intercept:.3f}\n"
    f"$R^2$ = {r2:.3f}"
)
ax.text(0.97, 0.97, stats_text,
        transform=ax.transAxes,
        fontsize=8,
        va="top", ha="right",
        color=PALETTE["black"],
        linespacing=1.5)

ax.set_xlabel(r"$\log_{10}$(parameters)", fontsize=10)
ax.set_ylabel(r"$\log_{10}$(validation loss)", fontsize=10)
ax.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(0.97, 0.78))

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Saved figure.pdf, figure.png, figure.svg")
print(f"OLS: slope={slope:.4f}, intercept={intercept:.4f}, R²={r2:.4f}")
print(f"OursModel point: ({ours_x:.3f}, {ours_y:.4f})")
