"""
RetroDiff architecture diagram.
Source data: data.json
Outputs: figure.pdf, figure.png, figure.svg
"""
import json
import matplotlib as mpl
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
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

with open("data.json") as f:
    data = json.load(f)

PALETTE = {
    "input":      "#0F4D92",
    "output":     "#009E73",
    "module":     "#E69F00",
    "datastore":  "#56B4E9",
    "group_ret":  "#EAF3FB",
    "group_gen":  "#FEF9E7",
    "border_ret": "#0F4D92",
    "border_gen": "#D55E00",
    "arrow":      "#272727",
    "arrow_ctrl": "#767676",
    "text":       "#272727",
}

fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5)
ax.axis("off")

# ── Group backgrounds ────────────────────────────────────────────────────────
ret_rect = FancyBboxPatch(
    (2.55, 0.65), 3.1, 3.5,
    boxstyle="round,pad=0.12",
    facecolor=PALETTE["group_ret"], edgecolor=PALETTE["border_ret"],
    linewidth=1.5, linestyle="--", zorder=1,
)
ax.add_patch(ret_rect)
ax.text(4.1, 4.05, "Retrieval", ha="center", va="bottom",
        fontsize=9, fontweight="bold", color=PALETTE["border_ret"], zorder=2)

gen_rect = FancyBboxPatch(
    (6.05, 0.65), 3.3, 3.5,
    boxstyle="round,pad=0.12",
    facecolor=PALETTE["group_gen"], edgecolor=PALETTE["border_gen"],
    linewidth=1.5, linestyle="--", zorder=1,
)
ax.add_patch(gen_rect)
ax.text(7.7, 4.05, "Generation", ha="center", va="bottom",
        fontsize=9, fontweight="bold", color=PALETTE["border_gen"], zorder=2)

# ── Node geometry ─────────────────────────────────────────────────────────────
# (cx, cy, w, h)
POS = {
    "input":    (0.95, 2.9,  1.4,  0.65),
    "retrieve": (4.1,  3.1,  1.8,  0.65),
    "db":       (4.1,  1.5,  1.8,  0.65),
    "diff":     (7.7,  3.1,  2.1,  0.65),
    "prior":    (7.7,  1.5,  2.1,  0.65),
    "output":   (10.2, 3.1,  1.4,  0.65),
}

stage_map = {s["id"]: s for s in data["stages"]}

def draw_node(ax, sid):
    cx, cy, w, h = POS[sid]
    s = stage_map[sid]
    color = PALETTE[s["kind"]]
    if s["kind"] == "datastore":
        # Cylinder-style: rounded rect with top ellipse hint
        body = FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle="round,pad=0.06",
            facecolor=color, edgecolor=PALETTE["arrow"],
            linewidth=1.2, zorder=3,
        )
        ax.add_patch(body)
        # top ellipse cap
        ell = mpatches.Ellipse(
            (cx, cy + h/2 - 0.04), w * 0.92, 0.22,
            facecolor=mpl.colors.to_rgba(color, 0.85),
            edgecolor=PALETTE["arrow"], linewidth=1.2, zorder=4,
        )
        ax.add_patch(ell)
    else:
        patch = FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle="round,pad=0.06",
            facecolor=color, edgecolor=PALETTE["arrow"],
            linewidth=1.2, zorder=3,
        )
        ax.add_patch(patch)
    ax.text(cx, cy, s["label"], ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white", zorder=5)

for sid in POS:
    draw_node(ax, sid)

# ── Arrow helpers ─────────────────────────────────────────────────────────────
def solid_arrow(ax, x1, y1, x2, y2, rad=0.0):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>", color=PALETTE["arrow"], lw=1.4,
            mutation_scale=12,
            connectionstyle=f"arc3,rad={rad}",
        ),
        zorder=6,
    )

def dashed_arrow(ax, x1, y1, x2, y2, rad=0.0):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>", color=PALETTE["arrow_ctrl"], lw=1.2,
            mutation_scale=10, linestyle="dashed",
            connectionstyle=f"arc3,rad={rad}",
        ),
        zorder=6,
    )

# ── Arrows ────────────────────────────────────────────────────────────────────
# Query → Retriever  (solid, data flow)
solid_arrow(ax, 1.65, 2.9, 3.2, 3.1)

# Retriever → KB  (dashed, query)
dashed_arrow(ax, 4.0, 2.775, 4.0, 1.825)

# KB → Retriever  (solid, data return)
solid_arrow(ax, 4.2, 1.825, 4.2, 2.775)

# Retriever → Diffusion Decoder  (solid, data flow)
solid_arrow(ax, 5.0, 3.1, 6.65, 3.1)

# Diffusion Decoder → Prior Network  (dashed, control)
dashed_arrow(ax, 7.6, 2.775, 7.6, 1.825)

# Prior Network → Diffusion Decoder  (dashed, feedback, curved)
dashed_arrow(ax, 6.65, 1.7, 6.65, 2.9, rad=-0.35)

# Diffusion Decoder → Generated Sample  (solid, data flow)
solid_arrow(ax, 8.75, 3.1, 9.5, 3.1)

# ── Legend ────────────────────────────────────────────────────────────────────
lx, ly = 0.15, 0.55
solid_arrow(ax, lx, ly, lx + 0.55, ly)
ax.text(lx + 0.65, ly, "data flow", va="center", fontsize=7.5, color=PALETTE["arrow"])

dashed_arrow(ax, lx, ly - 0.32, lx + 0.55, ly - 0.32)
ax.text(lx + 0.65, ly - 0.32, "control / feedback", va="center",
        fontsize=7.5, color=PALETTE["arrow_ctrl"])

# ── Title ─────────────────────────────────────────────────────────────────────
ax.set_title("RetroDiff — System Architecture", fontsize=11, fontweight="bold",
             pad=6, color=PALETTE["text"])

plt.tight_layout(pad=0.4)
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
