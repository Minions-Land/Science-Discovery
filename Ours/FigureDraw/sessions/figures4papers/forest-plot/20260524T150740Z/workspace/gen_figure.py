import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── load data ──────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

studies = d["studies"]
effects = np.array(d["effects"])
se      = np.array(d["se"])
xlabel  = d["label"]

n = len(studies)

# ── fixed-effects pooled estimate (inverse-variance weighting) ────────────────
w      = 1.0 / se**2
pooled = np.sum(w * effects) / np.sum(w)
se_pooled = 1.0 / np.sqrt(np.sum(w))
z95    = 1.96
ci_lo  = effects - z95 * se
ci_hi  = effects + z95 * se
pool_lo = pooled - z95 * se_pooled
pool_hi = pooled + z95 * se_pooled

# marker sizes proportional to weight (capped for aesthetics)
w_norm = w / w.max()
marker_sizes = 4 + 8 * w_norm   # range ~4–12 pt radius

# ── layout ────────────────────────────────────────────────────────────────────
fig_h = 0.45 * (n + 3)          # dynamic height
fig, ax = plt.subplots(figsize=(8, fig_h))

y_studies = np.arange(n, 0, -1)  # n … 1 (top to bottom)
y_pool    = 0                     # diamond below a gap

# study rows
for i, (y, lo, eff, hi, ms) in enumerate(
        zip(y_studies, ci_lo, effects, ci_hi, marker_sizes)):
    ax.plot([lo, hi], [y, y], color="#444444", lw=1.2, zorder=2)   # CI line
    ax.plot(eff, y, "s", color="#1f77b4",                           # square marker
            markersize=ms, markeredgecolor="white", markeredgewidth=0.5,
            zorder=3)

# vertical reference line at 0
ax.axvline(0, color="black", lw=0.8, linestyle="--", zorder=1)

# pooled diamond
dw = (pool_hi - pool_lo) / 2          # half-width
dh = 0.35                              # half-height
diamond_x = [pooled - dw, pooled,  pooled + dw, pooled,  pooled - dw]
diamond_y = [y_pool,       y_pool + dh, y_pool, y_pool - dh, y_pool]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=4)
ax.plot(diamond_x, diamond_y, color="#8b0000", lw=0.8, zorder=5)

# ── axes formatting ───────────────────────────────────────────────────────────
ytick_labels = list(studies) + ["", "Pooled (FE)"]
ytick_pos    = list(y_studies) + [0.8, 0]   # slight gap then diamond row

ax.set_yticks(ytick_pos)
ax.set_yticklabels(ytick_labels, fontsize=9)
ax.set_xlabel(xlabel, fontsize=9)
ax.set_ylim(-0.8, n + 0.6)

# x-axis: expand a bit beyond the data range
x_all = np.concatenate([ci_lo, ci_hi, [pool_lo, pool_hi]])
xpad  = (x_all.max() - x_all.min()) * 0.08
ax.set_xlim(x_all.min() - xpad, x_all.max() + xpad)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# annotate pooled estimate in the right margin
ax.text(x_all.max() + xpad * 0.4, y_pool,
        f"{pooled:.3f} [{pool_lo:.3f}, {pool_hi:.3f}]",
        va="center", ha="left", fontsize=7.5, color="#8b0000")

# column headers
ax.text(x_all.max() + xpad * 0.4, n + 0.3,
        "Effect [95% CI]", va="bottom", ha="left", fontsize=7.5,
        fontweight="bold")

# individual effect labels (right margin)
for y, eff, lo, hi in zip(y_studies, effects, ci_lo, ci_hi):
    ax.text(x_all.max() + xpad * 0.4, y,
            f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            va="center", ha="left", fontsize=7)

ax.set_title("Meta-analysis Forest Plot", fontsize=11, pad=8)

plt.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg",           bbox_inches="tight")

print(f"Pooled FE estimate: {pooled:.4f}  SE: {se_pooled:.4f}  "
      f"95% CI [{pool_lo:.4f}, {pool_hi:.4f}]")
print("Saved figure.pdf / figure.png / figure.svg")
