"""
gen_figure.py — Network graph with community coloring
Data: data.json (30 nodes, 4 communities, ~68 edges)
Layout: spring_layout, seed=42, k=0.4, iterations=100
"""

import json
import pathlib
import subprocess
import sys
import re

import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

PINNED_SEED = 42

# ColorBrewer Set2 — 4 communities
COMMUNITY_COLORS = {
    0: "#66C2A5",
    1: "#FC8D62",
    2: "#8DA0CB",
    3: "#E78AC3",
}

CWD = pathlib.Path(__file__).parent

# Load data
with open(CWD / "data.json") as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

n_nodes = G.number_of_nodes()
n_edges = G.number_of_edges()
n_communities = data["communities"]

# Degree-conditional node size (network-graph-tuning skill)
degrees = [G.degree(n) for n in G.nodes()]
deg_min = max(min(degrees), 1)
deg_max = max(degrees)
ratio = deg_max / deg_min

if ratio > 3:
    node_size_map = {n: 60 + 12 * G.degree(n) for n in G.nodes()}
    size_mode = f"proportional to degree (max/min ratio = {ratio:.1f})"
else:
    node_size_map = {n: 120 for n in G.nodes()}
    size_mode = f"constant (degrees flat: max/min ratio = {ratio:.1f})"

node_sizes = [node_size_map[n] for n in G.nodes()]
node_colors = [COMMUNITY_COLORS[G.nodes[n]["community"]] for n in G.nodes()]

# Layout
pos = nx.spring_layout(G, seed=PINNED_SEED, k=0.4, iterations=100)

# Edge alpha: 68 edges > 50, so use 0.30
edge_alpha = 0.30 if n_edges >= 50 else 0.50

# Draw
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.axis("off")

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=edge_alpha,
    width=0.6,
    edge_color="#555555",
)
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_size=node_sizes,
    node_color=node_colors,
    linewidths=0.5,
    edgecolors="#333333",
)

# Legend
legend_handles = [
    mpatches.Patch(facecolor=COMMUNITY_COLORS[c], edgecolor="#333333",
                   linewidth=0.5, label=f"Community {c}")
    for c in range(n_communities)
]
ax.legend(
    handles=legend_handles,
    loc="lower right",
    fontsize=8,
    handlelength=1.0,
    handleheight=0.9,
    borderpad=0.5,
)

fig.tight_layout(pad=0.3)

# Save
pdf_path = CWD / "figure.pdf"
png_path = CWD / "figure.png"
svg_path = CWD / "figure.svg"

fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {pdf_path}, {png_path}, {svg_path}")
print(f"Nodes: {n_nodes}, Edges: {n_edges}, Communities: {n_communities}")
print(f"Node size mode: {size_mode}")

# Post-save font verification
raw = pdf_path.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)
print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")
