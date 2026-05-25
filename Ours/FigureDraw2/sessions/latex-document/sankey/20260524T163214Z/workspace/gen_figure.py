import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

with open('data.json') as f:
    data = json.load(f)

nodes_list = data['nodes']
links = data['links']

# Column assignment (left-to-right pipeline stages)
col = {
    'Raw': 0, 'Cleaned': 1, 'Filtered': 2, 'Reject': 2,
    'Train': 3, 'Val': 3, 'Test': 3,
}
col_nodes = {
    0: ['Raw'],
    1: ['Cleaned'],
    2: ['Filtered', 'Reject'],
    3: ['Train', 'Val', 'Test'],
}

# Compute per-node flow totals
outflow = {n: 0 for n in nodes_list}
inflow  = {n: 0 for n in nodes_list}
for lk in links:
    outflow[lk['source']] += lk['value']
    inflow[lk['target']]  += lk['value']

# Node height = inflow for non-source nodes, outflow for source nodes
node_h = {}
for n in nodes_list:
    node_h[n] = outflow[n] if inflow[n] == 0 else inflow[n]

SCALE  = 1.0 / 1250   # map flow units → figure units
COL_X  = {0: 0.08, 1: 0.36, 2: 0.64, 3: 0.88}
NODE_W = 0.018
GAP    = 0.045

# Vertical positions (centered per column)
node_y = {}
for c, cnodes in col_nodes.items():
    total = sum(node_h[n] * SCALE for n in cnodes) + GAP * (len(cnodes) - 1)
    y = (1.0 - total) / 2
    for n in cnodes:
        node_y[n] = y
        y += node_h[n] * SCALE + GAP

# Colors
node_color = {
    'Raw':     '#4878CF',
    'Cleaned': '#6ACC65',
    'Filtered':'#D65F5F',
    'Train':   '#B47CC7',
    'Val':     '#C4AD66',
    'Test':    '#77BEDB',
    'Reject':  '#AAAAAA',
}
flow_color = {
    'Raw':     '#4878CF',
    'Cleaned': '#6ACC65',
    'Filtered':'#D65F5F',
}

fig, ax = plt.subplots(figsize=(11, 6))

out_y = {n: node_y[n] for n in nodes_list}
in_y  = {n: node_y[n] for n in nodes_list}

def bezier_band(ax, x0, x1, y0b, y1b, h, color, alpha=0.42):
    cx = (x0 + x1) / 2
    verts = [
        (x0, y0b + h),
        (cx, y0b + h), (cx, y1b + h), (x1, y1b + h),
        (x1, y1b),
        (cx, y1b), (cx, y0b), (x0, y0b),
        (x0, y0b + h),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    ax.add_patch(patches.PathPatch(
        Path(verts, codes), facecolor=color, edgecolor='none', alpha=alpha, zorder=1
    ))

for lk in links:
    src, tgt, val = lk['source'], lk['target'], lk['value']
    h  = val * SCALE
    x0 = COL_X[col[src]] + NODE_W
    x1 = COL_X[col[tgt]]
    bezier_band(ax, x0, x1, out_y[src], in_y[tgt], h, flow_color.get(src, '#888888'))
    out_y[src] += h
    in_y[tgt]  += h

# Draw nodes and labels
for n in nodes_list:
    x = COL_X[col[n]]
    y = node_y[n]
    h = node_h[n] * SCALE
    ax.add_patch(patches.Rectangle(
        (x, y), NODE_W, h,
        facecolor=node_color[n], edgecolor='white', linewidth=0.8, zorder=3
    ))
    lx = x + NODE_W + 0.012
    ax.text(lx, y + h / 2, f'{n}\n{node_h[n]:,}',
            va='center', ha='left', fontsize=9, fontweight='bold',
            color='#222222', zorder=4)

ax.set_xlim(-0.02, 1.12)
ax.set_ylim(-0.06, 1.08)
ax.axis('off')
ax.set_title('Dataset Preparation Flow', fontsize=14, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig('figure.pdf', bbox_inches='tight', dpi=150)
plt.savefig('figure.png', bbox_inches='tight', dpi=150)
plt.savefig('figure.svg', bbox_inches='tight')
plt.close()
print("Saved: figure.pdf  figure.png  figure.svg")
