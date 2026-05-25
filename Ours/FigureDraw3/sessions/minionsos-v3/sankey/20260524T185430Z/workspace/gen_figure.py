"""
Sankey diagram — dataset preparation flow.
archetype: sankey (distribution/structure family, figure-chart-atlas)
data: data.json
layout: single-panel, figsize ~(9, 5) inches
"""

import json
import pathlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import numpy as np

# Font stack — do NOT override per element
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "legend.frameon": False,
})

PALETTE = {
    "raw":      "#0F4D92",
    "cleaned":  "#2E86C1",
    "filtered": "#1A7A4A",
    "train":    "#117A65",
    "val":      "#1E8449",
    "test":     "#27AE60",
    "reject":   "#C0392B",
    "flow":     "#B0BEC5",
    "bg":       "#FAFAFA",
}

HERE = pathlib.Path(__file__).parent
data = json.loads((HERE / "data.json").read_text())

# ── layout constants ──────────────────────────────────────────────────────────
NODE_W   = 0.04   # node rectangle width (in x-units 0-1)
PAD      = 0.015  # vertical gap between stacked flows at a node
CURVE_RES = 100   # bezier resolution

# x positions for each column
COL_X = {
    "Raw":      0.05,
    "Cleaned":  0.30,
    "Filtered": 0.55,
    "Train":    0.82,
    "Val":      0.82,
    "Test":     0.82,
    "Reject":   0.82,
}

# node colors
NODE_COLOR = {
    "Raw":      PALETTE["raw"],
    "Cleaned":  PALETTE["cleaned"],
    "Filtered": PALETTE["filtered"],
    "Train":    PALETTE["train"],
    "Val":      PALETTE["val"],
    "Test":     PALETTE["test"],
    "Reject":   PALETTE["reject"],
}

# ── compute node heights (proportional to total flow) ────────────────────────
links = data["links"]
nodes = data["nodes"]

# total flow through each node (max of in-flow and out-flow)
in_flow  = {n: 0 for n in nodes}
out_flow = {n: 0 for n in nodes}
for lk in links:
    out_flow[lk["source"]] += lk["value"]
    in_flow[lk["target"]]  += lk["value"]

node_flow = {n: max(in_flow[n], out_flow[n]) for n in nodes}
# Raw is source-only
node_flow["Raw"] = out_flow["Raw"]

TOTAL = node_flow["Raw"]   # 1120 — normalise everything to this
Y_SCALE = 0.80             # fraction of figure height used for nodes

def h(val):
    return val / TOTAL * Y_SCALE

# ── assign y-positions for each node ─────────────────────────────────────────
# Nodes in the same column are stacked with a small gap
COLUMNS = {
    0: ["Raw"],
    1: ["Cleaned"],
    2: ["Filtered"],
    3: ["Train", "Val", "Test", "Reject"],
}

node_y = {}   # bottom y of each node rectangle
for col_nodes in COLUMNS.values():
    total_h = sum(h(node_flow[n]) for n in col_nodes)
    n_gaps  = len(col_nodes) - 1
    gap     = PAD
    total_span = total_h + n_gaps * gap
    y_start = 0.5 - total_span / 2   # centre vertically
    y = y_start
    for n in col_nodes:
        node_y[n] = y
        y += h(node_flow[n]) + gap

# ── draw ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(PALETTE["bg"])
ax.set_facecolor(PALETTE["bg"])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

def draw_node(name):
    x = COL_X[name]
    y = node_y[name]
    ht = h(node_flow[name])
    rect = mpatches.FancyBboxPatch(
        (x, y), NODE_W, ht,
        boxstyle="round,pad=0.003",
        linewidth=0,
        facecolor=NODE_COLOR[name],
        zorder=3,
    )
    ax.add_patch(rect)
    # label
    label_x = x + NODE_W / 2
    label_y = y + ht / 2
    ax.text(label_x, label_y, name,
            ha="center", va="center",
            fontsize=8, fontweight="bold",
            color="white", zorder=4)
    # value annotation outside node
    val = node_flow[name]
    if COL_X[name] >= 0.80:
        ax.text(x + NODE_W + 0.012, label_y, f"{val:,}",
                ha="left", va="center", fontsize=7.5, color="#444444", zorder=4)
    else:
        ax.text(x + NODE_W + 0.012, label_y, f"{val:,}",
                ha="left", va="center", fontsize=7.5, color="#444444", zorder=4)

# track how much of each node's out/in port has been consumed
out_cursor = {n: node_y[n] for n in nodes}   # next free y on right edge
in_cursor  = {n: node_y[n] for n in nodes}   # next free y on left edge

def draw_flow(src, tgt, val):
    flow_h = h(val)
    color  = NODE_COLOR[src]

    # source port: right edge of src node
    x0 = COL_X[src] + NODE_W
    y0_bot = out_cursor[src]
    y0_top = y0_bot + flow_h
    out_cursor[src] += flow_h + PAD * 0.3

    # target port: left edge of tgt node
    x1 = COL_X[tgt]
    y1_bot = in_cursor[tgt]
    y1_top = y1_bot + flow_h
    in_cursor[tgt] += flow_h + PAD * 0.3

    # cubic bezier ribbon
    cx = (x0 + x1) / 2
    t  = np.linspace(0, 1, CURVE_RES)

    def bezier(p0, p1, p2, p3):
        return ((1-t)**3 * p0 + 3*(1-t)**2*t * p1
                + 3*(1-t)*t**2 * p2 + t**3 * p3)

    # top edge: y0_top → y1_top
    xt = bezier(x0, cx, cx, x1)
    yt = bezier(y0_top, y0_top, y1_top, y1_top)
    # bottom edge: y1_bot → y0_bot (reversed)
    xb = bezier(x1, cx, cx, x0)
    yb = bezier(y1_bot, y1_bot, y0_bot, y0_bot)

    xs = np.concatenate([xt, xb])
    ys = np.concatenate([yt, yb])

    ax.fill(xs, ys, color=color, alpha=0.30, zorder=1, linewidth=0)
    # thin border lines
    ax.plot(xt, yt, color=color, alpha=0.55, linewidth=0.5, zorder=2)
    ax.plot(xb[::-1], yb[::-1], color=color, alpha=0.55, linewidth=0.5, zorder=2)

# draw flows first (behind nodes)
for lk in links:
    draw_flow(lk["source"], lk["target"], lk["value"])

# draw nodes on top
for n in nodes:
    draw_node(n)

# column labels
col_labels = {0.05: "Ingestion", 0.30: "Cleaning", 0.55: "Filtering", 0.82: "Split"}
for x, label in col_labels.items():
    ax.text(x + NODE_W / 2, 0.96, label,
            ha="center", va="top", fontsize=8, color="#666666",
            style="italic")

# title
ax.text(0.5, 1.01, "Dataset Preparation Flow",
        ha="center", va="bottom", fontsize=10, fontweight="bold",
        color="#222222", transform=ax.transAxes)

plt.tight_layout(pad=0.3)

out = HERE
fig.savefig(out / "figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig(out / "figure.png", bbox_inches="tight", dpi=300)
fig.savefig(out / "figure.svg", bbox_inches="tight")
plt.close(fig)
print("Saved figure.pdf, figure.png, figure.svg")
