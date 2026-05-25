"""
Sankey diagram of dataset preparation flow.
Data source: data.json
"""
import json
import pathlib
import subprocess
import sys
import re

import matplotlib as mpl
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
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ── palette ──────────────────────────────────────────────────────────────────
PALETTE = {
    "raw":      "#0F4D92",   # deep blue
    "cleaned":  "#2E86C1",   # mid blue
    "filtered": "#5DADE2",   # light blue
    "train":    "#1A7A4A",   # green
    "val":      "#27AE60",   # mid green
    "test":     "#82E0AA",   # light green
    "reject":   "#C0392B",   # red (directional: loss/rejection)
    "flow":     "#B0BEC5",   # neutral grey for flow bands
}

# ── load data ─────────────────────────────────────────────────────────────────
data = json.loads(pathlib.Path("data.json").read_text())
nodes_list = data["nodes"]
links = data["links"]

# ── layout constants ──────────────────────────────────────────────────────────
# Columns: 0=Raw, 1=Cleaned, 2=Filtered, 3=Train/Val/Test/Reject(right)
# We place Reject as a side-exit from Raw and Cleaned (flows right-down)
# Node x positions (0..1 normalised)
NODE_X = {
    "Raw":      0.05,
    "Cleaned":  0.32,
    "Filtered": 0.59,
    "Train":    0.86,
    "Val":      0.86,
    "Test":     0.86,
    "Reject":   0.86,
}

# Node colors
NODE_COLOR = {
    "Raw":      PALETTE["raw"],
    "Cleaned":  PALETTE["cleaned"],
    "Filtered": PALETTE["filtered"],
    "Train":    PALETTE["train"],
    "Val":      PALETTE["val"],
    "Test":     PALETTE["test"],
    "Reject":   PALETTE["reject"],
}

# ── compute node totals ───────────────────────────────────────────────────────
node_in  = {n: 0 for n in nodes_list}
node_out = {n: 0 for n in nodes_list}
for lk in links:
    node_out[lk["source"]] += lk["value"]
    node_in[lk["target"]]  += lk["value"]

# Node height = max(in, out) for sizing; Raw is the root
node_total = {}
for n in nodes_list:
    node_total[n] = max(node_in[n], node_out[n], 1)
# Raw is special: its total is sum of outflows
node_total["Raw"] = sum(lk["value"] for lk in links if lk["source"] == "Raw")

# ── figure setup ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# ── vertical layout ───────────────────────────────────────────────────────────
# We stack nodes vertically within each column.
# Column 0: Raw (single node)
# Column 1: Cleaned (single node, centred on Raw's main flow)
# Column 2: Filtered (single node)
# Column 3: Train, Val, Test stacked top; Reject at bottom

TOTAL = node_total["Raw"]   # 1120 (1000 + 120)
SCALE = 0.72                # fraction of figure height used for node bars
MARGIN_TOP = 0.88
BAR_W = 0.045               # node bar width in axes coords
GAP = 0.012                 # gap between stacked nodes in same column

def node_height(n):
    return node_total[n] / TOTAL * SCALE

# Column 3 layout: Train, Val, Test, Reject stacked with gaps
col3_nodes = ["Train", "Val", "Test", "Reject"]
col3_heights = [node_height(n) for n in col3_nodes]
col3_total_h = sum(col3_heights) + GAP * (len(col3_nodes) - 1)
col3_top = MARGIN_TOP - (SCALE - col3_total_h) / 2  # centre vertically

node_y_top = {}   # top y of each node bar
node_y_bot = {}   # bottom y of each node bar

# Place col3 nodes
y = col3_top
for n in col3_nodes:
    h = node_height(n)
    node_y_top[n] = y
    node_y_bot[n] = y - h
    y -= h + GAP

# Place single-column nodes centred on their main flow
def place_single(name, flow_centre_y):
    h = node_height(name)
    node_y_top[name] = flow_centre_y + h / 2
    node_y_bot[name] = flow_centre_y - h / 2

# Filtered: centred on Train+Val+Test combined centre
train_val_test_centre = (node_y_top["Train"] + node_y_bot["Test"]) / 2
place_single("Filtered", train_val_test_centre)

# Cleaned: centred on Filtered
cleaned_centre = (node_y_top["Filtered"] + node_y_bot["Filtered"]) / 2
place_single("Cleaned", cleaned_centre)

# Raw: centred on Cleaned
raw_centre = (node_y_top["Cleaned"] + node_y_bot["Cleaned"]) / 2
place_single("Raw", raw_centre)

# ── draw flow bands (cubic bezier) ───────────────────────────────────────────
# For each link, draw a filled bezier band between source and target nodes.
# Track current "cursor" on each node's right/left edge.
src_cursor  = {n: node_y_top[n] for n in nodes_list}   # next available top on right edge
tgt_cursor  = {n: node_y_top[n] for n in nodes_list}   # next available top on left edge

def draw_flow(ax, src, tgt, value, color, alpha=0.38):
    h = value / TOTAL * SCALE
    x0 = NODE_X[src] + BAR_W
    x1 = NODE_X[tgt]
    y0_top = src_cursor[src]
    y0_bot = y0_top - h
    y1_top = tgt_cursor[tgt]
    y1_bot = y1_top - h
    src_cursor[src] -= h
    tgt_cursor[tgt] -= h

    # cubic bezier control points
    cx = (x0 + x1) / 2
    verts_top = [(x0, y0_top), (cx, y0_top), (cx, y1_top), (x1, y1_top)]
    verts_bot = [(x1, y1_bot), (cx, y1_bot), (cx, y0_bot), (x0, y0_bot)]

    from matplotlib.path import Path
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path_top = Path(verts_top, codes)
    path_bot = Path(verts_bot, codes)

    # sample the bezier curves for fill
    t = np.linspace(0, 1, 60)
    def bezier(p0, p1, p2, p3, t):
        return ((1-t)**3 * np.array(p0) +
                3*(1-t)**2*t * np.array(p1) +
                3*(1-t)*t**2 * np.array(p2) +
                t**3 * np.array(p3))

    top_pts = bezier(verts_top[0], verts_top[1], verts_top[2], verts_top[3], t[:, None])
    bot_pts = bezier(verts_bot[0], verts_bot[1], verts_bot[2], verts_bot[3], t[:, None])

    xs = np.concatenate([top_pts[:, 0], bot_pts[:, 0]])
    ys = np.concatenate([top_pts[:, 1], bot_pts[:, 1]])
    ax.fill(xs, ys, color=color, alpha=alpha, linewidth=0, zorder=1)

# Draw flows in order: main flows first, then reject flows
flow_colors = {
    ("Raw",     "Cleaned"):  PALETTE["cleaned"],
    ("Raw",     "Reject"):   PALETTE["reject"],
    ("Cleaned", "Filtered"): PALETTE["filtered"],
    ("Cleaned", "Reject"):   PALETTE["reject"],
    ("Filtered","Train"):    PALETTE["train"],
    ("Filtered","Val"):      PALETTE["val"],
    ("Filtered","Test"):     PALETTE["test"],
}

# Sort: main flows first (non-reject), then reject
sorted_links = sorted(links, key=lambda lk: (lk["target"] == "Reject", lk["value"]))
sorted_links = sorted_links[::-1]  # largest first within each group

for lk in sorted_links:
    color = flow_colors.get((lk["source"], lk["target"]), PALETTE["flow"])
    draw_flow(ax, lk["source"], lk["target"], lk["value"], color)

# ── draw node bars ────────────────────────────────────────────────────────────
for n in nodes_list:
    x = NODE_X[n]
    y_bot = node_y_bot[n]
    h = node_y_top[n] - node_y_bot[n]
    rect = mpatches.FancyBboxPatch(
        (x, y_bot), BAR_W, h,
        boxstyle="square,pad=0",
        facecolor=NODE_COLOR[n],
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    ax.add_patch(rect)

# ── labels ────────────────────────────────────────────────────────────────────
label_offset_x = {
    "Raw":      -0.005,
    "Cleaned":  -0.005,
    "Filtered": -0.005,
    "Train":     0.005,
    "Val":       0.005,
    "Test":      0.005,
    "Reject":    0.005,
}
label_ha = {
    "Raw": "right", "Cleaned": "right", "Filtered": "right",
    "Train": "left", "Val": "left", "Test": "left", "Reject": "left",
}

for n in nodes_list:
    cx = NODE_X[n] + (BAR_W if label_ha[n] == "left" else 0) + label_offset_x[n]
    cy = (node_y_top[n] + node_y_bot[n]) / 2
    total_val = node_total[n]
    ax.text(cx, cy + 0.025, n, ha=label_ha[n], va="bottom",
            fontsize=9, fontweight="bold", color=NODE_COLOR[n], zorder=5)
    ax.text(cx, cy - 0.015, f"n={total_val:,}", ha=label_ha[n], va="top",
            fontsize=8, color="#555555", zorder=5)

# ── title ─────────────────────────────────────────────────────────────────────
ax.text(0.5, 0.97, "Dataset Preparation Flow", ha="center", va="top",
        fontsize=11, fontweight="bold", transform=ax.transAxes)

fig.tight_layout(pad=0.3)

# ── save ──────────────────────────────────────────────────────────────────────
out_dir = pathlib.Path(".")
fig.savefig(out_dir / "figure.pdf", bbox_inches="tight")
fig.savefig(out_dir / "figure.png", dpi=300, bbox_inches="tight")
fig.savefig(out_dir / "figure.svg", bbox_inches="tight")
plt.close(fig)
print("Saved figure.pdf, figure.png, figure.svg")

# ── font verification ─────────────────────────────────────────────────────────
pdf_path = pathlib.Path("figure.pdf")
out = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if out.returncode == 0:
    if "Type 3" in out.stdout:
        sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    # fallback: raw bytes check
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (pdffonts unavailable; byte-scan passed)")
