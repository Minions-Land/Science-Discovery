import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
with open("data.json") as f:
    data = json.load(f)

system_name = data["system_name"]
stages = {s["id"]: s for s in data["stages"]}
groups = data["groups"]

# ---------------------------------------------------------------------------
# Layout  (x, y) centres – hand-tuned for this pipeline
# ---------------------------------------------------------------------------
#
#  Query → Retriever ↔ KB        Diffusion Decoder → Generated Sample
#                                      ↕
#                               Prior Network
#
pos = {
    "input":  (1.0, 3.0),
    "retrieve": (3.0, 3.0),
    "db":     (3.0, 1.5),
    "diff":   (5.5, 3.0),
    "prior":  (5.5, 1.5),
    "output": (8.0, 3.0),
}

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 9.5)
ax.set_ylim(0.5, 4.5)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("white")

# ---------------------------------------------------------------------------
# Group backgrounds (rounded rectangles)
# ---------------------------------------------------------------------------
group_cfg = {
    "Retrieval":   {"color": "#DDEEFF", "ec": "#5588BB"},
    "Generation":  {"color": "#FFEECC", "ec": "#BB8833"},
}
group_bounds = {
    "Retrieval":  (1.9, 1.0, 2.2, 2.6),   # (x0, y0, w, h)
    "Generation": (4.4, 1.0, 2.2, 2.6),
}
for g in groups:
    lbl = g["label"]
    x0, y0, w, h = group_bounds[lbl]
    cfg = group_cfg[lbl]
    rect = FancyBboxPatch((x0, y0), w, h,
                          boxstyle="round,pad=0.15",
                          linewidth=1.5, linestyle="--",
                          edgecolor=cfg["ec"], facecolor=cfg["color"],
                          zorder=0, alpha=0.6)
    ax.add_patch(rect)
    ax.text(x0 + w / 2, y0 + h + 0.12, lbl,
            ha="center", va="bottom", fontsize=9,
            color=cfg["ec"], fontstyle="italic")

# ---------------------------------------------------------------------------
# Node shapes
# ---------------------------------------------------------------------------
BOX_W, BOX_H = 1.3, 0.55

node_style = {
    "input":     {"fc": "#CCFFCC", "ec": "#338833", "shape": "round,pad=0.1"},
    "output":    {"fc": "#FFCCCC", "ec": "#883333", "shape": "round,pad=0.1"},
    "module":    {"fc": "#FFFFFF", "ec": "#444444", "shape": "round,pad=0.1"},
    "datastore": {"fc": "#EEE8FF", "ec": "#5533AA", "shape": "round,pad=0.1"},
}

for nid, stage in stages.items():
    x, y = pos[nid]
    kind = stage["kind"]
    style = node_style[kind]

    if kind == "datastore":
        # cylinder-ish: draw ellipse top + rect body
        rect = FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2),
                              BOX_W, BOX_H,
                              boxstyle="round,pad=0.08",
                              linewidth=1.5,
                              edgecolor=style["ec"], facecolor=style["fc"],
                              zorder=2)
        ax.add_patch(rect)
        # extra top ellipse to hint at cylinder
        ell = mpatches.Ellipse((x, y + BOX_H / 2), BOX_W, 0.18,
                               linewidth=1.5, edgecolor=style["ec"],
                               facecolor=style["fc"], zorder=3)
        ax.add_patch(ell)
    else:
        rect = FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2),
                              BOX_W, BOX_H,
                              boxstyle=style["shape"],
                              linewidth=1.5,
                              edgecolor=style["ec"], facecolor=style["fc"],
                              zorder=2)
        ax.add_patch(rect)

    ax.text(x, y, stage["label"],
            ha="center", va="center", fontsize=9.5,
            fontweight="bold" if kind in ("input", "output") else "normal",
            zorder=4)

# ---------------------------------------------------------------------------
# Arrows
# ---------------------------------------------------------------------------
def draw_arrow(ax, src, dst, style="solid", color="#333333"):
    x0, y0 = pos[src]
    x1, y1 = pos[dst]
    # offset so arrow starts/ends at box edge, not centre
    dx = x1 - x0
    dy = y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist

    # half-widths to clip to box edge
    hw = BOX_W / 2 + 0.05
    hh = BOX_H / 2 + 0.05
    t_start = max(abs(hw / ux) if ux != 0 else 1e9,
                  abs(hh / uy) if uy != 0 else 1e9)
    t_start = min(abs(hw / ux) if ux != 0 else 1e9,
                  abs(hh / uy) if uy != 0 else 1e9)
    t_end = t_start

    xs = x0 + ux * t_start
    ys = y0 + uy * t_start
    xe = x1 - ux * t_end
    ye = y1 - uy * t_end

    ls = "-" if style == "solid" else "--"
    ax.annotate("",
                xy=(xe, ye), xytext=(xs, ys),
                arrowprops=dict(arrowstyle="-|>",
                                color=color,
                                lw=1.4,
                                linestyle=ls,
                                mutation_scale=14),
                zorder=3)

# Data-flow (solid) arrows derived from "arrows" list in each stage
drawn = set()
for nid, stage in stages.items():
    for src_id in stage.get("arrows", []):
        key = (src_id, nid)
        if key not in drawn:
            drawn.add(key)
            draw_arrow(ax, src_id, nid)

# Feedback / control: Prior Network feeds back into Diffusion Decoder (dashed)
draw_arrow(ax, "prior", "diff", style="dashed", color="#BB8833")

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
legend_elements = [
    mpatches.Patch(facecolor="#CCFFCC", edgecolor="#338833", label="Input"),
    mpatches.Patch(facecolor="#FFFFFF", edgecolor="#444444", label="Module"),
    mpatches.Patch(facecolor="#EEE8FF", edgecolor="#5533AA", label="Datastore"),
    mpatches.Patch(facecolor="#FFCCCC", edgecolor="#883333", label="Output"),
    plt.Line2D([0], [0], color="#333333", lw=1.4, label="Data flow"),
    plt.Line2D([0], [0], color="#BB8833", lw=1.4, linestyle="--", label="Control/feedback"),
]
ax.legend(handles=legend_elements, loc="lower left", fontsize=8,
          framealpha=0.85, ncol=2)

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
ax.set_title(f"{system_name} — System Architecture", fontsize=13, fontweight="bold", pad=8)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.tight_layout()
plt.savefig("figure.pdf", bbox_inches="tight", dpi=150)
plt.savefig("figure.png", bbox_inches="tight", dpi=150)
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
