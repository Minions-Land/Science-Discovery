import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.stats import gaussian_kde
from pathlib import Path

# Mandatory Nature-style rcParams
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.size'] = 8
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['legend.frameon'] = False

# Load data
with open('data.json') as f:
    data = json.load(f)

clusters = data['clusters']
samples = data['samples']
x_label = data['x_label']

# Palette: sequential cool-to-warm across 6 clusters
COLORS = [
    '#0F4D92',  # deep blue     — Cluster 1
    '#3775BA',  # medium blue   — Cluster 2
    '#42949E',  # teal          — Cluster 3
    '#8BCF8B',  # green         — Cluster 4
    '#E9A6A1',  # rose          — Cluster 5
    '#B64342',  # red           — Cluster 6
]

n_clusters = len(clusters)
x_min = min(min(v) for v in samples.values()) - 0.2
x_max = max(max(v) for v in samples.values()) + 0.2
x_grid = np.linspace(x_min, x_max, 512)

# Vertical offset between ridges
overlap = 0.55          # fraction of max KDE height used for spacing
kde_densities = []
for cl in clusters:
    vals = np.array(samples[cl])
    kde = gaussian_kde(vals, bw_method='scott')
    dens = kde(x_grid)
    kde_densities.append(dens)

max_density = max(d.max() for d in kde_densities)
v_step = max_density * (1 - overlap + 0.2)   # vertical step per cluster

fig_width = 3.5       # single-column Nature width (inches)
fig_height = 3.2
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

for i, (cl, dens, color) in enumerate(zip(clusters, kde_densities, COLORS)):
    offset = i * v_step
    y_base = offset * np.ones_like(x_grid)
    y_top  = offset + dens

    # Filled area under KDE
    ax.fill_between(x_grid, y_base, y_top,
                    color=color, alpha=0.72, linewidth=0)
    # KDE line
    ax.plot(x_grid, y_top, color=color, linewidth=0.9)
    # Baseline
    ax.plot(x_grid, y_base, color='white', linewidth=0.5, zorder=3)

    # Cluster label on the left
    ax.text(x_min - 0.05, offset + dens.max() * 0.45,
            cl, ha='right', va='center',
            fontsize=7, color=color, fontweight='bold')

# Axes clean-up
ax.set_xlim(x_min, x_max)
ax.set_ylim(-v_step * 0.15, (n_clusters - 1) * v_step + max_density * 1.15)
ax.set_xlabel(x_label, fontsize=8)
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='x', labelsize=7)

fig.tight_layout(pad=1.2)

out = Path('figure')
fig.savefig(str(out) + '.svg', bbox_inches='tight')
fig.savefig(str(out) + '.pdf', bbox_inches='tight')
fig.savefig(str(out) + '.png', dpi=300, bbox_inches='tight')
plt.close(fig)

print("Saved: figure.svg, figure.pdf, figure.png")
