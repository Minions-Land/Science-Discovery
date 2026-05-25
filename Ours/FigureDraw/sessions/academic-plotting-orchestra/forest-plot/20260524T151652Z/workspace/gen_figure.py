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

# 95% CI
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# Inverse-variance pooled estimate (fixed-effects)
weights = 1.0 / se**2
pooled = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_lo = pooled - 1.96 * pooled_se
pooled_hi = pooled + 1.96 * pooled_se

n = len(studies)
y_positions = list(range(n, 0, -1))  # top to bottom
pooled_y = 0

fig, ax = plt.subplots(figsize=(8, 6))

# Study rows
for i, (y, eff, lo, hi, w) in enumerate(zip(y_positions, effects, ci_lo, ci_hi, weights)):
    # CI line
    ax.plot([lo, hi], [y, y], color="black", linewidth=1.2, zorder=2)
    # Square marker sized by weight (relative)
    sq_size = 60 * (w / weights.max())
    ax.scatter([eff], [y], s=sq_size, color="steelblue", zorder=3, marker="s")

# Pooled diamond
diamond_half_height = 0.35
diamond_x = [pooled_lo, pooled, pooled_hi, pooled, pooled_lo]
diamond_y = [pooled_y, pooled_y + diamond_half_height,
             pooled_y, pooled_y - diamond_half_height, pooled_y]
ax.fill(diamond_x, diamond_y, color="firebrick", zorder=3)
ax.plot(diamond_x, diamond_y, color="darkred", linewidth=1, zorder=4)

# Null line
ax.axvline(0, color="gray", linestyle="--", linewidth=0.9, zorder=1)

# Y-axis labels
yticks = y_positions + [pooled_y]
ylabels = studies + ["Pooled (FE)"]
ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=9)

# Annotate effect sizes on the right
x_annot = max(ci_hi.max(), pooled_hi) + 0.05
for y, eff, lo, hi in zip(y_positions, effects, ci_lo, ci_hi):
    ax.text(x_annot, y, f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", ha="left", fontsize=7.5, color="black")
ax.text(x_annot, pooled_y,
        f"{pooled:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]",
        va="center", ha="left", fontsize=7.5, color="darkred", fontweight="bold")

ax.set_xlabel(xlabel, fontsize=10)
ax.set_title("Forest Plot: Meta-Analysis of 12 Studies", fontsize=11, fontweight="bold")

# Extend x-axis to fit annotations
ax.set_xlim(min(ci_lo.min(), pooled_lo) - 0.1, x_annot + 0.55)
ax.set_ylim(-0.8, n + 0.8)

# Separator line above pooled
ax.axhline(0.6, color="black", linewidth=0.8, linestyle="-")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled estimate: {pooled:.4f} (95% CI [{pooled_lo:.4f}, {pooled_hi:.4f}])")
