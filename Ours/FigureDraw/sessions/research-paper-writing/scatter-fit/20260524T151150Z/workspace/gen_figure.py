import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

# ── OLS fit ────────────────────────────────────────────────────────────────
slope, intercept, r, p, se = stats.linregress(x, y)
r2 = r ** 2

x_fit = np.linspace(x.min(), x.max(), 300)
y_fit = slope * x_fit + intercept

# ── find closest point to "OursModel" target (~9.4, ~0.205) ───────────────
target = np.array([9.4, 0.205])
dists = np.hypot(x - target[0], y - target[1])
idx = int(np.argmin(dists))
ours_x, ours_y = x[idx], y[idx]

# ── figure ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4.5))

# scatter (all points)
ax.scatter(x, y, s=28, color="#4878CF", alpha=0.65, linewidths=0.4,
           edgecolors="#2a4a8a", zorder=2, label="Models")

# OLS line
ax.plot(x_fit, y_fit, color="#E84040", linewidth=1.8, zorder=3, label="OLS fit")

# emphasised "OursModel" point
ax.scatter([ours_x], [ours_y], s=90, color="#F5A623", edgecolors="#8B5E00",
           linewidths=1.2, zorder=5)
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.25, ours_y + 0.012),
    fontsize=8.5,
    color="#8B5E00",
    arrowprops=dict(arrowstyle="-", color="#8B5E00", lw=0.9),
)

# annotation box
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
ax.set_title("Scaling Law: Validation Loss vs. Model Size", fontsize=11)
ax.legend(fontsize=9, loc="upper right", bbox_to_anchor=(0.97, 0.78))
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
fig.tight_layout()

# ── save ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"slope={slope:.4f}  intercept={intercept:.4f}  R²={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y}")
