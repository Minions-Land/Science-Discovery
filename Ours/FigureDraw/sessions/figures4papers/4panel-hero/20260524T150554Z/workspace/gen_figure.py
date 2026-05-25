import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

with open('data.json') as f:
    data = json.load(f)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 8,
    'axes.labelsize': 8,
    'axes.titlesize': 9,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
})

fig = plt.figure(figsize=(11, 6.5))
gs = gridspec.GridSpec(2, 3, width_ratios=[2, 1, 1], figure=fig,
                       hspace=0.50, wspace=0.38,
                       left=0.07, right=0.97, top=0.93, bottom=0.09)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_d = fig.add_subplot(gs[1, :])

BLUE   = '#4C72B0'
GREEN  = '#55A868'
RED    = '#C44E52'
PURPLE = '#8172B2'
LGRAY  = '#AAAAAA'
LBLUE  = '#9DC3E6'

def panel_label(ax, letter, dx=-0.13, dy=1.08):
    ax.text(dx, dy, letter, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top', ha='left',
            fontfamily='DejaVu Sans')

# ── Panel A: Method overview diagram ─────────────────────────────────────────
ax_a.set_xlim(0, 10)
ax_a.set_ylim(0, 6)
ax_a.axis('off')

stages = [
    ('Stage 1', 'Input\nEncoding',   BLUE),
    ('Stage 2', 'Attention\n& Memory', GREEN),
    ('Stage 3', 'Skill\nDecoding',   RED),
]
bw, bh = 2.1, 1.5
yc = 3.2
xs = [0.4, 3.65, 6.9]

for (title, sub, col), x in zip(stages, xs):
    box = FancyBboxPatch((x, yc - bh/2), bw, bh,
                         boxstyle='round,pad=0.12',
                         facecolor=col, edgecolor='white',
                         linewidth=1.8, alpha=0.92, zorder=3)
    ax_a.add_patch(box)
    ax_a.text(x + bw/2, yc + 0.22, title,
              ha='center', va='center', fontsize=8, fontweight='bold',
              color='white', zorder=4)
    ax_a.text(x + bw/2, yc - 0.32, sub,
              ha='center', va='center', fontsize=6.8,
              color='white', alpha=0.92, linespacing=1.3, zorder=4)

# arrows between stages
for x_tip in [2.5, 5.75]:
    ax_a.annotate('', xy=(x_tip + 1.15, yc), xytext=(x_tip, yc),
                  arrowprops=dict(arrowstyle='->', color='#555', lw=1.6),
                  zorder=5)

# output node
ox = 9.25
out = FancyBboxPatch((ox, yc - 0.62), 0.68, 1.24,
                     boxstyle='round,pad=0.1',
                     facecolor=PURPLE, edgecolor='white',
                     linewidth=1.8, alpha=0.92, zorder=3)
ax_a.add_patch(out)
ax_a.text(ox + 0.34, yc, 'Out', ha='center', va='center',
          fontsize=7.5, fontweight='bold', color='white', zorder=4)
ax_a.annotate('', xy=(ox, yc), xytext=(9.0, yc),
              arrowprops=dict(arrowstyle='->', color='#555', lw=1.6), zorder=5)

# residual skip arc (bottom)
ax_a.annotate('', xy=(6.9, yc - bh/2 - 0.05), xytext=(0.4, yc - bh/2 - 0.05),
              arrowprops=dict(arrowstyle='->', color=LGRAY, lw=1.1,
                              connectionstyle='arc3,rad=-0.35'), zorder=2)
ax_a.text(3.65, 1.05, 'residual skip', ha='center', va='top',
          fontsize=6.5, color=LGRAY, style='italic')

# data-flow label at top
ax_a.text(4.85, 5.55, 'Method Overview: 3-Stage Pipeline',
          ha='center', va='top', fontsize=9, fontweight='bold', color='#222')

panel_label(ax_a, 'A', dx=0.01, dy=1.04)

# ── Panel B: Ablation bars ────────────────────────────────────────────────────
b = data['panel_b']
items, vals = b['items'], b['values']
bar_colors = [BLUE if v == max(vals) else LBLUE for v in vals]

bars = ax_b.barh(items, vals, color=bar_colors, edgecolor='white', linewidth=0.6, height=0.6)
ax_b.set_xlabel('Accuracy (%)')
ax_b.set_title('Ablation Study', fontweight='bold', pad=5)
ax_b.set_xlim(50, 68)
ax_b.axvline(vals[0], color=BLUE, linestyle='--', linewidth=0.9, alpha=0.45)

for bar, v in zip(bars, vals):
    ax_b.text(v + 0.25, bar.get_y() + bar.get_height()/2,
              f'{v:.1f}', va='center', ha='left', fontsize=6.5)

panel_label(ax_b, 'B')

# ── Panel C: Training curves ──────────────────────────────────────────────────
c = data['panel_c']
ax_c.plot(c['steps'], c['Baseline'], color=LBLUE, lw=1.6, label='Baseline', alpha=0.9)
ax_c.plot(c['steps'], c['Ours'],     color=RED,   lw=1.6, label='Ours',     alpha=0.9)
ax_c.set_xlabel('Training Step (×10³)')
ax_c.set_ylabel('Loss')
ax_c.set_title('Training Curve', fontweight='bold', pad=5)
ax_c.legend(fontsize=6.5, frameon=False, loc='upper right')

panel_label(ax_c, 'C')

# ── Panel D: 5×5 sensitivity heatmap ─────────────────────────────────────────
d = data['panel_d']
mat = np.array(d['matrix'])
cmap = LinearSegmentedColormap.from_list('wb', ['#f7fbff', '#08519c'])

im = ax_d.imshow(mat, cmap=cmap, aspect='auto', vmin=0, vmax=1)
ax_d.set_xticks(range(len(d['x']))); ax_d.set_xticklabels(d['x'])
ax_d.set_yticks(range(len(d['y']))); ax_d.set_yticklabels(d['y'])
ax_d.set_xlabel('Sweep Parameter S')
ax_d.set_ylabel('Sweep Parameter P')
ax_d.set_title('Sensitivity Sweep (S × P)', fontweight='bold', pad=5)
ax_d.spines[:].set_visible(False)
ax_d.tick_params(length=0)

for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat[i, j]
        ax_d.text(j, i, f'{v:.2f}', ha='center', va='center',
                  fontsize=7.5, color='white' if v > 0.55 else '#222')

cb = fig.colorbar(im, ax=ax_d, orientation='vertical', fraction=0.014, pad=0.01)
cb.set_label('Score', fontsize=7)
cb.ax.tick_params(labelsize=6)

panel_label(ax_d, 'D', dx=-0.035, dy=1.13)

fig.savefig('figure.pdf', bbox_inches='tight', dpi=150)
fig.savefig('figure.png', bbox_inches='tight', dpi=150)
fig.savefig('figure.svg', bbox_inches='tight')
print("Saved figure.pdf, figure.png, figure.svg")
