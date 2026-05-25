import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

# Load data
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

# OLS fit
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r2 = r_value ** 2

# Find closest point to "OursModel" target (~9.4, ~0.205)
target = np.array([9.4, 0.205])
dists = np.sqrt((x - target[0])**2 + (y - target[1])**2)
ours_idx = np.argmin(dists)
ours_x, ours_y = x[ours_idx], y[ours_idx]

# Plot
fig, ax = plt.subplots(figsize=(6, 4.5))

# Scatter all points
mask = np.ones(len(x), dtype=bool)
mask[ours_idx] = False
ax.scatter(x[mask], y[mask], s=22, color="#4878CF", alpha=0.65, linewidths=0,
           zorder=2, label="Data points")

# Emphasized OursModel point
ax.scatter([ours_x], [ours_y], s=80, color="#E84040", zorder=4,
           edgecolors="white", linewidths=0.8, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.18, ours_y + 0.012),
    fontsize=8,
    color="#E84040",
    arrowprops=dict(arrowstyle="-", color="#E84040", lw=0.8),
)

# OLS line
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 200)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color="#333333", lw=1.5, zorder=3, label="OLS fit")

# Annotation box
ann_text = (
    f"$y = {slope:.4f}x + {intercept:.3f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(
    0.97, 0.97, ann_text,
    transform=ax.transAxes,
    fontsize=8.5,
    va="top", ha="right",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
              edgecolor="#cccccc", alpha=0.9),
)

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Chinchilla-style Scaling Law: Scatter + OLS Fit", fontsize=11)
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(0.97, 0.78))
ax.tick_params(labelsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"Saved figure.pdf, figure.png, figure.svg")
print(f"OLS: slope={slope:.4f}, intercept={intercept:.4f}, R²={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y} (index {ours_idx})")
