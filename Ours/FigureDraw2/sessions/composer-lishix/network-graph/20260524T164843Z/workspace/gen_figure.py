import json
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

with open("data.json") as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

communities = [G.nodes[n]["community"] for n in G.nodes()]
n_communities = data["communities"]

palette = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A"]
node_colors = [palette[c] for c in communities]

# Spring layout with fixed seed for reproducibility
pos = nx.spring_layout(G, seed=42, k=1.8 / np.sqrt(len(G.nodes())))

fig, ax = plt.subplots(figsize=(7, 7))

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.25, width=0.8, edge_color="#555555"
)
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors, node_size=220,
    linewidths=0.6, edgecolors="white"
)
nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=6, font_color="white", font_weight="bold"
)

legend_handles = [
    mpatches.Patch(color=palette[i], label=f"Community {i}")
    for i in range(n_communities)
]
ax.legend(handles=legend_handles, loc="upper left", framealpha=0.85,
          fontsize=8, title="Community", title_fontsize=8)

ax.set_title("Network Graph — Community Structure", fontsize=11, pad=10)
ax.axis("off")
fig.tight_layout()

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
