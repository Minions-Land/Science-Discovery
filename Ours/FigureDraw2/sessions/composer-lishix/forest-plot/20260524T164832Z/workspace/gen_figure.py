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

# Fixed-effects pooled estimate (inverse-variance weighting)
weights = 1.0 / se**2
pooled = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_ci_lo = pooled - 1.96 * pooled_se
pooled_ci_hi = pooled + 1.96 * pooled_se

ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

n = len(studies)
# y positions: studies top-to-bottom, then gap, then pooled
y_studies = np.arange(n, 0, -1, dtype=float)  # n down to 1
y_pooled = -0.5

fig, ax = plt.subplots(figsize=(8, 6))

# Marker sizes proportional to weight (relative)
rel_w = weights / weights.max()
marker_sizes = 40 + 120 * rel_w

# Study rows
for i, (study, eff, lo, hi, ms) in enumerate(
    zip(studies, effects, ci_lo, ci_hi, marker_sizes)
):
    y = y_studies[i]
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.2, zorder=2)
    ax.scatter([eff], [y], s=ms, color="#1f77b4", zorder=3, clip_on=False)

# Vertical line at 0
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# Separator line
ax.axhline(0.3, color="#888888", lw=0.8, linestyle="-")

# Pooled diamond
half_h = 0.35
diamond_x = [pooled_ci_lo, pooled, pooled_ci_hi, pooled, pooled_ci_lo]
diamond_y = [y_pooled, y_pooled + half_h, y_pooled, y_pooled - half_h, y_pooled]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=3)
ax.plot(diamond_x, diamond_y, color="#8b0000", lw=1, zorder=4)

# Y-axis labels
ytick_pos = list(y_studies) + [y_pooled]
ytick_labels = list(studies) + [f"Pooled (FE)\n{pooled:.3f} [{pooled_ci_lo:.3f}, {pooled_ci_hi:.3f}]"]
ax.set_yticks(ytick_pos)
ax.set_yticklabels(ytick_labels, fontsize=9)

# Annotations: effect [CI] on right side
x_annot = max(ci_hi.max(), pooled_ci_hi) + 0.05
for i, (eff, lo, hi) in enumerate(zip(effects, ci_lo, ci_hi)):
    ax.text(x_annot, y_studies[i], f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", ha="left", fontsize=7.5, color="#333333")

ax.set_xlabel(xlabel, fontsize=10)
ax.set_title("Forest Plot: Meta-Analysis of 12 Studies", fontsize=11, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(left=False)

# Expand x limits to fit annotations
ax.set_xlim(ci_lo.min() - 0.15, x_annot + 0.55)
ax.set_ylim(y_pooled - 0.7, n + 0.5)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled estimate: {pooled:.4f} (SE={pooled_se:.4f}), 95% CI [{pooled_ci_lo:.4f}, {pooled_ci_hi:.4f}]")
