import json
import sys
import numpy as np

with open('data.json') as f:
    data = json.load(f)

nodes_list = data['nodes']
links = data['links']
node_idx = {n: i for i, n in enumerate(nodes_list)}

PALETTE = {
    'Raw':     '#4C72B0',
    'Cleaned': '#55A868',
    'Filtered':'#DD8452',
    'Train':   '#8172B2',
    'Val':     '#CCB974',
    'Test':    '#64B5CD',
    'Reject':  '#C44E52',
}

def hex_to_rgba(hex_color, alpha=0.42):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f'rgba({r},{g},{b},{alpha})'

# ── Attempt 1: plotly + kaleido ──────────────────────────────────────────────
def save_plotly():
    import plotly.graph_objects as go

    sources = [node_idx[l['source']] for l in links]
    targets = [node_idx[l['target']] for l in links]
    values  = [l['value']            for l in links]

    node_colors = [PALETTE.get(n, '#888888') for n in nodes_list]
    link_colors = [hex_to_rgba(PALETTE.get(links[i]['source'], '#888888'))
                   for i in range(len(links))]

    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=22, thickness=26,
            line=dict(color='#333', width=0.5),
            label=nodes_list,
            color=node_colors,
            hovertemplate='%{label}<extra></extra>',
        ),
        link=dict(
            source=sources, target=targets, value=values,
            color=link_colors,
            hovertemplate='%{source.label} → %{target.label}: %{value:,}<extra></extra>',
        ),
    )])
    fig.update_layout(
        title=dict(text='Dataset Preparation Flow', font=dict(size=16, family='Arial')),
        font=dict(size=13, family='Arial'),
        width=900, height=500,
        margin=dict(l=25, r=25, t=55, b=25),
        paper_bgcolor='white',
    )
    fig.write_image('figure.pdf')
    fig.write_image('figure.png', scale=2)
    try:
        fig.write_image('figure.svg')
    except Exception:
        pass
    print('plotly: saved figure.pdf / figure.png')

# ── Attempt 2: matplotlib manual Sankey ─────────────────────────────────────
def save_matplotlib():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, Rectangle
    from matplotlib.path import Path
    import matplotlib.patches as mpatches

    # ── layout ──────────────────────────────────────────────────────────────
    # Columns (x centre of node bar)
    COL = {'Raw': 0.08, 'Cleaned': 0.33, 'Filtered': 0.58,
           'Train': 0.88, 'Val': 0.88, 'Test': 0.88, 'Reject': 0.88}
    NODE_W = 0.022   # bar half-width in data coords
    SCALE  = 1/1200  # pixels → y-height (total canvas height ≈ 1)

    # Compute total flow through each node
    flow_in  = {n: 0 for n in nodes_list}
    flow_out = {n: 0 for n in nodes_list}
    for l in links:
        flow_out[l['source']] += l['value']
        flow_in [l['target']] += l['value']

    node_height = {}
    for n in nodes_list:
        node_height[n] = max(flow_in[n], flow_out[n]) * SCALE

    # Y positions (bottom of each node bar), stacked per column
    col_nodes = {}
    for n in nodes_list:
        c = COL[n]
        col_nodes.setdefault(c, []).append(n)

    GAP = 0.04
    node_y0 = {}   # bottom y of each node
    for c, nlist in col_nodes.items():
        total_h = sum(node_height[n] for n in nlist) + GAP*(len(nlist)-1)
        y = 0.5 - total_h/2
        for n in nlist:
            node_y0[n] = y
            y += node_height[n] + GAP

    # ── draw ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Track how much of each node's in/out has been consumed (for stacking flows)
    out_cursor = {n: node_y0[n] for n in nodes_list}
    in_cursor  = {n: node_y0[n] for n in nodes_list}

    def bezier_band(x0, y0_bot, x1, y1_bot, h, color):
        """Draw a filled bezier band from (x0,y0_bot) to (x1,y1_bot) with height h."""
        cx = (x0 + x1) / 2
        verts = [
            (x0, y0_bot),
            (cx, y0_bot),
            (cx, y1_bot),
            (x1, y1_bot),
            (x1, y1_bot + h),
            (cx, y1_bot + h),
            (cx, y0_bot + h),
            (x0, y0_bot + h),
            (x0, y0_bot),
        ]
        codes = [Path.MOVETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.LINETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CLOSEPOLY]
        path = Path(verts, codes)
        patch = mpatches.PathPatch(path, facecolor=color, edgecolor='none', alpha=0.45, zorder=1)
        ax.add_patch(patch)

    for l in links:
        src, tgt, val = l['source'], l['target'], l['value']
        h = val * SCALE
        x0 = COL[src] + NODE_W
        x1 = COL[tgt] - NODE_W
        y0 = out_cursor[src]
        y1 = in_cursor[tgt]
        color = PALETTE.get(src, '#888888')
        bezier_band(x0, y0, x1, y1, h, color)
        out_cursor[src] += h
        in_cursor[tgt]  += h

    # Draw node bars on top
    for n in nodes_list:
        x = COL[n] - NODE_W
        y = node_y0[n]
        w = NODE_W * 2
        h = node_height[n]
        rect = Rectangle((x, y), w, h,
                          facecolor=PALETTE.get(n, '#888888'),
                          edgecolor='#333333', linewidth=0.8, zorder=2)
        ax.add_patch(rect)
        # Label
        label_x = COL[n]
        label_y = y + h/2
        ha = 'left' if COL[n] < 0.5 else 'right'
        offset = NODE_W + 0.012 if ha == 'left' else -(NODE_W + 0.012)
        ax.text(label_x + offset, label_y, f'{n}\n({max(flow_in[n],flow_out[n]):,})',
                ha=ha, va='center', fontsize=10, fontweight='bold',
                color='#222222', zorder=3)

    ax.set_title('Dataset Preparation Flow', fontsize=14, fontweight='bold',
                 pad=10, color='#222222')

    plt.tight_layout()
    fig.savefig('figure.pdf', bbox_inches='tight', dpi=150)
    fig.savefig('figure.png', bbox_inches='tight', dpi=200)
    try:
        fig.savefig('figure.svg', bbox_inches='tight')
    except Exception:
        pass
    plt.close(fig)
    print('matplotlib: saved figure.pdf / figure.png')

# ── Run ──────────────────────────────────────────────────────────────────────
try:
    save_plotly()
except Exception as e:
    print(f'plotly failed ({e}), falling back to matplotlib')
    save_matplotlib()
