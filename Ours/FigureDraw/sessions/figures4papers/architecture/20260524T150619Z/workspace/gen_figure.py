import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

with open("data.json") as f:
    data = json.load(f)

# ── Layout positions (x, y) in figure units ──────────────────────────────────
# Left-to-right pipeline: Query → Retriever ↔ KB,  Retriever → Diffusion Decoder → output
#                                                          ↕
#                                                    Prior Network

pos = {
    "input":  (1.0, 3.0),
    "retrieve": (3.0, 3.0),
    "db":     (3.0, 1.5),
    "diff":   (5.5, 3.0),
    "prior":  (5.5, 1.5),
    "output": (8.0, 3.0),
}

node_size = (1.3, 0.65)   # width, height

kind_styles = {
    "input":     dict(facecolor="#d0e8ff", edgecolor="#2176ae", linewidth=1.5),
    "output":    dict(facecolor="#d5f5e3", edgecolor="#1a7a46", linewidth=1.5),
    "module":    dict(facecolor="#fff3cd", edgecolor="#b5862a", linewidth=1.5),
    "datastore": dict(facecolor="#f0e6ff", edgecolor="#6a3fbf", linewidth=1.5),
}

group_styles = {
    "Retrieval":  dict(facecolor="#e8f4fd", edgecolor="#2176ae", linestyle="--", linewidth=1.2, alpha=0.55),
    "Generation": dict(facecolor="#fef9e7", edgecolor="#b5862a", linestyle="--", linewidth=1.2, alpha=0.55),
}

# Build stage lookup
stage_by_id = {s["id"]: s for s in data["stages"]}

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 9.5)
ax.set_ylim(0.5, 4.5)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.text(4.75, 4.2, data["system_name"], ha="center", va="center",
        fontsize=13, fontweight="bold", color="#222222")

# ── Draw group backgrounds ────────────────────────────────────────────────────
def group_bbox(node_ids, pad=0.45):
    xs = [pos[n][0] for n in node_ids]
    ys = [pos[n][1] for n in node_ids]
    x0 = min(xs) - node_size[0]/2 - pad
    y0 = min(ys) - node_size[1]/2 - pad
    w  = max(xs) - min(xs) + node_size[0] + 2*pad
    h  = max(ys) - min(ys) + node_size[1] + 2*pad
    return x0, y0, w, h

for group in data["groups"]:
    x0, y0, w, h = group_bbox(group["node_ids"])
    style = group_styles[group["label"]]
    rect = FancyBboxPatch((x0, y0), w, h,
                          boxstyle="round,pad=0.05",
                          facecolor=style["facecolor"],
                          edgecolor=style["edgecolor"],
                          linestyle=style["linestyle"],
                          linewidth=style["linewidth"],
                          alpha=style["alpha"],
                          zorder=1)
    ax.add_patch(rect)
    ax.text(x0 + w/2, y0 + h + 0.06, group["label"],
            ha="center", va="bottom", fontsize=8, color=style["edgecolor"],
            fontstyle="italic")

# ── Draw arrows ───────────────────────────────────────────────────────────────
def node_edge(src_id, dst_id, kind="solid"):
    sx, sy = pos[src_id]
    dx, dy = pos[dst_id]
    # Pick exit/entry points on box edges
    if abs(sx - dx) > abs(sy - dy):
        # horizontal dominant
        if dx > sx:
            start = (sx + node_size[0]/2, sy)
            end   = (dx - node_size[0]/2, dy)
        else:
            start = (sx - node_size[0]/2, sy)
            end   = (dx + node_size[0]/2, dy)
    else:
        # vertical dominant
        if dy > sy:
            start = (sx, sy + node_size[1]/2)
            end   = (dx, dy - node_size[1]/2)
        else:
            start = (sx, sy - node_size[1]/2)
            end   = (dx, dy + node_size[1]/2)
    return start, end

# Edges from arrows field → solid data-flow arrows
drawn_pairs = set()
for stage in data["stages"]:
    dst = stage["id"]
    for src in stage.get("arrows", []):
        pair = (src, dst)
        if pair in drawn_pairs:
            continue
        drawn_pairs.add(pair)
        start, end = node_edge(src, dst)
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color="#444444",
                                    lw=1.4, mutation_scale=14),
                    zorder=3)

# Dashed feedback arrow: Prior Network → Diffusion Decoder (control/feedback)
start, end = node_edge("prior", "diff")
ax.annotate("", xy=end, xytext=start,
            arrowprops=dict(arrowstyle="-|>", color="#888888",
                            lw=1.2, linestyle="dashed", mutation_scale=12),
            zorder=3)
# label the feedback arrow
mx = (pos["prior"][0] + pos["diff"][0]) / 2
my = (pos["prior"][1] + pos["diff"][1]) / 2 - 0.22
ax.text(mx, my, "guidance", ha="center", va="top", fontsize=6.5,
        color="#888888", style="italic")

# ── Draw nodes ────────────────────────────────────────────────────────────────
def draw_node(ax, stage_id, label, kind):
    x, y = pos[stage_id]
    style = kind_styles.get(kind, kind_styles["module"])
    w, h = node_size
    if kind == "datastore":
        # cylinder-ish: use an ellipse on top of a rectangle
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle="round,pad=0.07",
                              zorder=4, **style)
        ax.add_patch(rect)
        # top ellipse cap
        ell = mpatches.Ellipse((x, y + h/2 - 0.08), w, 0.22,
                               facecolor=style["facecolor"],
                               edgecolor=style["edgecolor"],
                               linewidth=style["linewidth"],
                               zorder=5)
        ax.add_patch(ell)
    else:
        shape = "round,pad=0.07" if kind in ("input", "output") else "square,pad=0.07"
        rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle=shape,
                              zorder=4, **style)
        ax.add_patch(rect)
    ax.text(x, y, label, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#222222", zorder=6)

for stage in data["stages"]:
    draw_node(ax, stage["id"], stage["label"], stage["kind"])

# ── Legend ────────────────────────────────────────────────────────────────────
legend_x, legend_y = 0.15, 1.05
ax.annotate("", xy=(legend_x + 0.45, legend_y),
            xytext=(legend_x, legend_y),
            arrowprops=dict(arrowstyle="-|>", color="#444444", lw=1.4, mutation_scale=12))
ax.text(legend_x + 0.52, legend_y, "data flow", va="center", fontsize=7, color="#444444")

ax.annotate("", xy=(legend_x + 0.45, legend_y - 0.3),
            xytext=(legend_x, legend_y - 0.3),
            arrowprops=dict(arrowstyle="-|>", color="#888888", lw=1.2,
                            linestyle="dashed", mutation_scale=12))
ax.text(legend_x + 0.52, legend_y - 0.3, "control / feedback", va="center",
        fontsize=7, color="#888888")

plt.tight_layout(pad=0.3)
plt.savefig("figure.pdf", dpi=300, bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
