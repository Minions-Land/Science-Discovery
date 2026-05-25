import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with open("data.json") as f:
    data = json.load(f)

classes = data["classes"]
conditions = data["conditions"]
proportions = data["proportions"]

colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

fig, ax = plt.subplots(figsize=(6, 4))

x = np.arange(len(conditions))
bottoms = np.zeros(len(conditions))

bars = []
for i, cls in enumerate(classes):
    vals = [proportions[cond][i] for cond in conditions]
    b = ax.bar(x, vals, bottom=bottoms, color=colors[i], width=0.6, label=cls)
    bars.append(b)
    bottoms += np.array(vals)

ax.set_xticks(x)
ax.set_xticklabels(conditions)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.set_ylabel("Proportion")
ax.set_xlabel("Condition")
ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done.")
