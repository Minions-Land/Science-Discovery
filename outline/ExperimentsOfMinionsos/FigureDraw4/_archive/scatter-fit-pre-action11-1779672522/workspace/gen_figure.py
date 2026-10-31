import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from scipy import stats
from pathlib import Path

cwd = Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())

x = np.array(data["x"])
y = np.array(data["y"])
x_label = data["x_label"]
y_label = data["y_label"]

slope, intercept, r, p, se = stats.linregress(x, y)
r2 = r ** 2

# Find closest point to (9.4, 0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
our_idx = int(np.argmin(dists))
our_x, our_y = x[our_idx], y[our_idx]

# Plot
fig, ax = plt.subplots(figsize=(5.5, 4.2))

# Color palette
scatter_color = "#4C72B0"
line_color = "#C44E52"
our_color = "#DD8452"

# Scatter
other_mask = np.ones(len(x), dtype=bool)
other_mask[our_idx] = False

ax.scatter(x[other_mask], y[other_mask],
           color=scatter_color, alpha=0.55, s=22, linewidths=0, zorder=2)

# Emphasized "OursModel" point
ax.scatter(our_x, our_y, color=our_color, s=80, zorder=5,
           edgecolors="white", linewidths=0.8)

# OLS line
x_range = np.linspace(x.min() - 0.15, x.max() + 0.15, 200)
y_fit = slope * x_range + intercept
ax.plot(x_range, y_fit, color=line_color, lw=1.6, zorder=3, label="OLS fit")

# Annotation: slope, intercept, R²
ann_text = (
    f"$y = {slope:.4f}x + {intercept:.3f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(0.97, 0.97, ann_text,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", alpha=0.85))

# OursModel label
label_offset_x = -0.55
label_offset_y = 0.012
ax.annotate(
    "OursModel",
    xy=(our_x, our_y),
    xytext=(our_x + label_offset_x, our_y + label_offset_y),
    fontsize=8, color=our_color, fontweight="bold",
    arrowprops=dict(arrowstyle="-", color=our_color, lw=0.9),
    zorder=6,
)

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Scaling Law: Model Size vs. Validation Loss", fontsize=11, pad=8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=8.5)
ax.grid(True, linestyle="--", alpha=0.35, zorder=0)

fig.tight_layout()

out_pdf = cwd / "figure.pdf"
out_png = cwd / "figure.png"
out_svg = cwd / "figure.svg"
fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
fig.savefig(out_png, dpi=150, bbox_inches="tight")
fig.savefig(out_svg, bbox_inches="tight")
print(f"Saved: {out_pdf}, {out_png}, {out_svg}")
print(f"OLS: slope={slope:.4f}, intercept={intercept:.4f}, R²={r2:.4f}")
print(f"OursModel point: ({our_x:.3f}, {our_y:.4f})")
