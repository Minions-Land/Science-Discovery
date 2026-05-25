import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

cwd = "/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2/sessions/latex-document/scatter-fit/20260524T162952Z/workspace"

with open(f"{cwd}/data.json") as f:
    data = json.load(f)

x = np.array(data["x"])
y = np.array(data["y"])
x_label = data["x_label"]
y_label = data["y_label"]

# OLS fit
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r2 = r_value ** 2

# Find closest point to (9.4, 0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x)**2 + (y - target_y)**2)
ours_idx = np.argmin(dists)
ours_x, ours_y = x[ours_idx], y[ours_idx]

# Plot
fig, ax = plt.subplots(figsize=(6, 4.5))

ax.scatter(x, y, s=28, alpha=0.65, color="#4878CF", edgecolors="white",
           linewidths=0.4, zorder=3, label="Models")

# OLS line
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 200)
y_fit = slope * x_fit + intercept
ax.plot(x_fit, y_fit, color="#E84040", linewidth=1.8, zorder=4, label="OLS fit")

# Emphasize OursModel point
ax.scatter([ours_x], [ours_y], s=90, color="#F5A623", edgecolors="#333",
           linewidths=1.2, zorder=5)
ax.annotate("OursModel",
            xy=(ours_x, ours_y),
            xytext=(ours_x + 0.25, ours_y + 0.012),
            fontsize=8.5,
            color="#333",
            arrowprops=dict(arrowstyle="-", color="#555", lw=0.8))

# Annotation box
ann_text = (f"slope = {slope:.4f}\n"
            f"intercept = {intercept:.4f}\n"
            f"$R^2$ = {r2:.4f}")
ax.text(0.97, 0.97, ann_text,
        transform=ax.transAxes,
        fontsize=8.5,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                  edgecolor="#ccc", alpha=0.9))

ax.set_xlabel(x_label, fontsize=11)
ax.set_ylabel(y_label, fontsize=11)
ax.set_title("Chinchilla-style Scaling Law: Validation Loss vs. Model Size", fontsize=11)
ax.legend(fontsize=9, loc="upper left")
ax.grid(True, linestyle="--", alpha=0.35, zorder=0)

fig.tight_layout()
fig.savefig(f"{cwd}/figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig(f"{cwd}/figure.png", dpi=150, bbox_inches="tight")
fig.savefig(f"{cwd}/figure.svg", bbox_inches="tight")
print(f"Saved. slope={slope:.4f}, intercept={intercept:.4f}, R2={r2:.4f}")
print(f"OursModel point: ({ours_x}, {ours_y})")
