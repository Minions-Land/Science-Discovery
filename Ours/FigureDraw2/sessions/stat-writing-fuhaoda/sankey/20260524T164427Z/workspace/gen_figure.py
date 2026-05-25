#!/usr/bin/env python3
"""Sankey diagram of dataset preparation flow."""
import json, sys

with open('data.json') as f:
    data = json.load(f)

nodes = data['nodes']
links = data['links']

PALETTE = {
    'Raw':      '#2196F3',
    'Cleaned':  '#4CAF50',
    'Filtered': '#FF9800',
    'Train':    '#9C27B0',
    'Val':      '#00BCD4',
    'Test':     '#F44336',
    'Reject':   '#9E9E9E',
}

def hex_rgba(h, a=0.45):
    h = h.lstrip('#')
    r, g, b = int(h[:2],16), int(h[2:4],16), int(h[4:],16)
    return f'rgba({r},{g},{b},{a})'

def make_plotly():
    import plotly.graph_objects as go
    idx = {n: i for i, n in enumerate(nodes)}
    src = [idx[l['source']] for l in links]
    tgt = [idx[l['target']] for l in links]
    val = [l['value'] for l in links]
    inflow  = {n: 0 for n in nodes}
    outflow = {n: 0 for n in nodes}
    for l in links:
        outflow[l['source']] += l['value']
        inflow[l['target']]  += l['value']
    labels = [f"{n}<br>{max(inflow[n], outflow[n]):,}" for n in nodes]
    node_colors = [PALETTE.get(n, '#888') for n in nodes]
    link_colors = [hex_rgba(PALETTE.get(nodes[s], '#888')) for s in src]
    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(pad=18, thickness=22,
                  line=dict(color='white', width=0.5),
                  label=labels, color=node_colors),
        link=dict(source=src, target=tgt, value=val, color=link_colors),
    ))
    fig.update_layout(
        title=dict(text='Dataset Preparation Flow', font=dict(size=15, family='Arial')),
        font=dict(size=12, family='Arial'),
        width=860, height=500,
        paper_bgcolor='white',
        margin=dict(l=15, r=15, t=45, b=15),
    )
    fig.write_image('figure.pdf')
    fig.write_image('figure.png', scale=2)
    try:
        fig.write_image('figure.svg')
    except Exception:
        pass

def make_matplotlib():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.path import Path
    import numpy as np

    SCALE = 1/100
    GAP   = 0.25
    NW    = 0.25   # node width

    inflow  = {n: 0 for n in nodes}
    outflow = {n: 0 for n in nodes}
    for l in links:
        outflow[l['source']] += l['value']
        inflow[l['target']]  += l['value']

    node_h = {n: max(inflow.get(n,0), outflow.get(n,0)) * SCALE for n in nodes}

    cols   = [['Raw'], ['Cleaned'], ['Filtered'], ['Train','Val','Test','Reject']]
    col_x  = [0.0, 2.5, 5.0, 7.5]

    def col_h(c):
        return sum(node_h[n] for n in c) + GAP*(len(c)-1)

    max_h = max(col_h(c) for c in cols)

    node_yb = {}
    for col_nodes, cx in zip(cols, col_x):
        y = (max_h - col_h(col_nodes)) / 2
        for n in col_nodes:
            node_yb[n] = y
            y += node_h[n] + GAP

    out_cur = {n: node_yb[n] for n in nodes}
    in_cur  = {n: node_yb[n] for n in nodes}

    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(-0.4, 8.2)
    ax.set_ylim(-0.4, max_h + 0.4)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    col_of = {n: i for i, c in enumerate(cols) for n in c}

    for l in links:
        s, t, v = l['source'], l['target'], l['value']
        h = v * SCALE
        x0 = col_x[col_of[s]] + NW
        x1 = col_x[col_of[t]]
        y0b = out_cur[s];  y0t = y0b + h
        y1b = in_cur[t];   y1t = y1b + h
        out_cur[s] += h
        in_cur[t]  += h
        cx = (x0 + x1) / 2
        verts = [
            (x0, y0b), (cx, y0b), (cx, y1b), (x1, y1b),
            (x1, y1t), (cx, y1t), (cx, y0t), (x0, y0t),
            (x0, y0b),
        ]
        codes = [Path.MOVETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.LINETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CLOSEPOLY]
        hx = PALETTE[s].lstrip('#')
        r,g,b = int(hx[:2],16)/255, int(hx[2:4],16)/255, int(hx[4:],16)/255
        ax.add_patch(patches.PathPatch(
            Path(verts, codes), facecolor=(r,g,b,0.4), edgecolor='none'))

    for n in nodes:
        cx = col_x[col_of[n]]
        yb = node_yb[n]
        h  = node_h[n]
        ax.add_patch(patches.Rectangle(
            (cx, yb), NW, h,
            facecolor=PALETTE[n], edgecolor='white', linewidth=0.8, zorder=3))
        total = max(inflow.get(n,0), outflow.get(n,0))
        ax.text(cx + NW/2, yb + h/2, f'{n}\n{total:,}',
                ha='center', va='center', fontsize=8.5, fontweight='bold',
                color='white', zorder=4)

    ax.set_title('Dataset Preparation Flow', fontsize=13, pad=8)
    plt.tight_layout()
    plt.savefig('figure.pdf', bbox_inches='tight', dpi=150)
    plt.savefig('figure.png', bbox_inches='tight', dpi=200)
    plt.savefig('figure.svg', bbox_inches='tight')
    plt.close()

try:
    make_plotly()
    print("Done (plotly+kaleido)")
except Exception as e:
    print(f"plotly failed: {e} — using matplotlib")
    make_matplotlib()
    print("Done (matplotlib)")
