import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load data
with open("data.json") as f:
    data = json.load(f)

studies = data["studies"]
effects = np.array(data["effects"])
se = np.array(data["se"])
xlabel = data["label"]

n = len(studies)
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# Inverse-variance weighted pooled estimate (fixed-effects)
weights = 1.0 / se**2
pooled_effect = np.sum(weights * effects) / np.sum(weights)
pooled_se = np.sqrt(1.0 / np.sum(weights))
pooled_lo = pooled_effect - 1.96 * pooled_se
pooled_hi = pooled_effect + 1.96 * pooled_se

# Normalize weights for marker sizes
rel_weights = weights / weights.max()

# ── Layout ────────────────────────────────────────────────────────────────────
fig_h = 0.45 * (n + 3)
fig, ax = plt.subplots(figsize=(8, fig_h))

y_positions = list(range(n, 0, -1))   # top study = highest y
y_pooled = 0                           # diamond at y = 0

# ── Per-study CI lines & squares ─────────────────────────────────────────────
for i, (y, eff, lo, hi, rw) in enumerate(
    zip(y_positions, effects, ci_lo, ci_hi, rel_weights)
):
    ax.plot([lo, hi], [y, y], color="steelblue", lw=1.4, zorder=2)
    sq_size = max(50, 220 * rw)
    ax.scatter(eff, y, s=sq_size, marker="s", color="steelblue",
               zorder=3, linewidths=0)

# ── Pooled diamond ────────────────────────────────────────────────────────────
diamond_h = 0.38
diamond = mpatches.FancyArrowPatch(
    posA=(pooled_lo, y_pooled),
    posB=(pooled_hi, y_pooled),
    arrowstyle=mpatches.ArrowStyle.Simple(
        head_width=0, head_length=0, tail_width=0),
)
# Draw diamond manually
dx = (pooled_hi - pooled_lo) / 2
cx = pooled_effect
verts = [
    (pooled_lo, y_pooled),
    (cx,        y_pooled + diamond_h),
    (pooled_hi, y_pooled),
    (cx,        y_pooled - diamond_h),
    (pooled_lo, y_pooled),
]
xs, ys = zip(*verts)
ax.fill(xs, ys, color="firebrick", zorder=4)
ax.plot(xs, ys, color="firebrick", lw=1, zorder=5)

# ── Reference line at 0 ───────────────────────────────────────────────────────
ax.axvline(0, color="black", lw=0.8, ls="--", zorder=1)

# ── Annotations: effect [95% CI] on right ────────────────────────────────────
x_annot = ax.get_xlim()[1] if ax.get_xlim()[1] > ci_hi.max() + 0.15 else ci_hi.max() + 0.15
x_annot = ci_hi.max() + 0.12

for y, eff, lo, hi in zip(y_positions, effects, ci_lo, ci_hi):
    ax.text(x_annot, y,
            f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", ha="left", fontsize=7.5, color="black")

# Pooled annotation
ax.text(x_annot, y_pooled,
        f"{pooled_effect:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]",
        va="center", ha="left", fontsize=7.5, fontweight="bold", color="firebrick")

# ── Y-axis labels ────────────────────────────────────────────────────────────
ax.set_yticks(y_positions + [y_pooled])
ax.set_yticklabels(studies + ["Pooled (FE)"], fontsize=8.5)
ax.tick_params(axis="y", length=0)

# ── Divider above pooled ──────────────────────────────────────────────────────
ax.axhline(0.6, color="gray", lw=0.7, ls="-")

# ── X-axis ────────────────────────────────────────────────────────────────────
ax.set_xlabel(xlabel, fontsize=9)
ax.set_title("Forest Plot of Study Effect Sizes", fontsize=11, pad=8)

# ── Axis limits ──────────────────────────────────────────────────────────────
x_pad = 0.08
ax.set_xlim(ci_lo.min() - x_pad, x_annot + 0.72)
ax.set_ylim(-0.7, n + 0.8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("figure.pdf", dpi=150, bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
print(f"Pooled effect (FE): {pooled_effect:.4f} [{pooled_lo:.4f}, {pooled_hi:.4f}]")
