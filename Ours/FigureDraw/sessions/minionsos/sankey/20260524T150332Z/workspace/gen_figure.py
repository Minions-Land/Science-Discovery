#!/usr/bin/env python3
"""Sankey diagram of dataset preparation flow."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as mpatches

with open('data.json') as f:
    data = json.load(f)

nodes_list = data['nodes']
links = data['links']

# Compute flows
node_inflow = {}
node_outflow = {}
for link in links:
    s, t, v = link['source'], link['target'], link['value']
    node_outflow[s] = node_outflow.get(s, 0) + v
    node_inflow[t] = node_inflow.get(t, 0) + v

# Column assignment
col = {'Raw': 0, 'Cleaned': 1, 'Filtered': 2, 'Train': 3, 'Val': 3, 'Test': 3, 'Reject': 3}

col_order = {
    0: ['Raw'],
    1: ['Cleaned'],
    2: ['Filtered'],
    3: ['Train', 'Val', 'Test', 'Reject'],
}

# Scale flows to figure height
max_flow = max(
    max(node_outflow.get(n, 0), node_inflow.get(n, 0)) for n in nodes_list
)
SCALE = 0.78 / max_flow
GAP = 0.028
NODE_W = 0.022

# Node heights
node_height = {
    n: max(node_inflow.get(n, 0), node_outflow.get(n, 0)) * SCALE
    for n in nodes_list
}

# Vertical positions (bottom y), centered per column
node_y = {}
for c, order in col_order.items():
    total_h = sum(node_height[n] for n in order) + GAP * (len(order) - 1)
    y = (1.0 - total_h) / 2.0
    for n in order:
        node_y[n] = y
        y += node_height[n] + GAP

# Horizontal positions
col_x = {0: 0.06, 1: 0.30, 2: 0.54, 3: 0.78}

# Colors
node_colors = {
    'Raw':     '#2166AC',
    'Cleaned': '#1A9641',
    'Filtered':'#E66101',
    'Train':   '#7B2D8B',
    'Val':     '#0571B0',
    'Test':    '#4DAC26',
    'Reject':  '#CA0020',
}
flow_colors = {
    'Raw':     (0.13, 0.40, 0.67, 0.38),
    'Cleaned': (0.10, 0.59, 0.25, 0.38),
    'Filtered':(0.90, 0.38, 0.00, 0.38),
}

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

def draw_flow(ax, x0, x1, y0b, y0t, y1b, y1t, color):
    cx = (x0 + x1) / 2.0
    verts = [
        (x0, y0b),
        (cx, y0b), (cx, y1b), (x1, y1b),
        (x1, y1t),
        (cx, y1t), (cx, y0t), (x0, y0t),
        (x0, y0b),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    patch = mpatches.PathPatch(Path(verts, codes),
                               facecolor=color, edgecolor='none', zorder=1)
    ax.add_patch(patch)

# Stacking cursors
out_y = {n: node_y[n] for n in nodes_list}
in_y  = {n: node_y[n] for n in nodes_list}

for link in links:
    s, t, v = link['source'], link['target'], link['value']
    h = v * SCALE
    x0 = col_x[col[s]] + NODE_W
    x1 = col_x[col[t]]
    y0b = out_y[s];  y0t = y0b + h
    y1b = in_y[t];   y1t = y1b + h
    out_y[s] = y0t
    in_y[t]  = y1t
    draw_flow(ax, x0, x1, y0b, y0t, y1b, y1t, flow_colors.get(s, (0.5,0.5,0.5,0.35)))

# Draw nodes
for n in nodes_list:
    x = col_x[col[n]]
    y = node_y[n]
    h = node_height[n]
    rect = plt.Rectangle((x, y), NODE_W, h,
                          facecolor=node_colors[n], edgecolor='white',
                          linewidth=0.8, zorder=3)
    ax.add_patch(rect)

    flow_val = max(node_inflow.get(n, 0), node_outflow.get(n, 0))
    label = f'{n}\n{flow_val:,}'
    c = col[n]
    if c == 0:
        ax.text(x - 0.012, y + h / 2, label,
                ha='right', va='center', fontsize=9.5, fontweight='bold',
                color=node_colors[n], zorder=4)
    elif c == 3:
        ax.text(x + NODE_W + 0.012, y + h / 2, label,
                ha='left', va='center', fontsize=9.5, fontweight='bold',
                color=node_colors[n], zorder=4)
    else:
        ax.text(x + NODE_W / 2, y + h + 0.018, label,
                ha='center', va='bottom', fontsize=9.5, fontweight='bold',
                color=node_colors[n], zorder=4)

# Flow value annotations (midpoint of each bezier)
out_y2 = {n: node_y[n] for n in nodes_list}
in_y2  = {n: node_y[n] for n in nodes_list}
for link in links:
    s, t, v = link['source'], link['target'], link['value']
    h = v * SCALE
    x0 = col_x[col[s]] + NODE_W
    x1 = col_x[col[t]]
    y0b = out_y2[s]; y0t = y0b + h
    y1b = in_y2[t];  y1t = y1b + h
    out_y2[s] = y0t
    in_y2[t]  = y1t
    xm = (x0 + x1) / 2
    ym = ((y0b + y0t) / 2 + (y1b + y1t) / 2) / 2
    ax.text(xm, ym, str(v), ha='center', va='center',
            fontsize=7.5, color='#333333', zorder=5,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.6, pad=1))

ax.set_title('Dataset Preparation Flow', fontsize=13, fontweight='bold',
             pad=10, color='#222222')

plt.tight_layout(pad=0.4)
plt.savefig('figure.pdf', dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig('figure.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig('figure.svg', bbox_inches='tight', facecolor='white')
print('Saved figure.pdf, figure.png, figure.svg')
