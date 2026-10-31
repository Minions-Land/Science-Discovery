"""
Sankey diagram of dataset preparation flow.
Data: data.json — nodes + links[{source, target, value}]
"""
import json
import pathlib
import subprocess
import sys

import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np

# ── palette ──────────────────────────────────────────────────────────────────
PALETTE = {
    "Raw":      "#0F4D92",
    "Cleaned":  "#2E86C1",
    "Filtered": "#1A7A4A",
    "Train":    "#117A65",
    "Val":      "#B7950B",
    "Test":     "#884EA0",
    "Reject":   "#C0392B",
}
ALPHA_FLOW = 0.38

# ── load data ─────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())
nodes = data["nodes"]
links = data["links"]

# ── layout constants ──────────────────────────────────────────────────────────
# Columns: Raw(0) → Cleaned/Reject(1) → Filtered/Reject(2) → Train/Val/Test/Reject(3)
# We place nodes in 4 x-columns.
COL_X = {
    "Raw":      0.05,
    "Cleaned":  0.32,
    "Filtered": 0.59,
    "Train":    0.86,
    "Val":      0.86,
    "Test":     0.86,
    "Reject":   0.86,
}

# Node heights proportional to total flow through them
def node_total(name):
    out = sum(l["value"] for l in links if l["source"] == name)
    inn = sum(l["value"] for l in links if l["target"] == name)
    return max(out, inn)

totals = {n: node_total(n) for n in nodes}
MAX_TOTAL = max(totals.values())
NODE_W = 0.022          # node rectangle width in axes coords
SCALE = 0.72            # total height scale factor
GAP = 0.025             # vertical gap between stacked nodes in same column

# Group nodes by column x
from collections import defaultdict
col_nodes = defaultdict(list)
for n in nodes:
    col_nodes[COL_X[n]].append(n)

# Sort within each column by a preferred order
ORDER = ["Train", "Val", "Test", "Reject", "Cleaned", "Filtered", "Raw"]
for x in col_nodes:
    col_nodes[x].sort(key=lambda n: ORDER.index(n) if n in ORDER else 99)

# Compute node y-positions (bottom of each node rect)
node_h = {n: totals[n] / MAX_TOTAL * SCALE for n in nodes}
node_y = {}  # bottom y of each node

for x, nlist in col_nodes.items():
    total_h = sum(node_h[n] for n in nlist) + GAP * (len(nlist) - 1)
    y_start = (1.0 - total_h) / 2.0  # centre vertically
    y = y_start
    for n in nlist:
        node_y[n] = y
        y += node_h[n] + GAP

# ── draw ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Track current "cursor" positions for flow attachment (source right, target left)
src_cursor = {n: node_y[n] for n in nodes}   # next available y on right edge
tgt_cursor = {n: node_y[n] for n in nodes}   # next available y on left edge

def cubic_bezier_patch(ax, x0, y0_bot, y0_top, x1, y1_bot, y1_top, color, alpha):
    """Draw a filled cubic Bezier ribbon between two vertical segments."""
    cx = (x0 + x1) / 2.0
    verts = [
        (x0, y0_bot),
        (cx, y0_bot),
        (cx, y1_bot),
        (x1, y1_bot),
        (x1, y1_top),
        (cx, y1_top),
        (cx, y0_top),
        (x0, y0_top),
        (x0, y0_bot),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    patch = mpatches.PathPatch(
        Path(verts, codes),
        facecolor=color,
        edgecolor="none",
        alpha=alpha,
        zorder=1,
    )
    ax.add_patch(patch)

# Draw flows
for link in links:
    src, tgt, val = link["source"], link["target"], link["value"]
    h = val / MAX_TOTAL * SCALE

    # source attachment (right edge of source node)
    sx = COL_X[src] + NODE_W
    sy_bot = src_cursor[src]
    sy_top = sy_bot + h
    src_cursor[src] += h

    # target attachment (left edge of target node)
    tx = COL_X[tgt]
    ty_bot = tgt_cursor[tgt]
    ty_top = ty_bot + h
    tgt_cursor[tgt] += h

    color = PALETTE[src]
    cubic_bezier_patch(ax, sx, sy_bot, sy_top, tx, ty_bot, ty_top, color, ALPHA_FLOW)

# Draw node rectangles
for n in nodes:
    x = COL_X[n]
    y = node_y[n]
    h = node_h[n]
    rect = mpatches.FancyBboxPatch(
        (x, y), NODE_W, h,
        boxstyle="square,pad=0",
        facecolor=PALETTE[n],
        edgecolor="white",
        linewidth=0.6,
        zorder=2,
    )
    ax.add_patch(rect)

# Labels
LABEL_FONTSIZE = 8.5
for n in nodes:
    x = COL_X[n]
    y = node_y[n] + node_h[n] / 2.0
    val = totals[n]
    # place label to the left for leftmost column, right for rightmost, outside for middle
    if x < 0.2:
        ha, xpos = "right", x - 0.008
    elif x > 0.8:
        ha, xpos = "left", x + NODE_W + 0.008
    else:
        ha, xpos = "left", x + NODE_W + 0.008

    ax.text(
        xpos, y,
        f"{n}\n{val:,}",
        ha=ha, va="center",
        fontsize=LABEL_FONTSIZE,
        color=PALETTE[n],
        fontweight="bold",
        linespacing=1.3,
    )

# Title
ax.text(
    0.5, 0.97,
    "Dataset Preparation Flow",
    ha="center", va="top",
    fontsize=11, fontweight="bold",
    color="#272727",
    transform=ax.transAxes,
)

fig.tight_layout(pad=0.3)

# ── save ──────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
plt.close(fig)
print(f"Saved: {pdf_path}, {png_path}, {svg_path}")

# ── font verification ─────────────────────────────────────────────────────────
import re
raw = pdf_path.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)
print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")
