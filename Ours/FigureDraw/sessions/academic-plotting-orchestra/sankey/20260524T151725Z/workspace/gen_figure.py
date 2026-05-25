import json
import plotly.graph_objects as go

with open("data.json") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]

node_index = {n: i for i, n in enumerate(nodes)}

# Color palette: one color per source node, grayed for Reject
source_colors = {
    "Raw":     "#4C72B0",
    "Cleaned": "#55A868",
    "Filtered":"#C44E52",
}
node_colors = [
    "#4C72B0",  # Raw
    "#55A868",  # Cleaned
    "#C44E52",  # Filtered
    "#8172B2",  # Train
    "#CCB974",  # Val
    "#64B5CD",  # Test
    "#AAAAAA",  # Reject
]

link_colors = []
for lk in links:
    base = source_colors.get(lk["source"], "#AAAAAA")
    # semi-transparent
    r, g, b = int(base[1:3], 16), int(base[3:5], 16), int(base[5:7], 16)
    link_colors.append(f"rgba({r},{g},{b},0.45)")

fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=20,
        thickness=22,
        line=dict(color="white", width=0.5),
        label=nodes,
        color=node_colors,
        hovertemplate="%{label}<br>Total: %{value}<extra></extra>",
    ),
    link=dict(
        source=[node_index[lk["source"]] for lk in links],
        target=[node_index[lk["target"]] for lk in links],
        value=[lk["value"] for lk in links],
        color=link_colors,
        hovertemplate="%{source.label} → %{target.label}<br>%{value} samples<extra></extra>",
    ),
))

fig.update_layout(
    title=dict(
        text="Dataset Preparation Flow",
        font=dict(size=16, family="Arial"),
        x=0.5,
        xanchor="center",
    ),
    font=dict(size=13, family="Arial"),
    width=820,
    height=480,
    margin=dict(l=30, r=30, t=60, b=30),
    paper_bgcolor="white",
)

fig.write_image("figure.pdf", format="pdf")
fig.write_image("figure.png", format="png", scale=2)
fig.write_image("figure.svg", format="svg")

print("Saved figure.pdf, figure.png, figure.svg")
