import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

with open("data.json") as f:
    data = json.load(f)

matrix = np.array(data["matrix"], dtype=float)
x_labels = data["x_labels"]
y_labels = data["y_labels"]
n = matrix.shape[0]

fig, ax = plt.subplots(figsize=(7, 6))

# Mask diagonal so off-diagonal gets the sequential colormap
off_diag = matrix.copy()
np.fill_diagonal(off_diag, np.nan)

# Off-diagonal uses Blues; diagonal handled separately
cmap = plt.cm.Blues
norm = mcolors.Normalize(vmin=0, vmax=np.nanmax(off_diag))

im = ax.imshow(off_diag, cmap=cmap, norm=norm, aspect="equal")

# Diagonal cells: use a distinct dark color (viridis-dark purple)
diag_color = "#2d0046"  # deep purple, clearly distinguishable
for i in range(n):
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1,
                                color=diag_color, zorder=1))

# Annotate all cells
for i in range(n):
    for j in range(n):
        val = int(matrix[i, j])
        if i == j:
            # White text on dark diagonal
            ax.text(j, i, str(val), ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold", zorder=2)
        else:
            # Choose text color for readability over Blues
            normed = norm(matrix[i, j])
            text_color = "white" if normed > 0.6 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    color=text_color, fontsize=7.5, zorder=2)

ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=10, labelpad=8)
ax.set_ylabel("True class", fontsize=10, labelpad=8)
ax.set_title("Confusion matrix (counts)", fontsize=11, pad=10)

# Colorbar for off-diagonal magnitude
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Count (off-diagonal)", fontsize=9)

# Thin grid lines to separate cells
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which="minor", color="white", linewidth=0.5)
ax.tick_params(which="minor", length=0)

plt.tight_layout()

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
