import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["x"])
y = np.array(d["y"])
x_label = d["x_label"]
y_label = d["y_label"]

# ── OLS fit ───────────────────────────────────────────────────────────────────
slope, intercept, r, p, se = stats.linregress(x, y)
r2 = r ** 2

x_fit = np.linspace(x.min(), x.max(), 300)
y_fit = slope * x_fit + intercept

# ── find closest point to "OursModel" target ──────────────────────────────────
target = np.array([9.4, 0.205])
dists = np.hypot(x - target[0], y - target[1])
idx_ours = int(np.argmin(dists))
x_ours, y_ours = x[idx_ours], y[idx_ours]

# ── figure style (Nature-like) ────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 8,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(3.5, 3.0))

# scatter (all points)
ax.scatter(x, y, s=18, color="#4878CF", alpha=0.65, linewidths=0.3,
           edgecolors="#2a4a8a", zorder=3, label="Models")

# OLS line
ax.plot(x_fit, y_fit, color="#E84040", linewidth=1.4, zorder=4, label="OLS fit")

# OursModel point
ax.scatter(x_ours, y_ours, s=60, color="#F5A623", edgecolors="#b07010",
           linewidths=0.8, zorder=5)
ax.annotate(
    "OursModel",
    xy=(x_ours, y_ours),
    xytext=(x_ours + 0.25, y_ours + 0.012),
    fontsize=7,
    color="#b07010",
    arrowprops=dict(arrowstyle="-", color="#b07010", lw=0.8),
)

# annotation box: slope, intercept, R²
ann_text = (
    f"slope = {slope:.4f}\n"
    f"intercept = {intercept:.4f}\n"
    f"$R^2$ = {r2:.4f}"
)
ax.text(0.97, 0.97, ann_text, transform=ax.transAxes,
        fontsize=7, va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.6))

ax.set_xlabel(x_label, fontsize=8)
ax.set_ylabel(y_label, fontsize=8)
ax.set_title("Neural Scaling Law: Parameters vs. Validation Loss", fontsize=8, pad=6)

legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#4878CF",
           markeredgecolor="#2a4a8a", markersize=5, label="Models"),
    Line2D([0], [0], color="#E84040", linewidth=1.4, label="OLS fit"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="#F5A623",
           markeredgecolor="#b07010", markersize=6, label="OursModel"),
]
ax.legend(handles=legend_elements, fontsize=7, frameon=True,
          framealpha=0.9, edgecolor="#cccccc", loc="upper right",
          bbox_to_anchor=(0.97, 0.72))

ax.tick_params(labelsize=7)
fig.tight_layout(pad=0.5)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"OursModel point: x={x_ours:.3f}, y={y_ours:.4f}")
print(f"OLS: slope={slope:.4f}, intercept={intercept:.4f}, R²={r2:.4f}")
print("Saved figure.pdf, figure.png, figure.svg")
