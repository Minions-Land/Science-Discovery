import json
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.size'] = 8
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open('data.json') as f:
    data = json.load(f)

benchmarks = data['benchmarks']
methods = data['methods']
values = data['values']

means = {m: [values[m][b]['mean'] for b in benchmarks] for m in methods}
stds  = {m: [values[m][b]['std']  for b in benchmarks] for m in methods}

# Nature single-column: 89 mm wide
fig_width_in = 89 / 25.4
fig_height_in = fig_width_in * 0.72
fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))

n_methods = len(methods)
n_benchmarks = len(benchmarks)
bar_width = 0.18
group_gap = 0.06
group_width = n_methods * bar_width + group_gap
x = np.arange(n_benchmarks) * (group_width + 0.15)

# Colorblind-friendly palette (Wong 2011) — last entry bold/dark for OursModel
palette = ['#999999', '#56B4E9', '#E69F00', '#D55E00']
hatches = ['', '///', '...', '']  # extra B&W discriminability

winner = data.get('winner_overall', 'OursModel')

bars_handles = []
for i, method in enumerate(methods):
    offsets = x + i * bar_width - (n_methods - 1) * bar_width / 2
    color = palette[i]
    lw = 1.4 if method == winner else 0.8
    edgecolor = '#111111' if method == winner else '#444444'
    b = ax.bar(
        offsets,
        means[method],
        width=bar_width,
        yerr=stds[method],
        color=color,
        hatch=hatches[i],
        edgecolor=edgecolor,
        linewidth=lw,
        error_kw=dict(elinewidth=0.8, capsize=2.0, ecolor='#222222', capthick=0.8),
        label=method,
        zorder=3,
    )
    bars_handles.append(b)

# Reasonable y-range: all values > 28; floor at max(0, min_mean - padding)
all_means = [v for m in methods for v in means[m]]
all_stds  = [v for m in methods for v in stds[m]]
y_min = max(0, min(all_means) - max(all_stds) - 4)
y_max = max(all_means) + max(all_stds) + 5
ax.set_ylim(y_min, y_max)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7.5)
ax.set_ylabel('Accuracy (%)', fontsize=8)
ax.yaxis.set_tick_params(labelsize=7)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linewidth=0.4, linestyle='--', color='#cccccc', zorder=0)

# Legend — bold winner label
legend_labels = [m + ' ★' if m == winner else m for m in methods]
legend = ax.legend(
    bars_handles,
    legend_labels,
    fontsize=6.5,
    ncol=2,
    frameon=False,
    loc='upper left',
    handlelength=1.2,
    handletextpad=0.4,
    columnspacing=0.8,
)
for text, method in zip(legend.get_texts(), methods):
    if method == winner:
        text.set_fontweight('bold')

fig.tight_layout(pad=0.4)

fig.savefig('figure.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')
print('Saved figure.pdf, figure.png, figure.svg')
