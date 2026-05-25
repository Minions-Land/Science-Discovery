import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats

# ── Data ────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

# ── OLS fit ─────────────────────────────────────────────────────────────────
slope, intercept, r_value, p_value, se = stats.linregress(x, y)
r2 = r_value ** 2

x_fit = np.linspace(x.min(), x.max(), 300)
y_fit = slope * x_fit + intercept

# ── Closest point to OursModel target (~9.4, ~0.205) ────────────────────────
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
idx_ours = int(np.argmin(dists))
ours_x, ours_y = x[idx_ours], y[idx_ours]

# ── Tol's palette ────────────────────────────────────────────────────────────
SCATTER_COLOR = "#0077BB"
FIT_COLOR     = "#CC3311"
OURS_COLOR    = "#EE7733"

# ── Figure ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(5.5, 4.2))
fig.patch.set_facecolor("white")

# Scatter
mask = np.ones(len(x), dtype=bool)
mask[idx_ours] = False
ax.scatter(x[mask], y[mask], s=22, color=SCATTER_COLOR, alpha=0.65,
           edgecolors="none", zorder=2, label="Data points")

# OLS line
ax.plot(x_fit, y_fit, color=FIT_COLOR, linewidth=1.6, zorder=3,
        label="OLS fit")

# OursModel point
ax.scatter([ours_x], [ours_y], s=80, color=OURS_COLOR, edgecolors="#333333",
           linewidths=0.8, zorder=5, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.35, ours_y + 0.014),
    fontsize=7.5,
    color="#333333",
    arrowprops=dict(arrowstyle="-", color="#555555", lw=0.7),
)

# Annotation box: slope, intercept, R²
ann_text = (
    f"$y = {slope:.4f}x + {intercept:.4f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(
    0.97, 0.97, ann_text,
    transform=ax.transAxes,
    fontsize=7.5,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
              edgecolor="#cccccc", linewidth=0.7),
)

# Axes
ax.set_xlabel(x_label, fontsize=9)
ax.set_ylabel(y_label, fontsize=9)
ax.tick_params(labelsize=8)

# Legend
legend_handles = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=SCATTER_COLOR,
           markersize=5, alpha=0.85, label="Data points"),
    Line2D([0], [0], color=FIT_COLOR, linewidth=1.5, label="OLS fit"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=OURS_COLOR,
           markeredgecolor="#333333", markeredgewidth=0.6,
           markersize=6, label="OursModel"),
]
ax.legend(handles=legend_handles, fontsize=7.5, loc="lower right",
          framealpha=0.9, edgecolor="#cccccc")

ax.spines[["top", "right"]].set_visible(False)
ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.5, zorder=0)

plt.tight_layout(pad=0.6)

# ── Save ────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"slope={slope:.4f}  intercept={intercept:.4f}  R²={r2:.4f}")
print(f"OursModel point: x={ours_x}, y={ours_y}  (index {idx_ours})")
print("Saved: figure.pdf, figure.png, figure.svg")
