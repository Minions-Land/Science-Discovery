import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

with open("data.json") as f:
    data = json.load(f)

# Layout positions (x, y) for each node — left to right pipeline
positions = {
    "input":  (0.5, 5.0),
    "retrieve": (2.5, 5.0),
    "db":     (2.5, 3.2),
    "diff":   (5.0, 5.0),
    "prior":  (5.0, 3.2),
    "output": (7.5, 5.0),
}

node_w, node_h = 1.3, 0.7

KIND_STYLE = {
    "input":     dict(facecolor="#d0e8ff", edgecolor="#2266aa", linewidth=1.5),
    "output":    dict(facecolor="#d4f5d4", edgecolor="#227722", linewidth=1.5),
    "module":    dict(facecolor="#fff3cc", edgecolor="#aa7700", linewidth=1.5),
    "datastore": dict(facecolor="#f0e0ff", edgecolor="#7733aa", linewidth=1.5),
}

GROUP_STYLE = dict(facecolor="#fffbe6", edgecolor="#ccaa00", linewidth=1.2, linestyle="--", alpha=0.4)

# Arrows defined in data: arrows list = [source_id, ...] for each stage
# Build edge list from data
edges = []
for stage in data["stages"]:
    for src in stage.get("arrows", []):
        edges.append((src, stage["id"]))

# Additional control/feedback arrow: prior -> diff (feedback)
feedback_edges = [("prior", "diff")]

# Lookup
stage_map = {s["id"]: s for s in data["stages"]}

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(-0.5, 9.0)
ax.set_ylim(1.8, 6.5)
ax.set_aspect("equal")
ax.axis("off")

# Draw group bounding boxes first (behind nodes)
group_padding = 0.5
for group in data["groups"]:
    ids = group["node_ids"]
    xs = [positions[i][0] for i in ids]
    ys = [positions[i][1] for i in ids]
    gx = min(xs) - node_w / 2 - group_padding
    gy = min(ys) - node_h / 2 - group_padding
    gw = max(xs) - min(xs) + node_w + 2 * group_padding
    gh = max(ys) - min(ys) + node_h + 2 * group_padding
    rect = FancyBboxPatch(
        (gx, gy), gw, gh,
        boxstyle="round,pad=0.15",
        **GROUP_STYLE,
        zorder=0,
    )
    ax.add_patch(rect)
    ax.text(
        gx + gw / 2, gy + gh + 0.05,
        group["label"],
        ha="center", va="bottom",
        fontsize=9, fontstyle="italic", color="#886600",
    )

# Draw solid data-flow arrows
def node_edge_point(node_id, direction):
    x, y = positions[node_id]
    if direction == "right":
        return x + node_w / 2, y
    if direction == "left":
        return x - node_w / 2, y
    if direction == "bottom":
        return x, y - node_h / 2
    if direction == "top":
        return x, y + node_h / 2

arrow_kw_solid = dict(
    arrowstyle="-|>", color="#333333", lw=1.4,
    mutation_scale=14,
    connectionstyle="arc3,rad=0",
    zorder=1,
)
arrow_kw_dashed = dict(
    arrowstyle="-|>", color="#886600", lw=1.2,
    linestyle="dashed", mutation_scale=12,
    connectionstyle="arc3,rad=-0.3",
    zorder=1,
)

for (src, dst) in edges:
    sx, sy = positions[src]
    dx, dy = positions[dst]
    # Determine exit/entry sides
    if abs(sy - dy) < 0.05:  # same row → horizontal
        x0, y0 = sx + node_w / 2, sy
        x1, y1 = dx - node_w / 2, dy
    else:  # vertical (retrieve -> db, diff -> prior)
        x0, y0 = sx, sy - node_h / 2
        x1, y1 = dx, dy + node_h / 2
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        **arrow_kw_solid,
    )
    ax.add_patch(arrow)

# Feedback arrows (dashed)
for (src, dst) in feedback_edges:
    sx, sy = positions[src]
    dx, dy = positions[dst]
    x0, y0 = sx - node_w / 2, sy
    x1, y1 = dx + node_w / 2, dy
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        **arrow_kw_dashed,
    )
    ax.add_patch(arrow)

# Draw nodes
for stage in data["stages"]:
    sid = stage["id"]
    x, y = positions[sid]
    kind = stage["kind"]
    style = KIND_STYLE[kind]
    if kind == "datastore":
        # cylinder shape approximated by ellipse + rectangle
        rect = FancyBboxPatch(
            (x - node_w / 2, y - node_h / 2 + 0.1),
            node_w, node_h - 0.2,
            boxstyle="round,pad=0.05",
            zorder=2,
            **style,
        )
        ax.add_patch(rect)
        ellipse_top = mpatches.Ellipse((x, y + node_h / 2 - 0.1), node_w, 0.25,
                                        zorder=3, **style)
        ellipse_bot = mpatches.Ellipse((x, y - node_h / 2 + 0.1), node_w, 0.25,
                                        zorder=3, facecolor=style["facecolor"],
                                        edgecolor=style["edgecolor"], linewidth=1.5)
        ax.add_patch(ellipse_bot)
        ax.add_patch(ellipse_top)
    else:
        box = FancyBboxPatch(
            (x - node_w / 2, y - node_h / 2),
            node_w, node_h,
            boxstyle="round,pad=0.1",
            zorder=2,
            **style,
        )
        ax.add_patch(box)
    ax.text(x, y, stage["label"], ha="center", va="center",
            fontsize=9.5, fontweight="bold", zorder=4)

# Legend
legend_elements = [
    mpatches.Patch(facecolor="#d0e8ff", edgecolor="#2266aa", label="Input/Output"),
    mpatches.Patch(facecolor="#fff3cc", edgecolor="#aa7700", label="Module"),
    mpatches.Patch(facecolor="#f0e0ff", edgecolor="#7733aa", label="Datastore (KB)"),
    mpatches.Patch(facecolor="#fffbe6", edgecolor="#ccaa00", linestyle="--", label="Stage Group"),
    plt.Line2D([0], [0], color="#333333", lw=1.4, label="Data flow"),
    plt.Line2D([0], [0], color="#886600", lw=1.2, linestyle="dashed", label="Control/feedback"),
]
ax.legend(handles=legend_elements, loc="lower left", fontsize=7.5,
          framealpha=0.8, ncol=2, handlelength=1.5)

ax.set_title("RetroDiff — System Architecture", fontsize=13, fontweight="bold", pad=10)

plt.tight_layout()
plt.savefig("figure.pdf", bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
