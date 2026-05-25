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

x = np.arange(len(conditions))
bar_width = 0.55

fig, ax = plt.subplots(figsize=(6, 4.5))

bottoms = np.zeros(len(conditions))
bars = []
for i, cls in enumerate(classes):
    vals = np.array([proportions[c][i] for c in conditions])
    b = ax.bar(x, vals, bar_width, bottom=bottoms, color=colors[i], label=cls,
               edgecolor="white", linewidth=0.6)
    bars.append(b)
    bottoms += vals

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=11)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.set_ylabel("Proportion", fontsize=12)
ax.set_xlabel("Condition", fontsize=12)
ax.set_title("Class Proportions Across Conditions", fontsize=13, pad=10)
ax.legend(title="Class", bbox_to_anchor=(1.01, 1), loc="upper left",
          fontsize=10, title_fontsize=10, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=10)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
