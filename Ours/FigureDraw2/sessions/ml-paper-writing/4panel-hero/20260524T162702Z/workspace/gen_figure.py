import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib import rcParams

# ── Typography ──────────────────────────────────────────────────────────────
rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
})

BLUE   = "#2563EB"
ORANGE = "#EA580C"
GRAY   = "#6B7280"
LBLUE  = "#DBEAFE"
LORG   = "#FEF3C7"

# ── Load data ────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

pb = data["panel_b"]
pc = data["panel_c"]
pd = data["panel_d"]

# ── Figure layout ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 7))
outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.40,
                          top=0.94, bottom=0.08, left=0.06, right=0.97)

# Top row: 3 columns with width_ratios=[2,1,1]
top_gs = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[0],
                                          width_ratios=[2, 1, 1],
                                          wspace=0.38)
ax_a = fig.add_subplot(top_gs[0])
ax_b = fig.add_subplot(top_gs[1])
ax_c = fig.add_subplot(top_gs[2])

# Bottom row: full width
ax_d = fig.add_subplot(outer[1])

# ── Helper: panel label ──────────────────────────────────────────────────────
def panel_label(ax, letter, dx=-0.04, dy=1.06):
    ax.text(dx, dy, letter, transform=ax.transAxes,
            fontsize=13, fontweight="bold", fontfamily="sans-serif",
            va="top", ha="left")

# ────────────────────────────────────────────────────────────────────────────
# PANEL A — conceptual overview (3-stage pipeline diagram)
# ────────────────────────────────────────────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis("off")

def draw_box(ax, x, y, w, h, label, sublabel, facecolor, edgecolor):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.12",
                         facecolor=facecolor, edgecolor=edgecolor, linewidth=1.6)
    ax.add_patch(box)
    ax.text(x, y + 0.18, label, ha="center", va="center",
            fontsize=9, fontweight="bold", color=edgecolor)
    ax.text(x, y - 0.28, sublabel, ha="center", va="center",
            fontsize=7, color=GRAY)

def arrow(ax, x0, x1, y, color="#374151"):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.4,
                                color=color, mutation_scale=12))

# Input
draw_box(ax_a, 1.15, 3.0, 1.6, 1.4, "Input", "raw data / tokens",
         "#F0FDF4", "#15803D")

# Stage 1
draw_box(ax_a, 3.3, 3.0, 1.6, 1.4, "Stage 1", "Encode + Attend",
         LBLUE, BLUE)

# Stage 2
draw_box(ax_a, 5.5, 3.0, 1.6, 1.4, "Stage 2", "Memory Update",
         "#EDE9FE", "#7C3AED")

# Stage 3
draw_box(ax_a, 7.7, 3.0, 1.6, 1.4, "Stage 3", "Skill Decode",
         LORG, ORANGE)

# Output
draw_box(ax_a, 9.3, 3.0, 0.9, 1.0, "Out", "prediction",
         "#FFF7ED", ORANGE)

# Arrows between boxes
for x0, x1 in [(1.95, 2.50), (4.10, 4.70), (6.30, 6.70), (8.50, 8.85)]:
    arrow(ax_a, x0, x1, 3.0)

# Residual skip connection (Stage 1 → Stage 3)
ax_a.annotate("", xy=(7.7, 4.55), xytext=(3.3, 4.55),
              arrowprops=dict(arrowstyle="-|>", lw=1.2,
                              color=BLUE, connectionstyle="arc3,rad=0.0",
                              mutation_scale=10))
ax_a.plot([3.3, 3.3], [3.70, 4.55], color=BLUE, lw=1.2, ls="--")
ax_a.plot([7.7, 7.7], [3.70, 4.55], color=BLUE, lw=1.2, ls="--")
ax_a.text(5.5, 4.72, "residual skip", ha="center", va="bottom",
          fontsize=7, color=BLUE, style="italic")

# Attention feedback loop (Stage 2 → Stage 1)
ax_a.annotate("", xy=(3.3, 1.45), xytext=(5.5, 1.45),
              arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#7C3AED",
                              mutation_scale=10))
ax_a.plot([3.3, 3.3], [2.30, 1.45], color="#7C3AED", lw=1.2, ls="--")
ax_a.plot([5.5, 5.5], [2.30, 1.45], color="#7C3AED", lw=1.2, ls="--")
ax_a.text(4.4, 1.22, "attn feedback", ha="center", va="top",
          fontsize=7, color="#7C3AED", style="italic")

# Title
ax_a.text(5.0, 5.55, "3-Stage Pipeline", ha="center", va="top",
          fontsize=10, fontweight="bold", color="#111827")

panel_label(ax_a, "A", dx=-0.01)

# ────────────────────────────────────────────────────────────────────────────
# PANEL B — ablation bars
# ────────────────────────────────────────────────────────────────────────────
items  = pb["items"]
values = pb["values"]
colors = [BLUE if v == max(values) else GRAY for v in values]
y_pos  = np.arange(len(items))

bars = ax_b.barh(y_pos, values, color=colors, height=0.55)
ax_b.set_yticks(y_pos)
ax_b.set_yticklabels(items, fontsize=8)
ax_b.set_xlabel("Accuracy (%)", fontsize=8)
ax_b.set_xlim(50, 68)
ax_b.tick_params(axis="x", labelsize=7)
ax_b.tick_params(axis="y", length=0)
ax_b.axvline(values[0], color=BLUE, lw=0.8, ls="--", alpha=0.5)

for bar, val in zip(bars, values):
    ax_b.text(val + 0.15, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7,
              color=BLUE if val == max(values) else GRAY)

ax_b.set_title("Ablation", fontsize=9, pad=4)
panel_label(ax_b, "B")

# ────────────────────────────────────────────────────────────────────────────
# PANEL C — training trends
# ────────────────────────────────────────────────────────────────────────────
steps    = pc["steps"]
baseline = pc["Baseline"]
ours     = pc["Ours"]

ax_c.plot(steps, baseline, color=GRAY,   lw=1.6, label="Baseline")
ax_c.plot(steps, ours,     color=ORANGE, lw=1.6, label="Ours")
ax_c.set_xlabel("Training step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss",                 fontsize=8)
ax_c.tick_params(labelsize=7)
ax_c.legend(fontsize=7, frameon=False, loc="upper right")
ax_c.set_title("Training curve", fontsize=9, pad=4)
panel_label(ax_c, "C")

# ────────────────────────────────────────────────────────────────────────────
# PANEL D — 5×5 sensitivity heatmap (full width)
# ────────────────────────────────────────────────────────────────────────────
matrix = np.array(pd["matrix"])
x_labels = pd["x"]
y_labels = pd["y"]

im = ax_d.imshow(matrix, aspect="auto", cmap="RdYlGn",
                 vmin=0, vmax=1, origin="upper")

ax_d.set_xticks(range(len(x_labels)))
ax_d.set_yticks(range(len(y_labels)))
ax_d.set_xticklabels(x_labels, fontsize=8)
ax_d.set_yticklabels(y_labels, fontsize=8)
ax_d.set_xlabel("Hyperparameter S", fontsize=8)
ax_d.set_ylabel("Hyperparameter P", fontsize=8)
ax_d.set_title("Sensitivity sweep (5×5)", fontsize=9, pad=4)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        color = "white" if val < 0.35 or val > 0.75 else "black"
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8, color=color)

cbar = fig.colorbar(im, ax=ax_d, orientation="vertical",
                    fraction=0.015, pad=0.01)
cbar.set_label("Score", fontsize=8)
cbar.ax.tick_params(labelsize=7)

panel_label(ax_d, "D", dx=-0.015, dy=1.10)

# ── Save ─────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg",           bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
