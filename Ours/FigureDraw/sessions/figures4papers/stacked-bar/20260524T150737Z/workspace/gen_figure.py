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

# Harmonious 4-color palette (colorblind-friendly)
colors = ["#4C72B0", "#55A868", "#C44E52", "#CCB974"]

x = np.arange(len(conditions))
bar_width = 0.55

fig, ax = plt.subplots(figsize=(6, 4))

bottoms = np.zeros(len(conditions))
bars = []
for i, cls in enumerate(classes):
    vals = np.array([proportions[c][i] for c in conditions])
    b = ax.bar(x, vals, bar_width, bottom=bottoms, color=colors[i], label=cls,
               edgecolor="white", linewidth=0.5)
    bars.append(b)
    bottoms += vals

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=10)
ax.set_ylabel("Proportion", fontsize=11)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=9)

ax.legend(loc="upper right", fontsize=9, framealpha=0.85,
          bbox_to_anchor=(1.0, 1.0), title_fontsize=9)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Done: figure.pdf, figure.png, figure.svg")
