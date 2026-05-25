import json
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    data = json.load(f)

G = nx.Graph()
community_map = {n["id"]: n["community"] for n in data["nodes"]}
for n in data["nodes"]:
    G.add_node(n["id"], community=n["community"])
for e in data["edges"]:
    G.add_edge(e["source"], e["target"])

n_communities = data["communities"]
palette = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A"]
node_colors = [palette[community_map[n]] for n in G.nodes()]

pos = nx.spring_layout(G, seed=42, k=1.8)

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect("equal")

nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.25, width=0.8, edge_color="#555555")
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                       node_size=220, linewidths=0.6,
                       edgecolors="white")
nx.draw_networkx_labels(G, pos, ax=ax, font_size=6.5,
                        font_color="white", font_weight="bold")

legend_handles = [
    mpatches.Patch(color=palette[c], label=f"Community {c}")
    for c in range(n_communities)
]
ax.legend(handles=legend_handles, loc="lower right", fontsize=8,
          framealpha=0.85, edgecolor="#cccccc")

ax.axis("off")
fig.tight_layout(pad=0.3)

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
