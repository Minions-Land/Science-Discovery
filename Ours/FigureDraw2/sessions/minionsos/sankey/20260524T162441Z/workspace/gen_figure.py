import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

with open("data.json") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# Layout: assign nodes to columns (stages)
col_map = {
    "Raw": 0,
    "Cleaned": 1,
    "Filtered": 2,
    "Train": 3,
    "Val": 3,
    "Test": 3,
    "Reject": 3,
}

# Color palette: source-node colors
node_colors = {
    "Raw":     "#4C72B0",
    "Cleaned": "#55A868",
    "Filtered":"#C44E52",
    "Train":   "#8172B2",
    "Val":     "#937860",
    "Test":    "#DA8BC3",
    "Reject":  "#AAAAAA",
}

# Compute vertical positions per column
# Each node's height proportional to its total outflow (or inflow for terminals)
def total_flow(node):
    out = sum(l["value"] for l in links if l["source"] == node)
    if out == 0:
        out = sum(l["value"] for l in links if l["target"] == node)
    return out

col_nodes = {}
for n in nodes:
    c = col_map[n]
    col_nodes.setdefault(c, []).append(n)

# Fixed ordering within each column
col_order = {
    0: ["Raw"],
    1: ["Cleaned"],
    2: ["Filtered"],
    3: ["Train", "Val", "Test", "Reject"],
}

GAP = 20          # gap between nodes in same column (in value units)
COL_X = {0: 0.0, 1: 0.3, 2: 0.6, 3: 1.0}
SCALE = 1/1000    # map value -> y-height

# Compute node y-extents (bottom, top) in data coordinates
node_extents = {}
for col, nlist in col_order.items():
    heights = [total_flow(n) * SCALE for n in nlist]
    total_h = sum(heights) + GAP * SCALE * (len(nlist) - 1)
    y = (1.0 - total_h) / 2  # center vertically
    for n, h in zip(nlist, heights):
        node_extents[n] = (y, y + h)
        y += h + GAP * SCALE

# For each node, track how much of its outflow/inflow has been drawn (for stacking flows)
out_cursor = {n: node_extents[n][0] for n in nodes}
in_cursor  = {n: node_extents[n][0] for n in nodes}

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-0.05, 1.10)
ax.set_ylim(-0.05, 1.10)
ax.axis("off")

NODE_W = 0.025

# Draw flows first (behind nodes)
for link in links:
    src = link["source"]
    tgt = link["target"]
    val = link["value"]
    h = val * SCALE

    sx = COL_X[col_map[src]] + NODE_W
    tx = COL_X[col_map[tgt]]

    sy0 = out_cursor[src]
    sy1 = sy0 + h
    out_cursor[src] += h

    ty0 = in_cursor[tgt]
    ty1 = ty0 + h
    in_cursor[tgt] += h

    color = node_colors[src]

    # Cubic bezier path for the flow band
    verts = []
    npts = 50
    for i in range(npts + 1):
        t = i / npts
        # Lerp with cubic ease
        cx1 = sx + (tx - sx) * 0.45
        cx2 = sx + (tx - sx) * 0.55
        # Top edge
        y_top = (1-t)**3 * sy1 + 3*(1-t)**2*t * sy1 + 3*(1-t)*t**2 * ty1 + t**3 * ty1
        # simple linear interpolation with smooth curve for x
        bx = (1-t)**3*sx + 3*(1-t)**2*t*cx1 + 3*(1-t)*t**2*cx2 + t**3*tx
        verts.append((bx, y_top))

    for i in range(npts, -1, -1):
        t = i / npts
        cx1 = sx + (tx - sx) * 0.45
        cx2 = sx + (tx - sx) * 0.55
        y_bot = (1-t)**3 * sy0 + 3*(1-t)**2*t * sy0 + 3*(1-t)*t**2 * ty0 + t**3 * ty0
        bx = (1-t)**3*sx + 3*(1-t)**2*t*cx1 + 3*(1-t)*t**2*cx2 + t**3*tx
        verts.append((bx, y_bot))

    from matplotlib.patches import Polygon
    poly = Polygon(verts, closed=True, facecolor=color, alpha=0.45, edgecolor="none", zorder=1)
    ax.add_patch(poly)

# Draw node rectangles
for n in nodes:
    y0, y1 = node_extents[n]
    x0 = COL_X[col_map[n]]
    rect = mpatches.FancyBboxPatch(
        (x0, y0), NODE_W, y1 - y0,
        boxstyle="square,pad=0",
        facecolor=node_colors[n], edgecolor="white", linewidth=0.8, zorder=2
    )
    ax.add_patch(rect)
    # Label
    mid_y = (y0 + y1) / 2
    val = total_flow(n)
    label = f"{n}\n{val:,}"
    ha = "right" if col_map[n] < 3 else "left"
    xoff = x0 - 0.012 if ha == "right" else x0 + NODE_W + 0.012
    ax.text(xoff, mid_y, label, ha=ha, va="center", fontsize=9,
            fontweight="bold", color=node_colors[n], zorder=3)

# Column header labels
for col, label in {0: "Raw Input", 1: "Cleaned", 2: "Filtered", 3: "Split"}.items():
    ax.text(COL_X[col] + NODE_W/2, 1.02, label, ha="center", va="bottom",
            fontsize=8, color="#555555", style="italic")

ax.set_title("Dataset Preparation Flow", fontsize=13, fontweight="bold", pad=12)

plt.tight_layout()
plt.savefig("figure.pdf", dpi=150, bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
