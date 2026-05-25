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

# 95% CI
z = 1.96
ci_lo = effects - z * se
ci_hi = effects + z * se

# Fixed-effects pooled estimate (inverse-variance weighting)
weights = 1.0 / se**2
pooled_effect = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_lo = pooled_effect - z * pooled_se
pooled_hi = pooled_effect + z * pooled_se

n = len(studies)
# y positions: studies top-to-bottom, gap, then pooled
y_studies = np.arange(n, 0, -1, dtype=float)  # n down to 1
y_pooled = -0.5

fig, ax = plt.subplots(figsize=(8, 6))

# Study-level CI lines and squares
sq_scale = 0.18  # square half-height
for i, (y, eff, lo, hi, w) in enumerate(zip(y_studies, effects, ci_lo, ci_hi, weights)):
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.2, zorder=2)
    # Square size proportional to weight
    sq = sq_scale * (w / weights.max()) ** 0.5
    rect = mpatches.FancyBboxPatch(
        (eff - sq / 2, y - sq / 2), sq, sq,
        boxstyle="square,pad=0",
        facecolor="#2166ac", edgecolor="#2166ac", zorder=3
    )
    ax.add_patch(rect)

# Pooled diamond
diam_h = 0.35  # half-height
diam_xs = [pooled_lo, pooled_effect, pooled_hi, pooled_effect, pooled_lo]
diam_ys = [y_pooled, y_pooled + diam_h, y_pooled, y_pooled - diam_h, y_pooled]
ax.fill(diam_xs, diam_ys, color="#d6604d", zorder=3)
ax.plot(diam_xs, diam_ys, color="#b2182b", lw=1.0, zorder=4)

# Vertical line at 0
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# Separator line between studies and pooled
ax.axhline(0.5, color="#aaaaaa", lw=0.7, linestyle="-")

# Y-axis labels
ytick_pos = list(y_studies) + [y_pooled]
ytick_labels = studies + ["Pooled (FE)"]
ax.set_yticks(ytick_pos)
ax.set_yticklabels(ytick_labels, fontsize=9)

# Annotate pooled estimate
ax.text(
    pooled_hi + 0.02, y_pooled,
    f"{pooled_effect:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]",
    va="center", ha="left", fontsize=8, color="#b2182b"
)

# Axis formatting
ax.set_xlabel(xlabel, fontsize=10)
ax.set_xlim(
    min(ci_lo.min(), pooled_lo) - 0.15,
    max(ci_hi.max(), pooled_hi) + 0.35
)
ax.set_ylim(y_pooled - 0.8, n + 0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

ax.set_title("Forest Plot: Meta-Analysis of Intervention Effect", fontsize=11, pad=10)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled effect: {pooled_effect:.4f} (95% CI: {pooled_lo:.4f}, {pooled_hi:.4f})")
print("Saved figure.pdf, figure.png, figure.svg")
