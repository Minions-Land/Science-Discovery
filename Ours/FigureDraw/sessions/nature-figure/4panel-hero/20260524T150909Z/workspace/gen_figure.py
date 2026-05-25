import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

pb = data["panel_b"]
pc = data["panel_c"]
pd = data["panel_d"]

# ── style ─────────────────────────────────────────────────────────────────────
BLUE   = "#2563EB"
ORANGE = "#F59E0B"
TEAL   = "#0D9488"
GRAY   = "#94A3B8"
BG     = "#F8FAFC"
DARK   = "#1E293B"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.facecolor": BG,
    "figure.facecolor": "white",
    "axes.labelcolor": DARK,
    "xtick.color": DARK,
    "ytick.color": DARK,
    "text.color": DARK,
})

# ── figure / gridspec ─────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 9))

outer = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38,
                          top=0.95, bottom=0.07, left=0.07, right=0.97)
top_gs = gridspec.GridSpecFromSubplotSpec(
    1, 3, subplot_spec=outer[0], wspace=0.38, width_ratios=[2, 1, 1]
)
bot_gs = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[1])

ax_a = fig.add_subplot(top_gs[0])
ax_b = fig.add_subplot(top_gs[1])
ax_c = fig.add_subplot(top_gs[2])
ax_d = fig.add_subplot(bot_gs[0])

# ── panel-label helper ────────────────────────────────────────────────────────
def panel_label(ax, letter):
    ax.text(-0.10, 1.08, letter, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="top", ha="left",
            fontfamily="sans-serif", color=DARK)

# ── Panel A: method overview ──────────────────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 10)
ax_a.axis("off")
ax_a.set_facecolor(BG)

def stage_box(ax, x, y, w, h, label, sub, color):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor="white",
                         linewidth=1.5, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.62, label, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white", zorder=4)
    ax.text(x + w/2, y + h*0.28, sub, ha="center", va="center",
            fontsize=6.5, color="white", alpha=0.92, zorder=4)

def arrow(ax, x1, x2, y):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                lw=1.6, mutation_scale=12),
                zorder=2)

# title
ax_a.text(5, 9.4, "3-Stage Pipeline", ha="center", va="center",
          fontsize=10, fontweight="bold", color=DARK)

# input icon
ax_a.text(0.55, 6.85, "Input\nData", ha="center", va="center",
          fontsize=7, color=GRAY)
circ = plt.Circle((0.55, 5.85), 0.5, color=GRAY, alpha=0.25, zorder=2)
ax_a.add_patch(circ)
ax_a.text(0.55, 5.85, "X", ha="center", va="center",
          fontsize=9, color=GRAY, fontweight="bold")

arrow(ax_a, 1.1, 1.9, 5.85)

# stage boxes
stage_box(ax_a, 1.9, 4.9, 2.2, 1.9, "Stage 1", "Feature\nExtraction", BLUE)
arrow(ax_a,  4.1, 4.85, 5.85)
stage_box(ax_a, 4.85, 4.9, 2.2, 1.9, "Stage 2", "Attention\n+ Memory", TEAL)
arrow(ax_a,  7.05, 7.8, 5.85)
stage_box(ax_a, 7.8, 4.9, 1.85, 1.9, "Stage 3", "Skill\nHead", ORANGE)

# output
arrow(ax_a, 9.65, 10.0, 5.85)  # clips to axis edge

# ablation legend inside A
ablation_items = [
    mpatches.Patch(facecolor=BLUE,   label="Attention"),
    mpatches.Patch(facecolor=TEAL,   label="Memory"),
    mpatches.Patch(facecolor=ORANGE, label="Skill Head"),
    mpatches.Patch(facecolor=GRAY,   label="Residual"),
]
legend = ax_a.legend(handles=ablation_items,
                     loc="lower center", ncol=4,
                     fontsize=6.5, frameon=True,
                     framealpha=0.85, edgecolor="#CBD5E1",
                     handlelength=1.0, handletextpad=0.4,
                     columnspacing=0.8,
                     bbox_to_anchor=(0.5, 0.02))

# component annotation brackets
for (xs, xe, yl, txt, col) in [
    (1.9, 4.1,  3.8, "Encoder",   BLUE),
    (4.85, 7.05, 3.8, "Reasoner",  TEAL),
    (7.8,  9.65, 3.8, "Decoder",   ORANGE),
]:
    ax_a.annotate("", xy=(xe, yl+0.3), xytext=(xs, yl+0.3),
                  arrowprops=dict(arrowstyle="|-|,widthA=0.2,widthB=0.2",
                                  color=col, lw=1.2), zorder=2)
    ax_a.text((xs+xe)/2, yl, txt, ha="center", va="center",
              fontsize=6.5, color=col)

panel_label(ax_a, "A")

# ── Panel B: ablation bars ────────────────────────────────────────────────────
items  = pb["items"]
values = pb["values"]
colors = [BLUE if v == max(values) else "#93C5FD" for v in values]
bars = ax_b.barh(items, values, color=colors, edgecolor="white",
                 linewidth=0.8, height=0.6)
ax_b.set_xlabel("Accuracy (%)", fontsize=8)
ax_b.set_xlim(48, 70)
ax_b.tick_params(labelsize=7.5)
ax_b.axvline(values[0], color=BLUE, linewidth=1.0, linestyle="--", alpha=0.5)
for bar, v in zip(bars, values):
    ax_b.text(v + 0.3, bar.get_y() + bar.get_height()/2,
              f"{v:.1f}", va="center", fontsize=7, color=DARK)
ax_b.set_title("Ablation", fontsize=9, pad=6)
panel_label(ax_b, "B")

# ── Panel C: training curves ──────────────────────────────────────────────────
steps    = pc["steps"]
baseline = pc["Baseline"]
ours     = pc["Ours"]

ax_c.plot(steps, baseline, color=GRAY,   linewidth=1.6, label="Baseline",
          zorder=2)
ax_c.plot(steps, ours,     color=ORANGE, linewidth=1.8, label="Ours",
          zorder=3)
ax_c.fill_between(steps, baseline, ours, alpha=0.12, color=ORANGE)
ax_c.set_xlabel("Training step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.tick_params(labelsize=7.5)
ax_c.legend(fontsize=7.5, frameon=False, loc="upper right")
ax_c.set_title("Training Trend", fontsize=9, pad=6)
panel_label(ax_c, "C")

# ── Panel D: 5×5 heatmap ─────────────────────────────────────────────────────
matrix = np.array(pd["matrix"])
xlabels = pd["x"]
ylabels = pd["y"]

im = ax_d.imshow(matrix, cmap="YlOrRd", aspect="auto",
                 vmin=0.0, vmax=1.0, interpolation="nearest")
ax_d.set_xticks(range(len(xlabels)))
ax_d.set_xticklabels(xlabels, fontsize=9)
ax_d.set_yticks(range(len(ylabels)))
ax_d.set_yticklabels(ylabels, fontsize=9)
ax_d.set_xlabel("Sensitivity Parameter S", fontsize=9)
ax_d.set_ylabel("Perturbation P", fontsize=9)
ax_d.set_title("Sensitivity Sweep", fontsize=9, pad=6)
ax_d.tick_params(length=0)

# cell annotations
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        v = matrix[i, j]
        txt_col = "white" if v > 0.65 else DARK
        ax_d.text(j, i, f"{v:.2f}", ha="center", va="center",
                  fontsize=8.5, color=txt_col, fontweight="bold")

cbar = fig.colorbar(im, ax=ax_d, orientation="vertical",
                    fraction=0.018, pad=0.02)
cbar.set_label("Score", fontsize=8)
cbar.ax.tick_params(labelsize=7.5)

panel_label(ax_d, "D")

# ── save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=200, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
