"""
Sankey diagram of dataset preparation flow.
Data: data.json with nodes and links.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ── Load data ────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

# ── Layout: assign each node an x-column ────────────────────────────────────
col = {
    "Raw":      0,
    "Cleaned":  1,
    "Filtered": 2,
    "Train":    3,
    "Val":      3,
    "Test":     3,
    "Reject":   3,
}

# Node heights proportional to their total flow (max in/out)
def node_flow(n):
    out = sum(l["value"] for l in links if l["source"] == n)
    inp = sum(l["value"] for l in links if l["target"] == n)
    return max(out, inp)

flows = {n: node_flow(n) for n in nodes}

# Vertical positions within each column
# Col 0: Raw; col 1: Cleaned; col 2: Filtered; col 3: Train/Val/Test/Reject (stacked)
col_nodes = {c: [] for c in range(4)}
for n in nodes:
    col_nodes[col[n]].append(n)

# Desired vertical order for col 3
col_nodes[3] = ["Train", "Val", "Test", "Reject"]

GAP = 20          # gap between nodes in same column (units = samples)
X_SCALE = 2.8     # horizontal spacing between columns
NODE_WIDTH = 0.25  # width of node rectangles in x-units

# ── Compute node y-centers ──────────────────────────────────────────────────
node_y = {}   # bottom-left y of each node rect
node_h = {}   # height of each node rect

SCALE = 1 / 100  # 1000 samples → 10 units tall

for c, ns in col_nodes.items():
    total = sum(flows[n] for n in ns) + GAP * (len(ns) - 1)
    y = total * SCALE / 2  # start from top
    for n in ns:
        h = flows[n] * SCALE
        node_y[n] = y - h
        node_h[n] = h
        y -= (h + GAP * SCALE)

# ── Colors ──────────────────────────────────────────────────────────────────
NODE_COLORS = {
    "Raw":      "#4C72B0",
    "Cleaned":  "#55A868",
    "Filtered": "#C44E52",
    "Train":    "#8172B2",
    "Val":      "#CCB974",
    "Test":     "#64B5CD",
    "Reject":   "#BBBBBB",
}

# Flow colors follow source node color
FLOW_ALPHA = 0.45

# ── Figure setup ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.set_xlim(-0.4, X_SCALE * 3 + NODE_WIDTH + 0.4)
ax.set_ylim(-5.8, 5.8)
ax.axis("off")

# ── Helper: draw a Bezier flow band ─────────────────────────────────────────
def draw_flow(ax, src, tgt, val, src_y_off, tgt_y_off, color):
    h = val * SCALE
    x0 = col[src] * X_SCALE + NODE_WIDTH
    x1 = col[tgt] * X_SCALE
    # source band: starts at node bottom + offset
    y0_bot = node_y[src] + src_y_off
    y0_top = y0_bot + h
    # target band
    y1_bot = node_y[tgt] + tgt_y_off
    y1_top = y1_bot + h

    # cubic Bezier control points
    cx = (x0 + x1) / 2
    verts_top = [
        (x0, y0_top), (cx, y0_top), (cx, y1_top), (x1, y1_top)
    ]
    verts_bot = [
        (x1, y1_bot), (cx, y1_bot), (cx, y0_bot), (x0, y0_bot)
    ]

    from matplotlib.path import Path
    codes_top = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    codes_bot = [Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    verts = verts_top + verts_bot + [(x0, y0_top)]
    codes = codes_top + codes_bot + [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=FLOW_ALPHA, zorder=1)
    ax.add_patch(patch)

# Track offsets for stacking flows at each node port
src_offsets = {n: 0.0 for n in nodes}
tgt_offsets = {n: 0.0 for n in nodes}

for link in links:
    src, tgt, val = link["source"], link["target"], link["value"]
    color = NODE_COLORS[src]
    draw_flow(ax, src, tgt, val, src_offsets[src], tgt_offsets[tgt], color)
    src_offsets[src] += val * SCALE
    tgt_offsets[tgt] += val * SCALE

# ── Draw node rectangles ─────────────────────────────────────────────────────
for n in nodes:
    x = col[n] * X_SCALE
    y = node_y[n]
    h = node_h[n]
    rect = mpatches.FancyBboxPatch(
        (x, y), NODE_WIDTH, h,
        boxstyle="square,pad=0",
        facecolor=NODE_COLORS[n], edgecolor="white", linewidth=1.2, zorder=3
    )
    ax.add_patch(rect)
    # Label
    cx = x + NODE_WIDTH / 2
    cy = y + h / 2
    fs = 9.5 if n not in ("Train", "Val", "Test") else 9
    ax.text(cx, cy, n, ha="center", va="center", fontsize=fs,
            fontweight="bold", color="white", zorder=4)
    # Value annotation above/below
    total = flows[n]
    ax.text(cx, y + h + 0.08, f"{total:,}", ha="center", va="bottom",
            fontsize=7.5, color="#444444", zorder=4)

# ── Column labels ─────────────────────────────────────────────────────────────
col_labels = {0: "Raw\ncorpus", 1: "Cleaned", 2: "Filtered", 3: "Split"}
for c, label in col_labels.items():
    x = c * X_SCALE + NODE_WIDTH / 2
    ax.text(x, 5.5, label, ha="center", va="top", fontsize=9,
            color="#555555", style="italic")

ax.set_title("Dataset Preparation Pipeline", fontsize=13, fontweight="bold",
             pad=10, color="#222222")

plt.tight_layout(pad=0.5)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
