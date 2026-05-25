import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

CWD = Path(__file__).parent
with open(CWD / "data.json") as f:
    data = json.load(f)

# ── colour palette ──────────────────────────────────────────────────────────
C_BLUE   = "#2563EB"
C_ORANGE = "#F97316"
C_GRAY   = "#6B7280"
C_LIGHT  = "#EFF6FF"
C_DARK   = "#1E3A5F"
C_HEAT   = "YlOrRd"

LABEL_KW = dict(fontsize=11, fontweight="bold", fontfamily="sans-serif",
                transform=None, va="top", ha="left")

fig = plt.figure(figsize=(12, 7.5), dpi=150)
gs  = gridspec.GridSpec(2, 3, width_ratios=[2, 1, 1],
                        hspace=0.42, wspace=0.38,
                        left=0.06, right=0.97, top=0.95, bottom=0.08)

# ── Panel A: method overview ─────────────────────────────────────────────────
ax_a = fig.add_subplot(gs[0, 0])
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 5)
ax_a.axis("off")

def rounded_box(ax, x, y, w, h, label, sublabel="", fc=C_LIGHT, ec=C_BLUE, lw=1.5):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.12",
                         facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2 + (0.18 if sublabel else 0), label,
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=C_DARK, zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.22, sublabel,
                ha="center", va="center", fontsize=6.8, color=C_GRAY, zorder=4)

def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=C_DARK,
                                lw=1.4, mutation_scale=12), zorder=5)

# Stage boxes
stages = [
    (0.4,  2.0, 2.6, 1.2, "Stage 1",   "Encode"),
    (3.7,  2.0, 2.6, 1.2, "Stage 2",   "Attend + Mem"),
    (7.0,  2.0, 2.6, 1.2, "Stage 3",   "Decode"),
]
for (x, y, w, h, lbl, sub) in stages:
    rounded_box(ax_a, x, y, w, h, lbl, sub)

# Arrows between stages
arrow(ax_a, 3.0, 2.6, 3.7, 2.6)
arrow(ax_a, 6.3, 2.6, 7.0, 2.6)

# Input / output
ax_a.text(0.4, 4.35, "Input", ha="center", va="center",
          fontsize=8, color=C_GRAY)
ax_a.annotate("", xy=(0.4+0.85, 3.2), xytext=(0.4+0.85, 4.1),
              arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2,
                              mutation_scale=10), zorder=5)

ax_a.text(9.65, 4.35, "Output", ha="center", va="center",
          fontsize=8, color=C_GRAY)
ax_a.annotate("", xy=(9.65-0.85, 4.1), xytext=(9.65-0.85, 3.2),
              arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.2,
                              mutation_scale=10), zorder=5)

# Skill / residual annotations
ax_a.annotate("", xy=(5.0, 2.0), xytext=(5.0, 0.7),
              arrowprops=dict(arrowstyle="<->", color=C_ORANGE, lw=1.3,
                              mutation_scale=10), zorder=5)
ax_a.text(5.0, 0.42, "Residual + Skill", ha="center", va="center",
          fontsize=7.5, color=C_ORANGE, style="italic")

ax_a.set_title("Method Overview", fontsize=9, color=C_GRAY, pad=4)

# ── Panel B: ablation bars ───────────────────────────────────────────────────
ax_b = fig.add_subplot(gs[0, 1])
items  = data["panel_b"]["items"]
values = data["panel_b"]["values"]
colors = [C_BLUE if i == "full" else C_GRAY for i in items]
bars = ax_b.barh(items, values, color=colors, height=0.55, zorder=3)
ax_b.set_xlim(50, 68)
ax_b.axvline(values[0], color=C_BLUE, lw=0.8, ls="--", alpha=0.5)
for bar, val in zip(bars, values):
    ax_b.text(val + 0.2, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7.5, color=C_DARK)
ax_b.set_xlabel("Score", fontsize=8)
ax_b.set_title("Ablation", fontsize=9, color=C_GRAY, pad=4)
ax_b.tick_params(labelsize=7.5)
ax_b.spines[["top", "right"]].set_visible(False)
ax_b.grid(axis="x", lw=0.4, alpha=0.4, zorder=0)

# ── Panel C: training curves ─────────────────────────────────────────────────
ax_c = fig.add_subplot(gs[0, 2])
steps    = data["panel_c"]["steps"]
baseline = data["panel_c"]["Baseline"]
ours     = data["panel_c"]["Ours"]
ax_c.plot(steps, baseline, color=C_GRAY,   lw=1.6, label="Baseline")
ax_c.plot(steps, ours,     color=C_ORANGE, lw=1.6, label="Ours")
ax_c.fill_between(steps, ours, baseline, alpha=0.12, color=C_ORANGE)
ax_c.set_xlabel("Step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss",        fontsize=8)
ax_c.set_title("Training Trend", fontsize=9, color=C_GRAY, pad=4)
ax_c.legend(fontsize=7.5, framealpha=0.6)
ax_c.tick_params(labelsize=7.5)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.grid(lw=0.4, alpha=0.4, zorder=0)

# ── Panel D: 5×5 heatmap ─────────────────────────────────────────────────────
ax_d = fig.add_subplot(gs[1, :])
matrix = np.array(data["panel_d"]["matrix"])
x_lbls = data["panel_d"]["x"]
y_lbls = data["panel_d"]["y"]
im = ax_d.imshow(matrix, cmap=C_HEAT, aspect="auto", vmin=0, vmax=1)
ax_d.set_xticks(range(len(x_lbls))); ax_d.set_xticklabels(x_lbls, fontsize=9)
ax_d.set_yticks(range(len(y_lbls))); ax_d.set_yticklabels(y_lbls, fontsize=9)
ax_d.set_xlabel("Sweep axis S", fontsize=9)
ax_d.set_ylabel("Sweep axis P", fontsize=9)
ax_d.set_title("Sensitivity Sweep (5×5)", fontsize=9, color=C_GRAY, pad=4)
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        v = matrix[i, j]
        ax_d.text(j, i, f"{v:.2f}", ha="center", va="center",
                  fontsize=8.5, color="white" if v > 0.6 else C_DARK)
cbar = fig.colorbar(im, ax=ax_d, fraction=0.015, pad=0.01)
cbar.ax.tick_params(labelsize=7.5)

# ── Panel labels A B C D ─────────────────────────────────────────────────────
for ax, lbl in [(ax_a, "A"), (ax_b, "B"), (ax_c, "C"), (ax_d, "D")]:
    ax.text(-0.06, 1.06, lbl, transform=ax.transAxes,
            fontsize=13, fontweight="bold", fontfamily="sans-serif",
            va="top", ha="left", color=C_DARK)

# ── Save ─────────────────────────────────────────────────────────────────────
fig.savefig(CWD / "figure.pdf", bbox_inches="tight")
fig.savefig(CWD / "figure.png", bbox_inches="tight", dpi=150)
fig.savefig(CWD / "figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
