"""
RetroDiff architecture diagram — boxes-and-arrows via matplotlib patches.
Data source: data.json
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

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

PALETTE = {
    "input":     "#0F4D92",
    "output":    "#0072B2",
    "module":    "#56B4E9",
    "datastore": "#E69F00",
    "group_bg":  "#EEF4FC",
    "group_gen": "#F3EFFA",
    "arrow_data": "#272727",
    "arrow_ctrl": "#767676",
    "text_dark":  "#272727",
    "text_light": "#FFFFFF",
}

with open("data.json") as f:
    data = json.load(f)

# --- Layout: left-to-right pipeline ---
# Positions (cx, cy) in figure-coord inches on a 9x4 inch canvas
#   Query  ->  [Retriever / KB]  ->  [DiffDecoder / Prior]  ->  Output
NODE_POS = {
    "input":   (0.9,  2.0),
    "retrieve":(3.0,  2.7),
    "db":      (3.0,  1.3),
    "diff":    (5.7,  2.7),
    "prior":   (5.7,  1.3),
    "output":  (8.2,  2.0),
}

NODE_W = 1.45
NODE_H = 0.55
DS_RAD = 0.30   # datastore cylinder radius

def node_rect(cx, cy, kind):
    """Return (x, y, w, h) for bounding box, lower-left origin."""
    if kind == "datastore":
        return cx - DS_RAD, cy - DS_RAD, DS_RAD*2, DS_RAD*2
    return cx - NODE_W/2, cy - NODE_H/2, NODE_W, NODE_H

def node_color(kind):
    if kind == "input":   return PALETTE["input"],      PALETTE["text_light"]
    if kind == "output":  return PALETTE["output"],     PALETTE["text_light"]
    if kind == "module":  return PALETTE["module"],     PALETTE["text_dark"]
    if kind == "datastore": return PALETTE["datastore"], PALETTE["text_dark"]
    return "#AAAAAA", PALETTE["text_dark"]

fig, ax = plt.subplots(figsize=(9.5, 4.2))
ax.set_xlim(0, 9.5)
ax.set_ylim(0, 4.2)
ax.axis("off")

# --- Group background panels ---
# Retrieval group: retrieve + db
groups_info = {
    g["label"]: g["node_ids"] for g in data["groups"]
}

def group_bbox(node_ids, pad=0.35):
    xs = [NODE_POS[n][0] for n in node_ids]
    ys = [NODE_POS[n][1] for n in node_ids]
    x0 = min(xs) - NODE_W/2 - pad
    y0 = min(ys) - NODE_H/2 - pad
    x1 = max(xs) + NODE_W/2 + pad
    y1 = max(ys) + NODE_H/2 + pad + 0.30  # headroom for label
    return x0, y0, x1 - x0, y1 - y0

group_colors = {
    "Retrieval":  PALETTE["group_bg"],
    "Generation": PALETTE["group_gen"],
}

for label, node_ids in groups_info.items():
    gx, gy, gw, gh = group_bbox(node_ids)
    rect = FancyBboxPatch((gx, gy), gw, gh,
                          boxstyle="round,pad=0.0",
                          linewidth=0.8, edgecolor="#AAAAAA",
                          facecolor=group_colors.get(label, "#F5F5F5"),
                          linestyle="--",
                          zorder=1)
    ax.add_patch(rect)
    ax.text(gx + gw/2, gy + gh - 0.12, label,
            ha="center", va="top", fontsize=8,
            color="#444444", style="italic", zorder=3)

# --- Build id->stage lookup ---
stages = {s["id"]: s for s in data["stages"]}

# --- Draw arrows FIRST (below nodes) ---
def get_port(src_id, dst_id):
    """Return approximate (x_src_out, y_src_out, x_dst_in, y_dst_in)."""
    sx, sy = NODE_POS[src_id]
    dx, dy = NODE_POS[dst_id]
    # horizontal bias: pick right/left ports if mostly horizontal
    if abs(dx - sx) >= abs(dy - sy):
        # horizontal
        if dx > sx:
            return sx + NODE_W/2, sy, dx - NODE_W/2, dy
        else:
            return sx - NODE_W/2, sy, dx + NODE_W/2, dy
    else:
        # vertical
        if dy > sy:
            return sx, sy + NODE_H/2, dx, dy - NODE_H/2
        else:
            return sx, sy - NODE_H/2, dx, dy + NODE_H/2

# datastore is a circle — adjust port
def adjust_for_datastore(node_id, x, y, other_x, other_y):
    if stages[node_id]["kind"] == "datastore":
        cx, cy = NODE_POS[node_id]
        dx, dy = other_x - cx, other_y - cy
        norm = (dx**2 + dy**2)**0.5
        return cx + DS_RAD * dx/norm, cy + DS_RAD * dy/norm
    return x, y

arrow_style = dict(arrowstyle="-|>", color=PALETTE["arrow_data"],
                   linewidth=1.4, mutation_scale=12)

# Also add control arrow: prior -> diff (feedback/control, dashed)
CTRL_ARROWS = {("prior", "diff")}

for stage in data["stages"]:
    dst_id = stage["id"]
    for src_id in stage.get("arrows", []):
        x0, y0, x1, y1 = get_port(src_id, dst_id)
        # Adjust for datastore endpoints
        x0, y0 = adjust_for_datastore(src_id, x0, y0, x1, y1)
        x1, y1 = adjust_for_datastore(dst_id, x1, y1, x0, y0)
        is_ctrl = (src_id, dst_id) in CTRL_ARROWS
        style = dict(arrowstyle="-|>",
                     color=PALETTE["arrow_ctrl"] if is_ctrl else PALETTE["arrow_data"],
                     linewidth=1.2 if is_ctrl else 1.4,
                     mutation_scale=11,
                     linestyle="dashed" if is_ctrl else "solid")
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>",
                                   color=style["color"],
                                   lw=style["linewidth"],
                                   linestyle=style["linestyle"],
                                   mutation_scale=style["mutation_scale"]),
                    zorder=2)

# --- Draw nodes ---
for sid, stage in stages.items():
    cx, cy = NODE_POS[sid]
    kind = stage["kind"]
    fc, tc = node_color(kind)
    label = stage["label"]

    if kind == "datastore":
        circle = plt.Circle((cx, cy), DS_RAD, facecolor=fc, edgecolor="#555555",
                             linewidth=0.8, zorder=4)
        ax.add_patch(circle)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=8, color=tc, fontweight="bold", zorder=5)
    else:
        rx = cx - NODE_W/2
        ry = cy - NODE_H/2
        box = FancyBboxPatch((rx, ry), NODE_W, NODE_H,
                             boxstyle="round,pad=0.06",
                             facecolor=fc, edgecolor="#333333",
                             linewidth=0.8, zorder=4)
        ax.add_patch(box)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=9, color=tc, fontweight="bold", zorder=5)

# --- Title ---
ax.text(4.75, 3.95, data["system_name"], ha="center", va="top",
        fontsize=12, fontweight="bold", color=PALETTE["text_dark"], zorder=6)

# --- Legend for arrow types ---
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=PALETTE["arrow_data"], linewidth=1.4,
           label="Data flow", marker=">", markersize=6),
    Line2D([0], [0], color=PALETTE["arrow_ctrl"], linewidth=1.2,
           linestyle="dashed", label="Control / feedback",
           marker=">", markersize=5),
]
ax.legend(handles=legend_elements, loc="lower right",
          fontsize=7.5, frameon=False,
          bbox_to_anchor=(1.0, 0.01))

plt.tight_layout(pad=0.3)

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
