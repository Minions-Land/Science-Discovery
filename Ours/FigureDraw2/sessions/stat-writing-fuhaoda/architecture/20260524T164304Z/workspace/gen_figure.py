import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

with open('data.json') as f:
    data = json.load(f)

# ── layout ──────────────────────────────────────────────────────────────────
positions = {
    'input':   (1.4, 3.5),
    'retrieve': (4.2, 3.5),
    'db':       (4.2, 1.7),
    'diff':     (7.8, 3.5),
    'prior':    (7.8, 1.7),
    'output':   (11.2, 3.5),
}

node_sizes = {          # (width, height)
    'input':   (1.5, 0.72),
    'retrieve': (1.6, 0.72),
    'db':       (1.3, 0.72),
    'diff':     (2.0, 0.72),
    'prior':    (1.8, 0.72),
    'output':   (1.9, 0.72),
}

fill_colors = {
    'input':     '#D6EAF8',
    'output':    '#D5F5E3',
    'module':    '#FDEBD0',
    'datastore': '#E8DAEF',
}
edge_colors = {
    'input':     '#2471A3',
    'output':    '#1E8449',
    'module':    '#CA6F1E',
    'datastore': '#7D3C98',
}

fig, ax = plt.subplots(figsize=(13.5, 5.5))
ax.set_xlim(0, 13.5)
ax.set_ylim(0.6, 5.4)
ax.axis('off')
fig.patch.set_facecolor('white')

# ── group backgrounds ────────────────────────────────────────────────────────
groups_coords = {
    'Retrieval':  (2.9, 0.95, 5.6, 4.65),   # x1,y1,x2,y2
    'Generation': (6.5, 0.95, 9.2, 4.65),
}
group_colors = {
    'Retrieval':  ('#EBF5FB', '#5DADE2', '#2E86C1'),
    'Generation': ('#FEF9E7', '#F5CBA7', '#D68910'),
}

for gname, (x1, y1, x2, y2) in groups_coords.items():
    fc, ec, tc = group_colors[gname]
    ax.add_patch(FancyBboxPatch(
        (x1, y1), x2 - x1, y2 - y1,
        boxstyle='round,pad=0.15',
        facecolor=fc, edgecolor=ec, linewidth=1.6, linestyle='--', zorder=1
    ))
    ax.text((x1 + x2) / 2, y2 - 0.18, gname,
            ha='center', va='top', fontsize=9.5, color=tc,
            fontweight='bold', zorder=2)

# ── helper: edge attachment point ───────────────────────────────────────────
def attach(node_id, side):
    x, y = positions[node_id]
    w, h = node_sizes[node_id]
    if side == 'right':  return (x + w / 2, y)
    if side == 'left':   return (x - w / 2, y)
    if side == 'top':    return (x, y + h / 2)
    if side == 'bottom': return (x, y - h / 2)

# ── draw arrows ──────────────────────────────────────────────────────────────
arrow_kw = dict(arrowstyle='->', color='#2C3E50', lw=1.6, mutation_scale=16)

def arrow(src, src_side, dst, dst_side, dashed=False, rad=0.0):
    sx, sy = attach(src, src_side)
    dx, dy = attach(dst, dst_side)
    ls = 'dashed' if dashed else 'solid'
    ax.annotate('', xy=(dx, dy), xytext=(sx, sy),
        arrowprops=dict(**arrow_kw,
                        connectionstyle=f'arc3,rad={rad}',
                        linestyle=ls),
        zorder=4)

arrow('input',   'right',  'retrieve', 'left')
arrow('retrieve','bottom', 'db',       'top')
arrow('retrieve','right',  'diff',     'left')
arrow('diff',    'bottom', 'prior',    'top')
arrow('diff',    'right',  'output',   'left')

# ── draw nodes ───────────────────────────────────────────────────────────────
stage_map = {s['id']: s for s in data['stages']}

for sid, (cx, cy) in positions.items():
    stage = stage_map[sid]
    kind  = stage['kind']
    label = stage['label']
    w, h  = node_sizes[sid]
    fc = fill_colors.get(kind, '#FDFEFE')
    ec = edge_colors.get(kind, '#555555')

    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.10',
        facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3
    )
    ax.add_patch(patch)

    # cylinder hint for datastore
    if kind == 'datastore':
        ax.plot([cx - w / 2 + 0.08, cx + w / 2 - 0.08],
                [cy + h / 2 - 0.08, cy + h / 2 - 0.08],
                color=ec, lw=0.9, zorder=4)

    ax.text(cx, cy, label, ha='center', va='center',
            fontsize=8.8, fontweight='bold', color='#1A1A1A', zorder=5)

# ── title ────────────────────────────────────────────────────────────────────
ax.set_title(data['system_name'] + ' — System Architecture',
             fontsize=13, fontweight='bold', pad=8, color='#1A1A1A')

# ── legend ───────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(facecolor='#D6EAF8', edgecolor='#2471A3', label='Input'),
    mpatches.Patch(facecolor='#FDEBD0', edgecolor='#CA6F1E', label='Module'),
    mpatches.Patch(facecolor='#E8DAEF', edgecolor='#7D3C98', label='Datastore'),
    mpatches.Patch(facecolor='#D5F5E3', edgecolor='#1E8449', label='Output'),
]
ax.legend(handles=legend_items, loc='lower right', fontsize=8,
          framealpha=0.85, edgecolor='#CCCCCC', ncol=4,
          bbox_to_anchor=(1.0, 0.0))

plt.tight_layout(pad=0.4)
plt.savefig('figure.pdf', bbox_inches='tight', dpi=150)
plt.savefig('figure.png', bbox_inches='tight', dpi=150)
plt.savefig('figure.svg', bbox_inches='tight')
plt.close()
print("Saved: figure.pdf  figure.png  figure.svg")
