"""
gen_figure.py — Network community figure
Data source: data.json (30 nodes, 4 communities)
"""

import json
import pathlib
import subprocess
import sys

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

# ── Load data ──────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

n_communities = data["communities"]  # 4
community_map = {node["id"]: node["community"] for node in data["nodes"]}

# Build community list for modularity (list of sets)
communities_list = [
    {n for n, d in G.nodes(data=True) if d["community"] == c}
    for c in range(n_communities)
]

# ── Degree-conditional node size (network-graph-tuning skill) ─────────────────
degrees = [G.degree(n) for n in G.nodes()]
deg_min = max(min(degrees), 1)
deg_max = max(degrees)
ratio = deg_max / deg_min

if ratio > 3:
    node_sizes = [60 + 12 * G.degree(n) for n in G.nodes()]
    size_mode = f"proportional to degree (max/min ratio = {ratio:.1f})"
else:
    node_sizes = [120] * len(G.nodes())
    size_mode = f"constant (degrees flat: max/min ratio = {ratio:.1f})"

# ── Layout ────────────────────────────────────────────────────────────────────
pos = nx.spring_layout(G, seed=PINNED_SEED, k=0.4, iterations=100)

# ── Colors — ColorBrewer Set2 (4 communities) ─────────────────────────────────
set2_4 = ["#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3"]
node_colors = [set2_4[community_map[n]] for n in G.nodes()]

# ── Modularity and intra-community edge stats ─────────────────────────────────
modularity_q = nx.algorithms.community.modularity(G, communities_list)

intra_edges = sum(
    1 for u, v in G.edges()
    if community_map[u] == community_map[v]
)
total_edges = G.number_of_edges()
intra_frac = intra_edges / total_edges

# ── Draw ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_axis_off()

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.30,          # edge_alpha = 0.30 for |edges| > 50
    width=0.6,
    edge_color="#888888",
)
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=node_sizes,
    linewidths=0.4,
    edgecolors="#444444",
)

# ── Legend ────────────────────────────────────────────────────────────────────
community_labels = [f"Community {c}" for c in range(n_communities)]
handles = [
    mpatches.Patch(facecolor=set2_4[c], edgecolor="#444444",
                   linewidth=0.4, label=community_labels[c])
    for c in range(n_communities)
]
ax.legend(
    handles=handles,
    loc="lower left",
    fontsize=8,
    handlelength=1.0,
    handleheight=0.8,
    borderpad=0.5,
)

plt.tight_layout(pad=0.3)

# ── Save ──────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {pdf_path}, {png_path}, {svg_path}")
print(f"Nodes: {G.number_of_nodes()}, Edges: {total_edges}")
print(f"Modularity Q = {modularity_q:.3f}")
print(f"Intra-community edges: {intra_edges}/{total_edges} = {intra_frac:.1%}")
print(f"Node size mode: {size_mode}")

# ── Font type verification (academic-plotting skill) ──────────────────────────
out = subprocess.run(
    ["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False
)
if out.returncode == 0:
    if "Type 3" in out.stdout:
        sys.stderr.write(
            f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n"
        )
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    # pdffonts not available — fallback raw-bytes check
    import re
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (fallback byte-scan, no /Type3 found)")

# ── Write caption.tex ─────────────────────────────────────────────────────────
# Determine community structure interpretation
if modularity_q > 0.3:
    q_interp = (
        f"Within-community edges account for \\textbf{{{intra_frac:.0%}}} of all "
        f"edges ({intra_edges}/{total_edges}), confirming meaningful cluster "
        r"separation ($Q > 0.3$)."
    )
elif modularity_q > 0:
    q_interp = (
        f"Within-community edges account for \\textbf{{{intra_frac:.0%}}} of all "
        f"edges ({intra_edges}/{total_edges}); modest community structure "
        r"($0 < Q \leq 0.3$)."
    )
else:
    q_interp = (
        f"Only \\textbf{{{intra_frac:.0%}}} of edges are within-community "
        f"({intra_edges}/{total_edges}); $Q < 0$ indicates the assigned labels "
        r"do not reflect the graph's structural communities (the ring-lattice "
        r"topology distributes edges uniformly across label boundaries)."
    )

caption_text = (
    r"\caption{Network of "
    + str(G.number_of_nodes())
    + r" nodes and "
    + str(total_edges)
    + r" edges, colored by pre-assigned community (4 communities, "
    + f"modularity $Q = {modularity_q:.2f}$"
    + r"). "
    + q_interp
    + r" Spring layout (seed = " + str(PINNED_SEED) + r", $k = 0.4$, 100 iterations). "
    + r"Node size: " + size_mode.replace("(", r"\textit{(").replace(")", r")}")
    + r". Edge $\alpha = 0.30$. Colors: ColorBrewer Set2.}"
)

caption_path = cwd / "caption.tex"
caption_path.write_text(caption_text + "\n")
print(f"Saved: {caption_path}")
