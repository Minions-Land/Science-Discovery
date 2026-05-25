import json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

communities = {n: G.nodes[n]["community"] for n in G.nodes}
n_communities = data["communities"]

# Palette: colorblind-friendly, distinct for 4 communities
palette = ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"]
node_colors = [palette[communities[n]] for n in G.nodes]

np.random.seed(42)
pos = nx.spring_layout(G, seed=42, k=1.8, iterations=80)

fig, ax = plt.subplots(figsize=(6, 6))

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.25, width=0.8, edge_color="#555555"
)
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=220,
    linewidths=0.6,
    edgecolors="white"
)
nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=6, font_color="white", font_weight="bold"
)

legend_handles = [
    mpatches.Patch(color=palette[i], label=f"Community {i}")
    for i in range(n_communities)
]
ax.legend(
    handles=legend_handles,
    loc="lower right",
    fontsize=8,
    framealpha=0.85,
    edgecolor="#cccccc"
)

ax.set_title("Community Structure of a 30-Node Network", fontsize=11, pad=10)
ax.axis("off")
fig.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done: figure.pdf, figure.png, figure.svg")
