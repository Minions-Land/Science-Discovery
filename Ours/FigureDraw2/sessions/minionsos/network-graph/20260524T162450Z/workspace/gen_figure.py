import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

with open("data.json") as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

n_communities = data["communities"]
community_colors = ["#E64B35", "#4DBBD5", "#00A087", "#F39B7F"]
node_colors = [community_colors[G.nodes[n]["community"]] for n in G.nodes()]

# Spring layout with fixed seed for reproducibility
pos = nx.spring_layout(G, seed=42, k=1.8 / np.sqrt(len(G.nodes())), iterations=100)

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("#F8F8F8")

# Separate intra- vs inter-community edges for visual clarity
intra_edges = [(u, v) for u, v in G.edges() if G.nodes[u]["community"] == G.nodes[v]["community"]]
inter_edges = [(u, v) for u, v in G.edges() if G.nodes[u]["community"] != G.nodes[v]["community"]]

nx.draw_networkx_edges(G, pos, edgelist=intra_edges, ax=ax,
                       edge_color="#888888", alpha=0.35, width=1.0)
nx.draw_networkx_edges(G, pos, edgelist=inter_edges, ax=ax,
                       edge_color="#333333", alpha=0.55, width=1.2, style="dashed")

nx.draw_networkx_nodes(G, pos, ax=ax,
                       node_color=node_colors,
                       node_size=260,
                       linewidths=0.8,
                       edgecolors="white")

nx.draw_networkx_labels(G, pos, ax=ax,
                        font_size=6.5, font_color="white", font_weight="bold")

legend_patches = [
    mpatches.Patch(color=community_colors[i], label=f"Community {i}")
    for i in range(n_communities)
]
ax.legend(handles=legend_patches, loc="lower right", framealpha=0.9,
          fontsize=8.5, title="Community", title_fontsize=9)

ax.set_title("Community Structure in a 30-Node Network", fontsize=12, fontweight="bold", pad=12)
ax.axis("off")
plt.tight_layout(pad=0.5)

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
