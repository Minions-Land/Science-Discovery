import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

# Load data
with open("data.json") as f:
    data = json.load(f)

# ── Figure layout ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 8))
fig.patch.set_facecolor("white")

outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38,
                          top=0.94, bottom=0.08, left=0.06, right=0.97)
top   = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[0],
                                         width_ratios=[2, 1, 1], wspace=0.38)
bot   = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[1])

ax_a = fig.add_subplot(top[0])
ax_b = fig.add_subplot(top[1])
ax_c = fig.add_subplot(top[2])
ax_d = fig.add_subplot(bot[0])

LABEL_KW = dict(fontsize=13, fontweight="bold", fontfamily="sans-serif",
                va="top", ha="left")
ACCENT  = "#2563EB"
ACCENT2 = "#F59E0B"
GRAY    = "#6B7280"
LIGHT   = "#EFF6FF"

# ── Panel A — method overview ──────────────────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis("off")

stages = [
    (1.1, 3.0, "Input\nEncoding",  "#DBEAFE", "#1D4ED8"),
    (4.3, 3.0, "Adaptive\nRouting", "#FEF3C7", "#D97706"),
    (7.5, 3.0, "Skill-Gated\nDecoding", "#D1FAE5", "#065F46"),
]
box_w, box_h = 2.0, 1.5

for (cx, cy, label, fc, ec) in stages:
    box = FancyBboxPatch((cx - box_w/2, cy - box_h/2), box_w, box_h,
                         boxstyle="round,pad=0.12", linewidth=1.8,
                         edgecolor=ec, facecolor=fc, zorder=3)
    ax_a.add_patch(box)
    ax_a.text(cx, cy, label, ha="center", va="center",
              fontsize=9.5, fontweight="bold", color=ec, zorder=4,
              linespacing=1.35)

# Arrows between stages
for x0, x1 in [(2.1, 3.3), (5.3, 6.5)]:
    ax_a.annotate("", xy=(x1, 3.0), xytext=(x0, 3.0),
                  arrowprops=dict(arrowstyle="-|>", color="#374151",
                                  lw=1.6, mutation_scale=14), zorder=2)

# Memory + skill side-feeds into middle box
for (sx, sy, tx, ty, lbl) in [
    (4.3, 5.2, 4.3, 3.75, "Memory\nBank"),
    (4.3, 0.8, 4.3, 2.25, "Skill\nLibrary"),
]:
    ax_a.annotate("", xy=(tx, ty), xytext=(sx, sy),
                  arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                  lw=1.3, linestyle="dashed",
                                  mutation_scale=11), zorder=2)
    ax_a.text(sx, sy + (0.28 if sy > 3 else -0.28), lbl,
              ha="center", va="center", fontsize=8, color=GRAY,
              fontweight="semibold")

# Output arrow + label
ax_a.annotate("", xy=(9.6, 3.0), xytext=(8.5, 3.0),
              arrowprops=dict(arrowstyle="-|>", color="#374151",
                              lw=1.6, mutation_scale=14), zorder=2)
ax_a.text(9.75, 3.0, "Output", ha="left", va="center",
          fontsize=8.5, color="#111827", fontweight="semibold")

# Title inside panel
ax_a.text(5.0, 5.7, "3-Stage Pipeline Overview",
          ha="center", va="top", fontsize=10.5, fontweight="bold",
          color="#111827")

ax_a.text(-0.02, 1.01, "A", transform=ax_a.transAxes, **LABEL_KW)

# ── Panel B — ablation bars ────────────────────────────────────────────────────
pb = data["panel_b"]
items  = pb["items"]
vals   = pb["values"]
colors = [ACCENT if i == 0 else GRAY for i in range(len(items))]
bars = ax_b.barh(items, vals, color=colors, height=0.55, edgecolor="white", linewidth=0.6)
ax_b.set_xlabel("Score", fontsize=8.5)
ax_b.set_title("Ablation", fontsize=9.5, fontweight="bold", pad=5)
ax_b.set_xlim(50, 68)
ax_b.xaxis.set_tick_params(labelsize=7.5)
ax_b.yaxis.set_tick_params(labelsize=8)
ax_b.spines[["top", "right"]].set_visible(False)
for bar, v in zip(bars, vals):
    ax_b.text(v + 0.15, bar.get_y() + bar.get_height()/2,
              f"{v:.1f}", va="center", fontsize=7.5, color="#111827")
ax_b.text(-0.18, 1.06, "B", transform=ax_b.transAxes, **LABEL_KW)

# ── Panel C — training curves ─────────────────────────────────────────────────
pc = data["panel_c"]
steps    = pc["steps"]
baseline = pc["Baseline"]
ours     = pc["Ours"]
ax_c.plot(steps, baseline, color=GRAY,   lw=1.5, label="Baseline", linestyle="--")
ax_c.plot(steps, ours,     color=ACCENT, lw=1.8, label="Ours")
ax_c.set_xlabel("Step (×10³)", fontsize=8.5)
ax_c.set_ylabel("Loss",        fontsize=8.5)
ax_c.set_title("Training Trend", fontsize=9.5, fontweight="bold", pad=5)
ax_c.legend(fontsize=7.5, frameon=False)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.xaxis.set_tick_params(labelsize=7.5)
ax_c.yaxis.set_tick_params(labelsize=7.5)
ax_c.text(-0.22, 1.06, "C", transform=ax_c.transAxes, **LABEL_KW)

# ── Panel D — 5×5 heatmap ─────────────────────────────────────────────────────
pd_ = data["panel_d"]
matrix = np.array(pd_["matrix"])
im = ax_d.imshow(matrix, cmap="viridis", aspect="auto", vmin=0, vmax=1)
ax_d.set_xticks(range(5)); ax_d.set_xticklabels(pd_["x"], fontsize=9)
ax_d.set_yticks(range(5)); ax_d.set_yticklabels(pd_["y"], fontsize=9)
ax_d.set_xlabel("Sweep Parameter S", fontsize=9.5)
ax_d.set_ylabel("Sweep Parameter P", fontsize=9.5)
ax_d.set_title("Sensitivity Sweep (5×5)", fontsize=10, fontweight="bold", pad=6)
for i in range(5):
    for j in range(5):
        v = matrix[i, j]
        ax_d.text(j, i, f"{v:.2f}", ha="center", va="center",
                  fontsize=8.5, color="white" if v < 0.6 else "black",
                  fontweight="semibold")
cbar = fig.colorbar(im, ax=ax_d, fraction=0.018, pad=0.02)
cbar.ax.tick_params(labelsize=8)
cbar.set_label("Score", fontsize=8.5)
ax_d.text(-0.04, 1.06, "D", transform=ax_d.transAxes, **LABEL_KW)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
