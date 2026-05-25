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

n_benchmarks = len(benchmarks)
n_methods = len(methods)
bar_width = 0.18
group_gap = 0.12
group_width = n_methods * bar_width + group_gap
x_centers = np.arange(n_benchmarks) * group_width

# Colors: colorblind-friendly palette + hatches for B&W readers
colors = ['#999999', '#56B4E9', '#E69F00', '#009E73']
hatches = ['', '//', 'xx', '']
edgecolors = ['#555555', '#1a7aad', '#b87800', '#007a58']

fig, ax = plt.subplots(figsize=(3.5, 2.6))

offsets = np.linspace(-(n_methods - 1) / 2, (n_methods - 1) / 2, n_methods) * bar_width

bars_list = []
for i, method in enumerate(methods):
    means = [values[method][b]['mean'] for b in benchmarks]
    stds  = [values[method][b]['std']  for b in benchmarks]
    x_pos = x_centers + offsets[i]
    bars = ax.bar(
        x_pos, means,
        width=bar_width,
        color=colors[i],
        edgecolor=edgecolors[i],
        linewidth=0.6,
        hatch=hatches[i],
        yerr=stds,
        capsize=2.5,
        error_kw=dict(elinewidth=0.7, ecolor='#333333', capthick=0.7),
        label=method,
        zorder=3
    )
    bars_list.append(bars)
    # Bold outline for OursModel to highlight winner
    if method == 'OursModel':
        for bar in bars:
            bar.set_linewidth(1.4)
            bar.set_edgecolor('#003d2a')

ax.set_xticks(x_centers)
ax.set_xticklabels(benchmarks, fontsize=7.5)
ax.set_ylabel('Accuracy (%)', fontsize=8)

# Y-range: minimum value is ~31, so start below that
all_means = [values[m][b]['mean'] for m in methods for b in benchmarks]
all_stds  = [values[m][b]['std']  for m in methods for b in benchmarks]
y_min = min(v - s for v, s in zip(all_means, all_stds))
y_max = max(v + s for v, s in zip(all_means, all_stds))
ax.set_ylim(max(0, y_min - 4), y_max + 4)

ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.6, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

legend = ax.legend(
    fontsize=7,
    frameon=True,
    framealpha=0.9,
    edgecolor='#cccccc',
    loc='upper left',
    handlelength=1.4,
    handleheight=0.9,
    borderpad=0.5,
    labelspacing=0.3,
)
# Bold the "OursModel" legend entry text
for text, method in zip(legend.get_texts(), methods):
    if method == 'OursModel':
        text.set_fontweight('bold')

fig.tight_layout(pad=0.4)

fig.savefig('figure.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')
print("Saved figure.pdf, figure.png, figure.svg")
