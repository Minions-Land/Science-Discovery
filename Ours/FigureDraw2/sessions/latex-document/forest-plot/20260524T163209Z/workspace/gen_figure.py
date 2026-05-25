import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    data = json.load(f)

studies = data["studies"]
effects = np.array(data["effects"])
se = np.array(data["se"])
xlabel = data["label"]

# 95% CI
z = 1.96
ci_lo = effects - z * se
ci_hi = effects + z * se

# Inverse-variance pooled estimate (fixed-effects)
weights = 1.0 / se**2
pooled = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_lo = pooled - z * pooled_se
pooled_hi = pooled + z * pooled_se

n = len(studies)
y_positions = list(range(n, 0, -1))  # top to bottom
y_pooled = 0

fig, ax = plt.subplots(figsize=(8, 6))

# Study rows
for i, (y, eff, lo, hi, w) in enumerate(zip(y_positions, effects, ci_lo, ci_hi, weights)):
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.2, zorder=2)
    # Square size proportional to weight
    sq = 0.06 + 0.18 * (w / weights.max())
    ax.plot(eff, y, "s", color="#1f77b4", markersize=6 * sq / 0.12, zorder=3)

# Pooled diamond
diamond_half_h = 0.35
diamond_x = [pooled_lo, pooled, pooled_hi, pooled, pooled_lo]
diamond_y = [y_pooled, y_pooled + diamond_half_h, y_pooled, y_pooled - diamond_half_h, y_pooled]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=4)
ax.plot(diamond_x, diamond_y, color="#8b0000", lw=1, zorder=5)

# Vertical line at 0
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# Y-axis labels
yticks = y_positions + [y_pooled]
ylabels = studies + ["Pooled (FE)"]
ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=9)

ax.set_xlabel(xlabel, fontsize=10)
ax.set_xlim(-0.6, 1.1)
ax.set_ylim(-0.8, n + 0.8)

# Separator line above pooled
ax.axhline(0.6, color="#aaaaaa", lw=0.8, linestyle="-")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Annotation for pooled estimate
ax.text(pooled_hi + 0.04, y_pooled,
        f"{pooled:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]",
        va="center", fontsize=8, color="#d62728")

ax.set_title("Forest Plot: Meta-Analysis of 12 Studies", fontsize=11, pad=10)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled estimate: {pooled:.4f} (95% CI: {pooled_lo:.4f}, {pooled_hi:.4f})")
