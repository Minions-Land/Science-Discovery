import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from scipy import stats

# Load data
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

# OLS fit
slope, intercept, r, p_val, se = stats.linregress(x, y)
r2 = r ** 2

# Find closest point to "OursModel" target (~9.4, ~0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
ours_idx = np.argmin(dists)
ours_x, ours_y = x[ours_idx], y[ours_idx]

# --- Figure ---
fig, ax = plt.subplots(figsize=(5.5, 4.2))

# Scatter: all points
mask = np.ones(len(x), dtype=bool)
mask[ours_idx] = False
ax.scatter(x[mask], y[mask], s=28, color="#4C72B0", alpha=0.65, linewidths=0,
           zorder=2, label="Models")

# Emphasized "OursModel" point
ax.scatter([ours_x], [ours_y], s=90, color="#DD4444", zorder=4,
           marker="*", label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.18, ours_y + 0.010),
    fontsize=8.5,
    color="#DD4444",
    fontweight="bold",
    arrowprops=dict(arrowstyle="-", color="#DD4444", lw=0.8),
    zorder=5,
)

# OLS line
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 300)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color="#E07B2A", lw=1.8, zorder=3, label="OLS fit")

# Annotation box
ann_text = (
    f"slope = {slope:.4f}\n"
    f"intercept = {intercept:.4f}\n"
    f"$R^2$ = {r2:.4f}"
)
ax.text(
    0.97, 0.97, ann_text,
    transform=ax.transAxes,
    fontsize=8.2,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
              edgecolor="#CCCCCC", alpha=0.9),
    family="monospace",
    zorder=6,
)

ax.set_xlabel(x_label, fontsize=11)
ax.set_ylabel(y_label, fontsize=11)
ax.set_title("Chinchilla-style Scaling Law Fit", fontsize=12, pad=8)
ax.legend(fontsize=9, loc="upper left", framealpha=0.85)
ax.grid(True, linestyle="--", alpha=0.35, zorder=0)
ax.tick_params(labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"OLS: slope={slope:.6f}, intercept={intercept:.6f}, R2={r2:.6f}")
print(f"OursModel point: x={ours_x}, y={ours_y} (index {ours_idx})")
print("Saved figure.pdf, figure.png, figure.svg")
