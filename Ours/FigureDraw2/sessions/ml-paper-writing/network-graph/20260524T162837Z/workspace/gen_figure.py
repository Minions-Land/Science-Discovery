import json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DATA_PATH = "data.json"

with open(DATA_PATH) as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

n_communities = data["communities"]
community_map = {n["id"]: n["community"] for n in data["nodes"]}

# Use a qualitative colormap with enough distinct colors
palette = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A"]
node_colors = [palette[community_map[n] % len(palette)] for n in G.nodes()]

# Spring layout with fixed seed for reproducibility
np.random.seed(42)
pos = nx.spring_layout(G, seed=42, k=1.8 / np.sqrt(len(G.nodes())), iterations=120)

fig, ax = plt.subplots(figsize=(6, 5.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("#f8f8f8")

# Draw edges first (behind nodes)
nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.25, width=0.8, edge_color="#555555"
)

# Draw nodes
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=220,
    linewidths=0.6,
    edgecolors="white"
)

# Draw node labels
nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=6.5,
    font_color="white",
    font_weight="bold"
)

# Legend
legend_handles = [
    mpatches.Patch(color=palette[c], label=f"Community {c}")
    for c in range(n_communities)
]
ax.legend(
    handles=legend_handles,
    loc="upper right",
    fontsize=8,
    framealpha=0.85,
    edgecolor="#cccccc",
    handlelength=1.2,
    handleheight=1.0,
)

ax.axis("off")
ax.set_title("Community Structure of a 30-Node Network", fontsize=10, pad=8)

plt.tight_layout(pad=0.4)

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved: figure.pdf, figure.png, figure.svg")
