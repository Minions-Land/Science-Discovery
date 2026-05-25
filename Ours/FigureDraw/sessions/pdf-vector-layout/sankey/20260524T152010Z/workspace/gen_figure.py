import json
import sys

with open("data.json") as f:
    data = json.load(f)

nodes = data["nodes"]
links = data["links"]
node_idx = {n: i for i, n in enumerate(nodes)}

source = [node_idx[l["source"]] for l in links]
target = [node_idx[l["target"]] for l in links]
value  = [l["value"]             for l in links]

# Palette: one color per node
NODE_COLORS = [
    "#4878CF",  # Raw       - blue
    "#6ACC65",  # Cleaned   - green
    "#D65F5F",  # Filtered  - red-orange
    "#B47CC7",  # Train     - purple
    "#C4AD66",  # Val       - gold
    "#77BEDB",  # Test      - sky
    "#E07B54",  # Reject    - burnt orange
]

# Link colors inherit from source node (semi-transparent)
LINK_COLORS_RGBA = [
    "rgba(72,120,207,0.35)",   # Raw → *
    "rgba(72,120,207,0.35)",   # Raw → *
    "rgba(106,204,101,0.35)",  # Cleaned → *
    "rgba(106,204,101,0.35)",  # Cleaned → *
    "rgba(214,95,95,0.35)",    # Filtered → *
    "rgba(214,95,95,0.35)",    # Filtered → *
    "rgba(214,95,95,0.35)",    # Filtered → *
]

def make_plotly():
    import plotly.graph_objects as go

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=22,
            line=dict(color="white", width=0.5),
            label=nodes,
            color=NODE_COLORS,
            hovertemplate="%{label}<br>Total: %{value}<extra></extra>",
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=LINK_COLORS_RGBA,
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
        paper_bgcolor="white",
        width=820,
        height=480,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def save_plotly(fig):
    fig.write_image("figure.pdf", engine="kaleido")
    fig.write_image("figure.png", engine="kaleido", scale=2)
    fig.write_image("figure.svg", engine="kaleido")
    print("Saved via plotly+kaleido: figure.pdf, figure.png, figure.svg")


def make_matplotlib():
    """Fallback: manual Sankey with matplotlib bezier patches."""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.path import Path
    import matplotlib.patches as patches

    # ---- layout ----
    # Columns: Raw(0) | Cleaned,Reject(1) | Filtered,Reject(2) | Train,Val,Test(3)
    # We treat Reject as a terminal node placed at col 3 bottom.
    COL_X = {
        "Raw":     0.05,
        "Cleaned": 0.32,
        "Filtered":0.59,
        "Train":   0.86,
        "Val":     0.86,
        "Test":    0.86,
        "Reject":  0.86,
    }

    # Compute node totals (max of in-flow, out-flow)
    node_in  = {n: 0 for n in nodes}
    node_out = {n: 0 for n in nodes}
    for l in links:
        node_out[l["source"]] += l["value"]
        node_in[l["target"]]  += l["value"]
    node_total = {n: max(node_in[n], node_out[n]) for n in nodes}

    SCALE = 1 / 1200  # map sample counts → figure height fraction
    NODE_W = 0.025
    GAP    = 0.04

    # Assign y-bottom for each node within its column
    col_nodes = {}
    for n in nodes:
        x = COL_X[n]
        col_nodes.setdefault(x, []).append(n)

    node_ybot = {}
    for x, ns in col_nodes.items():
        total_h = sum(node_total[n] * SCALE for n in ns)
        total_gap = GAP * (len(ns) - 1)
        start = (1 - total_h - total_gap) / 2
        y = start
        for n in ns:
            node_ybot[n] = y
            y += node_total[n] * SCALE + GAP

    # Track current fill offsets for links
    src_offset = {n: 0 for n in nodes}
    tgt_offset = {n: 0 for n in nodes}

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    color_map = dict(zip(nodes, NODE_COLORS))

    def hex_to_rgba(h, alpha=0.35):
        h = h.lstrip("#")
        r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
        return (r, g, b, alpha)

    # Draw links
    for l in links:
        s, t, v = l["source"], l["target"], l["value"]
        h = v * SCALE
        sx = COL_X[s] + NODE_W
        tx = COL_X[t]
        sy = node_ybot[s] + src_offset[s]
        ty = node_ybot[t] + tgt_offset[t]
        src_offset[s] += h
        tgt_offset[t] += h

        cx = (sx + tx) / 2
        verts = [
            (sx, sy), (cx, sy), (tx, ty), (tx, ty+h),
            (cx, sy+h), (sx, sy+h), (sx, sy),
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4]
        # Use two bezier segments
        verts2 = [
            (sx, sy),
            (cx, sy),
            (cx, ty),
            (tx, ty),
            (tx, ty+h),
            (cx, ty+h),
            (cx, sy+h),
            (sx, sy+h),
            (sx, sy),
        ]
        codes2 = [Path.MOVETO,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4,
                  Path.LINETO,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4,
                  Path.CLOSEPOLY]
        path = Path(verts2, codes2)
        patch = patches.PathPatch(path, facecolor=hex_to_rgba(color_map[s]),
                                  edgecolor="none", zorder=1)
        ax.add_patch(patch)

    # Draw nodes
    for n in nodes:
        x = COL_X[n]
        y = node_ybot[n]
        h = node_total[n] * SCALE
        rect = mpatches.FancyBboxPatch(
            (x, y), NODE_W, h,
            boxstyle="square,pad=0",
            facecolor=color_map[n], edgecolor="white", linewidth=0.8, zorder=2
        )
        ax.add_patch(rect)
        # Label
        label_x = x + NODE_W/2
        label_y = y + h/2
        ha = "center"
        ax.text(label_x, label_y + h/2 + 0.015, f"{n}\n({node_total[n]})",
                ha=ha, va="bottom", fontsize=9, fontweight="bold",
                color=color_map[n], zorder=3)

    ax.set_title("Dataset Preparation Flow", fontsize=14, pad=10)
    fig.tight_layout()
    fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
    fig.savefig("figure.png", bbox_inches="tight", dpi=200)
    try:
        fig.savefig("figure.svg", bbox_inches="tight")
    except Exception:
        pass
    print("Saved via matplotlib fallback: figure.pdf, figure.png")


# Try plotly first, fall back to matplotlib
try:
    import plotly.graph_objects as go
    fig = make_plotly()
    try:
        save_plotly(fig)
    except Exception as e:
        print(f"kaleido export failed ({e}), trying orca or writing HTML...")
        try:
            fig.write_image("figure.pdf", engine="orca")
            fig.write_image("figure.png", engine="orca", scale=2)
            fig.write_image("figure.svg", engine="orca")
            print("Saved via plotly+orca")
        except Exception as e2:
            print(f"orca also failed ({e2}), falling back to matplotlib")
            make_matplotlib()
except ImportError:
    print("plotly not available, using matplotlib")
    make_matplotlib()
