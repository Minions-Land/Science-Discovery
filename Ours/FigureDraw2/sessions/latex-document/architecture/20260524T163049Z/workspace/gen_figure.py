import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

with open("data.json") as f:
    data = json.load(f)

# ── Layout positions (x, y) in figure-coordinate space ──────────────────────
pos = {
    "input":   (0.50, 0.88),
    "retrieve": (0.30, 0.65),
    "db":       (0.30, 0.43),
    "diff":     (0.70, 0.65),
    "prior":    (0.70, 0.43),
    "output":   (0.50, 0.12),
}

BOX_W, BOX_H = 0.16, 0.09
ARROW_HEAD = dict(arrowstyle="-|>", color="#333333",
                  lw=1.6, mutation_scale=14)
DASH_ARROW = dict(arrowstyle="-|>", color="#888888",
                  lw=1.2, linestyle="dashed", mutation_scale=12)

colors = {
    "input":     "#DDEEFF",
    "output":    "#DDFFD5",
    "module":    "#FFF5CC",
    "datastore": "#F0E6FF",
}
edge_colors = {
    "input":     "#6699CC",
    "output":    "#44AA77",
    "module":    "#CC9900",
    "datastore": "#9966CC",
}

# Build id→kind lookup
kind = {s["id"]: s["kind"] for s in data["stages"]}
label = {s["id"]: s["label"] for s in data["stages"]}

fig, ax = plt.subplots(figsize=(7, 6.5))
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")
fig.patch.set_facecolor("white")

# ── Group shaded backgrounds ─────────────────────────────────────────────────
group_style = [
    {"fc": "#EEF5FF", "ec": "#88AACC"},
    {"fc": "#FFF8EE", "ec": "#CCAA66"},
]
for gi, grp in enumerate(data["groups"]):
    xs = [pos[n][0] for n in grp["node_ids"]]
    ys = [pos[n][1] for n in grp["node_ids"]]
    pad = 0.11
    rx = min(xs) - pad;  ry = min(ys) - pad * 0.7
    rw = max(xs) - min(xs) + 2 * pad
    rh = max(ys) - min(ys) + BOX_H + 2 * pad * 0.7
    rect = FancyBboxPatch((rx, ry), rw, rh,
                          boxstyle="round,pad=0.02",
                          fc=group_style[gi]["fc"],
                          ec=group_style[gi]["ec"],
                          lw=1.5, linestyle="--",
                          zorder=1, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(rx + rw / 2, ry + rh + 0.01, grp["label"],
            ha="center", va="bottom", fontsize=9,
            color=group_style[gi]["ec"], fontweight="bold",
            transform=ax.transAxes)

# ── Boxes ────────────────────────────────────────────────────────────────────
for sid, (cx, cy) in pos.items():
    k = kind[sid]
    bx, by = cx - BOX_W / 2, cy - BOX_H / 2
    if k == "datastore":
        # Cylinder-ish: use ellipse top + rectangle body
        rect = FancyBboxPatch((bx, by), BOX_W, BOX_H,
                              boxstyle="round,pad=0.012",
                              fc=colors[k], ec=edge_colors[k],
                              lw=1.8, zorder=3, transform=ax.transAxes)
    else:
        rect = FancyBboxPatch((bx, by), BOX_W, BOX_H,
                              boxstyle="round,pad=0.012",
                              fc=colors[k], ec=edge_colors[k],
                              lw=1.8, zorder=3, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(cx, cy, label[sid], ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#222222",
            transform=ax.transAxes, zorder=4)

# ── Arrows ───────────────────────────────────────────────────────────────────
# arrows field: src→ dst (data flows FROM src TO dst)
# For datastore (KB), the arrow is a feedback/query → use dashed style
for stage in data["stages"]:
    dst = stage["id"]
    for src in stage.get("arrows", []):
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        # Offset start/end to box edge
        dx, dy = x1 - x0, y1 - y0
        norm = (dx**2 + dy**2) ** 0.5
        ux, uy = dx / norm, dy / norm
        sx = x0 + ux * BOX_W / 2 * 1.1
        sy = y0 + uy * BOX_H / 2 * 1.1
        ex = x1 - ux * BOX_W / 2 * 1.2
        ey = y1 - uy * BOX_H / 2 * 1.2
        # KB (db) uses dashed arrow (retrieval query/feedback)
        style = DASH_ARROW if kind[dst] == "datastore" else ARROW_HEAD
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(**style, zorder=2),
                    xycoords="axes fraction", textcoords="axes fraction")

# ── Legend ───────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(fc=colors["input"],     ec=edge_colors["input"],     label="Input/Output"),
    mpatches.Patch(fc=colors["module"],    ec=edge_colors["module"],    label="Module"),
    mpatches.Patch(fc=colors["datastore"], ec=edge_colors["datastore"], label="Data Store"),
]
ax.legend(handles=legend_items, loc="lower right",
          fontsize=8, framealpha=0.85, edgecolor="#cccccc")

# ── Title ────────────────────────────────────────────────────────────────────
ax.set_title(data["system_name"] + " Architecture", fontsize=13,
             fontweight="bold", color="#111111", pad=8)

plt.tight_layout()
plt.savefig("figure.pdf", bbox_inches="tight", dpi=150)
plt.savefig("figure.png", bbox_inches="tight", dpi=150)
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
