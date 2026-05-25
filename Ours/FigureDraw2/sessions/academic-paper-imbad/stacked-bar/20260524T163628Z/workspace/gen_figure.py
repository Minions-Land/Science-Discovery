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

# 4 harmonious, distinguishable colors
colors = ["#4C72B0", "#55A868", "#C44E52", "#CCB974"]

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
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.set_ylabel("Proportion", fontsize=11)
ax.set_xlabel("Condition", fontsize=11)
ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done.")
