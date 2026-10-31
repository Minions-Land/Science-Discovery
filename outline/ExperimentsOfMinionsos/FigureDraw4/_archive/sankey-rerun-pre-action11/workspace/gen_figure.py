import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path

with open('data.json') as f:
    data = json.load(f)

nodes_list = data['nodes']
links = data['links']

columns = {'Raw': 0, 'Cleaned': 1, 'Filtered': 2, 'Train': 3, 'Val': 3, 'Test': 3, 'Reject': 3}
col_nodes = {0: ['Raw'], 1: ['Cleaned'], 2: ['Filtered'], 3: ['Train', 'Val', 'Test', 'Reject']}

inflow = {n: 0 for n in nodes_list}
outflow = {n: 0 for n in nodes_list}
for lk in links:
    outflow[lk['source']] += lk['value']
    inflow[lk['target']] += lk['value']

def node_flow(n):
    return outflow[n] if inflow[n] == 0 else inflow[n]

total = node_flow('Raw')

node_w = 0.055
col_x = {0: 0.05, 1: 0.31, 2: 0.57, 3: 0.83}
gap = 0.02

node_y = {}
node_hh = {}

for col, col_node_list in col_nodes.items():
    heights = [node_flow(n) / total for n in col_node_list]
    n_gaps = len(col_node_list) - 1
    total_h = sum(heights) + n_gaps * gap
    y = (1.0 - total_h) / 2
    for n, h in zip(col_node_list, heights):
        node_y[n] = y
        node_hh[n] = h
        y += h + gap

node_colors = {
    'Raw': '#2166AC', 'Cleaned': '#1A9641', 'Filtered': '#D01C8B',
    'Train': '#7B2D8B', 'Val': '#E6A817', 'Test': '#2CA02C', 'Reject': '#888888',
}
flow_colors = {'Raw': '#2166AC', 'Cleaned': '#1A9641', 'Filtered': '#D01C8B'}

out_y = {n: node_y[n] for n in nodes_list}
in_y  = {n: node_y[n] for n in nodes_list}

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor('white')

for lk in links:
    src, tgt, val = lk['source'], lk['target'], lk['value']
    h = val / total
    x0 = col_x[columns[src]] + node_w
    x1 = col_x[columns[tgt]]
    cx = (x0 + x1) / 2
    y0b, y1b = out_y[src], in_y[tgt]
    y0t, y1t = y0b + h, y1b + h
    out_y[src] += h
    in_y[tgt]  += h

    verts = [
        (x0, y0b), (cx, y0b), (cx, y1b), (x1, y1b),
        (x1, y1t), (cx, y1t), (cx, y0t), (x0, y0t), (x0, y0b),
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    color = flow_colors.get(src, '#888888')
    ax.add_patch(mpatches.PathPatch(Path(verts, codes),
                                    facecolor=color, edgecolor='none', alpha=0.35))

for n in nodes_list:
    x = col_x[columns[n]]
    y = node_y[n]
    h = node_hh[n]
    ax.add_patch(plt.Rectangle((x, y), node_w, h,
                                facecolor=node_colors[n], edgecolor='white',
                                linewidth=0.8, zorder=3))
    val_disp = node_flow(n)
    col = columns[n]
    if col == 3:
        ax.text(x + node_w + 0.012, y + h / 2, f'{n}  {val_disp:,}',
                ha='left', va='center', fontsize=8.5, fontweight='bold',
                color=node_colors[n], zorder=4)
    elif col == 0:
        ax.text(x - 0.012, y + h / 2, f'{val_disp:,}  {n}',
                ha='right', va='center', fontsize=8.5, fontweight='bold',
                color=node_colors[n], zorder=4)
    else:
        ax.text(x + node_w / 2, y + h / 2, f'{n}\n{val_disp:,}',
                ha='center', va='center', fontsize=7.5, fontweight='bold',
                color='white', zorder=4)

for col, label in {0: 'Raw Data', 1: 'Cleaned', 2: 'Filtered', 3: 'Split'}.items():
    ax.text(col_x[col] + node_w / 2, 0.96, label,
            ha='center', va='top', fontsize=9, color='#555555', style='italic')

ax.set_title('Dataset Preparation Flow', fontsize=12, fontweight='bold',
             color='#222222', pad=8)

plt.tight_layout(pad=0.5)
plt.savefig('figure.pdf', bbox_inches='tight', dpi=150)
plt.savefig('figure.png', bbox_inches='tight', dpi=150)
plt.savefig('figure.svg', bbox_inches='tight')
plt.close()
print("Done.")
