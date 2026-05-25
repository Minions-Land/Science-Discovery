import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.size'] = 8

with open('data.json') as f:
    data = json.load(f)

benchmarks = data['benchmarks']
methods = data['methods']
values = data['values']

# Colorblind-friendly palette (Wong 2011)
COLORS = {
    'Baseline':  '#999999',
    'Method-A':  '#56B4E9',
    'Method-B':  '#E69F00',
    'OursModel': '#009E73',
}
HATCHES = {
    'Baseline':  '',
    'Method-A':  '////',
    'Method-B':  '....',
    'OursModel': 'xxxx',
}

n_benchmarks = len(benchmarks)
n_methods = len(methods)
bar_width = 0.18
group_gap = 0.08
group_width = n_methods * bar_width + group_gap
x = np.arange(n_benchmarks) * group_width

fig, ax = plt.subplots(figsize=(3.5, 2.6))  # single-column: ~3.5 in wide

means = {m: [values[m][b]['mean'] for b in benchmarks] for m in methods}
stds  = {m: [values[m][b]['std']  for b in benchmarks] for m in methods}

for i, method in enumerate(methods):
    offsets = x + i * bar_width - (n_methods - 1) * bar_width / 2
    bars = ax.bar(
        offsets,
        means[method],
        width=bar_width,
        color=COLORS[method],
        hatch=HATCHES[method],
        edgecolor='white',
        linewidth=0.4,
        zorder=3,
        label=method,
    )
    ax.errorbar(
        offsets,
        means[method],
        yerr=stds[method],
        fmt='none',
        ecolor='#333333',
        elinewidth=0.8,
        capsize=2.0,
        capthick=0.8,
        zorder=4,
    )

# Highlight OursModel bars with a thin border
for i, method in enumerate(methods):
    if method == 'OursModel':
        offsets = x + i * bar_width - (n_methods - 1) * bar_width / 2
        for xpos, mean_val in zip(offsets, means[method]):
            ax.bar(xpos, mean_val, width=bar_width, fill=False,
                   edgecolor='#005030', linewidth=1.1, zorder=5)

# Axes
all_vals = [values[m][b]['mean'] for m in methods for b in benchmarks]
all_stds = [values[m][b]['std']  for m in methods for b in benchmarks]
y_min = min(v - s for v, s in zip(all_vals, all_stds))
y_max = max(v + s for v, s in zip(all_vals, all_stds))
y_lo = max(0, np.floor((y_min - 4) / 5) * 5)
y_hi = np.ceil((y_max + 4) / 5) * 5

ax.set_ylim(y_lo, y_hi)
ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7)
ax.set_ylabel('Accuracy (%)', fontsize=8)
ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator(2))
ax.tick_params(axis='y', which='both', direction='in', left=True)
ax.tick_params(axis='x', which='both', bottom=False)
ax.set_xlim(x[0] - group_width * 0.5, x[-1] + group_width * 0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', linewidth=0.4, alpha=0.6, zorder=0)

legend = ax.legend(
    fontsize=7,
    frameon=True,
    framealpha=0.9,
    edgecolor='#cccccc',
    ncol=2,
    loc='upper left',
    handlelength=1.4,
    handletextpad=0.4,
    columnspacing=0.8,
    borderpad=0.5,
)
legend.get_frame().set_linewidth(0.5)

fig.tight_layout(pad=0.4)

fig.savefig('figure.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')
print('Saved figure.pdf, figure.png, figure.svg')
