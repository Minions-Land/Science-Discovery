import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

# ── data ────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

pb_items  = d["panel_b"]["items"]
pb_vals   = d["panel_b"]["values"]
pc_steps  = d["panel_c"]["steps"]
pc_base   = d["panel_c"]["Baseline"]
pc_ours   = d["panel_c"]["Ours"]
pd_x      = d["panel_d"]["x"]
pd_y      = d["panel_d"]["y"]
pd_mat    = np.array(d["panel_d"]["matrix"])

# ── style ────────────────────────────────────────────────────────────────────
BLUE   = "#2563EB"
ORANGE = "#F97316"
GRAY   = "#94A3B8"
LIGHT  = "#EFF6FF"
DARK   = "#1E3A5F"
ACCENT = "#10B981"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size":   8,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

fig = plt.figure(figsize=(11, 7))
gs  = GridSpec(2, 3, figure=fig,
               width_ratios=[2, 1, 1],
               height_ratios=[1, 1],
               hspace=0.42, wspace=0.38,
               left=0.05, right=0.97, top=0.95, bottom=0.07)

ax_a = fig.add_subplot(gs[0, 0])   # top-left dominant
ax_b = fig.add_subplot(gs[0, 1])   # top-mid
ax_c = fig.add_subplot(gs[0, 2])   # top-right
ax_d = fig.add_subplot(gs[1, :])   # bottom full-width

# ── helper: bold panel label ─────────────────────────────────────────────────
def panel_label(ax, txt):
    ax.text(-0.08, 1.06, txt, transform=ax.transAxes,
            fontsize=12, fontweight="bold", fontfamily="sans-serif",
            va="top", ha="left", color=DARK)

# ════════════════════════════════════════════════════════════════════════════
# Panel A – conceptual overview
# ════════════════════════════════════════════════════════════════════════════
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 7)
ax_a.axis("off")

# stage definitions: (x-center, label, icon-char)
stages = [
    (1.2, "Input\nTokens",    "x"),
    (3.9, "Attention\nModule", "+"),
    (6.6, "Memory\nBank",     "[M]"),
    (9.1, "Output\nHead",    "y^"),
]
box_w, box_h = 1.8, 1.3
box_y = 3.0

for i, (cx, label, icon) in enumerate(stages):
    color = BLUE if i < 3 else ACCENT
    rect = FancyBboxPatch((cx - box_w/2, box_y - box_h/2), box_w, box_h,
                          boxstyle="round,pad=0.12", linewidth=1.5,
                          edgecolor=color, facecolor=LIGHT if i < 3 else "#ECFDF5")
    ax_a.add_patch(rect)
    ax_a.text(cx, box_y + 0.18, icon, ha="center", va="center", fontsize=11)
    ax_a.text(cx, box_y - 0.38, label, ha="center", va="center",
              fontsize=7, color=DARK, linespacing=1.3)
    # arrows between boxes
    if i < len(stages) - 1:
        nx = stages[i+1][0]
        ax_a.annotate("", xy=(nx - box_w/2 - 0.05, box_y),
                      xytext=(cx + box_w/2 + 0.05, box_y),
                      arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                      lw=1.3, mutation_scale=10))

# skill routing sub-box below stage 2 (Memory)
sk_cx = 3.9
sk_rect = FancyBboxPatch((sk_cx - 1.2, 0.9), 2.4, 0.9,
                          boxstyle="round,pad=0.1", linewidth=1.0,
                          edgecolor=ORANGE, facecolor="#FFF7ED", linestyle="--")
ax_a.add_patch(sk_rect)
ax_a.text(sk_cx, 1.35, "Skill Router", ha="center", va="center",
          fontsize=7, color=ORANGE, fontweight="bold")
# dashed link
ax_a.annotate("", xy=(sk_cx, box_y - box_h/2),
              xytext=(sk_cx, 1.35 + 0.45),
              arrowprops=dict(arrowstyle="<-", color=ORANGE, lw=1.0,
                              linestyle="dashed", mutation_scale=8))

# residual skip arrow
ax_a.annotate("", xy=(6.6 - box_w/2 - 0.05, box_y + 0.35),
              xytext=(1.2 + box_w/2 + 0.05, box_y + 0.35),
              arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0,
                              connectionstyle="arc3,rad=-0.35",
                              mutation_scale=9))
ax_a.text(3.9, 5.5, "residual", ha="center", va="center",
          fontsize=6.5, color=BLUE, style="italic")

# title
ax_a.text(5.0, 6.6, "3-Stage Pipeline Overview", ha="center", va="top",
          fontsize=9, fontweight="bold", color=DARK)

panel_label(ax_a, "A")

# ════════════════════════════════════════════════════════════════════════════
# Panel B – ablation bars
# ════════════════════════════════════════════════════════════════════════════
full_val = pb_vals[0]
colors_b = [BLUE if v == full_val else GRAY for v in pb_vals]
bars = ax_b.barh(pb_items, pb_vals, color=colors_b, height=0.55, zorder=2)
ax_b.set_xlim(48, 70)
ax_b.axvline(full_val, color=BLUE, lw=0.8, linestyle="--", alpha=0.5)
for bar, val in zip(bars, pb_vals):
    ax_b.text(val + 0.3, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7, color=DARK)
ax_b.set_xlabel("Accuracy (%)", fontsize=7.5)
ax_b.set_title("Ablation Study", fontsize=8.5, fontweight="bold", color=DARK, pad=4)
ax_b.tick_params(axis="y", labelsize=7)
ax_b.tick_params(axis="x", labelsize=7)
ax_b.grid(axis="x", lw=0.4, alpha=0.4, zorder=0)
panel_label(ax_b, "B")

# ════════════════════════════════════════════════════════════════════════════
# Panel C – training curves
# ════════════════════════════════════════════════════════════════════════════
ax_c.plot(pc_steps, pc_base, color=GRAY,   lw=1.6, label="Baseline", zorder=2)
ax_c.plot(pc_steps, pc_ours, color=ORANGE, lw=1.6, label="Ours",     zorder=3)
ax_c.fill_between(pc_steps, pc_base, pc_ours,
                  where=[o < b for o, b in zip(pc_ours, pc_base)],
                  alpha=0.12, color=ORANGE)
ax_c.set_xlabel("Training Step (×10³)", fontsize=7.5)
ax_c.set_ylabel("Loss", fontsize=7.5)
ax_c.set_title("Training Trend", fontsize=8.5, fontweight="bold", color=DARK, pad=4)
ax_c.legend(fontsize=7, frameon=False)
ax_c.tick_params(labelsize=7)
ax_c.grid(lw=0.3, alpha=0.35)
panel_label(ax_c, "C")

# ════════════════════════════════════════════════════════════════════════════
# Panel D – 5×5 sensitivity heatmap
# ════════════════════════════════════════════════════════════════════════════
im = ax_d.imshow(pd_mat, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
ax_d.set_xticks(range(len(pd_x))); ax_d.set_xticklabels(pd_x, fontsize=8)
ax_d.set_yticks(range(len(pd_y))); ax_d.set_yticklabels(pd_y, fontsize=8)
ax_d.set_xlabel("Hyperparameter S", fontsize=8.5)
ax_d.set_ylabel("Hyperparameter P", fontsize=8.5)
ax_d.set_title("Sensitivity Sweep (5×5)", fontsize=9, fontweight="bold", color=DARK, pad=6)
for i in range(pd_mat.shape[0]):
    for j in range(pd_mat.shape[1]):
        val = pd_mat[i, j]
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8, color="white" if val < 0.35 or val > 0.75 else DARK,
                  fontweight="bold")
cbar = fig.colorbar(im, ax=ax_d, fraction=0.015, pad=0.01)
cbar.ax.tick_params(labelsize=7.5)
cbar.set_label("Score", fontsize=8)
panel_label(ax_d, "D")

# ── save ─────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=200, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
