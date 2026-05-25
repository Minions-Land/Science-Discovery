import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

with open('data.json') as f:
    data = json.load(f)

fig, ax = plt.subplots(figsize=(11, 4.6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 4.6)
ax.axis('off')
fig.patch.set_facecolor('white')

C = {
    'input':    '#E3F2FD',
    'output':   '#FCE4EC',
    'module':   '#FFF8E1',
    'datastore':'#E8F5E9',
    'grp_ret':  '#EDE7F6',
    'grp_gen':  '#E1F5FE',
    'border':   '#37474F',
    'ret_bdr':  '#6A1B9A',
    'gen_bdr':  '#01579B',
    'arrow':    '#212121',
    'ctrl':     '#546E7A',
}

def node(cx, cy, w, h, label, color):
    ax.add_patch(FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.09',
        facecolor=color, edgecolor=C['border'], linewidth=1.5, zorder=3))
    ax.text(cx, cy, label, ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#1A1A1A', zorder=4)

def group(x0, y0, x1, y1, label, fc, ec):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0,
        boxstyle='round,pad=0.18',
        facecolor=fc, edgecolor=ec, linewidth=1.8,
        linestyle='--', alpha=0.55, zorder=1))
    ax.text((x0 + x1) / 2, y1 - 0.13, label,
            ha='center', va='top', fontsize=8.5,
            color=ec, fontstyle='italic', fontweight='bold', zorder=5)

def arrow(x1, y1, x2, y2, dashed=False, rad=0.0, bidir=False):
    style = '<->' if bidir else '->'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle=style,
                    color=C['ctrl'] if dashed else C['arrow'],
                    lw=1.5 if dashed else 1.7,
                    linestyle='dashed' if dashed else 'solid',
                    connectionstyle=f'arc3,rad={rad}',
                ), zorder=5)

# ── group backgrounds ──────────────────────────────────────────────────────────
group(2.25, 0.65, 4.75, 3.55, 'Retrieval',  C['grp_ret'], C['ret_bdr'])
group(6.25, 0.65, 8.75, 3.55, 'Generation', C['grp_gen'], C['gen_bdr'])

# ── nodes ──────────────────────────────────────────────────────────────────────
#          cx     cy    w     h    label               color
node(1.0,  2.3,  1.4,  0.65, 'Query',            C['input'])
node(3.5,  2.75, 1.75, 0.65, 'Retriever',        C['module'])
node(3.5,  1.35, 1.35, 0.65, 'KB',               C['datastore'])
node(7.5,  2.75, 2.05, 0.65, 'Diffusion Decoder',C['module'])
node(7.5,  1.35, 1.75, 0.65, 'Prior Network',    C['module'])
node(10.2, 2.3,  1.5,  0.65, 'Generated\nSample',C['output'])

# ── arrows ─────────────────────────────────────────────────────────────────────
# Query → Retriever
arrow(1.7, 2.3, 2.625, 2.75)
# Retriever ↔ KB  (bidirectional: query + retrieved docs)
arrow(3.5, 2.42, 3.5, 1.68, bidir=True)
# Retriever → Diffusion Decoder
arrow(4.375, 2.75, 6.475, 2.75)
# Diffusion Decoder → Prior Network  (dashed: control / conditioning)
arrow(7.5, 2.42, 7.5, 1.68, dashed=True)
# Diffusion Decoder → Generated Sample
arrow(8.525, 2.75, 9.45, 2.3)

# ── title ──────────────────────────────────────────────────────────────────────
ax.text(5.5, 4.3, data['system_name'],
        ha='center', va='center', fontsize=14,
        fontweight='bold', color='#1A237E')

# ── legend ─────────────────────────────────────────────────────────────────────
ax.legend(handles=[
    Line2D([0], [0], color=C['arrow'], lw=1.7, label='Data flow'),
    Line2D([0], [0], color=C['ctrl'],  lw=1.5, linestyle='dashed',
           label='Control / conditioning'),
], loc='lower right', fontsize=8.5, framealpha=0.85, edgecolor='#B0BEC5')

plt.tight_layout(pad=0.4)
for ext in ('pdf', 'png', 'svg'):
    plt.savefig(f'figure.{ext}', bbox_inches='tight', dpi=150)
plt.close()
print("Saved figure.pdf, figure.png, figure.svg")
