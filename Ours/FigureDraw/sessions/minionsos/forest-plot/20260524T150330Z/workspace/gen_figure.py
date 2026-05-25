import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# Load data
with open("data.json") as f:
    d = json.load(f)

studies = d["studies"]
effects = np.array(d["effects"])
se = np.array(d["se"])
xlabel = d["label"]

# Fixed-effects pooled estimate (inverse-variance weighting)
weights = 1.0 / se**2
pooled_effect = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_ci_lo = pooled_effect - 1.96 * pooled_se
pooled_ci_hi = pooled_effect + 1.96 * pooled_se

# Per-study 95% CIs
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# Weight percentages for display
w_pct = 100 * weights / np.sum(weights)

n = len(studies)
# y positions: studies top-to-bottom, then gap, then pooled
y_studies = np.arange(n, 0, -1, dtype=float)  # n down to 1
y_pooled = -0.5

fig, ax = plt.subplots(figsize=(9, 7))

# --- Study rows ---
for i, (study, eff, lo, hi, wp, y) in enumerate(
    zip(studies, effects, ci_lo, ci_hi, w_pct, y_studies)
):
    # CI line
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.2, zorder=2)
    # Square marker sized by weight
    sq_size = 4 + wp * 0.35
    ax.plot(eff, y, "s", color="#1f77b4", markersize=sq_size, zorder=3)

    # Labels on left
    ax.text(-1.05, y, study, va="center", ha="left", fontsize=9)
    # Effect and CI on right
    ax.text(
        1.05, y,
        f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
        va="center", ha="left", fontsize=8, color="#444444",
    )
    # Weight on far right
    ax.text(
        1.75, y,
        f"{wp:.1f}%",
        va="center", ha="left", fontsize=8, color="#666666",
    )

# --- Separator line ---
ax.axhline(y=0.5, color="#aaaaaa", lw=0.8, linestyle="--")

# --- Pooled diamond ---
diamond_half_w = (pooled_ci_hi - pooled_ci_lo) / 2
diamond_half_h = 0.35
diamond_x = [pooled_ci_lo, pooled_effect, pooled_ci_hi, pooled_effect, pooled_ci_lo]
diamond_y = [y_pooled, y_pooled + diamond_half_h, y_pooled,
             y_pooled - diamond_half_h, y_pooled]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=3)
ax.plot(diamond_x, diamond_y, color="#8b0000", lw=1.0, zorder=4)

# Pooled label
ax.text(-1.05, y_pooled, "Pooled (FE)", va="center", ha="left",
        fontsize=9, fontweight="bold")
ax.text(
    1.05, y_pooled,
    f"{pooled_effect:.3f} [{pooled_ci_lo:.3f}, {pooled_ci_hi:.3f}]",
    va="center", ha="left", fontsize=8, fontweight="bold", color="#8b0000",
)
ax.text(1.75, y_pooled, "100%", va="center", ha="left",
        fontsize=8, fontweight="bold", color="#666666")

# --- Null line ---
ax.axvline(x=0, color="#555555", lw=1.0, linestyle="-", zorder=1)

# --- Column headers ---
header_y = n + 0.8
ax.text(-1.05, header_y, "Study", va="center", ha="left",
        fontsize=9, fontweight="bold")
ax.text(1.05, header_y, "Effect [95% CI]", va="center", ha="left",
        fontsize=9, fontweight="bold")
ax.text(1.75, header_y, "Weight", va="center", ha="left",
        fontsize=9, fontweight="bold")

# --- Axes formatting ---
ax.set_xlim(-1.05, 2.1)
ax.set_ylim(y_pooled - 0.8, n + 1.2)
ax.set_xlabel(xlabel, fontsize=9)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(axis="x", labelsize=8)

plt.tight_layout()
plt.savefig("figure.pdf", bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled FE estimate: {pooled_effect:.4f} (SE={pooled_se:.4f}), "
      f"95% CI [{pooled_ci_lo:.4f}, {pooled_ci_hi:.4f}]")
