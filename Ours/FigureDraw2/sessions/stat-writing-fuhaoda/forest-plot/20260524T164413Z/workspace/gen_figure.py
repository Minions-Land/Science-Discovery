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

# 95% confidence intervals
z = 1.96
ci_lo = effects - z * se
ci_hi = effects + z * se

# Inverse-variance fixed-effect pooled estimate
weights = 1.0 / se**2
pooled = np.sum(weights * effects) / np.sum(weights)
pooled_se = 1.0 / np.sqrt(np.sum(weights))
pooled_lo = pooled - z * pooled_se
pooled_hi = pooled + z * pooled_se

n = len(studies)
# Rows: studies top-to-bottom, then a gap, then pooled
y_studies = list(range(n, 0, -1))   # n down to 1
y_pooled = -1                        # below gap

fig, ax = plt.subplots(figsize=(7, 6))
ax.set_xlim(-0.6, 1.0)

# Study-weight marker sizes (scaled to relative weight)
rel_w = weights / weights.max()
marker_sizes = 5 + rel_w * 10   # 5–15 pt^2-ish scale

for i, (y, eff, lo, hi, ms) in enumerate(
    zip(y_studies, effects, ci_lo, ci_hi, marker_sizes)
):
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.2)
    ax.plot(eff, y, "s", color="#1a6faf", markersize=ms, zorder=3)

# Diamond for pooled estimate
diamond_hw = 0.35   # half-height
diamond_x = [pooled_lo, pooled, pooled_hi, pooled, pooled_lo]
diamond_y = [y_pooled, y_pooled + diamond_hw, y_pooled, y_pooled - diamond_hw, y_pooled]
ax.fill(diamond_x, diamond_y, color="#c0392b", zorder=3)
ax.plot(diamond_x, diamond_y, color="#c0392b", lw=1.0, zorder=3)

# Vertical line at 0
ax.axvline(0, color="black", lw=0.8, ls="--", zorder=2)

# Study labels (left of plot)
for y, name in zip(y_studies, studies):
    ax.text(-0.62, y, name, va="center", ha="left", fontsize=8)

# Effect + CI text (right of plot)
for y, eff, lo, hi in zip(y_studies, effects, ci_lo, ci_hi):
    ax.text(1.02, y, f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", ha="left", fontsize=7, transform=ax.get_yaxis_transform(),
            clip_on=False)

ax.text(1.02, y_pooled,
        f"{pooled:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]",
        va="center", ha="left", fontsize=7, fontweight="bold",
        transform=ax.get_yaxis_transform(), clip_on=False)

# Column headers
ax.text(1.02, n + 1, "Effect [95% CI]",
        va="center", ha="left", fontsize=7, fontstyle="italic",
        transform=ax.get_yaxis_transform(), clip_on=False)
ax.text(-0.62, n + 1, "Study",
        va="center", ha="left", fontsize=8, fontstyle="italic")

# Pooled label
ax.text(-0.62, y_pooled, "Pooled (FE)", va="center", ha="left",
        fontsize=8, fontweight="bold")

# Separator line between studies and pooled
ax.axhline(0.5, color="black", lw=0.7, ls="-")

# Axes formatting
ax.set_yticks([])
ax.set_xlabel(xlabel, fontsize=9)
ax.set_ylim(y_pooled - 0.8, n + 1.5)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig("figure.pdf", bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print(f"Pooled estimate: {pooled:.4f} (SE {pooled_se:.4f}), 95% CI [{pooled_lo:.4f}, {pooled_hi:.4f}]")
