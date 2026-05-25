import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

with open("data.json") as f:
    data = json.load(f)

# ── layout positions (x, y) ──────────────────────────────────────────────────
pos = {
    "input":  (0.5, 3.0),
    "retrieve": (2.8, 3.0),
    "db":       (2.8, 1.2),
    "diff":     (5.5, 3.0),
    "prior":    (5.5, 1.2),
    "output":   (8.0, 3.0),
}

# node display properties
NODE_W, NODE_H = 1.3, 0.55
DATASTORE_W, DATASTORE_H = 1.1, 0.55

kind_style = {
    "input":     dict(fc="#D6EAF8", ec="#2980B9", lw=1.5),
    "output":    dict(fc="#D5F5E3", ec="#27AE60", lw=1.5),
    "module":    dict(fc="#FDFEFE", ec="#5D6D7E", lw=1.5),
    "datastore": dict(fc="#FEF9E7", ec="#D4AC0D", lw=1.5),
}

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(-0.3, 9.5)
ax.set_ylim(0.0, 4.2)
ax.set_aspect("equal")
ax.axis("off")

# ── group backgrounds ─────────────────────────────────────────────────────────
groups = {g["label"]: g["node_ids"] for g in data["groups"]}
group_style = {
    "Retrieval":  dict(fc="#EBF5FB", ec="#2980B9", lw=1.2, ls="--"),
    "Generation": dict(fc="#F9EBEA", ec="#C0392B", lw=1.2, ls="--"),
}
PAD = 0.55
for glabel, nids in groups.items():
    xs = [pos[n][0] for n in nids]
    ys = [pos[n][1] for n in nids]
    x0, y0 = min(xs) - NODE_W/2 - PAD, min(ys) - NODE_H/2 - PAD
    x1, y1 = max(xs) + NODE_W/2 + PAD, max(ys) + NODE_H/2 + PAD
    st = group_style[glabel]
    rect = FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle="round,pad=0.05",
        fc=st["fc"], ec=st["ec"], lw=st["lw"], ls=st["ls"],
        zorder=1,
    )
    ax.add_patch(rect)
    ax.text(
        (x0 + x1) / 2, y1 - 0.12, glabel,
        ha="center", va="top", fontsize=8.5,
        color=st["ec"], fontweight="bold", zorder=3,
    )

# ── helper: draw node ─────────────────────────────────────────────────────────
def draw_node(ax, nid, label, kind):
    x, y = pos[nid]
    st = kind_style[kind]
    if kind == "datastore":
        # cylinder-ish: rounded rect with extra top arc suggestion
        w, h = DATASTORE_W, DATASTORE_H
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.08",
            fc=st["fc"], ec=st["ec"], lw=st["lw"], zorder=4,
        )
        ax.add_patch(box)
        # top ellipse to suggest cylinder
        ell = mpatches.Ellipse(
            (x, y + h/2), w * 0.9, h * 0.28,
            fc=st["fc"], ec=st["ec"], lw=st["lw"], zorder=5,
        )
        ax.add_patch(ell)
    else:
        w, h = NODE_W, NODE_H
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.08",
            fc=st["fc"], ec=st["ec"], lw=st["lw"], zorder=4,
        )
        ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center",
            fontsize=8.5, fontweight="bold", zorder=6)

# ── draw nodes ────────────────────────────────────────────────────────────────
stage_map = {s["id"]: s for s in data["stages"]}
for s in data["stages"]:
    draw_node(ax, s["id"], s["label"], s["kind"])

# ── arrow routing ─────────────────────────────────────────────────────────────
# Determine which arrows are "feedback" (target y < source y) → dashed
def get_edge_points(src, tgt):
    sx, sy = pos[src]
    tx, ty = pos[tgt]
    sk = stage_map[src]["kind"]
    tk = stage_map[tgt]["kind"]
    sw = DATASTORE_W if sk == "datastore" else NODE_W
    sh = DATASTORE_H if sk == "datastore" else NODE_H
    tw = DATASTORE_W if tk == "datastore" else NODE_W
    th = DATASTORE_H if tk == "datastore" else NODE_H

    dx, dy = tx - sx, ty - sy
    if abs(dx) >= abs(dy):
        # horizontal dominant
        x0 = sx + np.sign(dx) * sw / 2
        y0 = sy
        x1 = tx - np.sign(dx) * tw / 2
        y1 = ty
    else:
        # vertical dominant
        x0 = sx
        y0 = sy + np.sign(dy) * sh / 2
        x1 = tx
        y1 = ty - np.sign(dy) * th / 2
    return (x0, y0), (x1, y1)

ARROW_KW = dict(
    arrowstyle="-|>",
    mutation_scale=14,
    zorder=7,
)

for s in data["stages"]:
    tgt = s["id"]
    for src in s.get("arrows", []):
        (x0, y0), (x1, y1) = get_edge_points(src, tgt)
        sy, ty = pos[src][1], pos[tgt][1]
        # prior ← diff: treat as control/feedback → dashed
        is_feedback = (tgt == "prior" and src == "diff")
        color = "#7F8C8D" if is_feedback else "#2C3E50"
        ls = "dashed" if is_feedback else "solid"
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                **ARROW_KW,
                color=color,
                linestyle=ls,
                connectionstyle="arc3,rad=0.0",
            ),
        )

# ── legend ────────────────────────────────────────────────────────────────────
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color="#2C3E50", lw=1.5, label="Data flow"),
    Line2D([0], [0], color="#7F8C8D", lw=1.5, ls="--", label="Control / feedback"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8,
          framealpha=0.85, edgecolor="#AAAAAA")

# ── title ─────────────────────────────────────────────────────────────────────
ax.set_title(data["system_name"] + " — Architecture", fontsize=12,
             fontweight="bold", pad=6)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
