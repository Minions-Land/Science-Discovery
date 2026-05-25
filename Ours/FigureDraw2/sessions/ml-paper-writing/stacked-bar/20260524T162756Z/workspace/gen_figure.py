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
colors = ["#4878CF", "#6ACC65", "#D65F5F", "#B47CC7"]

fig, ax = plt.subplots(figsize=(6, 4))

x = np.arange(len(conditions))
bottoms = np.zeros(len(conditions))

bars = []
for i, cls in enumerate(classes):
    vals = np.array([proportions[c][i] for c in conditions])
    b = ax.bar(x, vals, bottom=bottoms, color=colors[i], label=cls, width=0.6, edgecolor="white", linewidth=0.5)
    bars.append(b)
    bottoms += vals

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=11)
ax.set_ylabel("Proportion", fontsize=11)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.yaxis.set_major_locator(mticker.MultipleLocator(0.25))
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=10)

ax.legend(loc="upper right", fontsize=9, framealpha=0.85, edgecolor="none")

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done: figure.pdf, figure.png, figure.svg")
