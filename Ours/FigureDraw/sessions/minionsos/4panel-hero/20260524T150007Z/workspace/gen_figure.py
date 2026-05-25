import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.gridspec import GridSpec

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

# ── style ───────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 8,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

BLUE   = "#2563EB"
ORANGE = "#F97316"
GRAY   = "#6B7280"
LIGHT  = "#EFF6FF"
DARK   = "#1E3A5F"

fig = plt.figure(figsize=(10, 6.5))
gs  = GridSpec(2, 3, figure=fig, width_ratios=[2, 1, 1],
               hspace=0.42, wspace=0.38,
               left=0.06, right=0.97, top=0.93, bottom=0.09)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[1, :])

# ── panel-label helper ──────────────────────────────────────────────────────
def panel_label(ax, letter):
    ax.text(-0.08, 1.08, letter, transform=ax.transAxes,
            fontsize=11, fontweight="bold", fontfamily="sans-serif",
            va="top", ha="left")

# ═══════════════════════════════════════════════════════════════════════════
# PANEL A – conceptual 3-stage pipeline diagram
# ═══════════════════════════════════════════════════════════════════════════
ax_a.set_xlim(0, 1); ax_a.set_ylim(0, 1); ax_a.axis("off")

stages = [
    ("Stage 1\nEncode", 0.10, BLUE),
    ("Stage 2\nReason", 0.42, ORANGE),
    ("Stage 3\nDecode", 0.74, BLUE),
]
box_w, box_h = 0.22, 0.22
box_y = 0.52

for label, cx, color in stages:
    rect = FancyBboxPatch((cx - box_w/2, box_y - box_h/2), box_w, box_h,
                          boxstyle="round,pad=0.02", linewidth=1.2,
                          edgecolor=color, facecolor=LIGHT)
    ax_a.add_patch(rect)
    ax_a.text(cx, box_y, label, ha="center", va="center",
              fontsize=7.5, fontweight="bold", color=DARK, linespacing=1.4)

# arrows between stages
for x0, x1 in [(0.21, 0.31), (0.53, 0.63)]:
    ax_a.annotate("", xy=(x1, box_y), xytext=(x0, box_y),
                  arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                  lw=1.2, mutation_scale=10))

# output box
out_cx = 0.88
out_rect = FancyBboxPatch((out_cx - 0.09, box_y - 0.10), 0.18, 0.20,
                           boxstyle="round,pad=0.02", linewidth=1.2,
                           edgecolor="#10B981", facecolor="#ECFDF5")
ax_a.add_patch(out_rect)
ax_a.text(out_cx, box_y, "Output", ha="center", va="center",
          fontsize=7.5, fontweight="bold", color="#065F46")
ax_a.annotate("", xy=(out_cx - 0.09, box_y), xytext=(0.85, box_y),
              arrowprops=dict(arrowstyle="-|>", color=GRAY,
                              lw=1.2, mutation_scale=10))

# input label
ax_a.text(0.01, box_y, "Input", ha="left", va="center",
          fontsize=7.5, color=GRAY, style="italic")
ax_a.annotate("", xy=(stages[0][1] - box_w/2, box_y),
              xytext=(0.07, box_y),
              arrowprops=dict(arrowstyle="-|>", color=GRAY,
                              lw=1.2, mutation_scale=10))

# memory / skill feedback arcs
for label, cx, dy, col in [("Memory", 0.42, -0.18, ORANGE),
                             ("Skills",  0.74, -0.18, BLUE)]:
    ax_a.annotate("", xy=(cx - 0.12, box_y - box_h/2),
                  xytext=(cx + 0.12, box_y - box_h/2),
                  arrowprops=dict(arrowstyle="<|-", color=col, lw=0.9,
                                  connectionstyle=f"arc3,rad=0.4",
                                  mutation_scale=8))
    ax_a.text(cx, box_y - box_h/2 + dy, label, ha="center", va="top",
              fontsize=6.5, color=col, style="italic")

# title
ax_a.text(0.5, 0.97, "Method Overview", ha="center", va="top",
          fontsize=8.5, fontweight="bold", color=DARK,
          transform=ax_a.transAxes)

panel_label(ax_a, "A")

# ═══════════════════════════════════════════════════════════════════════════
# PANEL B – ablation bars
# ═══════════════════════════════════════════════════════════════════════════
items  = d["panel_b"]["items"]
values = d["panel_b"]["values"]
colors = [BLUE if i == 0 else GRAY for i in range(len(items))]

bars = ax_b.barh(items[::-1], values[::-1], color=colors[::-1],
                 height=0.55, edgecolor="white", linewidth=0.5)
for bar, val in zip(bars, values[::-1]):
    ax_b.text(val + 0.4, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=6.5, color=DARK)

ax_b.set_xlim(45, 70)
ax_b.set_xlabel("Accuracy (%)", fontsize=7)
ax_b.set_title("Ablation Study", fontsize=8, fontweight="bold", pad=4)
ax_b.tick_params(axis="y", labelsize=7)
ax_b.tick_params(axis="x", labelsize=6.5)
ax_b.axvline(values[0], color=BLUE, lw=0.8, ls="--", alpha=0.5)
panel_label(ax_b, "B")

# ═══════════════════════════════════════════════════════════════════════════
# PANEL C – training curves
# ═══════════════════════════════════════════════════════════════════════════
steps    = d["panel_c"]["steps"]
baseline = d["panel_c"]["Baseline"]
ours     = d["panel_c"]["Ours"]

ax_c.plot(steps, baseline, color=GRAY,   lw=1.4, label="Baseline", zorder=2)
ax_c.plot(steps, ours,     color=ORANGE, lw=1.4, label="Ours",     zorder=3)
ax_c.fill_between(steps, baseline, ours, alpha=0.12, color=ORANGE)

ax_c.set_xlabel("Training Step", fontsize=7)
ax_c.set_ylabel("Loss",          fontsize=7)
ax_c.set_title("Training Trend", fontsize=8, fontweight="bold", pad=4)
ax_c.legend(fontsize=6.5, frameon=False, loc="upper right")
ax_c.tick_params(labelsize=6.5)
panel_label(ax_c, "C")

# ═══════════════════════════════════════════════════════════════════════════
# PANEL D – 5×5 sensitivity heatmap
# ═══════════════════════════════════════════════════════════════════════════
matrix = np.array(d["panel_d"]["matrix"])
xlabels = d["panel_d"]["x"]
ylabels = d["panel_d"]["y"]

im = ax_d.imshow(matrix, aspect="auto", cmap="Blues", vmin=0, vmax=1,
                 interpolation="nearest")

ax_d.set_xticks(range(len(xlabels))); ax_d.set_xticklabels(xlabels, fontsize=8)
ax_d.set_yticks(range(len(ylabels))); ax_d.set_yticklabels(ylabels, fontsize=8)
ax_d.set_xlabel("Sweep Parameter S", fontsize=8)
ax_d.set_ylabel("Probe P",           fontsize=8)
ax_d.set_title("Sensitivity Sweep (5×5)", fontsize=8.5, fontweight="bold", pad=4)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        v = matrix[i, j]
        ax_d.text(j, i, f"{v:.2f}", ha="center", va="center",
                  fontsize=7.5, color="white" if v > 0.6 else DARK)

cbar = fig.colorbar(im, ax=ax_d, fraction=0.015, pad=0.01)
cbar.ax.tick_params(labelsize=7)
cbar.set_label("Score", fontsize=7)

panel_label(ax_d, "D")

# ── save ────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg",           bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
