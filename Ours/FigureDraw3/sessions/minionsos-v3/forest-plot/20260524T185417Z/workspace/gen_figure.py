import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

# --- load data ---
with open("data.json") as f:
    d = json.load(f)

studies = d["studies"]
effects = np.array(d["effects"])
se = np.array(d["se"])
xlabel = d["label"]

# --- inverse-variance pooled estimate ---
w = 1.0 / se**2
pooled_effect = np.sum(w * effects) / np.sum(w)
pooled_se = np.sqrt(1.0 / np.sum(w))
pooled_ci_lo = pooled_effect - 1.96 * pooled_se
pooled_ci_hi = pooled_effect + 1.96 * pooled_se

# per-study 95% CIs
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

n_studies = len(studies)
# y positions: studies top-to-bottom, then gap, then pooled
y_studies = np.arange(n_studies, 0, -1, dtype=float)   # n_studies … 1
y_pooled = -0.5

# marker size proportional to weight (visual weight)
w_norm = w / w.max()
marker_sizes = 4 + 6 * w_norm   # range ~4–10 pt

# --- figure ---
fig, ax = plt.subplots(figsize=(7, 6))

PALETTE = {
    "study":   "#0F4D92",
    "ci":      "#0F4D92",
    "pooled":  "#1A1A1A",
    "null":    "#888888",
    "diamond": "#1A1A1A",
}

# null line
ax.axvline(0, color=PALETTE["null"], linewidth=0.8, linestyle="--", zorder=1)

# per-study CI lines and point estimates
for i, (y, eff, lo, hi, ms) in enumerate(
        zip(y_studies, effects, ci_lo, ci_hi, marker_sizes)):
    ax.plot([lo, hi], [y, y], color=PALETTE["ci"], linewidth=0.9, zorder=2)
    ax.plot(eff, y, "o", color=PALETTE["study"],
            markersize=ms, zorder=3, markeredgewidth=0)

# pooled diamond
dw = (pooled_ci_hi - pooled_ci_lo) / 2   # half-width
dh = 0.35                                  # half-height
diamond_x = [pooled_ci_lo, pooled_effect, pooled_ci_hi, pooled_effect, pooled_ci_lo]
diamond_y = [y_pooled, y_pooled + dh, y_pooled, y_pooled - dh, y_pooled]
ax.fill(diamond_x, diamond_y, color=PALETTE["diamond"], zorder=3)

# separator line between studies and pooled
ax.axhline(0.3, color="#cccccc", linewidth=0.6, xmin=0.0, xmax=1.0)

# y-axis labels
ytick_pos = list(y_studies) + [y_pooled]
ytick_labels = list(studies) + ["Pooled (IV)"]
ax.set_yticks(ytick_pos)
ax.set_yticklabels(ytick_labels, fontsize=8)
ax.tick_params(axis="y", length=0)

# pooled label bold
labels = ax.get_yticklabels()
labels[-1].set_fontweight("bold")
labels[-1].set_fontsize(8.5)

# x axis
ax.set_xlabel(xlabel, fontsize=9)
ax.tick_params(axis="x", direction="out", length=2.5, width=0.6, labelsize=8)
ax.spines["left"].set_visible(False)

# annotate pooled estimate
ax.text(pooled_effect, y_pooled - dh - 0.25,
        f"{pooled_effect:.3f} [{pooled_ci_lo:.3f}, {pooled_ci_hi:.3f}]",
        ha="center", va="top", fontsize=7.5, color=PALETTE["pooled"])

# x limits with padding
xpad = 0.05
xmin = min(ci_lo.min(), pooled_ci_lo) - xpad
xmax = max(ci_hi.max(), pooled_ci_hi) + xpad
ax.set_xlim(xmin, xmax)
ax.set_ylim(y_pooled - 0.9, y_studies[0] + 0.6)

# "Favours control" / "Favours intervention" annotations
ax.text(-0.02, y_pooled - 0.85, "← Favours control",
        ha="right", va="bottom", fontsize=7, color="#555555",
        transform=ax.get_yaxis_transform())
ax.text(0.02, y_pooled - 0.85, "Favours intervention →",
        ha="left", va="bottom", fontsize=7, color="#555555",
        transform=ax.get_yaxis_transform())

fig.tight_layout()

out = Path(".")
fig.savefig(out / "figure.pdf", bbox_inches="tight")
fig.savefig(out / "figure.png", dpi=300, bbox_inches="tight")
fig.savefig(out / "figure.svg", bbox_inches="tight")
print(f"Pooled effect: {pooled_effect:.4f}  SE: {pooled_se:.4f}  "
      f"95% CI [{pooled_ci_lo:.4f}, {pooled_ci_hi:.4f}]")
