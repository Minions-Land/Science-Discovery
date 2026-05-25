import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

with open("data.json") as f:
    data = json.load(f)

classes = data["classes"]
conditions = data["conditions"]
proportions = data["proportions"]

# Build matrix: rows = classes, cols = conditions
mat = np.array([proportions[c] for c in conditions]).T  # shape (4, 5)

# Harmonious 4-color palette (colorblind-friendly)
colors = ["#4E79A7", "#F28E2B", "#59A14F", "#E15759"]

fig, ax = plt.subplots(figsize=(6, 4.2))

bottoms = np.zeros(len(conditions))
bars = []
for i, (cls, color) in enumerate(zip(classes, colors)):
    b = ax.bar(conditions, mat[i], bottom=bottoms, color=color, label=cls,
               width=0.55, edgecolor="white", linewidth=0.6)
    bars.append(b)
    bottoms += mat[i]

ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
ax.set_ylabel("Proportion", fontsize=10)
ax.set_xlabel("Condition", fontsize=10)
ax.set_title("Class Proportions Across Conditions", fontsize=11, fontweight="bold")
ax.tick_params(axis="both", labelsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.legend(title="Class", fontsize=8, title_fontsize=9,
          loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)

fig.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
