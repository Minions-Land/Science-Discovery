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
slope, intercept, r, p, se = stats.linregress(x, y)
r2 = r ** 2

# Find closest point to (9.4, 0.205) for "OursModel"
target = np.array([9.4, 0.205])
dists = np.sqrt((x - target[0])**2 + (y - target[1])**2)
idx = np.argmin(dists)
ours_x, ours_y = x[idx], y[idx]

# Figure
fig, ax = plt.subplots(figsize=(5.5, 4.2))

# Scatter
ax.scatter(x, y, s=22, alpha=0.55, color="#4878CF", edgecolors="none", zorder=2, label="Data points")

# Highlight OursModel
ax.scatter([ours_x], [ours_y], s=80, color="#E24A33", zorder=4, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.18, ours_y + 0.012),
    fontsize=8.5,
    color="#E24A33",
    arrowprops=dict(arrowstyle="-", color="#E24A33", lw=0.8),
)

# OLS line
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 200)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color="#333333", lw=1.5, zorder=3, label="OLS fit")

# Annotations
ann_text = (
    f"$y = {slope:.4f}\\,x + {intercept:.3f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(
    0.97, 0.97, ann_text,
    transform=ax.transAxes,
    fontsize=8.5,
    va="top", ha="right",
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.8),
)

ax.set_xlabel(x_label.replace("log10", r"$\log_{10}$"), fontsize=10)
ax.set_ylabel(y_label.replace("log10", r"$\log_{10}$"), fontsize=10)
ax.set_title("Chinchilla-style Scaling Law", fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5, framealpha=0.85)
ax.tick_params(labelsize=8.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"slope={slope:.5f}  intercept={intercept:.5f}  R2={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y}")
