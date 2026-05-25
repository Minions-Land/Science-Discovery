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
community_map = {n["id"]: n["community"] for n in data["nodes"]}

# Color palette — qualitative, colorblind-friendly
palette = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488"]
node_colors = [palette[community_map[n]] for n in G.nodes()]

rng = np.random.default_rng(42)
pos = nx.spring_layout(G, seed=42, k=1.8 / np.sqrt(len(G.nodes())), iterations=120)

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

nx.draw_networkx_edges(
    G, pos, ax=ax,
    alpha=0.25, width=0.8,
    edge_color="#555555",
)
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=260,
    linewidths=0.6,
    edgecolors="white",
)
nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=6,
    font_color="white",
    font_weight="bold",
)

legend_handles = [
    mpatches.Patch(facecolor=palette[c], edgecolor="none", label=f"Community {c}")
    for c in range(n_communities)
]
ax.legend(
    handles=legend_handles,
    loc="lower right",
    fontsize=8,
    framealpha=0.9,
    edgecolor="#cccccc",
    handlelength=1.2,
    handleheight=1.0,
)

ax.set_axis_off()
ax.set_title("Community structure in a 30-node network", fontsize=10, pad=8)

fig.tight_layout(pad=0.5)
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
