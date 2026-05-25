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

means = np.array([[values[m][b]['mean'] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]['std']  for b in benchmarks] for m in methods])

# Palette: colorblind-friendly + distinguishable
colors  = ['#999999', '#4477AA', '#EE6677', '#228833']
hatches = ['',        '////',    '....',    'xxxx'   ]

bar_width = 0.18
group_gap = 0.08
x = np.arange(n_benchmarks) * (n_methods * bar_width + group_gap)

fig, ax = plt.subplots(figsize=(3.5, 2.6))  # single-column width

for i, (method, color, hatch) in enumerate(zip(methods, colors, hatches)):
    offsets = x + i * bar_width - (n_methods - 1) * bar_width / 2
    lw = 1.5 if method == 'OursModel' else 0.8
    ec = '#111111' if method == 'OursModel' else '#555555'
    bars = ax.bar(
        offsets, means[i], bar_width,
        yerr=stds[i],
        color=color, hatch=hatch,
        edgecolor=ec, linewidth=lw,
        error_kw=dict(elinewidth=0.8, capsize=2.0, ecolor='#333333', capthick=0.8),
        label=method,
        zorder=3,
    )

# y-axis: skip zero since all values are above 25; start at 20
all_vals = means - stds
ymin = max(0, np.floor(all_vals.min() / 5) * 5 - 5)
ymax = np.ceil((means + stds).max() / 5) * 5 + 5
ax.set_ylim(ymin, ymax)

ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=7.5)
ax.set_ylabel('Accuracy (%)', fontsize=8)
ax.yaxis.grid(True, linestyle='--', linewidth=0.4, alpha=0.7, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend — OursModel last so it stands out at the end
handles, labels = ax.get_legend_handles_labels()
# Reorder: Baseline, Method-A, Method-B, OursModel (already in order)
legend = ax.legend(
    handles, labels,
    fontsize=6.5,
    ncol=2,
    frameon=True,
    framealpha=0.9,
    edgecolor='#cccccc',
    loc='upper left',
    handlelength=1.6,
    handleheight=0.9,
    columnspacing=0.8,
    handletextpad=0.4,
)
# Bold OursModel label
for text in legend.get_texts():
    if text.get_text() == 'OursModel':
        text.set_fontweight('bold')

fig.tight_layout(pad=0.4)

fig.savefig('figure.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')

print("Saved figure.pdf, figure.png, figure.svg")
