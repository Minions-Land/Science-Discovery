import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

with open("data.json") as f:
    data = json.load(f)

classes = data["classes"]
conditions = data["conditions"]
proportions = data["proportions"]

# Build matrix: rows=conditions, cols=classes
mat = np.array([proportions[c] for c in conditions])

colors = ["#4C72B0", "#55A868", "#C44E52", "#DD8452"]

fig, ax = plt.subplots(figsize=(6, 4))

bottoms = np.zeros(len(conditions))
x = np.arange(len(conditions))

for i, cls in enumerate(classes):
    vals = mat[:, i]
    ax.bar(x, vals, bottom=bottoms, color=colors[i], label=cls, width=0.6, edgecolor="white", linewidth=0.5)
    bottoms += vals

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=10)
ax.set_ylabel("Proportion", fontsize=11)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
ax.legend(title="Class", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9, title_fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done.")
