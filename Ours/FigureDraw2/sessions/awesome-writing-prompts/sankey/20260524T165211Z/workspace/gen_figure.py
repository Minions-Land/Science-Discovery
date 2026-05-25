import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path

with open('data.json') as f:
    data = json.load(f)

nodes_list = data['nodes']
links = data['links']

node_in  = {n: 0 for n in nodes_list}
node_out = {n: 0 for n in nodes_list}
for lk in links:
    node_out[lk['source']] += lk['value']
    node_in[lk['target']]  += lk['value']

node_total = {n: max(node_in[n], node_out[n]) for n in nodes_list}

columns = {'Raw': 0, 'Cleaned': 1, 'Filtered': 2,
           'Train': 3, 'Val': 3, 'Test': 3, 'Reject': 3}

col_x = {0: 0.08, 1: 0.35, 2: 0.60, 3: 0.87}
node_width = 0.022
scale = 1200.0
gap = 0.025

node_colors = {
    'Raw':     '#2166AC',
    'Cleaned': '#4DAC26',
    'Filtered':'#D01C8B',
    'Train':   '#7B2D8B',
    'Val':     '#E6AB02',
    'Test':    '#1B9E77',
    'Reject':  '#888888',
}
link_colors = {
    'Raw':     '#2166AC',
    'Cleaned': '#4DAC26',
    'Filtered':'#D01C8B',
}

col_nodes = {
    0: ['Raw'],
    1: ['Cleaned'],
    2: ['Filtered'],
    3: ['Train', 'Val', 'Test', 'Reject'],
}

node_h = {n: node_total[n] / scale for n in nodes_list}

node_y = {}
for col, col_node_list in col_nodes.items():
    total_h   = sum(node_h[n] for n in col_node_list)
    total_gap = gap * (len(col_node_list) - 1)
    y = (1.0 - total_h - total_gap) / 2
    for n in col_node_list:
        node_y[n] = y
        y += node_h[n] + gap

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor('#F8F8F8')
ax.set_facecolor('#F8F8F8')

node_out_off = {n: 0.0 for n in nodes_list}
node_in_off  = {n: 0.0 for n in nodes_list}

for lk in links:
    src, tgt, val = lk['source'], lk['target'], lk['value']
    sx = col_x[columns[src]] + node_width / 2
    tx = col_x[columns[tgt]] - node_width / 2
    fh = val / scale
    cx = (sx + tx) / 2

    sy0 = node_y[src] + node_out_off[src];  sy1 = sy0 + fh
    ty0 = node_y[tgt] + node_in_off[tgt];   ty1 = ty0 + fh
    node_out_off[src] += fh
    node_in_off[tgt]  += fh

    verts = [
        (sx, sy0), (cx, sy0), (cx, ty0), (tx, ty0),
        (tx, ty1), (cx, ty1), (cx, sy1), (sx, sy1),
        (sx, sy0),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    color = link_colors.get(src, '#aaaaaa')
    ax.add_patch(mpatches.PathPatch(
        Path(verts, codes), facecolor=color, alpha=0.35,
        edgecolor='none', zorder=1))

for n in nodes_list:
    col = columns[n]
    x, y, h = col_x[col], node_y[n], node_h[n]
    ax.add_patch(plt.Rectangle(
        (x - node_width/2, y), node_width, h,
        facecolor=node_colors[n], edgecolor='white',
        linewidth=0.8, zorder=3))
    label = f'{n}\n{node_total[n]:,}'
    if col < 3:
        ax.text(x - node_width/2 - 0.012, y + h/2, label,
                ha='right', va='center', fontsize=8.5, fontweight='bold',
                color=node_colors[n])
    else:
        ax.text(x + node_width/2 + 0.012, y + h/2, label,
                ha='left', va='center', fontsize=8.5, fontweight='bold',
                color=node_colors[n])

ax.set_title('Dataset Preparation Flow', fontsize=13, fontweight='bold', pad=12)

plt.tight_layout(pad=1.5)
for ext in ('pdf', 'png', 'svg'):
    plt.savefig(f'figure.{ext}', bbox_inches='tight',
                dpi=150, facecolor=fig.get_facecolor())
print("Saved figure.pdf, figure.png, figure.svg")
