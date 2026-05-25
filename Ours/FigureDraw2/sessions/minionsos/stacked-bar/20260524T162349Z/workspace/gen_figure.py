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
proportions = [np.array(data["proportions"][c]) for c in conditions]

# 4 harmonious but distinguishable colors (colorbrewer-inspired)
colors = ["#4E79A7", "#F28E2B", "#59A14F", "#E15759"]

x = np.arange(len(conditions))
bar_width = 0.55

fig, ax = plt.subplots(figsize=(6, 4))

bottoms = np.zeros(len(conditions))
bars = []
for i, (cls, col) in enumerate(zip(classes, colors)):
    vals = np.array([proportions[j][i] for j in range(len(conditions))])
    b = ax.bar(x, vals, bar_width, bottom=bottoms, color=col, label=cls,
               edgecolor="white", linewidth=0.5)
    bars.append(b)
    bottoms += vals

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=10)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
ax.set_ylabel("Proportion", fontsize=11)
ax.set_xlabel("Condition", fontsize=11)
ax.set_title("Class Proportions Across Conditions", fontsize=12, fontweight="bold")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", labelsize=9)

legend = ax.legend(
    handles=[mpatches.Patch(color=colors[i], label=classes[i]) for i in range(len(classes))],
    title="Class", title_fontsize=9, fontsize=9,
    loc="upper right", framealpha=0.85, edgecolor="lightgray"
)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
