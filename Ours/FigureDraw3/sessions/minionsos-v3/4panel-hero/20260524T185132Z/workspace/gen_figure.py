"""
gen_figure.py  --  4-panel hero figure
layout: gridspec(2, 3, width_ratios=[2,1,1], height_ratios=[1.4, 1])
figsize: 11x6 inches (= 280 x 152 mm)
layout-budget choice: panel labels bold 9pt, no above-axes legend, caption external
Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
Do NOT override per element — all text inherits from here.
"""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

# ── rcParams ──────────────────────────────────────────────────────────────────
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

# ── palette ───────────────────────────────────────────────────────────────────
PALETTE = {
    "signal":       "#0F4D92",
    "signal_soft":  "#B4C0E4",
    "neutral":      "#767676",
    "neutral_light": "#D8D8D8",
    "accent":       "#D55E00",
    "accent_soft":  "#F5C6A8",
    "black":        "#272727",
    "bg":           "#F7F7F7",
}

# ── data ─────────────────────────────────────────────────────────────────────
here = Path(__file__).parent
with open(here / "data.json") as f:
    data = json.load(f)

# panel B
b_items  = data["panel_b"]["items"]
b_values = np.array(data["panel_b"]["values"])

# panel C
steps    = np.array(data["panel_c"]["steps"])
baseline = np.array(data["panel_c"]["Baseline"])
ours     = np.array(data["panel_c"]["Ours"])

# panel D
d_x      = data["panel_d"]["x"]
d_y      = data["panel_d"]["y"]
d_matrix = np.array(data["panel_d"]["matrix"])

# ── figure / gridspec ─────────────────────────────────────────────────────────
fig = plt.figure(figsize=(11, 6))
gs = fig.add_gridspec(
    2, 3,
    width_ratios=[2, 1, 1],
    height_ratios=[1.4, 1],
    left=0.06, right=0.97,
    top=0.94, bottom=0.10,
    wspace=0.40, hspace=0.52,
)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[1, :])


# ═══════════════════════════════════════════════════════════════════════════════
# Panel A — Method overview: 3-stage pipeline
# ═══════════════════════════════════════════════════════════════════════════════
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 10)
ax_a.axis("off")
ax_a.set_facecolor(PALETTE["bg"])
fig.patches.extend([mpatches.FancyBboxPatch(
    (ax_a.get_position().x0, ax_a.get_position().y0),
    ax_a.get_position().width, ax_a.get_position().height,
    boxstyle="round,pad=0.005",
    transform=fig.transFigure, zorder=0,
    facecolor=PALETTE["bg"], edgecolor="none"
)])

# Stage boxes (x centres at 1.3, 5, 8.7; y band 3.5–8.5)
stages = [
    ("Stage 1\nInput\nEncoding",  1.3, 5.8, PALETTE["signal"],      PALETTE["signal_soft"]),
    ("Stage 2\nAttentive\nMemory", 5.0, 5.8, PALETTE["accent"],      PALETTE["accent_soft"]),
    ("Stage 3\nAdaptive\nDecoding", 8.7, 5.8, "#1A7A4A",             "#A8DBBE"),
]

box_w, box_h = 2.3, 2.7
for label, cx, cy, fc, bg in stages:
    rect = mpatches.FancyBboxPatch(
        (cx - box_w/2, cy - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.15",
        linewidth=1.4, edgecolor=fc, facecolor=bg,
        transform=ax_a.transData, zorder=3,
    )
    ax_a.add_patch(rect)
    ax_a.text(cx, cy, label, ha="center", va="center",
              fontsize=7.5, fontweight="bold", color=fc,
              multialignment="center", zorder=4)

# Arrows between stages
for x0, x1 in [(2.5, 3.85), (6.15, 7.55)]:
    ax_a.annotate("", xy=(x1, 5.8), xytext=(x0, 5.8),
                  arrowprops=dict(arrowstyle="-|>", color=PALETTE["neutral"],
                                  lw=1.4, mutation_scale=12),
                  zorder=4)

# Input node (left)
ax_a.add_patch(mpatches.FancyBboxPatch(
    (0.05, 5.0), 0.65, 1.5,
    boxstyle="round,pad=0.1", linewidth=1.0,
    edgecolor=PALETTE["neutral"], facecolor="white", zorder=3
))
ax_a.text(0.375, 5.75, "Input", ha="center", va="center",
          fontsize=6.5, color=PALETTE["neutral"], zorder=4)
ax_a.annotate("", xy=(0.7 + box_w/2 - 1.85, 5.8), xytext=(0.70, 5.8),
              arrowprops=dict(arrowstyle="-|>", color=PALETTE["neutral"],
                              lw=1.2, mutation_scale=10), zorder=4)

# Output node (right)
ax_a.add_patch(mpatches.FancyBboxPatch(
    (9.3, 5.0), 0.65, 1.5,
    boxstyle="round,pad=0.1", linewidth=1.0,
    edgecolor="#1A7A4A", facecolor="white", zorder=3
))
ax_a.text(9.625, 5.75, "Output", ha="center", va="center",
          fontsize=6.5, color="#1A7A4A", zorder=4)
ax_a.annotate("", xy=(9.3, 5.8), xytext=(8.7 + box_w/2, 5.8),
              arrowprops=dict(arrowstyle="-|>", color="#1A7A4A",
                              lw=1.2, mutation_scale=10), zorder=4)

# Key component callouts below pipeline
components = [
    (1.3, 3.0, "Self-attention\n+ positional\nembedding", PALETTE["signal"]),
    (5.0, 3.0, "Episodic\nmemory\ncache", PALETTE["accent"]),
    (8.7, 3.0, "Residual\nskill\nadapter", "#1A7A4A"),
]
for cx, cy, txt, fc in components:
    ax_a.plot([cx, cx], [cy + 0.65, cy + 1.2], color=fc, lw=0.8, ls="--", zorder=2)
    ax_a.text(cx, cy, txt, ha="center", va="top",
              fontsize=6.2, color=fc, multialignment="center", zorder=4)

# Title for panel A
ax_a.text(5.0, 9.3, "Method Overview: Three-Stage Pipeline",
          ha="center", va="top", fontsize=8, fontweight="bold",
          color=PALETTE["black"], zorder=4)

# Ablation impact legend (bottom strip)
for i, (label, color) in enumerate([
    ("-attn", PALETTE["signal"]),
    ("-mem", PALETTE["accent"]),
    ("-residual", "#1A7A4A"),
    ("-skill", "#7B2D8B"),
]):
    ax_a.add_patch(mpatches.Rectangle(
        (0.5 + i*2.3, 0.5), 0.35, 0.35,
        transform=ax_a.transData, color=color, zorder=3
    ))
    ax_a.text(0.95 + i*2.3, 0.67, label, va="center",
              fontsize=6, color=PALETTE["neutral"], zorder=4)


# ═══════════════════════════════════════════════════════════════════════════════
# Panel B — Ablation bars
# ═══════════════════════════════════════════════════════════════════════════════
bar_colors = [PALETTE["signal"] if n == "full" else PALETTE["neutral_light"]
              for n in b_items]
bar_colors[0] = PALETTE["signal"]

bars = ax_b.barh(b_items, b_values, color=bar_colors,
                 edgecolor="none", height=0.55)

# Zoom y-axis to data range
span = b_values.max() - b_values.min()
ax_b.set_xlim(b_values.min() - 0.1*span, b_values.max() + 0.18*span)
ax_b.tick_params(axis="x", direction="out", length=2.2, width=0.6, labelsize=7)
ax_b.tick_params(axis="y", direction="out", length=0, labelsize=7.5)
ax_b.set_xlabel("Accuracy (%)", fontsize=8, labelpad=4)
ax_b.set_title("Ablation", fontsize=8.5, fontweight="bold", pad=6)

# Value labels on bars
for bar, val in zip(bars, b_values):
    ax_b.text(val + 0.08*span, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=6.8, color=PALETTE["black"])


# ═══════════════════════════════════════════════════════════════════════════════
# Panel C — Training trend
# ═══════════════════════════════════════════════════════════════════════════════
ax_c.plot(steps, baseline, color=PALETTE["neutral"], lw=1.5,
          label="Baseline", zorder=2)
ax_c.plot(steps, ours, color=PALETTE["signal"], lw=1.8,
          label="Ours", zorder=3)

ax_c.set_yscale("log")
ax_c.set_xlabel("Step (×1k)", fontsize=8, labelpad=4)
ax_c.set_ylabel("Loss", fontsize=8, labelpad=4)
ax_c.set_title("Training Trend", fontsize=8.5, fontweight="bold", pad=6)
ax_c.tick_params(direction="out", length=2.2, width=0.6, labelsize=7)
ax_c.legend(fontsize=7, loc="upper right")

# Annotate final-step gap
gap = baseline[-1] - ours[-1]
ax_c.annotate("", xy=(steps[-1], ours[-1]),
              xytext=(steps[-1], baseline[-1]),
              arrowprops=dict(arrowstyle="<->", color=PALETTE["accent"], lw=1.0))
ax_c.text(steps[-1] + 0.5, (ours[-1] + baseline[-1])/2,
          f"Δ{gap:.2f}", fontsize=6.5, color=PALETTE["accent"], va="center")


# ═══════════════════════════════════════════════════════════════════════════════
# Panel D — 5×5 sensitivity heatmap (full-width bottom)
# ═══════════════════════════════════════════════════════════════════════════════
im = ax_d.imshow(d_matrix, cmap="Blues", vmin=0, vmax=1, aspect="auto")

ax_d.set_xticks(range(len(d_x)))
ax_d.set_xticklabels(d_x, fontsize=8)
ax_d.set_yticks(range(len(d_y)))
ax_d.set_yticklabels(d_y, fontsize=8)
ax_d.set_xlabel("Sensitivity parameter", fontsize=8.5, labelpad=4)
ax_d.set_ylabel("Probe\ndepth", fontsize=8.5, labelpad=4)
ax_d.set_title("Sensitivity Sweep (5×5)", fontsize=9, fontweight="bold", pad=6)
ax_d.tick_params(direction="out", length=0, width=0)
ax_d.spines[:].set_visible(False)

# Cell annotations
for i in range(len(d_y)):
    for j in range(len(d_x)):
        v = d_matrix[i, j]
        ax_d.text(j, i, f"{v:.2f}", ha="center", va="center",
                  fontsize=7.5, color="white" if v > 0.6 else PALETTE["black"],
                  fontweight="bold" if v > 0.85 else "normal")

cbar = fig.colorbar(im, ax=ax_d, fraction=0.012, pad=0.015)
cbar.ax.tick_params(labelsize=7)
cbar.set_label("Score", fontsize=7.5)


# ═══════════════════════════════════════════════════════════════════════════════
# Panel labels A B C D
# ═══════════════════════════════════════════════════════════════════════════════
label_kw = dict(fontsize=11, fontweight="bold", ha="left", va="top",
                transform=fig.transFigure, color=PALETTE["black"],
                fontfamily="sans-serif")

for ax, letter in [(ax_a, "A"), (ax_b, "B"), (ax_c, "C"), (ax_d, "D")]:
    pos = ax.get_position()
    fig.text(pos.x0 - 0.005, pos.y1 + 0.012, letter, **label_kw)


# ═══════════════════════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════════════════════
out = here
fig.savefig(out / "figure.pdf", bbox_inches="tight")
fig.savefig(out / "figure.png", dpi=300, bbox_inches="tight")
fig.savefig(out / "figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
