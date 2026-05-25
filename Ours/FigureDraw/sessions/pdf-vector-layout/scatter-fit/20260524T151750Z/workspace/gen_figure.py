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
r2 = r ** 2

# Find closest point to (9.4, 0.205)
target = np.array([9.4, 0.205])
dists = np.hypot(x - target[0], y - target[1])
idx = np.argmin(dists)
ours_x, ours_y = x[idx], y[idx]

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.scatter(x, y, s=22, alpha=0.65, color="#4878CF", edgecolors="none", zorder=2, label="Models")

x_fit = np.linspace(x.min(), x.max(), 200)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color="#D65F5F", linewidth=1.8, zorder=3, label="OLS fit")

# Highlight OursModel point
ax.scatter([ours_x], [ours_y], s=80, color="#E8A838", edgecolors="#333", linewidths=0.8, zorder=4)
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.18, ours_y + 0.012),
    fontsize=8,
    color="#333",
    arrowprops=dict(arrowstyle="-", color="#555", lw=0.8),
)

# Annotation box
ann_text = (
    f"slope = {slope:.4f}\n"
    f"intercept = {intercept:.4f}\n"
    f"$R^2$ = {r2:.4f}"
)
ax.text(
    0.97, 0.97, ann_text,
    transform=ax.transAxes,
    fontsize=8,
    va="top", ha="right",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#ccc", alpha=0.9),
)

ax.set_xlabel(x_label, fontsize=10)
ax.set_ylabel(y_label, fontsize=10)
ax.set_title("Chinchilla-style Scaling Law: Validation Loss vs. Model Size", fontsize=10)
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(0.97, 0.72))
ax.tick_params(labelsize=8)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"slope={slope:.4f}, intercept={intercept:.4f}, R2={r2:.4f}")
print(f"OursModel point: ({ours_x}, {ours_y})")
