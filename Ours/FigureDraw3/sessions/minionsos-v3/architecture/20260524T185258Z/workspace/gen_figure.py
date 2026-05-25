#!/usr/bin/env python3
"""gen_figure.py — Architecture diagram for RetroDiff (data.json)"""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse
from matplotlib.lines import Line2D

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8,
    'pdf.fonttype': 42,
    'svg.fonttype': 'none',
})

with open('data.json') as f:
    data = json.load(f)

fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11)
ax.set_ylim(0, 5)
ax.axis('off')

pos = {
    'input':    (1.2,  3.5),
    'retrieve': (3.7,  3.5),
    'db':       (3.7,  1.9),
    'diff':     (6.9,  3.5),
    'prior':    (6.9,  1.9),
    'output':   (9.5,  3.5),
}
node_w = {
    'input': 1.4, 'retrieve': 1.5, 'db': 1.3,
    'diff': 1.9, 'prior': 1.7, 'output': 1.9,
}
NODE_H = 0.55

labels = {s['id']: s['label'] for s in data['stages']}
kinds  = {s['id']: s['kind']  for s in data['stages']}

node_fc = {
    'input': '#F8FAFC', 'retrieve': '#DBEAFE', 'db': '#FEF3C7',
    'diff': '#EDE9FE', 'prior': '#DDD6FE', 'output': '#F0FDF4',
}
node_ec = {
    'input': '#475569', 'retrieve': '#1D4ED8', 'db': '#92400E',
    'diff': '#5B21B6', 'prior': '#4C1D95', 'output': '#14532D',
}

# Group backgrounds
group_specs = {
    'Retrieval':  {'x0': 2.65, 'y0': 1.15, 'x1': 4.85, 'y1': 4.25,
                   'fc': '#EFF6FF', 'ec': '#93C5FD'},
    'Generation': {'x0': 5.65, 'y0': 1.15, 'x1': 8.05, 'y1': 4.25,
                   'fc': '#F5F3FF', 'ec': '#A78BFA'},
}
for gname, g in group_specs.items():
    w, h = g['x1'] - g['x0'], g['y1'] - g['y0']
    ax.add_patch(FancyBboxPatch(
        (g['x0'], g['y0']), w, h,
        boxstyle='round,pad=0.15',
        facecolor=g['fc'], edgecolor=g['ec'],
        linewidth=1.2, linestyle='--', zorder=1, alpha=0.85
    ))
    ax.text(g['x0'] + w/2, g['y1'] + 0.12, gname,
            ha='center', va='bottom', fontsize=7.5, fontweight='bold',
            color='#475569', zorder=3)

# Draw nodes
def node_box(ax, nid):
    cx, cy = pos[nid]
    w, h = node_w[nid], NODE_H
    fc, ec = node_fc[nid], node_ec[nid]

    if kinds[nid] == 'datastore':
        ell_h = 0.18
        # Body (rectangle, no top rounding)
        ax.add_patch(plt.Polygon(
            [(cx - w/2, cy - h/2),
             (cx + w/2, cy - h/2),
             (cx + w/2, cy + h/2 - ell_h/2),
             (cx - w/2, cy + h/2 - ell_h/2)],
            closed=True, facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=4
        ))
        # Bottom ellipse cap
        ax.add_patch(Ellipse((cx, cy - h/2), w, ell_h,
                             facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=5))
        # Top ellipse cap
        ax.add_patch(Ellipse((cx, cy + h/2 - ell_h/2), w, ell_h,
                             facecolor='#FDE68A', edgecolor=ec, linewidth=1.5, zorder=5))
    else:
        ax.add_patch(FancyBboxPatch(
            (cx - w/2, cy - h/2), w, h,
            boxstyle='round,pad=0.08',
            facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=4
        ))

    ax.text(cx, cy, labels[nid],
            ha='center', va='center', fontsize=8, fontweight='bold',
            color='#1E293B', zorder=6)

for nid in pos:
    node_box(ax, nid)

# Edge helpers
def edge_pt(nid, side):
    cx, cy = pos[nid]
    w, h = node_w[nid], NODE_H
    return {
        'right':  (cx + w/2, cy),
        'left':   (cx - w/2, cy),
        'bottom': (cx, cy - h/2),
        'top':    (cx, cy + h/2),
    }[side]

def arrow(src, tgt, s_side, t_side, dashed=False):
    x0, y0 = edge_pt(src, s_side)
    x1, y1 = edge_pt(tgt, t_side)
    ls = 'dashed' if dashed else 'solid'
    col = '#64748B' if dashed else '#1E293B'
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(
                    arrowstyle='->', color=col, lw=1.4,
                    linestyle=ls,
                    connectionstyle='arc3,rad=0',
                    mutation_scale=12,
                ), zorder=7)

arrow('input',    'retrieve', 'right',  'left')
arrow('retrieve', 'db',       'bottom', 'top')
arrow('retrieve', 'diff',     'right',  'left')
arrow('diff',     'prior',    'bottom', 'top',  dashed=True)
arrow('diff',     'output',   'right',  'left')

# Legend
ax.legend(handles=[
    Line2D([0], [0], color='#1E293B', lw=1.4, label='Data flow'),
    Line2D([0], [0], color='#64748B', lw=1.4, linestyle='--', label='Control / feedback'),
], loc='lower left', fontsize=7, frameon=True, framealpha=0.9,
   edgecolor='#CBD5E1', bbox_to_anchor=(0.01, 0.02))

fig.savefig('figure.pdf', bbox_inches='tight')
fig.savefig('figure.png', bbox_inches='tight', dpi=150)
fig.savefig('figure.svg', bbox_inches='tight')
plt.close()
print("Done: figure.pdf  figure.png  figure.svg")
