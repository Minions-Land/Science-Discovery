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

# Build matrix: rows = classes, cols = conditions
mat = np.array([proportions[c] for c in conditions]).T  # shape (4, 5)

colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]

fig, ax = plt.subplots(figsize=(6, 4))

bottoms = np.zeros(len(conditions))
x = np.arange(len(conditions))

for i, (cls, color) in enumerate(zip(classes, colors)):
    bars = ax.bar(x, mat[i], bottom=bottoms, color=color, label=cls,
                  width=0.6, edgecolor="white", linewidth=0.6)
    # Add percentage labels inside segments if tall enough
    for j, (h, b) in enumerate(zip(mat[i], bottoms)):
        if h > 0.06:
            ax.text(j, b + h / 2, f"{h:.0%}", ha="center", va="center",
                    fontsize=7.5, color="white", fontweight="bold")
    bottoms += mat[i]

ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=10)
ax.set_ylabel("Proportion", fontsize=10)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
ax.tick_params(axis="y", labelsize=9)

ax.legend(title="Class", bbox_to_anchor=(1.01, 1), loc="upper left",
          fontsize=8, title_fontsize=9, frameon=False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
