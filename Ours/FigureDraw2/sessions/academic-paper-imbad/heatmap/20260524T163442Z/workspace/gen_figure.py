import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data.json") as f:
    d = json.load(f)

matrix = np.array(d["matrix"])
x_labels = d["x_labels"]
y_labels = d["y_labels"]

fig, ax = plt.subplots(figsize=(7, 6))

# Off-diagonal mask: use Blues cmap; diagonal handled separately
masked_off = np.ma.masked_where(np.eye(10, dtype=bool), matrix)
masked_diag = np.ma.masked_where(~np.eye(10, dtype=bool), matrix)

im = ax.imshow(masked_off, cmap="Blues", vmin=0, vmax=matrix.max(), aspect="auto")
ax.imshow(masked_diag, cmap="Greens", vmin=matrix.min(), vmax=matrix.max(), aspect="auto")

# Annotate all cells
for i in range(10):
    for j in range(10):
        val = matrix[i, j]
        if i == j:
            # white text on green diagonal
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
        else:
            # dark text on light cells, light text on dark cells
            norm_val = val / matrix.max()
            color = "white" if norm_val > 0.5 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=color)

ax.set_xticks(range(10))
ax.set_yticks(range(10))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=10, labelpad=6)
ax.set_ylabel("True class", fontsize=10, labelpad=6)
ax.set_title("Confusion Matrix (counts)", fontsize=11, pad=10)

# Colorbars
cbar_off = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar_off.set_label("Count (off-diagonal)", fontsize=8)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
