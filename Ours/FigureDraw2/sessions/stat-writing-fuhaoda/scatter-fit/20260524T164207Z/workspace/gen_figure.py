import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

slope, intercept, r, p, se = stats.linregress(x, y)
r2 = r**2

# Find closest point to (~9.4, ~0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x)**2 + (y - target_y)**2)
ours_idx = np.argmin(dists)
ours_x, ours_y = x[ours_idx], y[ours_idx]

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.scatter(x, y, s=22, alpha=0.65, color="#4878CF", edgecolors="none", zorder=2, label="Models")

# Highlight OursModel point
ax.scatter([ours_x], [ours_y], s=80, color="#E84040", zorder=4, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.18, ours_y + 0.012),
    fontsize=8,
    color="#E84040",
    arrowprops=dict(arrowstyle="-", color="#E84040", lw=0.8),
)

# OLS fit line
x_fit = np.linspace(x.min(), x.max(), 200)
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
    bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#cccccc", lw=0.8),
)

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Scaling Law: Validation Loss vs. Model Size", fontsize=11)
ax.legend(fontsize=8, framealpha=0.9)
ax.tick_params(labelsize=8)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"slope={slope:.5f}, intercept={intercept:.5f}, R2={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y}")
