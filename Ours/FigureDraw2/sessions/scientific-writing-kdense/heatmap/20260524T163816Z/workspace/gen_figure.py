import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

with open("data.json") as f:
    data = json.load(f)

matrix = np.array(data["matrix"])
x_labels = data["x_labels"]
y_labels = data["y_labels"]

fig, ax = plt.subplots(figsize=(7, 6))

# Off-diagonal mask for colormap: use Blues on off-diagonal, white on diagonal
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

diag_vals = np.diag(matrix)

# Plot off-diagonal cells with Blues colormap
im = ax.imshow(off_diag, cmap="Blues", aspect="equal",
               vmin=0, vmax=np.nanmax(off_diag))

# Overlay diagonal cells in a dark viridis color
diag_cmap = plt.cm.get_cmap("viridis")
diag_norm = mcolors.Normalize(vmin=min(diag_vals), vmax=max(diag_vals))

for i in range(len(x_labels)):
    color = diag_cmap(diag_norm(diag_vals[i]))
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, color=color))

# Annotate all cells
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        if i == j:
            # White text on dark diagonal
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
        else:
            # Dark text on light off-diagonal; use white if cell is dark
            bg_norm = val / (np.nanmax(off_diag) if np.nanmax(off_diag) > 0 else 1)
            txt_color = "white" if bg_norm > 0.6 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=txt_color)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=11)
ax.set_ylabel("True class", fontsize=11)
ax.set_title("Confusion Matrix (counts)", fontsize=12, pad=10)

# Colorbar for off-diagonal
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Off-diagonal count", fontsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
