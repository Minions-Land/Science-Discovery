"""
Sankey diagram of dataset preparation flow.
Uses matplotlib patches (rectangles + cubic Bezier paths) for a clean look.
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patches as patches

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

nodes_list = data["nodes"]
links = data["links"]

# ── layout: assign columns (x) and compute y stacking per column ───────────
# Determine column order by BFS / topological
from collections import defaultdict, deque

out_edges = defaultdict(list)
in_edges  = defaultdict(list)
for lk in links:
    out_edges[lk["source"]].append(lk)
    in_edges[lk["target"]].append(lk)

# Topological sort to assign columns
def topo_columns(nodes, out_edges):
    indegree = {n: 0 for n in nodes}
    for n in nodes:
        for lk in out_edges[n]:
            indegree[lk["target"]] += 1
    col = {n: 0 for n in nodes}   # initialise all nodes at column 0
    queue = deque([n for n in nodes if indegree[n] == 0])
    while queue:
        n = queue.popleft()
        c = col[n]
        for lk in out_edges[n]:
            t = lk["target"]
            col[t] = max(col[t], c + 1)
            indegree[t] -= 1
            if indegree[t] == 0:
                queue.append(t)
    return col

col_of = topo_columns(nodes_list, out_edges)
# group nodes per column
from itertools import groupby
cols = defaultdict(list)
for n in nodes_list:
    cols[col_of.get(n, 0)].append(n)

# total flow through each node
node_value = {}
for n in nodes_list:
    ins  = sum(lk["value"] for lk in in_edges[n])
    outs = sum(lk["value"] for lk in out_edges[n])
    node_value[n] = max(ins, outs)
# source nodes have no in-edges; use out sum
for n in nodes_list:
    if not in_edges[n]:
        node_value[n] = sum(lk["value"] for lk in out_edges[n])

# ── figure geometry ────────────────────────────────────────────────────────
FIG_W, FIG_H = 10, 6
NODE_W = 0.35          # node rectangle width (in data coords)
GAP    = 0.12          # gap between stacked nodes
TOTAL  = sum(node_value[n] for n in cols[0])   # scale reference

num_cols = max(col_of.values()) + 1
x_positions = {c: 1.0 + c * (FIG_W - 2.0) / (num_cols - 1) for c in range(num_cols)}

# Assign y positions within each column (bottom-up, centred)
node_y = {}   # bottom-left y of each node rectangle
node_h = {}   # height of each node rectangle

SCALE = (FIG_H - 1.0)  # total usable height in data coords

for c, group in cols.items():
    total_h = sum(node_value[n] / TOTAL * SCALE for n in group)
    total_gap = GAP * (len(group) - 1)
    block_h = total_h + total_gap
    y_start = (FIG_H - block_h) / 2
    y = y_start
    for n in group:
        h = node_value[n] / TOTAL * SCALE
        node_y[n] = y
        node_h[n] = h
        y += h + GAP

# ── colors ─────────────────────────────────────────────────────────────────
SOURCE_COLORS = {
    "Raw":     "#4C72B0",
    "Cleaned": "#55A868",
    "Filtered":"#C44E52",
}
NODE_COLORS = {
    "Raw":     "#4C72B0",
    "Cleaned": "#55A868",
    "Filtered":"#C44E52",
    "Train":   "#8172B2",
    "Val":     "#CCB974",
    "Test":    "#64B5CD",
    "Reject":  "#AAAAAA",
}

# ── draw ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")

# Track current "cursor" positions (where next flow exits / enters)
out_cursor = {n: node_y[n] for n in nodes_list}   # flows leave from bottom up
in_cursor  = {n: node_y[n] for n in nodes_list}

def cubic_bezier_patch(x0, y0, h0, x1, y1, h1, color, alpha=0.45):
    """Draw a filled cubic Bezier ribbon between two vertical bars."""
    cx = (x0 + x1) / 2
    verts = [
        (x0, y0),
        (cx, y0),
        (cx, y1),
        (x1, y1),
        (x1, y1 + h1),
        (cx, y1 + h1),
        (cx, y0 + h0),
        (x0, y0 + h0),
        (x0, y0),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=color, edgecolor="none", alpha=alpha, zorder=1)
    ax.add_patch(patch)

# Draw flows
for lk in links:
    s, t, v = lk["source"], lk["target"], lk["value"]
    h = v / TOTAL * SCALE
    x_s = x_positions[col_of[s]] + NODE_W
    x_t = x_positions[col_of[t]]
    y_s = out_cursor[s]
    y_t = in_cursor[t]
    color = SOURCE_COLORS.get(s, "#888888")
    cubic_bezier_patch(x_s, y_s, h, x_t, y_t, h, color)
    out_cursor[s] += h
    in_cursor[t]  += h

# Draw node rectangles
for n in nodes_list:
    x = x_positions[col_of[n]]
    y = node_y[n]
    h = node_h[n]
    rect = mpatches.FancyBboxPatch(
        (x, y), NODE_W, h,
        boxstyle="square,pad=0",
        facecolor=NODE_COLORS.get(n, "#999999"),
        edgecolor="white", linewidth=1.2, zorder=2
    )
    ax.add_patch(rect)
    # label
    ax.text(
        x + NODE_W / 2, y + h / 2,
        f"{n}\n{node_value[n]:,}",
        ha="center", va="center",
        fontsize=8.5, fontweight="bold",
        color="white", zorder=3
    )

# Title
ax.set_title("Dataset Preparation Flow", fontsize=13, fontweight="bold", pad=8)

plt.tight_layout(pad=0.4)
fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
