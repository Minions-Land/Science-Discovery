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

# Inverse-variance weights and pooled estimate (fixed-effects)
w = 1.0 / se**2
pooled = np.sum(w * effects) / np.sum(w)
pooled_se = np.sqrt(1.0 / np.sum(w))
pooled_ci_lo = pooled - 1.96 * pooled_se
pooled_ci_hi = pooled + 1.96 * pooled_se

ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

n = len(studies)
y_pos = list(range(n, 0, -1))  # top to bottom

# Marker sizes proportional to weight (normalised)
w_norm = w / w.max()
marker_sizes = 6 + 8 * w_norm  # range ~6–14 pt

fig, ax = plt.subplots(figsize=(8, 6))

# Per-study CI lines and squares
for i, (y, eff, lo, hi, ms) in enumerate(zip(y_pos, effects, ci_lo, ci_hi, marker_sizes)):
    ax.plot([lo, hi], [y, y], color="#333333", linewidth=1.2, zorder=2)
    ax.plot(eff, y, "s", color="#1f77b4", markersize=ms, zorder=3)

# Pooled diamond (y = 0)
y_pool = 0
dh = 0.35
diamond_x = [pooled_ci_lo, pooled, pooled_ci_hi, pooled, pooled_ci_lo]
diamond_y = [y_pool, y_pool + dh, y_pool, y_pool - dh, y_pool]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=4)
ax.plot(diamond_x, diamond_y, color="#8b0000", linewidth=0.8, zorder=5)

# Vertical line at 0
ax.axvline(0, color="black", linewidth=0.8, linestyle="--", zorder=1)

# Y-axis labels
all_y = y_pos + [y_pool]
all_labels = studies + ["Pooled (FE)"]
ax.set_yticks(all_y)
ax.set_yticklabels(all_labels, fontsize=9)

# Annotate effect sizes on the right
x_right = max(ci_hi.max(), pooled_ci_hi) + 0.05
for y, eff, lo, hi in zip(y_pos, effects, ci_lo, ci_hi):
    ax.text(x_right, y, f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", ha="left", fontsize=7.5, color="#333333")
ax.text(x_right, y_pool,
        f"{pooled:.3f} [{pooled_ci_lo:.3f}, {pooled_ci_hi:.3f}]",
        va="center", ha="left", fontsize=7.5, fontweight="bold", color="#8b0000")

ax.set_xlabel(xlabel, fontsize=10)
ax.set_title("Forest Plot — Meta-analysis (Fixed-Effects)", fontsize=11, pad=10)

# Extend x-axis to fit annotations
x_max = x_right + 0.55
x_min = min(ci_lo.min(), pooled_ci_lo) - 0.1
ax.set_xlim(x_min, x_max)
ax.set_ylim(-0.8, n + 0.8)

# Separator line above pooled
ax.axhline(0.6, color="#aaaaaa", linewidth=0.8, linestyle="-")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled estimate: {pooled:.4f} (95% CI [{pooled_ci_lo:.4f}, {pooled_ci_hi:.4f}])")
