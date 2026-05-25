import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    d = json.load(f)

studies = d["studies"]
effects = np.array(d["effects"])
se = np.array(d["se"])
xlabel = d["label"]

# Inverse-variance weights and random-effects pooled estimate (DerSimonian-Laird)
w = 1.0 / se**2
theta_fe = np.sum(w * effects) / np.sum(w)
Q = np.sum(w * (effects - theta_fe)**2)
k = len(effects)
tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w) - np.sum(w**2) / np.sum(w)))

w_re = 1.0 / (se**2 + tau2)
theta_re = np.sum(w_re * effects) / np.sum(w_re)
se_re = np.sqrt(1.0 / np.sum(w_re))
ci_lo_re = theta_re - 1.96 * se_re
ci_hi_re = theta_re + 1.96 * se_re

ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# Relative marker sizes proportional to RE weight
rel_w = w_re / w_re.max()
marker_sizes = 4 + rel_w * 8  # points, used as square half-width in data coords

fig, ax = plt.subplots(figsize=(8, 6))

n = len(studies)
y_positions = list(range(n, 0, -1))  # top to bottom

for i, (y, lo, hi, eff, ms) in enumerate(zip(y_positions, ci_lo, ci_hi, effects, marker_sizes)):
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.2, zorder=2)
    ax.plot(eff, y, "s", color="#1f77b4", markersize=ms, zorder=3)

# Diamond for pooled estimate at y=0
diamond_y = 0
diamond_h = 0.35
diamond_x = [ci_lo_re, theta_re, ci_hi_re, theta_re]
diamond_yy = [diamond_y, diamond_y + diamond_h, diamond_y, diamond_y - diamond_h]
ax.fill(diamond_x, diamond_yy, color="#d62728", zorder=4)
ax.plot(diamond_x + [diamond_x[0]], diamond_yy + [diamond_yy[0]], color="#8b0000", lw=1, zorder=5)

# Vertical line at 0
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# Axes
ax.set_yticks(y_positions + [0])
ax.set_yticklabels(studies + [f"Pooled (RE)\n{theta_re:.3f} [{ci_lo_re:.3f}, {ci_hi_re:.3f}]"],
                   fontsize=9)
ax.set_xlabel(xlabel, fontsize=10)
ax.set_xlim(min(ci_lo) - 0.15, max(ci_hi) + 0.15)
ax.set_ylim(-0.8, n + 0.8)

# Separator line above pooled
ax.axhline(0.65, color="#aaaaaa", lw=0.8, linestyle="-")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("Forest Plot: Meta-Analysis of 12 Studies", fontsize=12, pad=10)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled RE estimate: {theta_re:.4f} (95% CI [{ci_lo_re:.4f}, {ci_hi_re:.4f}])")
print(f"tau^2 = {tau2:.4f}, Q = {Q:.4f}, df = {k-1}")
