import json, pathlib, sys
import plotly.graph_objects as go

cwd = pathlib.Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())

nodes = data["nodes"]
node_idx = {n: i for i, n in enumerate(nodes)}

# Color palette: one color per source node, grey for sinks
source_colors = {
    "Raw":     "#4C72B0",
    "Cleaned": "#55A868",
    "Filtered":"#C44E52",
}
node_colors = []
for n in nodes:
    if n in source_colors:
        node_colors.append(source_colors[n])
    elif n == "Reject":
        node_colors.append("#AAAAAA")
    elif n == "Train":
        node_colors.append("#8172B2")
    elif n == "Val":
        node_colors.append("#CCB974")
    elif n == "Test":
        node_colors.append("#64B5CD")
    else:
        node_colors.append("#BBBBBB")

# Link colors: inherit from source with transparency
def hex_to_rgba(h, a=0.45):
    h = h.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

sources, targets, values, link_colors = [], [], [], []
for lk in data["links"]:
    s = node_idx[lk["source"]]
    t = node_idx[lk["target"]]
    sources.append(s)
    targets.append(t)
    values.append(lk["value"])
    sc = source_colors.get(lk["source"], "#AAAAAA")
    link_colors.append(hex_to_rgba(sc))

fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=20,
        thickness=22,
        line=dict(color="white", width=0.5),
        label=nodes,
        color=node_colors,
        hovertemplate="%{label}<extra></extra>",
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors,
        hovertemplate="%{source.label} → %{target.label}: %{value}<extra></extra>",
    ),
))

fig.update_layout(
    title=dict(
        text="Dataset Preparation Flow",
        font=dict(size=16, family="Arial"),
        x=0.5,
    ),
    font=dict(size=13, family="Arial"),
    paper_bgcolor="white",
    width=820,
    height=480,
    margin=dict(l=30, r=30, t=60, b=30),
)

pdf_path = str(cwd / "figure.pdf")
png_path = str(cwd / "figure.png")
svg_path = str(cwd / "figure.svg")

fig.write_image(pdf_path, format="pdf")
fig.write_image(png_path, format="png", scale=2)
fig.write_image(svg_path, format="svg")

print(f"Saved: {pdf_path}")
print(f"Saved: {png_path}")
print(f"Saved: {svg_path}")
