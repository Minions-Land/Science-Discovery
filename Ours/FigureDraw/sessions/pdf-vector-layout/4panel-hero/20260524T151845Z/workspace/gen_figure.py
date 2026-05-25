import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from pathlib import Path

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

pb = d["panel_b"]
pc = d["panel_c"]
pd = d["panel_d"]

# ── figure layout ──────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 7))
fig.patch.set_facecolor("white")

outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38,
                          top=0.94, bottom=0.08, left=0.06, right=0.97)

top_gs = gridspec.GridSpecFromSubplotSpec(
    1, 3, subplot_spec=outer[0], wspace=0.38, width_ratios=[2, 1, 1]
)

ax_a = fig.add_subplot(top_gs[0])
ax_b = fig.add_subplot(top_gs[1])
ax_c = fig.add_subplot(top_gs[2])
ax_d = fig.add_subplot(outer[1])

LABEL_KW = dict(fontsize=11, fontweight="bold", fontfamily="sans-serif",
                va="top", ha="left")

# ── Panel A: method overview diagram ──────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis("off")

STAGE_COLOR = ["#4C72B0", "#55A868", "#C44E52"]
STAGE_LABEL = ["Stage 1\nEncode", "Stage 2\nReason", "Stage 3\nDecode"]
STAGE_X = [1.2, 4.5, 7.8]
BOX_W, BOX_H = 1.9, 1.1

for i, (sx, sl, sc) in enumerate(zip(STAGE_X, STAGE_LABEL, STAGE_COLOR)):
    rect = mpatches.FancyBboxPatch(
        (sx - BOX_W / 2, 2.6), BOX_W, BOX_H,
        boxstyle="round,pad=0.12", linewidth=1.4,
        edgecolor=sc, facecolor=sc + "22"
    )
    ax_a.add_patch(rect)
    ax_a.text(sx, 3.15, sl, ha="center", va="center",
              fontsize=8.5, color=sc, fontweight="bold", linespacing=1.3)

# arrows between stages
for x0, x1 in [(STAGE_X[0] + BOX_W / 2, STAGE_X[1] - BOX_W / 2),
               (STAGE_X[1] + BOX_W / 2, STAGE_X[2] - BOX_W / 2)]:
    ax_a.annotate("", xy=(x1, 3.15), xytext=(x0, 3.15),
                  arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.3))

# input / output labels
ax_a.text(0.15, 3.15, "Input\n$x$", ha="center", va="center",
          fontsize=8, color="#333")
ax_a.annotate("", xy=(STAGE_X[0] - BOX_W / 2, 3.15), xytext=(0.55, 3.15),
              arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.3))

ax_a.text(9.85, 3.15, "Output\n$\\hat{y}$", ha="center", va="center",
          fontsize=8, color="#333")
ax_a.annotate("", xy=(9.45, 3.15), xytext=(STAGE_X[2] + BOX_W / 2, 3.15),
              arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.3))

# skill / memory annotations below
for sx, note in zip(STAGE_X, ["Token\nembedding", "Attention +\nMemory", "Skill\nhead"]):
    ax_a.text(sx, 2.3, note, ha="center", va="top",
              fontsize=7.5, color="#666", linespacing=1.3)

# title inside panel
ax_a.text(5.0, 5.7, "3-Stage Pipeline", ha="center", va="top",
          fontsize=9.5, fontweight="bold", color="#222")

ax_a.text(0.01, 1.0, "Panel A", transform=ax_a.transAxes,
          fontsize=11, fontweight="bold", fontfamily="sans-serif",
          va="bottom", ha="left", color="#222")

# ── Panel B: ablation bars ─────────────────────────────────────────────────
colors_b = ["#4C72B0" if v == max(pb["values"]) else "#9DB8D2"
            for v in pb["values"]]
bars = ax_b.barh(pb["items"], pb["values"], color=colors_b,
                 edgecolor="white", height=0.6)
ax_b.set_xlim(50, 68)
ax_b.set_xlabel("Score", fontsize=8)
ax_b.tick_params(axis="y", labelsize=8)
ax_b.tick_params(axis="x", labelsize=7.5)
ax_b.spines[["top", "right"]].set_visible(False)
for bar, val in zip(bars, pb["values"]):
    ax_b.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
              f"{val:.1f}", va="center", fontsize=7.5, color="#333")
ax_b.set_title("Ablation", fontsize=9, pad=4)
ax_b.text(-0.18, 1.04, "B", transform=ax_b.transAxes, **LABEL_KW)

# ── Panel C: training curves ───────────────────────────────────────────────
steps = pc["steps"]
ax_c.plot(steps, pc["Baseline"], color="#9DB8D2", lw=1.5,
          label="Baseline", linestyle="--")
ax_c.plot(steps, pc["Ours"], color="#4C72B0", lw=1.8, label="Ours")
ax_c.set_xlabel("Step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.tick_params(labelsize=7.5)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.legend(fontsize=7.5, frameon=False)
ax_c.set_title("Training Trend", fontsize=9, pad=4)
ax_c.text(-0.22, 1.04, "C", transform=ax_c.transAxes, **LABEL_KW)

# ── Panel D: 5×5 heatmap ──────────────────────────────────────────────────
mat = np.array(pd["matrix"])
im = ax_d.imshow(mat, aspect="auto", cmap="viridis", vmin=0, vmax=1)
ax_d.set_xticks(range(5))
ax_d.set_xticklabels(pd["x"], fontsize=9)
ax_d.set_yticks(range(5))
ax_d.set_yticklabels(pd["y"], fontsize=9)
ax_d.set_xlabel("Sweep parameter S", fontsize=9)
ax_d.set_ylabel("Sweep parameter P", fontsize=9)
ax_d.set_title("Sensitivity Sweep", fontsize=9, pad=4)
for i in range(5):
    for j in range(5):
        ax_d.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center",
                  fontsize=8, color="white" if mat[i, j] < 0.6 else "black")
cbar = fig.colorbar(im, ax=ax_d, fraction=0.025, pad=0.02)
cbar.ax.tick_params(labelsize=8)
cbar.set_label("Score", fontsize=8)
ax_d.text(-0.06, 1.04, "D", transform=ax_d.transAxes, **LABEL_KW)

# ── Panel A label (axes coords) ────────────────────────────────────────────
ax_a.text(0.01, 1.04, "A", transform=ax_a.transAxes, **LABEL_KW)

# ── save ───────────────────────────────────────────────────────────────────
out = Path(".")
fig.savefig(out / "figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig(out / "figure.png", dpi=150, bbox_inches="tight")
fig.savefig(out / "figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
