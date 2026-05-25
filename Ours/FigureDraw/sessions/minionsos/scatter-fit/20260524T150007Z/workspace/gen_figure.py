import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats

with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r2 = r_value ** 2

# Find point closest to (9.4, 0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
idx = np.argmin(dists)
ours_x, ours_y = x[idx], y[idx]

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.scatter(x, y, s=28, alpha=0.6, color="#4C72B0", edgecolors="none", zorder=2, label="Models")

x_fit = np.linspace(x.min(), x.max(), 300)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color="#C44E52", linewidth=1.8, zorder=3, label="OLS fit")

ax.scatter([ours_x], [ours_y], s=90, color="#DD8800", edgecolors="black",
           linewidths=0.8, zorder=5, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.25, ours_y + 0.012),
    fontsize=8.5,
    color="#DD8800",
    arrowprops=dict(arrowstyle="-", color="#DD8800", lw=0.8),
)

annot = (
    f"$y = {slope:.4f}x + {intercept:.3f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(
    0.97, 0.97, annot,
    transform=ax.transAxes,
    ha="right", va="top",
    fontsize=9,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#cccccc", alpha=0.85),
)

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Scaling Law: Validation Loss vs. Model Size", fontsize=11)
ax.legend(fontsize=9, loc="upper right", bbox_to_anchor=(0.99, 0.72))

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"slope={slope:.4f}, intercept={intercept:.4f}, R2={r2:.4f}")
print(f"OursModel point: ({ours_x}, {ours_y})")
