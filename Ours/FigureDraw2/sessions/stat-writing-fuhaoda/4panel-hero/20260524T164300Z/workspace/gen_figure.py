import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

pb = d["panel_b"]
pc = d["panel_c"]
pd = d["panel_d"]

# ── figure layout ──────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 7))
gs = gridspec.GridSpec(2, 3, width_ratios=[2, 1, 1],
                       hspace=0.42, wspace=0.38,
                       left=0.06, right=0.97, top=0.93, bottom=0.09)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[1, :])

LABEL_KW = dict(fontsize=11, fontweight="bold", fontfamily="sans-serif",
                va="top", ha="left")
ACCENT   = "#2563EB"   # blue
ORANGE   = "#EA580C"
GRAY     = "#6B7280"

# ── Panel A: method overview diagram ──────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis("off")

stages = [
    ("Stage 1\nEncode", 1.0, 3.0, ACCENT),
    ("Stage 2\nReason", 4.0, 3.0, "#7C3AED"),
    ("Stage 3\nDecode", 7.0, 3.0, ORANGE),
]
box_w, box_h = 1.7, 1.1

for label, cx, cy, color in stages:
    rect = FancyBboxPatch((cx - box_w/2, cy - box_h/2), box_w, box_h,
                          boxstyle="round,pad=0.08", linewidth=1.5,
                          edgecolor=color, facecolor=color + "22")
    ax_a.add_patch(rect)
    ax_a.text(cx, cy, label, ha="center", va="center",
              fontsize=8.5, fontweight="bold", color=color)

# arrows between stages
for x_start, x_end in [(1.85, 3.15), (4.85, 6.15)]:
    ax_a.annotate("", xy=(x_end, 3.0), xytext=(x_start, 3.0),
                  arrowprops=dict(arrowstyle="-|>", color=GRAY,
                                 lw=1.4, mutation_scale=14))

# input / output nodes
for label, cx, cy, color in [("Input\nData", 0.5, 3.0, GRAY),
                               ("Output", 9.5, 3.0, "#059669")]:
    ax_a.text(cx, cy, label, ha="center", va="center",
              fontsize=8, color=color, fontweight="bold",
              bbox=dict(boxstyle="round,pad=0.25", fc="white",
                        ec=color, lw=1.2))

ax_a.annotate("", xy=(0.85, 3.0), xytext=(0.15, 3.0),
              arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2, mutation_scale=12))
ax_a.annotate("", xy=(9.15, 3.0), xytext=(8.85, 3.0),
              arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2, mutation_scale=12))

# memory / attention / skill annotations
annots = [
    (2.5, 4.5, "Attention\nModule", ACCENT),
    (5.0, 4.5, "Memory\nBank", "#7C3AED"),
    (7.5, 4.5, "Skill\nRouter", ORANGE),
]
for ax_x, ax_y, txt, col in annots:
    ax_a.text(ax_x, ax_y, txt, ha="center", va="bottom",
              fontsize=7.5, color=col, style="italic")
    ax_a.plot([ax_x, ax_x], [ax_y - 0.05, ax_y - 0.65],
              color=col, lw=0.9, ls="--", alpha=0.7)

ax_a.set_title("Method Overview", fontsize=9, color=GRAY, pad=4)
ax_a.text(0.01, 0.99, "A", transform=ax_a.transAxes, **LABEL_KW)

# ── Panel B: ablation bars ─────────────────────────────────────────────────
items  = pb["items"]
values = pb["values"]
colors = [ACCENT if v == max(values) else "#93C5FD" for v in values]
bars = ax_b.barh(items, values, color=colors, edgecolor="white", height=0.6)
ax_b.set_xlim(50, 68)
ax_b.set_xlabel("Accuracy (%)", fontsize=8)
ax_b.tick_params(axis="both", labelsize=8)
ax_b.spines[["top", "right"]].set_visible(False)
for bar, val in zip(bars, values):
    ax_b.text(val + 0.2, bar.get_y() + bar.get_height()/2,
              f"{val:.1f}", va="center", fontsize=7.5, color="#1E3A5F")
ax_b.set_title("Ablation Study", fontsize=9, color=GRAY, pad=4)
ax_b.text(0.01, 0.99, "B", transform=ax_b.transAxes, **LABEL_KW)

# ── Panel C: training curves ───────────────────────────────────────────────
steps    = pc["steps"]
baseline = pc["Baseline"]
ours     = pc["Ours"]
ax_c.plot(steps, baseline, color=GRAY,   lw=1.5, label="Baseline", ls="--")
ax_c.plot(steps, ours,     color=ACCENT, lw=1.8, label="Ours")
ax_c.set_xlabel("Training Step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.tick_params(axis="both", labelsize=8)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.legend(fontsize=7.5, frameon=False)
ax_c.set_title("Training Trend", fontsize=9, color=GRAY, pad=4)
ax_c.text(0.01, 0.99, "C", transform=ax_c.transAxes, **LABEL_KW)

# ── Panel D: 5×5 sensitivity heatmap ──────────────────────────────────────
matrix = np.array(pd["matrix"])
im = ax_d.imshow(matrix, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
ax_d.set_xticks(range(5))
ax_d.set_xticklabels(pd["x"], fontsize=9)
ax_d.set_yticks(range(5))
ax_d.set_yticklabels(pd["y"], fontsize=9)
ax_d.set_xlabel("Hyperparameter S", fontsize=9)
ax_d.set_ylabel("Hyperparameter P", fontsize=9)
for i in range(5):
    for j in range(5):
        val = matrix[i, j]
        txt_col = "white" if val < 0.25 or val > 0.75 else "black"
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8, color=txt_col, fontweight="bold")
cbar = fig.colorbar(im, ax=ax_d, fraction=0.025, pad=0.02)
cbar.set_label("Score", fontsize=8)
cbar.ax.tick_params(labelsize=8)
ax_d.set_title("Sensitivity Sweep (S × P)", fontsize=9, color=GRAY, pad=4)
ax_d.text(0.005, 0.97, "D", transform=ax_d.transAxes, **LABEL_KW)

# ── save ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
