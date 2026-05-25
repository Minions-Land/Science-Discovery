import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

with open('data.json') as f:
    data = json.load(f)

# ── layout positions (x, y) ──────────────────────────────────────────────────
pos = {
    'input':  (0.50, 0.88),
    'retrieve': (0.35, 0.64),
    'db':       (0.35, 0.42),
    'diff':     (0.65, 0.64),
    'prior':    (0.65, 0.42),
    'output':   (0.50, 0.10),
}

BOX_W, BOX_H = 0.18, 0.09
DS_R = 0.045   # datastore ellipse radius
FONT = 9

# ── style per kind ────────────────────────────────────────────────────────────
STYLE = {
    'input':     dict(fc='#D6EAF8', ec='#2874A6', lw=1.5),
    'output':    dict(fc='#D5F5E3', ec='#1E8449', lw=1.5),
    'module':    dict(fc='#FDFEFE', ec='#555555', lw=1.2),
    'datastore': dict(fc='#FEF9E7', ec='#B7950B', lw=1.2),
}

GROUP_STYLE = dict(fc='#F4F6F7', ec='#AAB7B8', lw=1.0, ls='--', alpha=0.55)

fig, ax = plt.subplots(figsize=(5.0, 5.5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_aspect('equal')

# ── helper: center bbox of a node ─────────────────────────────────────────────
def bbox(nid):
    x, y = pos[nid]
    return x - BOX_W / 2, y - BOX_H / 2, BOX_W, BOX_H

def node_center(nid):
    return pos[nid]

def node_edge(nid, direction):
    """Return the point on the edge of a node in a given direction ('N','S','E','W')."""
    x, y = pos[nid]
    if direction == 'N': return (x, y + BOX_H / 2)
    if direction == 'S': return (x, y - BOX_H / 2)
    if direction == 'E': return (x + BOX_W / 2, y)
    if direction == 'W': return (x - BOX_W / 2, y)

# ── draw group backgrounds ────────────────────────────────────────────────────
for g in data['groups']:
    xs = [pos[n][0] for n in g['node_ids']]
    ys = [pos[n][1] for n in g['node_ids']]
    pad = 0.05
    gx = min(xs) - BOX_W / 2 - pad
    gy = min(ys) - BOX_H / 2 - pad
    gw = max(xs) - min(xs) + BOX_W + 2 * pad
    gh = max(ys) - min(ys) + BOX_H + 2 * pad
    rect = FancyBboxPatch((gx, gy), gw, gh,
                          boxstyle='round,pad=0.015',
                          **GROUP_STYLE,
                          zorder=0)
    ax.add_patch(rect)
    ax.text(gx + gw / 2, gy + gh + 0.005, g['label'],
            ha='center', va='bottom', fontsize=7.5,
            color='#555555', style='italic')

# ── draw nodes ────────────────────────────────────────────────────────────────
id_to_label = {s['id']: s['label'] for s in data['stages']}
id_to_kind  = {s['id']: s['kind']  for s in data['stages']}

for stage in data['stages']:
    nid   = stage['id']
    kind  = stage['kind']
    label = stage['label']
    x, y  = pos[nid]
    st    = STYLE[kind]

    if kind == 'datastore':
        # cylinder-like: ellipse
        ell = mpatches.Ellipse((x, y), BOX_W, BOX_H * 0.75,
                               fc=st['fc'], ec=st['ec'], lw=st['lw'], zorder=2)
        ax.add_patch(ell)
    else:
        bx, by, bw, bh = bbox(nid)
        rect = FancyBboxPatch((bx, by), bw, bh,
                              boxstyle='round,pad=0.012',
                              fc=st['fc'], ec=st['ec'], lw=st['lw'], zorder=2)
        ax.add_patch(rect)

    ax.text(x, y, label, ha='center', va='center',
            fontsize=FONT, fontweight='bold' if kind in ('input', 'output') else 'normal',
            zorder=3)

# ── draw arrows ───────────────────────────────────────────────────────────────
ARROW_KW = dict(arrowstyle='->', color='#222222', lw=1.2,
                connectionstyle='arc3,rad=0.0', zorder=4,
                mutation_scale=12)

def draw_arrow(src, dst, style='solid', color='#222222'):
    sx, sy = pos[src]
    dx, dy = pos[dst]

    # choose entry/exit edges
    if abs(sx - dx) < 0.01:   # vertical
        sp = (sx, sy - BOX_H / 2)
        dp = (dx, dy + BOX_H / 2)
    elif sy > dy:
        sp = (sx - BOX_W / 2 if dx < sx else sx + BOX_W / 2, sy)
        dp = (dx + BOX_W / 2 if dx < sx else dx - BOX_W / 2, dy)
    else:
        sp = (sx, sy + BOX_H / 2)
        dp = (dx, dy - BOX_H / 2)

    ls = 'dashed' if style == 'dashed' else 'solid'
    arr = FancyArrowPatch(sp, dp,
                          arrowstyle='->', color=color,
                          linewidth=1.2,
                          linestyle=ls,
                          connectionstyle='arc3,rad=0.0',
                          mutation_scale=12, zorder=4)
    ax.add_patch(arr)

for stage in data['stages']:
    for src_id in stage.get('arrows', []):
        dst_id = stage['id']
        # db ↔ retrieve is a lookup (feedback) → dashed
        is_feedback = (src_id == 'retrieve' and dst_id == 'db') or \
                      (src_id == 'db'       and dst_id == 'retrieve')
        draw_arrow(src_id, dst_id,
                   style='dashed' if is_feedback else 'solid')

# db feeds back into diff (knowledge) — dashed feedback arrow
arr_fb = FancyArrowPatch(
    (pos['db'][0] + BOX_W / 2, pos['db'][1]),
    (pos['diff'][0] - BOX_W / 2, pos['diff'][1]),
    arrowstyle='->', color='#888888',
    linewidth=1.0, linestyle='dashed',
    connectionstyle='arc3,rad=-0.25',
    mutation_scale=11, zorder=4)
ax.add_patch(arr_fb)

# prior feeds back into diff — dashed
arr_pr = FancyArrowPatch(
    (pos['prior'][0], pos['prior'][1] + BOX_H / 2),
    (pos['diff'][0],  pos['diff'][1]  - BOX_H / 2),
    arrowstyle='->', color='#888888',
    linewidth=1.0, linestyle='dashed',
    connectionstyle='arc3,rad=0.0',
    mutation_scale=11, zorder=4)
ax.add_patch(arr_pr)

# ── title ─────────────────────────────────────────────────────────────────────
ax.set_title(data['system_name'], fontsize=12, fontweight='bold', pad=6)

# ── legend ────────────────────────────────────────────────────────────────────
leg_handles = [
    mpatches.Patch(fc='white', ec='black', lw=1.2, label='Solid: data flow'),
    mpatches.Patch(fc='white', ec='#888888', lw=1.0, linestyle='--', label='Dashed: control/feedback'),
]
ax.legend(handles=leg_handles, loc='lower center', fontsize=7,
          framealpha=0.8, edgecolor='#CCCCCC',
          bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
fig.savefig('figure.pdf', bbox_inches='tight', dpi=150)
fig.savefig('figure.png', bbox_inches='tight', dpi=150)
fig.savefig('figure.svg', bbox_inches='tight')
print("Saved figure.pdf, figure.png, figure.svg")
