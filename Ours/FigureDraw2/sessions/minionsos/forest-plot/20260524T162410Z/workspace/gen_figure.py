import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load data
with open("data.json") as f:
    d = json.load(f)

studies = d["studies"]
effects = np.array(d["effects"])
se = np.array(d["se"])
xlabel = d["label"]

# Inverse-variance pooled estimate
weights = 1.0 / se**2
pooled_effect = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_ci_lo = pooled_effect - 1.96 * pooled_se
pooled_ci_hi = pooled_effect + 1.96 * pooled_se

ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

n = len(studies)
# y positions: studies top-to-bottom, then gap, then pooled
y_studies = np.arange(n, 0, -1, dtype=float)  # n down to 1
y_pooled = -0.5

fig, ax = plt.subplots(figsize=(8, 6))

# Per-study CI lines and point estimates
for i, (y, eff, lo, hi, w) in enumerate(zip(y_studies, effects, ci_lo, ci_hi, weights)):
    ax.plot([lo, hi], [y, y], color="#444444", lw=1.2, zorder=2)
    # Square size proportional to weight
    size = 40 + 120 * (w / weights.max())
    ax.scatter(eff, y, s=size, color="#1f77b4", zorder=3, marker="s")

# Pooled diamond
diamond_half_height = 0.35
diamond_x = [pooled_ci_lo, pooled_effect, pooled_ci_hi, pooled_effect, pooled_ci_lo]
diamond_y = [y_pooled, y_pooled + diamond_half_height,
             y_pooled, y_pooled - diamond_half_height, y_pooled]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=4)
ax.plot(diamond_x, diamond_y, color="#8b0000", lw=1, zorder=5)

# Vertical line at 0
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# Separator line between studies and pooled
ax.axhline(0.5, color="#aaaaaa", lw=0.7, linestyle="-")

# Y-axis labels
ytick_pos = list(y_studies) + [y_pooled]
ytick_labels = studies + ["Pooled (IV)"]
ax.set_yticks(ytick_pos)
ax.set_yticklabels(ytick_labels, fontsize=9)

# Annotate pooled estimate
ax.text(pooled_ci_hi + 0.02, y_pooled,
        f"{pooled_effect:.3f} [{pooled_ci_lo:.3f}, {pooled_ci_hi:.3f}]",
        va="center", fontsize=8, color="#d62728")

# Annotate per-study estimates
for y, eff, lo, hi in zip(y_studies, effects, ci_lo, ci_hi):
    ax.text(ci_hi.max() + 0.02, y,
            f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", fontsize=7.5, color="#333333")

ax.set_xlabel(xlabel, fontsize=10)
ax.set_title("Forest Plot: Meta-Analysis of 12 Studies", fontsize=11, fontweight="bold")

# Tighten x limits to leave room for annotations
x_min = ci_lo.min() - 0.15
x_max = ci_hi.max() + 0.55
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_pooled - 0.8, n + 0.8)

# Legend
sq = mpatches.Patch(color="#1f77b4", label="Study estimate (size ∝ weight)")
dia = mpatches.Patch(color="#d62728", label="Pooled estimate (IV)")
ax.legend(handles=[sq, dia], fontsize=8, loc="lower right")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled effect: {pooled_effect:.4f} (SE={pooled_se:.4f}), "
      f"95% CI [{pooled_ci_lo:.4f}, {pooled_ci_hi:.4f}]")
