import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Mandatory editable-text rules
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.size'] = 8
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['legend.frameon'] = False

# 4 harmonious, distinguishable colors from the Nature palette
COLORS = ["#0F4D92", "#42949E", "#9A4D8E", "#E28E2C"]

cwd = Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

classes = data["classes"]       # 4 classes
conditions = data["conditions"] # 5 conditions
proportions = data["proportions"]

# Build matrix: shape (n_classes, n_conditions)
mat = np.array([proportions[c] for c in conditions]).T  # (4, 5)

fig, ax = plt.subplots(figsize=(3.5, 2.8))

x = np.arange(len(conditions))
bottoms = np.zeros(len(conditions))

bars = []
for i, (cls, color) in enumerate(zip(classes, COLORS)):
    b = ax.bar(x, mat[i], bottom=bottoms, color=color,
               edgecolor='white', linewidth=0.4, label=cls, width=0.65)
    bars.append(b)
    bottoms += mat[i]

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=7)
ax.set_ylabel("Proportion", fontsize=8)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
ax.tick_params(axis='y', labelsize=7)
ax.tick_params(axis='x', length=0)
ax.spines['bottom'].set_linewidth(0.8)
ax.spines['left'].set_linewidth(0.8)

leg = ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.01, 1),
    borderaxespad=0,
    fontsize=6.5,
    handlelength=1.0,
    handleheight=0.9,
    handletextpad=0.4,
)

fig.tight_layout(pad=1.5)

out = cwd / "figure"
fig.savefig(str(out) + ".pdf", bbox_inches="tight")
fig.savefig(str(out) + ".png", dpi=300, bbox_inches="tight")
fig.savefig(str(out) + ".svg", bbox_inches="tight")
plt.close(fig)
print("Saved figure.pdf, figure.png, figure.svg")
