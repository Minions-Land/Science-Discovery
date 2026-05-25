import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

with open("data.json") as f:
    data = json.load(f)

# ── layout positions (x, y) in figure coords ─────────────────────────────────
pos = {
    "input":   (0.12, 0.50),
    "retrieve":(0.38, 0.65),
    "db":      (0.38, 0.35),
    "diff":    (0.65, 0.65),
    "prior":   (0.65, 0.35),
    "output":  (0.88, 0.50),
}

# box sizes (half-width, half-height)
BOX_HW, BOX_HH = 0.10, 0.07

# ── group bounding boxes ──────────────────────────────────────────────────────
groups = {
    "Retrieval":  {"node_ids": ["retrieve", "db"],   "color": "#D6EAF8", "edge": "#2E86C1"},
    "Generation": {"node_ids": ["diff", "prior"],    "color": "#D5F5E3", "edge": "#1E8449"},
}

# node styles by kind
KIND_STYLE = {
    "input":     {"fc": "#F0F0F0", "ec": "#555555", "style": "round,pad=0.05"},
    "output":    {"fc": "#FFF3CD", "ec": "#D4A017", "style": "round,pad=0.05"},
    "module":    {"fc": "#FDFEFE", "ec": "#2C3E50", "style": "round,pad=0.05"},
    "datastore": {"fc": "#EBF5FB", "ec": "#1A5276", "style": "round,pad=0.05"},
}

# ── figure setup ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
fig.patch.set_facecolor("white")

# ── draw group boxes ──────────────────────────────────────────────────────────
PAD = 0.06
for grp_label, grp in groups.items():
    xs = [pos[n][0] for n in grp["node_ids"]]
    ys = [pos[n][1] for n in grp["node_ids"]]
    x0 = min(xs) - BOX_HW - PAD
    x1 = max(xs) + BOX_HW + PAD
    y0 = min(ys) - BOX_HH - PAD
    y1 = max(ys) + BOX_HH + PAD
    rect = FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0.02",
        facecolor=grp["color"], edgecolor=grp["edge"],
        linewidth=1.5, linestyle="--",
        transform=ax.transAxes, zorder=1,
    )
    ax.add_patch(rect)
    ax.text(
        (x0 + x1) / 2, y1 - 0.01,
        grp_label,
        ha="center", va="top",
        fontsize=9, color=grp["edge"], fontweight="bold",
        transform=ax.transAxes, zorder=5,
    )

# ── build arrow map from data.json ───────────────────────────────────────────
# arrows list means: node.id is TARGET; each element of arrows is SOURCE id
arrow_map = []
for stage in data["stages"]:
    for src in stage.get("arrows", []):
        arrow_map.append((src, stage["id"]))

# extra feedback arrow: prior -> diff (control / feedback, dashed)
feedback_arrows = [("prior", "diff")]

def node_edge_point(src, dst, half_w=BOX_HW, half_h=BOX_HH):
    """Return exit point on box edge toward dst."""
    sx, sy = pos[src]
    dx, dy = pos[dst]
    ddx, ddy = dx - sx, dy - sy
    if abs(ddx) == 0 and abs(ddy) == 0:
        return sx, sy
    # clip to box boundary
    if abs(ddx) > 0:
        t_x = half_w / abs(ddx)
    else:
        t_x = float("inf")
    if abs(ddy) > 0:
        t_y = half_h / abs(ddy)
    else:
        t_y = float("inf")
    t = min(t_x, t_y)
    return sx + ddx * t, sy + ddy * t

# ── draw solid data-flow arrows ───────────────────────────────────────────────
for src, dst in arrow_map:
    sx, sy = node_edge_point(src, dst)
    ex, ey = node_edge_point(dst, src)
    ax.annotate(
        "", xy=(ex, ey), xytext=(sx, sy),
        xycoords="axes fraction", textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="-|>", color="#2C3E50",
            lw=1.6, mutation_scale=14,
            connectionstyle="arc3,rad=0.0",
        ),
        zorder=3,
    )

# ── draw dashed feedback arrows ───────────────────────────────────────────────
for src, dst in feedback_arrows:
    sx, sy = node_edge_point(src, dst, half_w=BOX_HW, half_h=BOX_HH)
    ex, ey = node_edge_point(dst, src, half_w=BOX_HW, half_h=BOX_HH)
    ax.annotate(
        "", xy=(ex, ey), xytext=(sx, sy),
        xycoords="axes fraction", textcoords="axes fraction",
        arrowprops=dict(
            arrowstyle="-|>", color="#7F8C8D",
            lw=1.3, linestyle="dashed", mutation_scale=12,
            connectionstyle="arc3,rad=-0.35",
        ),
        zorder=3,
    )

# ── draw node boxes ───────────────────────────────────────────────────────────
for stage in data["stages"]:
    nid = stage["id"]
    x, y = pos[nid]
    kind = stage.get("kind", "module")
    sty = KIND_STYLE.get(kind, KIND_STYLE["module"])

    if kind == "datastore":
        # cylinder-like: ellipse top cap + rectangle body
        body = FancyBboxPatch(
            (x - BOX_HW, y - BOX_HH), 2 * BOX_HW, 2 * BOX_HH,
            boxstyle=sty["style"],
            facecolor=sty["fc"], edgecolor=sty["ec"],
            linewidth=1.8, transform=ax.transAxes, zorder=4,
        )
        ax.add_patch(body)
        ellipse = mpatches.Ellipse(
            (x, y + BOX_HH), 2 * BOX_HW, 0.03,
            facecolor=sty["ec"], edgecolor=sty["ec"],
            linewidth=0, alpha=0.25, transform=ax.transAxes, zorder=4,
        )
        ax.add_patch(ellipse)
    else:
        box = FancyBboxPatch(
            (x - BOX_HW, y - BOX_HH), 2 * BOX_HW, 2 * BOX_HH,
            boxstyle=sty["style"],
            facecolor=sty["fc"], edgecolor=sty["ec"],
            linewidth=1.8, transform=ax.transAxes, zorder=4,
        )
        ax.add_patch(box)

    ax.text(
        x, y, stage["label"],
        ha="center", va="center",
        fontsize=10, fontweight="semibold",
        color="#1A1A1A",
        transform=ax.transAxes, zorder=5,
        wrap=True,
    )

# ── legend ────────────────────────────────────────────────────────────────────
legend_handles = [
    mpatches.Patch(facecolor="#FDFEFE", edgecolor="#2C3E50", label="Module"),
    mpatches.Patch(facecolor="#EBF5FB", edgecolor="#1A5276", label="Datastore"),
    mpatches.Patch(facecolor="#F0F0F0", edgecolor="#555555", label="Input / Output"),
    plt.Line2D([0], [0], color="#2C3E50", lw=1.6, label="Data flow"),
    plt.Line2D([0], [0], color="#7F8C8D", lw=1.3, linestyle="dashed", label="Control / Feedback"),
]
ax.legend(
    handles=legend_handles,
    loc="lower center",
    ncol=5,
    fontsize=7.5,
    framealpha=0.85,
    bbox_to_anchor=(0.5, -0.04),
)

# ── title ─────────────────────────────────────────────────────────────────────
ax.set_title(
    f"{data['system_name']} — System Architecture",
    fontsize=13, fontweight="bold", pad=10,
)

plt.tight_layout(rect=[0, 0.05, 1, 1])

fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=200)
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved: figure.pdf, figure.png, figure.svg")
