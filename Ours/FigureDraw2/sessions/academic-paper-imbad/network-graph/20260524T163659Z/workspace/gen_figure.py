import json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DATA_FILE = "data.json"
SEED = 42

with open(DATA_FILE) as f:
    data = json.load(f)

G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], community=node["community"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

n_communities = data["communities"]
community_map = {n["id"]: n["community"] for n in data["nodes"]}

# Color palette — colorblind-friendly qualitative
palette = ["#4477AA", "#EE6677", "#228833", "#CCBB44"]
node_colors = [palette[community_map[n]] for n in G.nodes()]

pos = nx.spring_layout(G, seed=SEED, k=2.2 / np.sqrt(len(G.nodes())), iterations=80)

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("white")

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.25,
    width=0.8,
    edge_color="#555555",
)

nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=220,
    linewidths=0.6,
    edgecolors="white",
)

nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=6,
    font_color="white",
    font_weight="bold",
)

legend_patches = [
    mpatches.Patch(facecolor=palette[c], label=f"Community {c}")
    for c in range(n_communities)
]
ax.legend(
    handles=legend_patches,
    loc="lower right",
    fontsize=8,
    framealpha=0.85,
    edgecolor="#cccccc",
)

ax.set_title("Community Structure of a 30-Node Network", fontsize=11, pad=10)
ax.axis("off")
plt.tight_layout(pad=0.5)

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
