import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------- load data ----------
with open("data.json") as f:
    data = json.load(f)

pb = data["panel_b"]
pc = data["panel_c"]
pd = data["panel_d"]

# ---------- style ----------
BLUE   = "#2563EB"
ORANGE = "#F97316"
GRAY   = "#6B7280"
LIGHT  = "#EFF6FF"
DARK   = "#1E3A5F"
GREEN  = "#10B981"
RED    = "#EF4444"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "axes.titlesize": 9,
    "figure.dpi": 150,
})

LABEL_KW = dict(fontsize=11, fontweight="bold", fontfamily="DejaVu Sans",
                va="top", ha="left")

fig = plt.figure(figsize=(12, 7))
gs_outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38,
                              height_ratios=[1, 0.72])

# top row: 3 columns
gs_top = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs_outer[0],
                                          wspace=0.40, width_ratios=[2, 1, 1])
ax_a = fig.add_subplot(gs_top[0])
ax_b = fig.add_subplot(gs_top[1])
ax_c = fig.add_subplot(gs_top[2])

# bottom row: full width
ax_d = fig.add_subplot(gs_outer[1])

# =====================================================================
# PANEL A – method overview diagram
# =====================================================================
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis("off")

def rounded_box(ax, x, y, w, h, color, label, sublabel=None, alpha=1.0):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=color, edgecolor="white",
                          linewidth=1.8, alpha=alpha, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2 + (0.18 if sublabel else 0),
            label, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white", zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.28, sublabel, ha="center", va="center",
                fontsize=6.8, color="white", alpha=0.9, zorder=4)

def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=DARK,
                                lw=1.6, mutation_scale=14),
                zorder=5)

# Stage boxes
rounded_box(ax_a, 0.4, 2.9, 2.1, 1.8, BLUE,   "Input",        "Raw data")
rounded_box(ax_a, 3.95, 2.9, 2.1, 1.8, ORANGE, "Processing",   "Attn + Mem")
rounded_box(ax_a, 7.5, 2.9, 2.1, 1.8, GREEN,  "Output",        "Prediction")

# Arrows between stages
arrow(ax_a, 2.50, 3.80, 3.95, 3.80)
arrow(ax_a, 6.05, 3.80, 7.50, 3.80)

# Residual skip-connection arc
ax_a.annotate("",
    xy=(7.55, 3.1), xytext=(0.45, 3.1),
    arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2,
                    connectionstyle="arc3,rad=-0.35", mutation_scale=11),
    zorder=5)
ax_a.text(4.0, 1.75, "residual", ha="center", va="top",
          fontsize=7, color=GRAY, style="italic")

# Skill module below processing
rounded_box(ax_a, 3.95, 0.6, 2.1, 1.6, "#7C3AED", "Skill\nBank", alpha=0.88)
arrow(ax_a, 5.0, 2.9, 5.0, 2.20)

# Stage labels
for x_mid, lbl in [(1.45, "Stage 1"), (5.0, "Stage 2"), (8.55, "Stage 3")]:
    ax_a.text(x_mid, 5.05, lbl, ha="center", va="bottom",
              fontsize=7.5, color=DARK, fontweight="bold")
    ax_a.plot([x_mid - 1.0, x_mid + 1.0], [4.90, 4.90],
              color=DARK, lw=0.8, alpha=0.4, zorder=2)

ax_a.set_title("Method Overview", fontsize=9, fontweight="bold",
               color=DARK, pad=4)

# =====================================================================
# PANEL B – ablation bars
# =====================================================================
items  = pb["items"]
values = pb["values"]
colors = [BLUE if v == max(values) else GRAY for v in values]
bars = ax_b.barh(items, values, color=colors, height=0.55, zorder=3)
ax_b.set_xlim(48, 70)
ax_b.axvline(values[0], color=BLUE, lw=1.0, ls="--", alpha=0.6)
for bar, val in zip(bars, values):
    ax_b.text(val + 0.3, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7, color=DARK)
ax_b.set_xlabel("Accuracy (%)")
ax_b.set_title("Ablation Study", fontweight="bold")
ax_b.grid(axis="x", lw=0.5, alpha=0.4, zorder=0)
ax_b.invert_yaxis()

# =====================================================================
# PANEL C – training curves
# =====================================================================
steps    = pc["steps"]
baseline = pc["Baseline"]
ours     = pc["Ours"]

ax_c.plot(steps, baseline, color=GRAY,   lw=1.8, label="Baseline", zorder=3)
ax_c.plot(steps, ours,     color=ORANGE, lw=2.0, label="Ours",     zorder=4)
ax_c.fill_between(steps, baseline, ours,
                  where=[o < b for o, b in zip(ours, baseline)],
                  color=ORANGE, alpha=0.12, zorder=2)
ax_c.set_xlabel("Training step")
ax_c.set_ylabel("Loss")
ax_c.set_title("Training Convergence", fontweight="bold")
ax_c.legend(fontsize=7, framealpha=0.7, loc="upper right")
ax_c.grid(lw=0.4, alpha=0.4, zorder=0)

# =====================================================================
# PANEL D – 5×5 heatmap
# =====================================================================
matrix = np.array(pd["matrix"])
x_lbl  = pd["x"]
y_lbl  = pd["y"]

im = ax_d.imshow(matrix, aspect="auto", cmap="RdYlGn",
                 vmin=0.0, vmax=1.0, origin="upper")
ax_d.set_xticks(range(len(x_lbl))); ax_d.set_xticklabels(x_lbl, fontsize=8)
ax_d.set_yticks(range(len(y_lbl))); ax_d.set_yticklabels(y_lbl, fontsize=8)
ax_d.set_xlabel("Sensitivity parameter S", fontsize=8)
ax_d.set_ylabel("Penalty weight P", fontsize=8)
ax_d.set_title("Sensitivity Sweep (Accuracy)", fontweight="bold")
ax_d.spines[:].set_visible(False)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        v = matrix[i, j]
        txt_color = "white" if v < 0.35 or v > 0.80 else DARK
        ax_d.text(j, i, f"{v:.2f}", ha="center", va="center",
                  fontsize=8, color=txt_color, fontweight="bold")

cbar = fig.colorbar(im, ax=ax_d, orientation="vertical",
                    fraction=0.018, pad=0.02)
cbar.set_label("Accuracy", fontsize=8)
cbar.ax.tick_params(labelsize=7)

# =====================================================================
# Panel labels A B C D
# =====================================================================
label_positions = {
    "A": ax_a, "B": ax_b, "C": ax_c, "D": ax_d
}
for lbl, ax in label_positions.items():
    ax.text(-0.06, 1.06, lbl, transform=ax.transAxes, **LABEL_KW)

# =====================================================================
# Save
# =====================================================================
fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
