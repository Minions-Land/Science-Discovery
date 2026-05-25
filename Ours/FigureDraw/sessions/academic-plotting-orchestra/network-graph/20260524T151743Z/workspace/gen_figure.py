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

n_communities = data["communities"]
community_map = {n["id"]: n["community"] for n in data["nodes"]}

# Community-aware spring layout: place nodes near community centroids
rng = np.random.default_rng(42)
community_colors = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A"]

pos = nx.spring_layout(G, seed=42, k=0.55, iterations=80)

node_colors = [community_colors[community_map[n]] for n in G.nodes()]

fig, ax = plt.subplots(figsize=(7, 7))

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.25,
    width=0.8,
    edge_color="#444444"
)

nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=280,
    linewidths=0.8,
    edgecolors="white"
)

nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=6,
    font_color="white",
    font_weight="bold"
)

legend_patches = [
    mpatches.Patch(color=community_colors[c], label=f"Community {c}")
    for c in range(n_communities)
]
ax.legend(
    handles=legend_patches,
    loc="lower right",
    fontsize=8,
    framealpha=0.85,
    edgecolor="#cccccc"
)

ax.set_title("Network Graph — Community Structure", fontsize=11, pad=10)
ax.axis("off")
fig.tight_layout()

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
