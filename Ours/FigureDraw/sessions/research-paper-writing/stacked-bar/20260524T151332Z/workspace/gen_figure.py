import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

with open("data.json") as f:
    data = json.load(f)

classes = data["classes"]
conditions = data["conditions"]
proportions = data["proportions"]

# 4 distinguishable but harmonious colors (colorbrewer-inspired)
colors = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759"]

fig, ax = plt.subplots(figsize=(6, 4))

x = np.arange(len(conditions))
bottoms = np.zeros(len(conditions))

bars = []
for i, cls in enumerate(classes):
    vals = [proportions[c][i] for c in conditions]
    b = ax.bar(x, vals, bottom=bottoms, color=colors[i], label=cls, width=0.6, edgecolor="white", linewidth=0.5)
    bars.append(b)
    bottoms += np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=10)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
ax.set_ylabel("Proportion", fontsize=10)
ax.set_xlabel("Condition", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(
    handles=[mpatches.Patch(color=colors[i], label=classes[i]) for i in range(len(classes))],
    loc="upper right",
    frameon=False,
    fontsize=9,
    title_fontsize=9,
)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
