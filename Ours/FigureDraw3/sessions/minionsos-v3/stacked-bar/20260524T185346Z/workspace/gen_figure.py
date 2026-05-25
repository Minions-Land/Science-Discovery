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

# Build array: shape (n_conditions, n_classes)
arr = np.array([proportions[c] for c in conditions])

colors = ["#4C72B0", "#55A868", "#C44E52", "#DD8452"]

fig, ax = plt.subplots(figsize=(5.5, 4.0))

bottoms = np.zeros(len(conditions))
bars = []
for i, (cls, color) in enumerate(zip(classes, colors)):
    vals = arr[:, i]
    b = ax.bar(conditions, vals, bottom=bottoms, color=color, label=cls,
               edgecolor="white", linewidth=0.6, width=0.6)
    bars.append(b)
    bottoms += vals

ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
ax.set_ylabel("Proportion", fontsize=10)
ax.set_xlabel("Condition", fontsize=10)
ax.tick_params(axis="both", labelsize=9)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(title="Class", fontsize=8, title_fontsize=8,
          loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0,
          frameon=False)

fig.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
