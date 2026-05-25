import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.patheffects import withStroke

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

pb = data["panel_b"]
pc = data["panel_c"]
pd = data["panel_d"]

# ── figure layout ───────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor("white")

outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38,
                          top=0.95, bottom=0.07, left=0.06, right=0.97)
top_gs = gridspec.GridSpecFromSubplotSpec(
    1, 3, subplot_spec=outer[0], width_ratios=[2, 1, 1], wspace=0.38)
bot_ax = fig.add_subplot(outer[1])
ax_a   = fig.add_subplot(top_gs[0])
ax_b   = fig.add_subplot(top_gs[1])
ax_c   = fig.add_subplot(top_gs[2])

LABEL_KW = dict(fontsize=11, fontweight="bold", fontfamily="DejaVu Sans",
                va="top", ha="left")

# ── PANEL A – method overview diagram ───────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis("off")

BLUE   = "#2176AE"
ORANGE = "#E87722"
GREEN  = "#3BB273"
GRAY   = "#F0F2F5"
DARK   = "#1C2B3A"

def rounded_box(ax, x, y, w, h, color, label, sublabel="", radius=0.35):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=f"round,pad=0.0,rounding_size={radius}",
                         facecolor=color, edgecolor="white", linewidth=1.5,
                         zorder=3)
    ax.add_patch(box)
    ax.text(x, y + 0.07, label, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white", zorder=4)
    if sublabel:
        ax.text(x, y - 0.38, sublabel, ha="center", va="center",
                fontsize=6.5, color="white", alpha=0.85, zorder=4)

def arrow(ax, x0, x1, y, color="#888", lw=1.4):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=12), zorder=5)

# input token strip
ax_a.add_patch(FancyBboxPatch((0.35, 2.55), 1.3, 0.9,
    boxstyle="round,pad=0.0,rounding_size=0.25",
    facecolor=GRAY, edgecolor="#BCC5CE", linewidth=1, zorder=2))
ax_a.text(1.0, 3.0, "Input\nTokens", ha="center", va="center",
          fontsize=7.5, color=DARK, fontweight="bold")

# three stage boxes
stages = [
    (3.0, 3.0, BLUE,   "Stage 1",   "Encode"),
    (5.2, 3.0, ORANGE, "Stage 2",   "Attend"),
    (7.4, 3.0, GREEN,  "Stage 3",   "Decode"),
]
for sx, sy, sc, sl, sub in stages:
    rounded_box(ax_a, sx, sy, 1.55, 0.95, sc, sl, sub)

# arrows between boxes
arrow(ax_a, 1.65, 2.22, 3.0, "#AAB")
arrow(ax_a, 3.78, 4.42, 3.0, "#AAB")
arrow(ax_a, 5.98, 6.62, 3.0, "#AAB")

# output box
ax_a.add_patch(FancyBboxPatch((8.35, 2.55), 1.3, 0.9,
    boxstyle="round,pad=0.0,rounding_size=0.25",
    facecolor="#E8F4EA", edgecolor="#3BB273", linewidth=1.5, zorder=2))
ax_a.text(9.0, 3.0, "Output", ha="center", va="center",
          fontsize=7.5, color=DARK, fontweight="bold")
arrow(ax_a, 8.18, 8.35, 3.0, "#AAB")

# memory / skill feedback arcs
for (sx, col, lbl) in [(3.0, BLUE, "Memory"), (5.2, ORANGE, "Skills")]:
    ax_a.annotate("", xy=(sx - 0.55, 2.52), xytext=(sx + 0.55, 2.52),
                  arrowprops=dict(arrowstyle="-|>", color=col,
                                  connectionstyle="arc3,rad=0.55",
                                  lw=1.2, mutation_scale=10,
                                  linestyle="dashed"), zorder=5)
    ax_a.text(sx, 1.75, lbl, ha="center", va="center",
              fontsize=6.5, color=col, style="italic")

# legend strip at top
for i, (lbl, col) in enumerate(
        [("Stage 1: Encode", BLUE), ("Stage 2: Attend", ORANGE),
         ("Stage 3: Decode", GREEN)]):
    ax_a.add_patch(mpatches.Rectangle((0.4 + i*3.1, 5.3), 0.22, 0.22,
                                       color=col, zorder=3))
    ax_a.text(0.7 + i*3.1, 5.41, lbl, fontsize=6.5, va="center", color=DARK)

ax_a.text(0.02, 0.97, "A", transform=ax_a.transAxes, **LABEL_KW)

# ── PANEL B – ablation bars ──────────────────────────────────────────────────
colors_b = [GREEN if v == max(pb["values"]) else "#7BAFD4" for v in pb["values"]]
bars = ax_b.barh(pb["items"], pb["values"], color=colors_b,
                 edgecolor="white", linewidth=0.7, height=0.55)
ax_b.set_xlim(50, 68)
ax_b.axvline(pb["values"][0], color=GREEN, lw=1.0, ls="--", alpha=0.6)
for bar, val in zip(bars, pb["values"]):
    ax_b.text(val + 0.15, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7)
ax_b.set_xlabel("Score (%)", fontsize=8)
ax_b.set_title("Ablation", fontsize=9, fontweight="bold", pad=4)
ax_b.tick_params(axis="both", labelsize=7)
ax_b.spines[["top", "right"]].set_visible(False)
ax_b.text(-0.18, 1.03, "B", transform=ax_b.transAxes, **LABEL_KW)

# ── PANEL C – training curves ────────────────────────────────────────────────
steps = pc["steps"]
ax_c.plot(steps, pc["Baseline"], color="#7BAFD4", lw=1.5,
          label="Baseline", alpha=0.9)
ax_c.plot(steps, pc["Ours"], color=ORANGE, lw=1.8,
          label="Ours", alpha=0.95)
ax_c.set_xlabel("Step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.set_title("Training Trend", fontsize=9, fontweight="bold", pad=4)
ax_c.legend(fontsize=7, frameon=False)
ax_c.tick_params(axis="both", labelsize=7)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.text(-0.22, 1.03, "C", transform=ax_c.transAxes, **LABEL_KW)

# ── PANEL D – heatmap ────────────────────────────────────────────────────────
matrix = np.array(pd["matrix"])
im = bot_ax.imshow(matrix, aspect="auto", cmap="viridis",
                   vmin=0, vmax=1, interpolation="nearest")
bot_ax.set_xticks(range(len(pd["x"])))
bot_ax.set_xticklabels(pd["x"], fontsize=9)
bot_ax.set_yticks(range(len(pd["y"])))
bot_ax.set_yticklabels(pd["y"], fontsize=9)
bot_ax.set_xlabel("Sweep Parameter S", fontsize=9)
bot_ax.set_ylabel("Sweep Parameter P", fontsize=9)
bot_ax.set_title("Sensitivity Sweep (5×5)", fontsize=10, fontweight="bold", pad=5)
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        tc = "white" if val < 0.5 else "black"
        bot_ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=8, color=tc)
cbar = fig.colorbar(im, ax=bot_ax, fraction=0.025, pad=0.02)
cbar.set_label("Score", fontsize=8)
cbar.ax.tick_params(labelsize=7)
bot_ax.text(-0.04, 1.04, "D", transform=bot_ax.transAxes, **LABEL_KW)

# ── save ─────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
