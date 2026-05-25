import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

studies = d["studies"]
effects = np.array(d["effects"])
se = np.array(d["se"])
xlabel = d["label"]

n = len(studies)
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# ── Fixed-effects pooled estimate (inverse-variance weighting) ─────────────
w = 1.0 / se**2
pool_effect = np.sum(w * effects) / np.sum(w)
pool_se = np.sqrt(1.0 / np.sum(w))
pool_lo = pool_effect - 1.96 * pool_se
pool_hi = pool_effect + 1.96 * pool_se

# ── Layout ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))

y_positions = list(range(n, 0, -1))   # study n at top, study 1 at bottom
y_pool = 0                             # pooled at very bottom, below a gap

# Per-study CI lines + markers
for i, (y, eff, lo, hi) in enumerate(zip(y_positions, effects, ci_lo, ci_hi)):
    ax.plot([lo, hi], [y, y], color="#333333", lw=1.5, solid_capstyle="round")
    ax.plot(eff, y, "s", color="#1f77b4", ms=7, zorder=3)

# Separator line
ax.axhline(y=0.5, color="#888888", lw=0.8, linestyle="--")

# Diamond for pooled estimate
diamond_half_h = 0.35
diamond_x = [pool_lo, pool_effect, pool_hi, pool_effect, pool_lo]
diamond_y = [y_pool, y_pool + diamond_half_h, y_pool, y_pool - diamond_half_h, y_pool]
ax.fill(diamond_x, diamond_y, color="#d62728", zorder=4)

# Vertical line at zero (null effect)
y_max = n + 0.7
ax.axvline(x=0, color="#555555", lw=1.0, linestyle=":")

# ── Axes formatting ──────────────────────────────────────────────────────────
all_ticks = list(y_positions) + [y_pool]
all_labels = studies + [f"Pooled (IV-FE)\n{pool_effect:.3f} [{pool_lo:.3f}, {pool_hi:.3f}]"]
ax.set_yticks(all_ticks)
ax.set_yticklabels(all_labels, fontsize=9)
ax.set_ylim(y_pool - 0.8, n + 0.7)

ax.set_xlabel(xlabel, fontsize=10)
ax.set_title("Forest Plot — Meta-analysis of 12 Studies", fontsize=11, fontweight="bold")

# Annotate effect sizes and 95% CI on the right side
x_annot = max(ci_hi) + 0.05
ax.text(x_annot, n + 0.55, "Effect (95% CI)", fontsize=8, va="center", ha="left",
        style="italic", color="#444444")
for y, eff, lo, hi in zip(y_positions, effects, ci_lo, ci_hi):
    ax.text(x_annot, y, f"{eff:.3f} [{lo:.3f}, {hi:.3f}]",
            fontsize=7.5, va="center", ha="left", color="#333333")
ax.text(x_annot, y_pool, f"{pool_effect:.3f} [{pool_lo:.3f}, {pool_hi:.3f}]",
        fontsize=8, va="center", ha="left", color="#d62728", fontweight="bold")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Extend x-axis to fit annotations
ax.set_xlim(min(ci_lo) - 0.15, x_annot + 0.55)

plt.tight_layout()

# ── Save ─────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
print(f"Pooled effect: {pool_effect:.4f}  95% CI [{pool_lo:.4f}, {pool_hi:.4f}]")
