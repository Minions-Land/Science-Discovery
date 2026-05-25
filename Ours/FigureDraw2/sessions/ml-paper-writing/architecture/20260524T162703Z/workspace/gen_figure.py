import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Load data
with open("data.json") as f:
    data = json.load(f)

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")

# Node positions (x_center, y_center)
positions = {
    "input":  (1.0, 2.5),
    "retrieve": (3.0, 3.2),
    "db":       (3.0, 1.8),
    "diff":     (6.0, 3.2),
    "prior":    (6.0, 1.8),
    "output":   (9.0, 2.5),
}

node_w, node_h = 1.4, 0.7

# Node styles
kind_style = {
    "input":     dict(boxstyle="round,pad=0.15", facecolor="#D6EAF8", edgecolor="#2980B9", lw=1.8),
    "output":    dict(boxstyle="round,pad=0.15", facecolor="#D5F5E3", edgecolor="#27AE60", lw=1.8),
    "module":    dict(boxstyle="round,pad=0.15", facecolor="#FDFEFE", edgecolor="#5D6D7E", lw=1.5),
    "datastore": dict(boxstyle="round,pad=0.15", facecolor="#FEF9E7", edgecolor="#F39C12", lw=1.5),
}

# Group bounding boxes
group_colors = {
    "Retrieval":  ("#EBF5FB", "#2980B9"),
    "Generation": ("#EAFAF1", "#27AE60"),
}

groups = {g["label"]: g["node_ids"] for g in data["groups"]}

def group_bbox(node_ids, pad=0.35):
    xs = [positions[n][0] for n in node_ids]
    ys = [positions[n][1] for n in node_ids]
    x0 = min(xs) - node_w / 2 - pad
    y0 = min(ys) - node_h / 2 - pad
    x1 = max(xs) + node_w / 2 + pad
    y1 = max(ys) + node_h / 2 + pad
    return x0, y0, x1 - x0, y1 - y0

for label, node_ids in groups.items():
    fc, ec = group_colors[label]
    x, y, w, h = group_bbox(node_ids)
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.1",
                          facecolor=fc, edgecolor=ec,
                          lw=1.2, linestyle="--", zorder=0)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h + 0.05, label,
            ha="center", va="bottom", fontsize=9,
            color=ec, fontweight="bold")

# Build id->label map
id_label = {s["id"]: s["label"] for s in data["stages"]}
id_kind  = {s["id"]: s["kind"]  for s in data["stages"]}

# Draw arrows first (behind boxes)
arrow_kw_solid = dict(arrowstyle="-|>", color="#444444", lw=1.4,
                      connectionstyle="arc3,rad=0.0",
                      mutation_scale=14, zorder=1)
arrow_kw_dashed = dict(arrowstyle="-|>", color="#888888", lw=1.2,
                       linestyle="dashed",
                       connectionstyle="arc3,rad=0.15",
                       mutation_scale=12, zorder=1)

# prior -> diff is a feedback/control arrow (dashed)
feedback_pairs = {("prior", "diff")}

for stage in data["stages"]:
    dst = stage["id"]
    for src in stage.get("arrows", []):
        x0, y0 = positions[src]
        x1, y1 = positions[dst]
        # offset start/end to box edges
        dx = x1 - x0
        dy = y1 - y0
        dist = (dx**2 + dy**2) ** 0.5
        ux, uy = dx / dist, dy / dist
        sx = x0 + ux * node_w / 2
        sy = y0 + uy * node_h / 2
        ex = x1 - ux * node_w / 2
        ey = y1 - uy * node_h / 2

        if (src, dst) in feedback_pairs:
            kw = arrow_kw_dashed
        else:
            kw = arrow_kw_solid

        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=kw, zorder=1)

# Draw nodes
for stage in data["stages"]:
    nid = stage["id"]
    label = stage["label"]
    kind = stage["kind"]
    cx, cy = positions[nid]
    style = kind_style[kind]
    box = FancyBboxPatch((cx - node_w / 2, cy - node_h / 2),
                         node_w, node_h, zorder=2, **style)
    ax.add_patch(box)
    ax.text(cx, cy, label, ha="center", va="center",
            fontsize=9, fontweight="bold", zorder=3)

# Legend
legend_elements = [
    mpatches.Patch(facecolor="#D6EAF8", edgecolor="#2980B9", label="Input/Output"),
    mpatches.Patch(facecolor="#FDFEFE", edgecolor="#5D6D7E", label="Module"),
    mpatches.Patch(facecolor="#FEF9E7", edgecolor="#F39C12", label="Datastore"),
    plt.Line2D([0], [0], color="#444444", lw=1.4, label="Data flow"),
    plt.Line2D([0], [0], color="#888888", lw=1.2, linestyle="dashed", label="Control/feedback"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=7.5,
          framealpha=0.85, edgecolor="#cccccc")

ax.set_title("RetroDiff — System Architecture", fontsize=12, fontweight="bold", pad=8)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
