import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.patheffects import withStroke

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

# ── style ─────────────────────────────────────────────────────────────────────
BLUE   = "#2563EB"
ORANGE = "#F97316"
GRAY   = "#6B7280"
LIGHT  = "#EFF6FF"
DARK   = "#1E3A5F"
PANEL_LABEL_KW = dict(fontsize=11, fontweight="bold", fontfamily="sans-serif",
                      va="top", ha="left", transform=None)

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
})

# ── layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(11, 7))
outer = gridspec.GridSpec(2, 3, figure=fig,
                          width_ratios=[2, 1, 1],
                          hspace=0.42, wspace=0.38,
                          left=0.06, right=0.97,
                          top=0.94, bottom=0.08)

ax_a = fig.add_subplot(outer[0, 0])
ax_b = fig.add_subplot(outer[0, 1])
ax_c = fig.add_subplot(outer[0, 2])
ax_d = fig.add_subplot(outer[1, :])   # full-width bottom

# ── helper: panel label ───────────────────────────────────────────────────────
def panel_label(ax, letter):
    ax.text(-0.08, 1.08, letter, transform=ax.transAxes,
            fontsize=12, fontweight="bold", fontfamily="sans-serif",
            va="top", ha="left")

# ══════════════════════════════════════════════════════════════════════════════
# PANEL A – conceptual overview (3-stage pipeline)
# ══════════════════════════════════════════════════════════════════════════════
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 5)
ax_a.axis("off")
panel_label(ax_a, "A")

# title
ax_a.text(5, 4.65, "Method Overview: 3-Stage Pipeline",
          ha="center", va="top", fontsize=9, fontweight="bold", color=DARK)

# stage boxes
stages = [
    (1.2, "Stage 1\nEncoding",   "#DBEAFE", BLUE),
    (4.5, "Stage 2\nReasoning",  "#FEF3C7", "#D97706"),
    (7.8, "Stage 3\nDecoding",   "#D1FAE5", "#059669"),
]
box_w, box_h = 2.0, 1.5
box_y = 2.5

for cx, label, fc, ec in stages:
    rect = FancyBboxPatch((cx - box_w/2, box_y - box_h/2), box_w, box_h,
                          boxstyle="round,pad=0.12", linewidth=1.5,
                          edgecolor=ec, facecolor=fc, zorder=3)
    ax_a.add_patch(rect)
    ax_a.text(cx, box_y, label, ha="center", va="center",
              fontsize=8, fontweight="semibold", color=DARK, zorder=4)

# arrows between stages
for x0, x1 in [(2.2, 3.5), (5.5, 6.8)]:
    ax_a.annotate("", xy=(x1, box_y), xytext=(x0, box_y),
                  arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                  lw=1.5, mutation_scale=14), zorder=2)

# input / output labels
ax_a.text(0.15, box_y, "Input\nTokens", ha="center", va="center",
          fontsize=7, color=GRAY, style="italic")
ax_a.annotate("", xy=(0.2, box_y), xytext=(0.2, box_y),
              arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax_a.annotate("", xy=(ax_a.get_xlim()[1]-0.2, box_y),
              xytext=(8.8, box_y),
              arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
ax_a.text(9.85, box_y, "Output", ha="center", va="center",
          fontsize=7, color=GRAY, style="italic")

# component icons below each box
icons = [
    (1.2, 1.35, ["Attention", "Memory"]),
    (4.5, 1.35, ["Residual", "Skill"]),
    (7.8, 1.35, ["Beam\nSearch", "CRF"]),
]
for cx, cy, comps in icons:
    for i, comp in enumerate(comps):
        dx = -0.55 + i * 1.1
        mini = FancyBboxPatch((cx + dx - 0.45, cy - 0.28), 0.9, 0.56,
                              boxstyle="round,pad=0.06", linewidth=0.8,
                              edgecolor="#CBD5E1", facecolor="#F8FAFC", zorder=3)
        ax_a.add_patch(mini)
        ax_a.text(cx + dx, cy, comp, ha="center", va="center",
                  fontsize=6, color="#475569", zorder=4)

# key modules legend
legend_items = [
    mpatches.Patch(facecolor="#DBEAFE", edgecolor=BLUE,   label="Encoding"),
    mpatches.Patch(facecolor="#FEF3C7", edgecolor="#D97706", label="Reasoning"),
    mpatches.Patch(facecolor="#D1FAE5", edgecolor="#059669", label="Decoding"),
]
ax_a.legend(handles=legend_items, loc="lower center", ncol=3,
            fontsize=6.5, frameon=False, bbox_to_anchor=(0.5, -0.02))

# ══════════════════════════════════════════════════════════════════════════════
# PANEL B – ablation bars
# ══════════════════════════════════════════════════════════════════════════════
panel_label(ax_b, "B")
items  = d["panel_b"]["items"]
values = d["panel_b"]["values"]
full_val = values[0]

colors = [BLUE if v == full_val else "#93C5FD" for v in values]
bars = ax_b.barh(items[::-1], values[::-1], color=colors[::-1],
                 edgecolor="white", linewidth=0.5, height=0.6)

# value labels
for bar, val in zip(bars, values[::-1]):
    ax_b.text(val + 0.3, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7, color=DARK)

ax_b.set_xlabel("Accuracy (%)", fontsize=7)
ax_b.set_xlim(50, 70)
ax_b.set_title("Ablation Study", fontsize=8, fontweight="bold", pad=4)
ax_b.axvline(full_val, color=BLUE, lw=1, ls="--", alpha=0.5)
ax_b.tick_params(axis="y", labelsize=7)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL C – training curves
# ══════════════════════════════════════════════════════════════════════════════
panel_label(ax_c, "C")
steps    = d["panel_c"]["steps"]
baseline = d["panel_c"]["Baseline"]
ours     = d["panel_c"]["Ours"]

ax_c.plot(steps, baseline, color=GRAY,   lw=1.5, label="Baseline", zorder=2)
ax_c.plot(steps, ours,     color=ORANGE, lw=1.5, label="Ours",     zorder=3)
ax_c.fill_between(steps, baseline, ours, alpha=0.12, color=ORANGE)

ax_c.set_xlabel("Training Step", fontsize=7)
ax_c.set_ylabel("Loss",          fontsize=7)
ax_c.set_title("Training Convergence", fontsize=8, fontweight="bold", pad=4)
ax_c.legend(fontsize=7, frameon=False, loc="upper right")
ax_c.set_xlim(0, 29)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL D – 5×5 heatmap
# ══════════════════════════════════════════════════════════════════════════════
panel_label(ax_d, "D")
matrix = np.array(d["panel_d"]["matrix"])
x_labels = d["panel_d"]["x"]
y_labels = d["panel_d"]["y"]

im = ax_d.imshow(matrix, cmap="Blues", aspect="auto", vmin=0, vmax=1)

ax_d.set_xticks(range(len(x_labels)))
ax_d.set_xticklabels(x_labels, fontsize=8)
ax_d.set_yticks(range(len(y_labels)))
ax_d.set_yticklabels(y_labels, fontsize=8)
ax_d.set_xlabel("Sweep Parameter S", fontsize=8)
ax_d.set_ylabel("Probe P",           fontsize=8)
ax_d.set_title("Sensitivity Sweep (5×5)", fontsize=9, fontweight="bold", pad=5)

# cell annotations
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        color = "white" if val > 0.6 else DARK
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8, color=color, fontweight="semibold")

cbar = fig.colorbar(im, ax=ax_d, fraction=0.015, pad=0.01)
cbar.set_label("Score", fontsize=7)
cbar.ax.tick_params(labelsize=7)

# ── save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg",           bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
