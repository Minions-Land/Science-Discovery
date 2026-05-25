"""
4-panel hero figure: method overview + ablation bars + training curves + sensitivity heatmap.
Data source: data.json (all values from file; no hardcoded numbers).

layout: gridspec(2, 3, width_ratios=[2,1,1], height_ratios=[1.4, 1])
figsize: 11x6 inches
layout-budget: legend inside axes, caption external
"""

import json
import pathlib
import subprocess
import sys

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

# ── Palette (single blue-family + neutral grey) ──────────────────────────────
PALETTE = {
    "signal":       "#2B5BA8",   # deep blue — Ours / full method
    "signal_mid":   "#5A85C8",   # mid blue — ablation 1
    "signal_soft":  "#8AAEE0",   # soft blue — ablation 2
    "neutral":      "#9A9A9A",   # grey — ablation 3
    "neutral_light":"#C4C4C4",   # light grey — ablation 4
    "baseline":     "#D8D8D8",   # near-white grey — baseline line
    "bg":           "#F5F5F5",   # panel A background tint
    "black":        "#272727",
    "text_dark":    "#3A3A3A",
}

# ── Load data ────────────────────────────────────────────────────────────────
data = json.loads(pathlib.Path("data.json").read_text())

pb = data["panel_b"]
pc = data["panel_c"]
pd = data["panel_d"]

# ── Figure layout ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(11, 6))
gs = fig.add_gridspec(
    2, 3,
    width_ratios=[2, 1, 1],
    height_ratios=[1.4, 1],
    left=0.06, right=0.97,
    top=0.93, bottom=0.10,
    wspace=0.38, hspace=0.52,
)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[1, :])

# ── Panel label helper ───────────────────────────────────────────────────────
def panel_label(ax, letter):
    ax.text(
        -0.12, 1.06, letter,
        transform=ax.transAxes,
        fontsize=11, fontweight="bold",
        va="top", ha="left",
        color=PALETTE["black"],
    )

# ════════════════════════════════════════════════════════════════════════════
# Panel A — Method overview (3-stage pipeline diagram)
# ════════════════════════════════════════════════════════════════════════════
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)
ax_a.set_facecolor(PALETTE["bg"])
ax_a.axis("off")
panel_label(ax_a, "A")

# Background title
ax_a.text(0.5, 0.93, "Method Overview", ha="center", va="top",
          fontsize=9, fontweight="bold", color=PALETTE["black"])

# Stage boxes
stages = [
    ("Stage 1\nInput\nEncoding",  0.13, "#D6E4F7"),
    ("Stage 2\nAttention\n+ Memory", 0.50, "#B8D4F0"),
    ("Stage 3\nSkill-gated\nDecoding", 0.87, "#8AAEE0"),
]
box_w, box_h = 0.22, 0.30
box_y = 0.46

for label, cx, fc in stages:
    rect = mpatches.FancyBboxPatch(
        (cx - box_w / 2, box_y - box_h / 2), box_w, box_h,
        boxstyle="round,pad=0.015",
        facecolor=fc, edgecolor=PALETTE["signal"], linewidth=1.0,
        transform=ax_a.transAxes, clip_on=False,
    )
    ax_a.add_patch(rect)
    ax_a.text(cx, box_y, label, ha="center", va="center",
              fontsize=7.5, color=PALETTE["black"],
              transform=ax_a.transAxes)

# Arrows between stages
arrow_kw = dict(
    transform=ax_a.transAxes,
    arrowprops=dict(arrowstyle="-|>", color=PALETTE["signal"],
                    lw=1.2, mutation_scale=10),
    annotation_clip=False,
)
ax_a.annotate("", xy=(stages[1][1] - box_w / 2 - 0.01, box_y),
              xytext=(stages[0][1] + box_w / 2 + 0.01, box_y), **arrow_kw)
ax_a.annotate("", xy=(stages[2][1] - box_w / 2 - 0.01, box_y),
              xytext=(stages[1][1] + box_w / 2 + 0.01, box_y), **arrow_kw)

# Input / Output labels
ax_a.text(0.02, box_y, "Input\nTokens", ha="left", va="center",
          fontsize=7, color=PALETTE["neutral"], transform=ax_a.transAxes)
ax_a.text(0.98, box_y, "Output\nPrediction", ha="right", va="center",
          fontsize=7, color=PALETTE["neutral"], transform=ax_a.transAxes)

# Residual skip connection arc
from matplotlib.patches import Arc
arc = Arc((0.50, box_y - box_h / 2 - 0.10), 0.74, 0.18,
          angle=0, theta1=0, theta2=180,
          color=PALETTE["signal_soft"], lw=1.0,
          transform=ax_a.transAxes)
ax_a.add_patch(arc)
ax_a.text(0.50, box_y - box_h / 2 - 0.20, "residual skip",
          ha="center", va="top", fontsize=6.5,
          color=PALETTE["signal_soft"], transform=ax_a.transAxes)

# Component legend (bottom)
legend_items = [
    ("Attention", PALETTE["signal_mid"]),
    ("Memory", PALETTE["signal_soft"]),
    ("Skill gate", PALETTE["signal"]),
]
for i, (lbl, col) in enumerate(legend_items):
    lx = 0.18 + i * 0.30
    ax_a.add_patch(mpatches.Rectangle(
        (lx - 0.04, 0.06), 0.08, 0.055,
        facecolor=col, edgecolor="none",
        transform=ax_a.transAxes, alpha=0.7,
    ))
    ax_a.text(lx, 0.04, lbl, ha="center", va="top",
              fontsize=6.5, color=PALETTE["text_dark"],
              transform=ax_a.transAxes)

# ════════════════════════════════════════════════════════════════════════════
# Panel B — Ablation bars
# ════════════════════════════════════════════════════════════════════════════
panel_label(ax_b, "B")

items = pb["items"]
values = np.array(pb["values"])
n = len(items)
x = np.arange(n)

# Color: full method = signal blue; ablations = graded neutrals
bar_colors = [
    PALETTE["signal"],
    PALETTE["signal_mid"],
    PALETTE["signal_soft"],
    PALETTE["neutral"],
    PALETTE["neutral_light"],
]

bars = ax_b.bar(x, values, width=0.65, color=bar_colors, zorder=3)

# Value labels on bars
for bar, val in zip(bars, values):
    ax_b.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
              f"{val:.1f}", ha="center", va="bottom",
              fontsize=7, color=PALETTE["text_dark"])

# Zoom y-axis to data range
span = values.max() - values.min()
ax_b.set_ylim(values.min() - 0.10 * span, values.max() + 0.18 * span)

ax_b.set_xticks(x)
ax_b.set_xticklabels(items, fontsize=7, rotation=30, ha="right")
ax_b.set_ylabel("Score", fontsize=8)
ax_b.tick_params(direction="out", length=2.2, width=0.6)
ax_b.yaxis.grid(True, linewidth=0.4, color="#E0E0E0", zorder=0)
ax_b.set_axisbelow(True)

# ════════════════════════════════════════════════════════════════════════════
# Panel C — Training curves (Baseline vs Ours)
# ════════════════════════════════════════════════════════════════════════════
panel_label(ax_c, "C")

steps = np.array(pc["steps"])
baseline = np.array(pc["Baseline"])
ours = np.array(pc["Ours"])

ax_c.plot(steps, baseline, color=PALETTE["neutral"],
          linewidth=1.6, label="Baseline", zorder=3)
ax_c.plot(steps, ours, color=PALETTE["signal"],
          linewidth=1.6, label="Ours", zorder=4)

# Annotate final-step gap
gap = baseline[-1] - ours[-1]
ax_c.annotate(
    f"−{gap:.2f}",
    xy=(steps[-1], ours[-1]),
    xytext=(-28, 6), textcoords="offset points",
    fontsize=7, color=PALETTE["signal"],
    arrowprops=dict(arrowstyle="-", color=PALETTE["signal"],
                    lw=0.7, shrinkA=0, shrinkB=0),
)

ax_c.set_xlabel("Training step", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.tick_params(direction="out", length=2.2, width=0.6)
ax_c.legend(fontsize=8, loc="upper right")
ax_c.yaxis.grid(True, linewidth=0.4, color="#E0E0E0", zorder=0)
ax_c.set_axisbelow(True)

# ════════════════════════════════════════════════════════════════════════════
# Panel D — 5×5 sensitivity heatmap (full-width bottom)
# ════════════════════════════════════════════════════════════════════════════
panel_label(ax_d, "D")

matrix = np.array(pd["matrix"])
x_labels = pd["x"]
y_labels = pd["y"]

im = ax_d.imshow(
    matrix, aspect="auto", cmap="Blues",
    vmin=0, vmax=1, interpolation="nearest",
)

# Cell value annotations
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        txt_color = "white" if val > 0.65 else PALETTE["text_dark"]
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8, color=txt_color)

ax_d.set_xticks(np.arange(len(x_labels)))
ax_d.set_yticks(np.arange(len(y_labels)))
ax_d.set_xticklabels(x_labels, fontsize=8)
ax_d.set_yticklabels(y_labels, fontsize=8)
ax_d.set_xlabel("Hyperparameter S", fontsize=8)
ax_d.set_ylabel("Hyperparameter P", fontsize=8)
ax_d.tick_params(direction="out", length=2.2, width=0.6)
ax_d.spines["left"].set_visible(True)
ax_d.spines["bottom"].set_visible(True)

cbar = fig.colorbar(im, ax=ax_d, fraction=0.015, pad=0.01)
cbar.ax.tick_params(labelsize=7)
cbar.set_label("Score", fontsize=7)

# ── Save ─────────────────────────────────────────────────────────────────────
out_pdf = pathlib.Path("figure.pdf")
out_png = pathlib.Path("figure.png")
out_svg = pathlib.Path("figure.svg")

fig.savefig(out_pdf, bbox_inches="tight")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
fig.savefig(out_svg, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {out_pdf}, {out_png}, {out_svg}")

# ── Font-type verification ────────────────────────────────────────────────────
result = subprocess.run(
    ["pdffonts", str(out_pdf)],
    capture_output=True, text=True, check=False,
)
if result.returncode == 0:
    if "Type 3" in result.stdout:
        sys.stderr.write(
            f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{result.stdout}\n"
        )
        sys.exit(2)
    print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")
else:
    # pdffonts not available — fallback to raw byte scan
    raw = out_pdf.read_bytes()
    import re
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (byte-scan fallback) — no /Type3 in figure.pdf")
