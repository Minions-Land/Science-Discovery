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

n = len(studies)
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# Inverse-variance pooled estimate (fixed-effect)
weights = 1.0 / se**2
pooled = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_lo = pooled - 1.96 * pooled_se
pooled_hi = pooled + 1.96 * pooled_se

# --- Layout ---
fig_h = 0.45 * (n + 3)
fig, ax = plt.subplots(figsize=(7, fig_h))

# Y positions: studies top-to-bottom, then gap, then pooled
y_studies = np.arange(n, 0, -1, dtype=float)   # n, n-1, …, 1
y_pooled = -0.5

# Marker size proportional to weight (normalised)
w_norm = weights / weights.max()
marker_sizes = 6 + 60 * w_norm   # area proxy; tweak as needed

# Colour palette
study_color = "#2166ac"
pooled_color = "#d6604d"

# --- Study rows ---
for i, (y, eff, lo, hi, ms) in enumerate(
        zip(y_studies, effects, ci_lo, ci_hi, marker_sizes)):
    ax.plot([lo, hi], [y, y], color=study_color, lw=1.2, zorder=2)
    ax.plot(eff, y, "s", color=study_color, markersize=np.sqrt(ms),
            zorder=3)

# --- Pooled diamond ---
diamond_half_h = 0.28
diamond_x = [pooled_lo, pooled, pooled_hi, pooled, pooled_lo]
diamond_y = [y_pooled,
             y_pooled + diamond_half_h,
             y_pooled,
             y_pooled - diamond_half_h,
             y_pooled]
ax.fill(diamond_x, diamond_y, color=pooled_color, zorder=4)
ax.plot(diamond_x, diamond_y, color=pooled_color, lw=1, zorder=5)

# --- Null line ---
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# --- Axes dressing ---
all_y = list(y_studies) + [y_pooled]
ax.set_yticks(list(y_studies) + [y_pooled])
labels = list(studies) + [
    f"Pooled  {pooled:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]"
]
ax.set_yticklabels(labels, fontsize=9)
ax.tick_params(axis="y", length=0)

x_margin = 0.08
xmin = min(ci_lo.min(), pooled_lo) - x_margin
xmax = max(ci_hi.max(), pooled_hi) + x_margin
ax.set_xlim(xmin, xmax)
ax.set_ylim(y_pooled - 0.7, n + 0.7)

ax.set_xlabel(xlabel, fontsize=9)
ax.set_title("Forest Plot — Meta-Analysis", fontsize=11, fontweight="bold")

# Separator line above pooled
ax.axhline(0.2, color="gray", lw=0.6, linestyle="-")

# Annotation box with pooled stats
pooled_txt = (
    f"Pooled effect (fixed-effects IV)\n"
    f"OR = {pooled:.3f}  95 % CI [{pooled_lo:.3f}, {pooled_hi:.3f}]"
)
ax.text(xmax - 0.01, y_pooled, pooled_txt,
        ha="right", va="center", fontsize=7.5,
        bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow",
                  ec=pooled_color, lw=0.8))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"Pooled effect = {pooled:.4f}  SE = {pooled_se:.4f}  "
      f"95% CI [{pooled_lo:.4f}, {pooled_hi:.4f}]")
print("Saved figure.pdf, figure.png, figure.svg")
