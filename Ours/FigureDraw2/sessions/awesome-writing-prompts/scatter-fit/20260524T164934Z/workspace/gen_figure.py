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

# Find the point closest to OursModel target (~9.4, ~0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
ours_idx = np.argmin(dists)
ours_x, ours_y = x[ours_idx], y[ours_idx]

# Fit line range
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 300)
y_fit = slope * x_fit + intercept

# --- Plot ---
fig, ax = plt.subplots(figsize=(6.5, 4.5))

# Scatter all points (grey)
mask = np.ones(len(x), dtype=bool)
mask[ours_idx] = False
ax.scatter(x[mask], y[mask], color="#6baed6", edgecolors="#2171b5",
           linewidths=0.5, alpha=0.75, s=36, zorder=2, label="Models")

# Emphasized OursModel point
ax.scatter([ours_x], [ours_y], color="#e6550d", edgecolors="#a63603",
           linewidths=0.8, s=90, zorder=4, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.35, ours_y + 0.012),
    fontsize=8,
    color="#a63603",
    arrowprops=dict(arrowstyle="-", color="#a63603", lw=0.8),
    zorder=5,
)

# OLS line
ax.plot(x_fit, y_fit, color="#d62728", linewidth=1.6, zorder=3, label="OLS fit")

# Annotation box
annot_text = (
    f"$y = {slope:.4f}x + {intercept:.3f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(
    0.97, 0.97, annot_text,
    transform=ax.transAxes,
    fontsize=8.5,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#aaaaaa", linewidth=0.8),
    zorder=6,
)

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Scaling Law: Validation Loss vs. Parameter Count", fontsize=11)
ax.legend(fontsize=8.5, loc="upper left", framealpha=0.85)
ax.tick_params(labelsize=9)
ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.5)

fig.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"slope={slope:.4f}  intercept={intercept:.4f}  R2={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y}")
