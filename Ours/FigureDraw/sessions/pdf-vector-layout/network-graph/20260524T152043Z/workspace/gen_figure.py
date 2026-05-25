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
community = {}
for node in data["nodes"]:
    G.add_node(node["id"])
    community[node["id"]] = node["community"]

for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

n_communities = data["communities"]
palette = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A"]
node_colors = [palette[community[n]] for n in G.nodes()]

np.random.seed(42)
pos = nx.spring_layout(G, seed=42, k=1.8 / np.sqrt(len(G.nodes())), iterations=100)

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

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
ax.legend(
    handles=legend_handles, loc="lower right",
    framealpha=0.9, fontsize=9, title="Community", title_fontsize=9
)

ax.set_title("Network Graph — Community Structure", fontsize=12, pad=10)
ax.axis("off")
plt.tight_layout()

plt.savefig("figure.pdf", dpi=150, bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
