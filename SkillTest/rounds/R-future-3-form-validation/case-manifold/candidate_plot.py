from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures/figures-novel-form/manifold/data/manifold-cells.csv"
OUT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "Arial",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 7,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.55,
})

df = pd.read_csv(DATA).sort_values("pseudotime")
cmap = LinearSegmentedColormap.from_list(
    "cyan_trajectory",
    ["#d8f2f0", "#95d6d3", "#41bfb9", "#138f95", "#0d5f6c"],
)

fig, ax = plt.subplots(figsize=(5.9, 3.75))

ax.scatter(
    df["x"],
    df["y"],
    c=df["pseudotime"],
    cmap=cmap,
    s=10,
    alpha=0.74,
    linewidths=0,
    zorder=2,
)

paths = {
    "early trajectory": ["progenitor", "intermediate"],
    "terminal A branch": ["intermediate", "terminal_A"],
    "terminal B branch": ["intermediate", "terminal_B"],
}

branch_segments = []
branch_values = []
for labels in paths.values():
    pts = []
    vals = []
    for label in labels:
        sub = df[df["cluster"] == label].sort_values("pseudotime")
        grouped = sub.groupby(pd.qcut(sub["pseudotime"], 18, duplicates="drop"), observed=True)
        centers = grouped[["x", "y", "pseudotime"]].median().dropna()
        pts.extend(centers[["x", "y"]].to_numpy())
        vals.extend(centers["pseudotime"].to_numpy())
    pts = np.asarray(pts)
    vals = np.asarray(vals)
    order = np.argsort(vals)
    pts = pts[order]
    vals = vals[order]
    branch_segments.extend(np.stack([pts[:-1], pts[1:]], axis=1))
    branch_values.extend((vals[:-1] + vals[1:]) / 2)

lc = LineCollection(
    branch_segments,
    cmap=cmap,
    norm=plt.Normalize(df["pseudotime"].min(), df["pseudotime"].max()),
    linewidths=2.6,
    alpha=0.95,
    zorder=4,
    capstyle="round",
)
lc.set_array(np.asarray(branch_values))
ax.add_collection(lc)

centers = df.groupby("cluster")[["x", "y", "pseudotime"]].median()
bif = centers.loc["intermediate"]
ax.scatter([bif["x"]], [bif["y"]], s=58, color="#0d5f6c", edgecolor="white", linewidth=0.8, zorder=5)
ax.annotate(
    "bifurcation",
    xy=(bif["x"], bif["y"]),
    xytext=(bif["x"] - 1.0, bif["y"] + 0.85),
    arrowprops=dict(arrowstyle="-", lw=0.8, color="#5b7375"),
    color="#3c5557",
    fontsize=7,
)

for label, dx, dy in [
    ("progenitor", -0.95, -0.45),
    ("terminal A", 0.15, 0.58),
    ("terminal B", 0.18, -0.62),
]:
    key = label.replace(" ", "_")
    c = centers.loc[key if key in centers.index else "progenitor"]
    ax.text(c["x"] + dx, c["y"] + dy, label, color="#385a5c", fontsize=7, weight="bold")

ax.text(
    0.03,
    0.05,
    "pseudotime flow",
    transform=ax.transAxes,
    color="#5f7476",
    fontsize=7,
)

ax.set_xlabel("Manifold coordinate 1")
ax.set_ylabel("Manifold coordinate 2")
ax.set_xticks(np.linspace(np.floor(df["x"].min()), np.ceil(df["x"].max()), 3))
ax.set_yticks(np.linspace(np.floor(df["y"].min()), np.ceil(df["y"].max()), 3))
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=2.2, width=0.55, colors="#6a6a6a")
ax.set_aspect("equal", adjustable="box")

sm = mpl.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(df["pseudotime"].min(), df["pseudotime"].max()))
cbar = fig.colorbar(sm, ax=ax, shrink=0.58, pad=0.02, aspect=16)
cbar.set_label("pseudotime", color="#5f7476")
cbar.outline.set_visible(False)
cbar.ax.tick_params(length=2, width=0.5, colors="#6a6a6a")

fig.tight_layout(pad=0.35)
for ext in ("svg", "pdf", "png"):
    kwargs = {"dpi": 300} if ext == "png" else {}
    fig.savefig(OUT / f"candidate.{ext}", bbox_inches="tight", **kwargs)
