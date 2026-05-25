#!/usr/bin/env python3
"""Sankey diagram of dataset preparation flow."""
import json, sys

with open('data.json') as f:
    data = json.load(f)

nodes = data['nodes']
links = data['links']
node_idx = {n: i for i, n in enumerate(nodes)}

NODE_COLORS = {
    'Raw':     '#1f77b4',
    'Cleaned': '#2ca02c',
    'Filtered':'#ff7f0e',
    'Train':   '#9467bd',
    'Val':     '#8c564b',
    'Test':    '#e377c2',
    'Reject':  '#d62728',
}

def try_plotly():
    import plotly.graph_objects as go
    src = [node_idx[l['source']] for l in links]
    tgt = [node_idx[l['target']] for l in links]
    val = [l['value'] for l in links]
    src_rgba = {
        'Raw':     'rgba(31,119,180,0.5)',
        'Cleaned': 'rgba(44,160,44,0.5)',
        'Filtered':'rgba(255,127,14,0.5)',
    }
    link_colors = [src_rgba.get(l['source'], 'rgba(150,150,150,0.4)') for l in links]
    node_colors = [NODE_COLORS.get(n, '#aaa') for n in nodes]
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(pad=15, thickness=22,
                  line=dict(color='white', width=0.5),
                  label=nodes, color=node_colors),
        link=dict(source=src, target=tgt, value=val, color=link_colors),
    ))
    fig.update_layout(
        title_text='Dataset Preparation Flow',
        font=dict(size=13, family='Arial'),
        width=900, height=480,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='white',
    )
    fig.write_image('figure.pdf')
    fig.write_image('figure.png', scale=2)
    try:
        fig.write_image('figure.svg')
    except Exception:
        pass
    print('Generated with plotly+kaleido')


def try_matplotlib():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    import matplotlib.colors as mcolors

    col = {'Raw': 0, 'Cleaned': 1, 'Filtered': 2,
           'Train': 3, 'Val': 3, 'Test': 3, 'Reject': 3}

    out_flow = {n: 0 for n in nodes}
    in_flow  = {n: 0 for n in nodes}
    for l in links:
        out_flow[l['source']] += l['value']
        in_flow[l['target']]  += l['value']

    node_h = {n: max(out_flow[n], in_flow[n], 1) for n in nodes}

    # Stack nodes per column bottom-to-top
    col_order = {
        0: ['Raw'],
        1: ['Cleaned'],
        2: ['Filtered'],
        3: ['Train', 'Val', 'Test', 'Reject'],
    }
    GAP = 30
    node_ybot = {}
    for c, ns in col_order.items():
        total = sum(node_h[n] for n in ns) + GAP * (len(ns) - 1)
        y = -total / 2
        for n in ns:
            node_ybot[n] = y
            y += node_h[n] + GAP

    out_cur = {n: node_ybot[n] for n in nodes}
    in_cur  = {n: node_ybot[n] for n in nodes}

    NODE_W = 0.12
    X_SCALE = 3.2

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(-0.3, X_SCALE * 3 + NODE_W + 0.4)
    ax.set_ylim(-750, 750)
    ax.axis('off')

    # Draw nodes
    for n in nodes:
        x = col[n] * X_SCALE
        yb = node_ybot[n]
        h = node_h[n]
        color = NODE_COLORS.get(n, '#aaa')
        rect = plt.Rectangle((x, yb), NODE_W, h,
                              facecolor=color, edgecolor='white',
                              linewidth=1.2, zorder=3)
        ax.add_patch(rect)
        label = f'{n}\n{int(h)}'
        ax.text(x + NODE_W / 2, yb + h / 2, label,
                ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='white', zorder=4)

    src_palette = {
        'Raw':     mcolors.to_rgba('#1f77b4', alpha=0.45),
        'Cleaned': mcolors.to_rgba('#2ca02c', alpha=0.45),
        'Filtered':mcolors.to_rgba('#ff7f0e', alpha=0.45),
    }

    for l in links:
        s, t, v = l['source'], l['target'], l['value']
        color = src_palette.get(s, mcolors.to_rgba('#999', alpha=0.4))

        x0 = col[s] * X_SCALE + NODE_W
        x1 = col[t] * X_SCALE
        cx = (x0 + x1) / 2

        y0b = out_cur[s];  y0t = y0b + v;  out_cur[s] += v
        y1b = in_cur[t];   y1t = y1b + v;  in_cur[t]  += v

        verts = [
            (x0, y0t), (cx, y0t), (cx, y1t), (x1, y1t),
            (x1, y1b), (cx, y1b), (cx, y0b), (x0, y0b),
            (x0, y0t),
        ]
        codes = [Path.MOVETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.LINETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes),
                               facecolor=color, edgecolor='none', zorder=2))

    ax.set_title('Dataset Preparation Flow', fontsize=14, pad=8)
    fig.tight_layout()
    fig.savefig('figure.pdf', bbox_inches='tight', dpi=150)
    fig.savefig('figure.png', bbox_inches='tight', dpi=200)
    fig.savefig('figure.svg', bbox_inches='tight')
    plt.close()
    print('Generated with matplotlib (manual Sankey)')


try:
    try_plotly()
except Exception as e:
    print(f'plotly failed: {e}', file=sys.stderr)
    try_matplotlib()
