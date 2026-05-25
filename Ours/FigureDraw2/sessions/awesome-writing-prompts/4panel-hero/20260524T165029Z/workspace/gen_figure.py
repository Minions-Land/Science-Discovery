import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.patheffects import withStroke

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

b_items  = d["panel_b"]["items"]
b_vals   = d["panel_b"]["values"]
c_steps  = d["panel_c"]["steps"]
c_base   = d["panel_c"]["Baseline"]
c_ours   = d["panel_c"]["Ours"]
hx       = d["panel_d"]["x"]
hy       = d["panel_d"]["y"]
hmat     = np.array(d["panel_d"]["matrix"])

# ── figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 7))
gs_outer = gridspec.GridSpec(
    2, 1, figure=fig,
    height_ratios=[1, 1],
    hspace=0.45
)
gs_top = gridspec.GridSpecFromSubplotSpec(
    1, 3, subplot_spec=gs_outer[0],
    width_ratios=[2, 1, 1],
    wspace=0.35
)
ax_a = fig.add_subplot(gs_top[0])
ax_b = fig.add_subplot(gs_top[1])
ax_c = fig.add_subplot(gs_top[2])
ax_d = fig.add_subplot(gs_outer[1])

LABEL_KW = dict(fontsize=14, fontweight="bold", fontfamily="sans-serif",
                va="top", ha="left")

BLUE  = "#2563EB"
GREEN = "#16A34A"
AMBER = "#D97706"
GRAY  = "#6B7280"
LIGHT = "#EFF6FF"

# ── Panel A: method overview ───────────────────────────────────────────────────
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)
ax_a.axis("off")

# title
ax_a.text(0.5, 0.97, "Method Overview", ha="center", va="top",
          fontsize=10, fontweight="bold", color="#1E293B",
          transform=ax_a.transAxes)

stages = [
    ("Input\nTokens",   0.12, "#DBEAFE", BLUE),
    ("Attention\n+ Memory", 0.42, "#D1FAE5", GREEN),
    ("Skill\nRouter",   0.72, "#FEF3C7", AMBER),
]
box_w, box_h = 0.18, 0.28
y_center = 0.54

for label, xc, fc, ec in stages:
    box = FancyBboxPatch(
        (xc - box_w / 2, y_center - box_h / 2), box_w, box_h,
        boxstyle="round,pad=0.02", linewidth=1.5,
        edgecolor=ec, facecolor=fc,
        transform=ax_a.transAxes, zorder=3
    )
    ax_a.add_patch(box)
    ax_a.text(xc, y_center, label, ha="center", va="center",
              fontsize=8, fontweight="semibold", color="#1E293B",
              transform=ax_a.transAxes, zorder=4, linespacing=1.3)

# arrows between boxes
for x0, x1 in [(0.21, 0.33), (0.51, 0.63)]:
    ax_a.annotate("", xy=(x1, y_center), xytext=(x0, y_center),
                  xycoords="axes fraction", textcoords="axes fraction",
                  arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.5))

# output box
out_x = 0.88
out_box = FancyBboxPatch(
    (out_x - 0.09, y_center - 0.14), 0.18, 0.28,
    boxstyle="round,pad=0.02", linewidth=1.5,
    edgecolor="#7C3AED", facecolor="#EDE9FE",
    transform=ax_a.transAxes, zorder=3
)
ax_a.add_patch(out_box)
ax_a.text(out_x, y_center, "Output\nPrediction", ha="center", va="center",
          fontsize=8, fontweight="semibold", color="#1E293B",
          transform=ax_a.transAxes, zorder=4, linespacing=1.3)
ax_a.annotate("", xy=(0.79, y_center), xytext=(0.81, y_center),
              xycoords="axes fraction", textcoords="axes fraction",
              arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.5))

# residual skip connection (arc)
ax_a.annotate("",
    xy=(0.72, y_center - box_h / 2 - 0.02),
    xytext=(0.12, y_center - box_h / 2 - 0.02),
    xycoords="axes fraction", textcoords="axes fraction",
    arrowprops=dict(
        arrowstyle="-|>", color="#94A3B8", lw=1.2,
        connectionstyle="arc3,rad=-0.35"
    )
)
ax_a.text(0.42, 0.17, "residual skip", ha="center", va="top",
          fontsize=6.5, color="#94A3B8", transform=ax_a.transAxes, style="italic")

ax_a.text(0.01, 0.99, "A", **LABEL_KW, transform=ax_a.transAxes)

# ── Panel B: ablation bars ─────────────────────────────────────────────────────
full_idx = b_items.index("full")
colors_b = [GREEN if i == full_idx else "#93C5FD" for i in range(len(b_items))]
bars = ax_b.barh(b_items, b_vals, color=colors_b, edgecolor="white", linewidth=0.8, height=0.6)
ax_b.set_xlim(50, 68)
ax_b.axvline(b_vals[full_idx], color=GREEN, lw=1.2, ls="--", alpha=0.6)
for bar, val in zip(bars, b_vals):
    ax_b.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
              f"{val:.1f}", va="center", fontsize=7.5, color="#1E293B")
ax_b.set_xlabel("Accuracy (%)", fontsize=8)
ax_b.set_title("Ablation Study", fontsize=9, fontweight="bold", pad=4)
ax_b.tick_params(labelsize=7.5)
ax_b.spines[["top", "right"]].set_visible(False)
ax_b.text(-0.18, 1.04, "B", transform=ax_b.transAxes,
          fontsize=14, fontweight="bold", fontfamily="sans-serif", va="top")

# ── Panel C: training curves ───────────────────────────────────────────────────
ax_c.plot(c_steps, c_base, color=GRAY,  lw=1.5, label="Baseline", ls="--")
ax_c.plot(c_steps, c_ours, color=BLUE,  lw=2.0, label="Ours")
ax_c.set_xlabel("Training Step (×10³)", fontsize=8)
ax_c.set_ylabel("Loss", fontsize=8)
ax_c.set_title("Training Trend", fontsize=9, fontweight="bold", pad=4)
ax_c.legend(fontsize=7, framealpha=0.7, loc="upper right")
ax_c.tick_params(labelsize=7.5)
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.text(-0.22, 1.04, "C", transform=ax_c.transAxes,
          fontsize=14, fontweight="bold", fontfamily="sans-serif", va="top")

# ── Panel D: sensitivity heatmap ───────────────────────────────────────────────
im = ax_d.imshow(hmat, aspect="auto", cmap="viridis", vmin=0, vmax=1,
                 interpolation="nearest")
ax_d.set_xticks(range(len(hx)))
ax_d.set_xticklabels(hx, fontsize=9)
ax_d.set_yticks(range(len(hy)))
ax_d.set_yticklabels(hy, fontsize=9)
ax_d.set_xlabel("Hyperparameter S", fontsize=9)
ax_d.set_ylabel("Hyperparameter P", fontsize=9)
ax_d.set_title("Sensitivity Sweep (5 × 5 Grid)", fontsize=10, fontweight="bold", pad=5)

for i in range(hmat.shape[0]):
    for j in range(hmat.shape[1]):
        val = hmat[i, j]
        col = "white" if val < 0.5 else "black"
        ax_d.text(j, i, f"{val:.2f}", ha="center", va="center",
                  fontsize=8.5, color=col, fontweight="bold")

cbar = fig.colorbar(im, ax=ax_d, fraction=0.025, pad=0.02)
cbar.set_label("Score", fontsize=8)
cbar.ax.tick_params(labelsize=7.5)

ax_d.text(-0.055, 1.06, "D", transform=ax_d.transAxes,
          fontsize=14, fontweight="bold", fontfamily="sans-serif", va="top")

# ── save ───────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
