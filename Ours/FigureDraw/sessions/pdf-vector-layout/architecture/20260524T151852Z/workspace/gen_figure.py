import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

with open("data.json") as f:
    data = json.load(f)

# Layout positions (x, y) for each node id
positions = {
    "input":  (0.5, 4.5),
    "retrieve": (0.5, 3.2),
    "db":     (1.8, 3.2),
    "diff":   (0.5, 1.9),
    "prior":  (1.8, 1.9),
    "output": (0.5, 0.6),
}

node_styles = {
    "input":     dict(boxstyle="round,pad=0.3", fc="#D6EAF8", ec="#2980B9", lw=1.5),
    "output":    dict(boxstyle="round,pad=0.3", fc="#D5F5E3", ec="#27AE60", lw=1.5),
    "module":    dict(boxstyle="round,pad=0.3", fc="#FDFEFE", ec="#5D6D7E", lw=1.5),
    "datastore": dict(boxstyle="round,pad=0.3", fc="#FEF9E7", ec="#F39C12", lw=1.5),
}

# Build id->stage map
stages = {s["id"]: s for s in data["stages"]}

fig, ax = plt.subplots(figsize=(5.5, 6.5))
ax.set_xlim(-0.3, 3.0)
ax.set_ylim(0.0, 5.4)
ax.axis("off")

# Draw group bounding boxes
group_bounds = {
    "Retrieval":  (-0.15, 2.65, 2.55, 1.1),   # x, y, w, h
    "Generation": (-0.15, 1.35, 2.55, 1.1),
}
group_colors = {
    "Retrieval":  "#EBF5FB",
    "Generation": "#F9EBEA",
}
group_edge = {
    "Retrieval":  "#2980B9",
    "Generation": "#C0392B",
}

for g in data["groups"]:
    lbl = g["label"]
    x, y, w, h = group_bounds[lbl]
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.08",
                          fc=group_colors[lbl], ec=group_edge[lbl],
                          lw=1.2, linestyle="--", zorder=0)
    ax.add_patch(rect)
    ax.text(x + w - 0.05, y + h - 0.05, lbl,
            ha="right", va="top", fontsize=7.5,
            color=group_edge[lbl], style="italic", zorder=1)

# Draw arrows first (behind nodes)
arrow_kw_solid = dict(arrowstyle="-|>", color="#2C3E50", lw=1.3,
                      connectionstyle="arc3,rad=0.0",
                      mutation_scale=12, zorder=1)
arrow_kw_dashed = dict(arrowstyle="-|>", color="#7F8C8D", lw=1.1,
                       linestyle="dashed",
                       connectionstyle="arc3,rad=0.0",
                       mutation_scale=10, zorder=1)

# prior -> diff is a feedback/control arrow (dashed)
feedback_pairs = {("prior", "diff")}

node_w, node_h = 0.72, 0.38

def node_edge(src_id, dst_id):
    sx, sy = positions[src_id]
    dx, dy = positions[dst_id]
    # exit bottom of src, enter top of dst (if dst is below)
    if dy < sy:
        return (sx, sy - node_h / 2), (dx, dy + node_h / 2)
    elif dy > sy:
        return (sx, sy + node_h / 2), (dx, dy - node_h / 2)
    else:
        # same row: exit right of src, enter left of dst
        return (sx + node_w / 2, sy), (dx - node_w / 2, dy)

for stage in data["stages"]:
    for src_id in stage.get("arrows", []):
        dst_id = stage["id"]
        start, end = node_edge(src_id, dst_id)
        is_feedback = (src_id, dst_id) in feedback_pairs or (dst_id, src_id) in feedback_pairs
        kw = dict(arrow_kw_dashed) if is_feedback else dict(arrow_kw_solid)
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle=kw.pop("arrowstyle"),
                                   color=kw.pop("color"),
                                   lw=kw.pop("lw"),
                                   connectionstyle=kw.pop("connectionstyle"),
                                   mutation_scale=kw.pop("mutation_scale"),
                                   **({} if not is_feedback else {"linestyle": "dashed"})),
                    zorder=2)

# prior -> diff feedback arrow (dashed, offset to right)
px, py = positions["prior"]
dx, dy = positions["diff"]
ax.annotate("", xy=(dx + node_w / 2 + 0.05, dy),
            xytext=(px + node_w / 2 + 0.05, py),
            arrowprops=dict(arrowstyle="-|>", color="#7F8C8D", lw=1.1,
                            connectionstyle="arc3,rad=-0.35",
                            mutation_scale=10, linestyle="dashed"),
            zorder=2)
ax.text(2.55, 2.9, "condition", fontsize=6, color="#7F8C8D", ha="center", va="center",
        rotation=90)

# Draw nodes
for stage in data["stages"]:
    sid = stage["id"]
    x, y = positions[sid]
    kind = stage["kind"]
    style = node_styles.get(kind, node_styles["module"])
    bbox = dict(boxstyle=style["boxstyle"], fc=style["fc"], ec=style["ec"], lw=style["lw"])
    ax.text(x, y, stage["label"], ha="center", va="center",
            fontsize=9, fontweight="bold" if kind in ("input", "output") else "normal",
            bbox=bbox, zorder=3)

# Title
ax.set_title(data["system_name"] + " Architecture", fontsize=11, fontweight="bold", pad=8)

# Legend
legend_elements = [
    mpatches.Patch(fc="#D6EAF8", ec="#2980B9", label="Input/Output"),
    mpatches.Patch(fc="#FDFEFE", ec="#5D6D7E", label="Module"),
    mpatches.Patch(fc="#FEF9E7", ec="#F39C12", label="Datastore"),
    plt.Line2D([0], [0], color="#2C3E50", lw=1.3, label="Data flow"),
    plt.Line2D([0], [0], color="#7F8C8D", lw=1.1, linestyle="--", label="Control/feedback"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=6.5,
          framealpha=0.85, edgecolor="#CCCCCC")

plt.tight_layout()
plt.savefig("figure.pdf", bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
