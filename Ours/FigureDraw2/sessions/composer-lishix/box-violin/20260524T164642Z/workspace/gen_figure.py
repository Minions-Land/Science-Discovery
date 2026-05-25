import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# ── Load data ──────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

order = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
labels = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
data = [d["samples"][c] for c in order]
metric = d.get("metric", "Relative cell viability")

# ── Palette ────────────────────────────────────────────────────────────────────
palette = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

rng = np.random.default_rng(42)

fig, ax = plt.subplots(figsize=(6.5, 5))

positions = np.arange(1, len(order) + 1)

# ── Violin ─────────────────────────────────────────────────────────────────────
vp = ax.violinplot(data, positions=positions, widths=0.6,
                   showmeans=False, showmedians=False, showextrema=False)
for body, color in zip(vp["bodies"], palette):
    body.set_facecolor(color)
    body.set_alpha(0.35)
    body.set_edgecolor("none")

# ── Box (thin, no fliers) ──────────────────────────────────────────────────────
bp = ax.boxplot(data, positions=positions, widths=0.18,
                patch_artist=True, showfliers=False,
                medianprops=dict(color="white", linewidth=2.2, solid_capstyle="round"),
                whiskerprops=dict(color="#333333", linewidth=1.2),
                capprops=dict(color="#333333", linewidth=1.2),
                boxprops=dict(linewidth=0))
for patch, color in zip(bp["boxes"], palette):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)

# ── Jittered points ────────────────────────────────────────────────────────────
for pos, vals, color in zip(positions, data, palette):
    jitter = rng.uniform(-0.22, 0.22, size=len(vals))
    ax.scatter(pos + jitter, vals,
               color=color, alpha=0.35, s=14, linewidths=0,
               zorder=3)

# ── Mann-Whitney U significance brackets vs Control ───────────────────────────
ctrl = data[0]
bracket_y_start = max(max(g) for g in data) + 0.08
step = 0.14

sig_pairs = []
for i in range(1, len(order)):
    u_stat, p = stats.mannwhitneyu(ctrl, data[i], alternative="two-sided")
    if p < 0.05:
        sig_pairs.append((0, i, p))

def sig_label(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    return "*"

for k, (i, j, p) in enumerate(sig_pairs):
    y = bracket_y_start + k * step
    x1, x2 = positions[i], positions[j]
    ax.plot([x1, x1, x2, x2], [y - 0.03, y, y, y - 0.03],
            color="#444444", linewidth=1.0)
    ax.text((x1 + x2) / 2, y + 0.01, sig_label(p),
            ha="center", va="bottom", fontsize=10, color="#444444")

# ── Axes ───────────────────────────────────────────────────────────────────────
ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_xlim(0.35, len(order) + 0.65)
ax.set_ylabel(metric.capitalize(), fontsize=11)
ax.set_title("Relative Cell Viability Across Treatment Conditions", fontsize=12, pad=10)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.set_tick_params(labelsize=9)

ax.axhline(1.0, color="#aaaaaa", linewidth=0.8, linestyle="--", zorder=0)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
