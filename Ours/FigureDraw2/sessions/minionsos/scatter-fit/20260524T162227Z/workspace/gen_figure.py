import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Load data
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

# OLS fit
coeffs = np.polyfit(x, y, 1)
slope, intercept = coeffs
y_pred = np.polyval(coeffs, x)
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - y.mean()) ** 2)
r2 = 1 - ss_res / ss_tot

# Find closest point to (9.4, 0.205)
target = np.array([9.4, 0.205])
dists = np.sqrt((x - target[0]) ** 2 + (y - target[1]) ** 2)
ours_idx = int(np.argmin(dists))
ours_x, ours_y = x[ours_idx], y[ours_idx]

# Plot
fig, ax = plt.subplots(figsize=(6, 4.5))

# Scatter — all points except ours
mask = np.ones(len(x), dtype=bool)
mask[ours_idx] = False
ax.scatter(x[mask], y[mask], s=22, color="#4878CF", alpha=0.65, linewidths=0,
           zorder=2, label="Models")

# OursModel point
ax.scatter([ours_x], [ours_y], s=80, color="#E84040", zorder=4,
           edgecolors="white", linewidths=0.8, label="OursModel")
ax.annotate("OursModel",
            xy=(ours_x, ours_y),
            xytext=(ours_x + 0.18, ours_y + 0.012),
            fontsize=8, color="#E84040",
            arrowprops=dict(arrowstyle="-", color="#E84040", lw=0.8))

# OLS line
x_line = np.linspace(x.min() - 0.1, x.max() + 0.1, 200)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color="#333333", lw=1.5, zorder=3, label="OLS fit")

# Annotation box
ann_text = (f"$y = {slope:.4f}x + {intercept:.3f}$\n"
            f"$R^2 = {r2:.3f}$")
ax.text(0.97, 0.97, ann_text,
        transform=ax.transAxes,
        fontsize=8.5, va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                  edgecolor="#cccccc", alpha=0.9))

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Scaling Law: Validation Loss vs. Model Size", fontsize=11)
ax.legend(fontsize=8.5, framealpha=0.9)
ax.tick_params(labelsize=9)
ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.5)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"slope={slope:.4f}  intercept={intercept:.4f}  R2={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y}")
