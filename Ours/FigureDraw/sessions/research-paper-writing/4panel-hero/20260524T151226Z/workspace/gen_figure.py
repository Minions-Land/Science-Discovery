import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.patheffects import withStroke

# ── Load data ────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

pb = data["panel_b"]
pc = data["panel_c"]
pd = data["panel_d"]

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 8))
fig.patch.set_facecolor("white")

outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38, height_ratios=[1, 0.72])
top   = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[0],
                                         wspace=0.35, width_ratios=[2, 1, 1])
bot   = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[1])

ax_a = fig.add_subplot(top[0])
ax_b = fig.add_subplot(top[1])
ax_c = fig.add_subplot(top[2])
ax_d = fig.add_subplot(bot[0])

LABEL_KW = dict(fontsize=13, fontweight="bold", fontfamily="DejaVu Sans",
                va="top", ha="left", transform=None)

COLOR_OURS     = "#2166AC"
COLOR_BASE     = "#D6604D"
COLOR_FULL     = "#2166AC"
COLOR_ABLATION = "#92C5DE"

# ══════════════════════════════════════════════════════════════════════════════
# Panel A – Method overview (conceptual diagram)
# ══════════════════════════════════════════════════════════════════════════════
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)
ax_a.axis("off")

def _box(ax, xy, wh, label, sublabel="", fc="#EAF2FB", ec="#2166AC", lw=1.4):
    x, y = xy
    w, h = wh
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                         fc=fc, ec=ec, lw=lw, zorder=3, clip_on=False)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2 + (0.03 if sublabel else 0), label,
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color="#1a1a2e", zorder=4, clip_on=False)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.06, sublabel,
                ha="center", va="center", fontsize=6.5, color="#555",
                zorder=4, clip_on=False)

def _arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color="#444",
                                lw=1.3, mutation_scale=12),
                zorder=2, annotation_clip=False)

# Stage boxes
stages = [
    (0.04, 0.54, 0.21, 0.28, "Stage 1", "Input\nEncoder"),
    (0.30, 0.54, 0.21, 0.28, "Stage 2", "Attention\n+ Memory"),
    (0.56, 0.54, 0.21, 0.28, "Stage 3", "Skill\nDecoder"),
]
for x, y, w, h, lbl, sub in stages:
    _box(ax_a, (x, y), (w, h), lbl, sub)

# Arrows between stages
arrow_y = 0.68
_arrow(ax_a, 0.25, arrow_y, 0.30, arrow_y)
_arrow(ax_a, 0.51, arrow_y, 0.56, arrow_y)
_arrow(ax_a, 0.77, arrow_y, 0.82, arrow_y)

# Output box
_box(ax_a, (0.78, 0.54), (0.18, 0.28), "Output", "Prediction",
     fc="#E8F5E9", ec="#388E3C")

# Input annotation
ax_a.annotate("", xy=(0.04, arrow_y), xytext=(0.0, arrow_y),
              arrowprops=dict(arrowstyle="-|>", color="#444", lw=1.3,
                              mutation_scale=12),
              annotation_clip=False)
ax_a.text(-0.01, arrow_y, "Input", ha="right", va="center",
          fontsize=7.5, color="#333", clip_on=False)

# Residual skip connection (curved)
ax_a.annotate("", xy=(0.56, 0.56), xytext=(0.30, 0.56),
              arrowprops=dict(arrowstyle="-|>",
                              connectionstyle="arc3,rad=-0.45",
                              color="#9B59B6", lw=1.2, linestyle="dashed",
                              mutation_scale=10),
              annotation_clip=False)
ax_a.text(0.43, 0.37, "residual", ha="center", va="top",
          fontsize=6.5, color="#9B59B6", style="italic", clip_on=False)

# Components legend row
comp_x = [0.04, 0.30, 0.56, 0.04]
comp_y = [0.22, 0.22, 0.22, 0.05]
comp_labels = ["Attention\nModule", "Memory\nBank", "Skill\nHead", ""]
comp_fc = ["#FFF3E0", "#FCE4EC", "#F3E5F5"]
comp_ec = ["#E65100", "#C2185B", "#7B1FA2"]
for i, (cx, cy, cl, cfc, cec) in enumerate(zip(comp_x[:3], comp_y[:3],
                                                comp_labels[:3],
                                                comp_fc, comp_ec)):
    _box(ax_a, (cx, cy), (0.18, 0.20), cl, fc=cfc, ec=cec, lw=1.1)

# Bracket connecting stage 2 to components below
for cx in [0.04, 0.30, 0.56]:
    ax_a.plot([cx+0.09, cx+0.09], [0.54, 0.42], color="#aaa",
              lw=0.8, ls="--", zorder=1, clip_on=False)

ax_a.text(0.5, 0.97, "Method Overview", ha="center", va="top",
          fontsize=9, color="#333", style="italic", clip_on=False)

# ══════════════════════════════════════════════════════════════════════════════
# Panel B – Ablation bars
# ══════════════════════════════════════════════════════════════════════════════
items  = pb["items"]
values = pb["values"]
colors = [COLOR_FULL if v == max(values) else COLOR_ABLATION for v in values]

y_pos = np.arange(len(items))
bars = ax_b.barh(y_pos, values, color=colors, edgecolor="white",
                 height=0.6, zorder=3)
ax_b.set_yticks(y_pos)
ax_b.set_yticklabels(items, fontsize=8)
ax_b.set_xlabel("Accuracy (%)", fontsize=8)
ax_b.set_xlim(50, 68)
ax_b.axvline(values[0], color=COLOR_FULL, lw=1.0, ls="--", alpha=0.5)
ax_b.set_title("Ablation Study", fontsize=9, pad=4)
ax_b.tick_params(axis="both", labelsize=7.5)
ax_b.spines[["top", "right"]].set_visible(False)
ax_b.grid(axis="x", lw=0.4, alpha=0.4, zorder=0)

for bar, val in zip(bars, values):
    ax_b.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", ha="left", fontsize=7, color="#333")

# ══════════════════════════════════════════════════════════════════════════════
# Panel C – Training curves
# ══════════════════════════════════════════════════════════════════════════════
steps    = pc["steps"]
baseline = pc["Baseline"]
ours     = pc["Ours"]

ax_c.plot(steps, baseline, color=COLOR_BASE,  lw=1.6, label="Baseline", zorder=3)
ax_c.plot(steps, ours,     color=COLOR_OURS,  lw=1.6, label="Ours",     zorder=3)
ax_c.fill_between(steps, baseline, ours, alpha=0.12, color=COLOR_OURS, zorder=2)
ax_c.set_xlabel("Training Step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.set_title("Training Convergence", fontsize=9, pad=4)
ax_c.legend(fontsize=7.5, framealpha=0.7, loc="upper right")
ax_c.tick_params(axis="both", labelsize=7.5)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.grid(lw=0.4, alpha=0.4, zorder=0)

# ══════════════════════════════════════════════════════════════════════════════
# Panel D – Sensitivity heatmap
# ══════════════════════════════════════════════════════════════════════════════
matrix = np.array(pd["matrix"])
x_labels = pd["x"]
y_labels = pd["y"]

im = ax_d.imshow(matrix, aspect="auto", cmap="RdYlGn", vmin=0, vmax=1,
                 interpolation="nearest")

ax_d.set_xticks(range(len(x_labels)))
ax_d.set_xticklabels(x_labels, fontsize=8.5)
ax_d.set_yticks(range(len(y_labels)))
ax_d.set_yticklabels(y_labels, fontsize=8.5)
ax_d.set_xlabel("Hyperparameter Scale (S)", fontsize=9)
ax_d.set_ylabel("Penalty Factor (P)", fontsize=9)
ax_d.set_title("Sensitivity Sweep", fontsize=9, pad=4)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        txt_color = "white" if val < 0.35 or val > 0.75 else "black"
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8.5, color=txt_color, fontweight="bold")

cbar = fig.colorbar(im, ax=ax_d, fraction=0.015, pad=0.01)
cbar.ax.tick_params(labelsize=7.5)
cbar.set_label("Score", fontsize=8)

# ══════════════════════════════════════════════════════════════════════════════
# Panel labels A B C D
# ══════════════════════════════════════════════════════════════════════════════
label_kw = dict(fontsize=14, fontweight="bold", fontfamily="DejaVu Sans",
                va="top", ha="left",
                xycoords="axes fraction", annotation_clip=False)
for ax, lbl in [(ax_a, "A"), (ax_b, "B"), (ax_c, "C"), (ax_d, "D")]:
    ax.annotate(lbl, xy=(-0.04, 1.06), **label_kw)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
