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

# 95% confidence intervals
ci_low = effects - 1.96 * se
ci_high = effects + 1.96 * se

# Inverse-variance weighted pooled estimate (fixed-effects)
weights = 1.0 / (se ** 2)
pooled_effect = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_ci_low = pooled_effect - 1.96 * pooled_se
pooled_ci_high = pooled_effect + 1.96 * pooled_se

n = len(studies)
# y positions: studies top-to-bottom, then gap, then pooled
y_studies = np.arange(n, 0, -1, dtype=float)  # n down to 1
y_pooled = 0.0  # below the gap

fig, ax = plt.subplots(figsize=(8, 6.5))

# Marker size proportional to weight (relative)
w_norm = weights / weights.max()
marker_sizes = 6 + 80 * w_norm  # area scale

# Study rows
for i, (y, eff, lo, hi, ms) in enumerate(zip(y_studies, effects, ci_low, ci_high, marker_sizes)):
    ax.plot([lo, hi], [y, y], color="steelblue", linewidth=1.2, zorder=2)
    ax.plot(eff, y, "s", color="steelblue", markersize=np.sqrt(ms), zorder=3)

# Pooled diamond
diamond_half_height = 0.35
diamond_x = [pooled_ci_low, pooled_effect, pooled_ci_high, pooled_effect, pooled_ci_low]
diamond_y = [y_pooled, y_pooled + diamond_half_height,
             y_pooled, y_pooled - diamond_half_height, y_pooled]
ax.fill(diamond_x, diamond_y, color="firebrick", zorder=4)
ax.plot(diamond_x, diamond_y, color="darkred", linewidth=0.8, zorder=5)

# Null-effect vertical line
ax.axvline(0, color="black", linewidth=0.9, linestyle="--", zorder=1)

# Axes formatting
all_ys = list(y_studies) + [y_pooled]
ax.set_yticks(list(y_studies) + [y_pooled])
ax.set_yticklabels(list(studies) + [f"Pooled (FE)"], fontsize=9)
ax.set_ylim(y_pooled - 0.7, y_studies[0] + 0.7)

# Add separator line between studies and pooled
ax.axhline(0.5, color="gray", linewidth=0.7, linestyle="-")

ax.set_xlabel(xlabel, fontsize=9)
ax.set_title("Forest Plot: Intervention vs Control", fontsize=11, fontweight="bold")

# x-axis limits with a bit of padding
x_pad = 0.05
x_min = min(ci_low.min(), pooled_ci_low) - x_pad
x_max = max(ci_high.max(), pooled_ci_high) + x_pad
ax.set_xlim(x_min, x_max)

# Annotate pooled estimate value
ax.text(x_max + 0.02, y_pooled,
        f"{pooled_effect:.3f}\n[{pooled_ci_low:.3f}, {pooled_ci_high:.3f}]",
        va="center", ha="left", fontsize=7.5, color="darkred",
        transform=ax.transData, clip_on=False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled effect (FE): {pooled_effect:.4f}  SE: {pooled_se:.4f}  "
      f"95% CI [{pooled_ci_low:.4f}, {pooled_ci_high:.4f}]")
