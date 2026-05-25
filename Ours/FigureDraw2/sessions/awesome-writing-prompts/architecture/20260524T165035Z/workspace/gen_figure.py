import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ── palette ──────────────────────────────────────────────────────────────────
C_INPUT   = "#D6EAF8"   # light blue
C_OUTPUT  = "#D5F5E3"   # light green
C_MODULE  = "#EBF5FB"   # very light blue
C_STORE   = "#FEF9E7"   # light yellow
C_GROUP   = "#F2F3F4"   # near-white grey
C_EDGE    = "#5D6D7E"   # dark slate
C_ARROW   = "#2E4057"
C_TEXT    = "#1A252F"
C_BORDER  = "#AEB6BF"

# ── node positions (x, y) in data coords ─────────────────────────────────────
# Layout:
#   input  →  retrieve  →  diff  →  output
#                ↕               ↕
#               db            prior
POS = {
    "input":   (0.5, 3.0),
    "retrieve":(2.5, 3.0),
    "db":      (2.5, 1.5),
    "diff":    (5.0, 3.0),
    "prior":   (5.0, 1.5),
    "output":  (7.5, 3.0),
}

NODE_W, NODE_H = 1.4, 0.7
DB_W,   DB_H   = 1.2, 0.6

def draw_node(ax, nid, label, kind):
    x, y = POS[nid]
    w = DB_W if kind == "datastore" else NODE_W
    h = DB_H if kind == "datastore" else NODE_H

    if kind == "input":
        color, lw = C_INPUT, 1.5
    elif kind == "output":
        color, lw = C_OUTPUT, 1.5
    elif kind == "datastore":
        color, lw = C_STORE, 1.2
    else:
        color, lw = C_MODULE, 1.2

    style = "round,pad=0.05"
    box = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=style,
        linewidth=lw,
        edgecolor=C_BORDER,
        facecolor=color,
        zorder=3,
    )
    ax.add_patch(box)

    # cylinder hint for datastore
    if kind == "datastore":
        ax.text(x, y, label, ha="center", va="center",
                fontsize=9, color=C_TEXT, fontweight="bold", zorder=4)
        # small lines to suggest cylinder
        for dy in (-h/2 + 0.05, h/2 - 0.05):
            ax.plot([x - w/2 + 0.05, x + w/2 - 0.05], [y + dy, y + dy],
                    color=C_BORDER, lw=0.8, zorder=4)
    else:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=9, color=C_TEXT, fontweight="bold", zorder=4)

def arrow(ax, src, dst, dashed=False):
    x0, y0 = POS[src]
    x1, y1 = POS[dst]

    # offset from box edge
    dx, dy = x1 - x0, y1 - y0
    dist = (dx**2 + dy**2) ** 0.5
    ux, uy = dx/dist, dy/dist

    w = DB_W if src == "db" else NODE_W
    h = DB_H if src == "db" else NODE_H
    w2 = DB_W if dst == "db" else NODE_W
    h2 = DB_H if dst == "db" else NODE_H

    # simple edge-clipping: move start/end to box boundary
    sx = x0 + ux * (w/2 + 0.05)
    sy = y0 + uy * (h/2 + 0.05)
    ex = x1 - ux * (w2/2 + 0.05)
    ey = y1 - uy * (h2/2 + 0.05)

    ls = (0, (4, 3)) if dashed else "solid"
    ax.annotate(
        "", xy=(ex, ey), xytext=(sx, sy),
        arrowprops=dict(
            arrowstyle="-|>",
            color=C_ARROW,
            lw=1.4,
            linestyle=ls,
            mutation_scale=12,
        ),
        zorder=2,
    )

def draw_group(ax, label, node_ids, pad=0.35):
    xs = [POS[n][0] for n in node_ids]
    ys = [POS[n][1] for n in node_ids]
    x0, x1 = min(xs) - NODE_W/2 - pad, max(xs) + NODE_W/2 + pad
    y0, y1 = min(ys) - NODE_H/2 - pad, max(ys) + NODE_H/2 + pad
    rect = FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0.1",
        linewidth=1.0,
        edgecolor=C_BORDER,
        facecolor=C_GROUP,
        linestyle="--",
        zorder=1,
    )
    ax.add_patch(rect)
    ax.text(x0 + 0.12, y1 - 0.12, label,
            ha="left", va="top", fontsize=8,
            color=C_EDGE, style="italic", zorder=5)

# ── main ─────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.set_xlim(-0.3, 9.0)
ax.set_ylim(0.5, 4.2)
ax.set_aspect("equal")
ax.axis("off")

# title
ax.text(4.35, 4.0, data["system_name"],
        ha="center", va="center", fontsize=13,
        fontweight="bold", color=C_TEXT)

# groups (drawn first, behind nodes)
for g in data["groups"]:
    draw_group(ax, g["label"], g["node_ids"])

# arrows
stage_map = {s["id"]: s for s in data["stages"]}
for s in data["stages"]:
    for src_id in s.get("arrows", []):
        # feedback arrow from db back to retrieve is dashed (control)
        dashed = (src_id == "retrieve" and s["id"] == "db")
        arrow(ax, src_id, s["id"], dashed=dashed)

# nodes
for s in data["stages"]:
    draw_node(ax, s["id"], s["label"], s["kind"])

# legend
solid_patch = mpatches.FancyArrow(0, 0, 0.3, 0, width=0.01,
                                   color=C_ARROW, length_includes_head=True)
legend_elements = [
    mpatches.Patch(facecolor=C_INPUT,  edgecolor=C_BORDER, label="Input / Output"),
    mpatches.Patch(facecolor=C_MODULE, edgecolor=C_BORDER, label="Module"),
    mpatches.Patch(facecolor=C_STORE,  edgecolor=C_BORDER, label="Datastore"),
    plt.Line2D([0],[0], color=C_ARROW, lw=1.4, label="Data flow"),
    plt.Line2D([0],[0], color=C_ARROW, lw=1.4, linestyle=(0,(4,3)), label="Control / feedback"),
]
ax.legend(handles=legend_elements, loc="lower right",
          fontsize=7.5, framealpha=0.85, edgecolor=C_BORDER,
          bbox_to_anchor=(1.0, 0.0))

plt.tight_layout(pad=0.3)
plt.savefig("figure.pdf", bbox_inches="tight", dpi=150)
plt.savefig("figure.png", bbox_inches="tight", dpi=150)
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
