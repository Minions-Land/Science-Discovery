"""
Sankey diagram of dataset preparation flow.
Uses matplotlib with manual Bezier-path ribbons for a clean look.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe

# ── Load data ────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

nodes_list = data["nodes"]
links = data["links"]

# ── Layout: assign each node to a column (stage) ────────────────────────────
stage = {
    "Raw":      0,
    "Cleaned":  1,
    "Filtered": 2,
    "Train":    3,
    "Val":      3,
    "Test":     3,
    "Reject":   3,
}

# Node totals (sum of outflow or inflow, whichever is larger)
node_out = {n: 0 for n in nodes_list}
node_in  = {n: 0 for n in nodes_list}
for lk in links:
    node_out[lk["source"]] += lk["value"]
    node_in[lk["target"]]  += lk["value"]

node_total = {n: max(node_out[n], node_in[n]) for n in nodes_list}

# ── Color palette ────────────────────────────────────────────────────────────
source_color = {
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

# ── Vertical positioning ─────────────────────────────────────────────────────
GAP   = 0.05   # gap between nodes in the same column (fraction of total height)
TOTAL = 1.0    # canvas height

def layout_column(nodes_in_col, gap=GAP):
    """Return {node: (y_bottom, height)} for nodes stacked in a column."""
    totals = [node_total[n] for n in nodes_in_col]
    scale  = (TOTAL - gap * (len(nodes_in_col) - 1)) / sum(totals)
    result = {}
    y = 0.0
    for n, t in zip(nodes_in_col, totals):
        h = t * scale
        result[n] = (y, h)
        y += h + gap
    return result

# Define column contents (order determines stacking bottom→top)
columns = {
    0: ["Raw"],
    1: ["Cleaned"],
    2: ["Filtered"],
    3: ["Train", "Val", "Test", "Reject"],
}

col_layout = {}
for col, nodes_in_col in columns.items():
    col_layout[col] = layout_column(nodes_in_col)

# Merge into flat node→(y_bot, height) dict
node_pos = {}
for col, layout in col_layout.items():
    node_pos.update(layout)

# X positions for each column
x_cols = {0: 0.05, 1: 0.30, 2: 0.55, 3: 0.80}
NODE_WIDTH = 0.06

# ── Drawing ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(0, 1)
ax.set_ylim(-0.02, 1.05)
ax.axis("off")

# Track "current fill level" for each node's left and right edge
node_right_fill = {n: node_pos[n][0] for n in nodes_list}  # outflow cursor
node_left_fill  = {n: node_pos[n][0] for n in nodes_list}  # inflow cursor

# Compute global scale: largest node total → height in data coords
max_total = max(node_total.values())
def val_to_h(val, node):
    y_bot, h = node_pos[node]
    return h * val / node_total[node]

def draw_ribbon(ax, x_src, y_src_bot, y_src_top,
                x_tgt, y_tgt_bot, y_tgt_top, color, alpha=0.45):
    """Draw a Bezier ribbon between two vertical extents."""
    cp_x = (x_src + x_tgt) / 2
    verts = [
        (x_src, y_src_bot),
        (cp_x,  y_src_bot),
        (cp_x,  y_tgt_bot),
        (x_tgt, y_tgt_bot),
        (x_tgt, y_tgt_top),
        (cp_x,  y_tgt_top),
        (cp_x,  y_src_top),
        (x_src, y_src_top),
        (x_src, y_src_bot),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    path  = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=alpha, zorder=1)
    ax.add_patch(patch)

# Draw ribbons
for lk in links:
    src, tgt, val = lk["source"], lk["target"], lk["value"]
    col_src = stage[src]
    col_tgt = stage[tgt]

    x_src_right = x_cols[col_src] + NODE_WIDTH
    x_tgt_left  = x_cols[col_tgt]

    # Outflow slice on source
    h_src = val_to_h(val, src)
    y_src_bot = node_right_fill[src]
    y_src_top = y_src_bot + h_src
    node_right_fill[src] = y_src_top

    # Inflow slice on target
    h_tgt = val_to_h(val, tgt)
    y_tgt_bot = node_left_fill[tgt]
    y_tgt_top = y_tgt_bot + h_tgt
    node_left_fill[tgt] = y_tgt_top

    color = source_color.get(src, "#999999")
    draw_ribbon(ax, x_src_right, y_src_bot, y_src_top,
                    x_tgt_left,  y_tgt_bot, y_tgt_top, color)

# Draw node rectangles
for node in nodes_list:
    col  = stage[node]
    x    = x_cols[col]
    y_b, h = node_pos[node]
    rect = mpatches.FancyBboxPatch(
        (x, y_b), NODE_WIDTH, h,
        boxstyle="square,pad=0",
        facecolor=node_color[node], edgecolor="white", linewidth=0.8,
        zorder=2
    )
    ax.add_patch(rect)
    # Label
    label_x = x + NODE_WIDTH / 2
    label_y = y_b + h / 2
    val_str = f"\n{node_total[node]:,}"
    ax.text(label_x, label_y, f"{node}{val_str}",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color="white", zorder=3,
            path_effects=[pe.withStroke(linewidth=1.5, foreground="black")])

# Column headers
headers = {0: "Raw\nCorpus", 1: "Cleaned", 2: "Filtered", 3: "Splits"}
for col, label in headers.items():
    ax.text(x_cols[col] + NODE_WIDTH / 2, 1.02, label,
            ha="center", va="bottom", fontsize=9, color="#444444", style="italic")

fig.suptitle("Dataset Preparation Flow", fontsize=12, fontweight="bold", y=1.00)
plt.tight_layout(rect=[0, 0, 1, 0.97])

# ── Save ─────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
