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

slope, intercept, r_value, p_value, _ = stats.linregress(x, y)
r2 = r_value ** 2

# Find closest data point to the "OursModel" hint (~9.4, ~0.205)
target = np.array([9.4, 0.205])
dists = np.hypot(x - target[0], y - target[1])
idx = np.argmin(dists)
ours_x, ours_y = x[idx], y[idx]

x_fit = np.linspace(x.min() - 0.2, x.max() + 0.2, 300)
y_fit = slope * x_fit + intercept

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.scatter(x, y, s=22, alpha=0.6, color="#4878CF", edgecolors="none",
           zorder=2, label="Models")

ax.plot(x_fit, y_fit, color="#D65F5F", linewidth=1.8, zorder=3,
        label=f"OLS: $y = {slope:.4f}x + {intercept:.3f}$")

ax.scatter([ours_x], [ours_y], s=80, color="#E8A838", edgecolors="black",
           linewidths=0.8, zorder=4, label="OursModel")
ax.annotate("OursModel",
            xy=(ours_x, ours_y),
            xytext=(ours_x + 0.25, ours_y + 0.012),
            fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color="black", lw=0.7),
            color="black")

ax.text(0.97, 0.97,
        f"$R^2 = {r2:.3f}$\nslope $= {slope:.4f}$\nintercept $= {intercept:.3f}$",
        transform=ax.transAxes,
        va="top", ha="right",
        fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", alpha=0.85))

ax.set_xlabel(d["x_label"], fontsize=10)
ax.set_ylabel(d["y_label"], fontsize=10)
ax.set_title("Chinchilla-style Scaling Law", fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5, framealpha=0.85)
ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.5)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"slope={slope:.4f}  intercept={intercept:.4f}  R2={r2:.4f}")
print(f"OursModel point: ({ours_x}, {ours_y})")
