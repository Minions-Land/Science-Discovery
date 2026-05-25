"""
Sankey diagram of dataset preparation flow using matplotlib Bezier paths.
"""

import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np

# ── load data ──────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# ── layout: assign x-columns manually ─────────────────────────────────────────
# Column 0: Raw
# Column 1: Cleaned, Reject (partial)
# Column 2: Filtered, Reject (partial)
# Column 3: Train, Val, Test, Reject (partial)
col_x = {
    "Raw":      0.05,
    "Cleaned":  0.28,
    "Filtered": 0.51,
    "Train":    0.74,
    "Val":      0.74,
    "Test":     0.74,
    "Reject":   0.74,
}

# ── compute node total flows ───────────────────────────────────────────────────
node_out = {n: 0 for n in nodes}
node_in  = {n: 0 for n in nodes}
for lk in links:
    node_out[lk["source"]] += lk["value"]
    node_in[lk["target"]]  += lk["value"]

node_height = {}
for n in nodes:
    node_height[n] = max(node_in[n], node_out[n])

# ── vertical stacking per column ───────────────────────────────────────────────
# Map node -> y_bottom (center of the node band)
total_height = 1000
gap = 22  # gap between nodes in same column

col_nodes = {}
for n in nodes:
    col_nodes.setdefault(col_x[n], []).append(n)

node_y_bottom = {}
for col, col_ns in col_nodes.items():
    heights = [node_height[n] for n in col_ns]
    total_col = sum(heights) + gap * (len(col_ns) - 1)
    y_start = (total_height - total_col) / 2
    y = y_start
    for n in col_ns:
        node_y_bottom[n] = y
        y += node_height[n] + gap

# ── track how much of each node's top/bottom has been consumed by links ────────
node_out_cursor = {n: node_y_bottom[n] for n in nodes}
node_in_cursor  = {n: node_y_bottom[n] for n in nodes}

# ── colors ─────────────────────────────────────────────────────────────────────
source_colors = {
    "Raw":      "#4C72B0",
    "Cleaned":  "#55A868",
    "Filtered": "#C44E52",
}
node_color = {
    "Raw":      "#4C72B0",
    "Cleaned":  "#55A868",
    "Filtered": "#C44E52",
    "Train":    "#8172B2",
    "Val":      "#937860",
    "Test":     "#DA8BC3",
    "Reject":   "#BBBBBB",
}
link_source_color = {}
for lk in links:
    link_source_color[(lk["source"], lk["target"])] = source_colors.get(lk["source"], "#AAAAAA")

# ── figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.set_xlim(0, 1)
ax.set_ylim(0, total_height)
ax.axis("off")

NODE_W = 0.022  # node rectangle width in data coords (x)

def draw_flow(ax, x0, y0_src, x1, y1_dst, w, color, alpha=0.45):
    """Draw a Bezier ribbon between two nodes."""
    # control points: horizontal bezier
    cx = (x0 + x1) / 2
    verts = [
        (x0,        y0_src),
        (cx,        y0_src),
        (cx,        y1_dst),
        (x1,        y1_dst),
        (x1,        y1_dst + w),
        (cx,        y1_dst + w),
        (cx,        y0_src + w),
        (x0,        y0_src + w),
        (x0,        y0_src),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_patch(patch)

# ── draw links ─────────────────────────────────────────────────────────────────
for lk in links:
    src, tgt, val = lk["source"], lk["target"], lk["value"]
    color = source_colors.get(src, "#AAAAAA")

    x_src_right = col_x[src] + NODE_W
    x_tgt_left  = col_x[tgt]

    y_src = node_out_cursor[src]
    y_tgt = node_in_cursor[tgt]

    draw_flow(ax, x_src_right, y_src, x_tgt_left, y_tgt, val, color)

    node_out_cursor[src] += val
    node_in_cursor[tgt]  += val

# ── draw nodes ─────────────────────────────────────────────────────────────────
for n in nodes:
    x = col_x[n]
    yb = node_y_bottom[n]
    h = node_height[n]
    rect = patches.FancyBboxPatch(
        (x, yb), NODE_W, h,
        boxstyle="square,pad=0",
        facecolor=node_color[n], edgecolor="white", linewidth=0.8
    )
    ax.add_patch(rect)

# ── labels ─────────────────────────────────────────────────────────────────────
label_offset_x = 0.005
for n in nodes:
    x = col_x[n]
    yb = node_y_bottom[n]
    h = node_height[n]
    yc = yb + h / 2
    val = node_height[n]
    label = f"{n}\n({val:,})"
    # place label to right of right-column nodes, left of others
    if col_x[n] >= 0.7:
        ax.text(x + NODE_W + label_offset_x, yc, label,
                va="center", ha="left", fontsize=8, color="#222222",
                fontfamily="DejaVu Sans")
    else:
        ax.text(x + NODE_W / 2, yc, label,
                va="center", ha="center", fontsize=7.5, color="white",
                fontweight="bold", fontfamily="DejaVu Sans")

# ── title ──────────────────────────────────────────────────────────────────────
ax.set_title("Dataset Preparation Flow", fontsize=12, fontweight="bold", pad=8,
             color="#111111")

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
