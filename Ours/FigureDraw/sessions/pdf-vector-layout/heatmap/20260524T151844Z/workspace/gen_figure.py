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

fig, ax = plt.subplots(figsize=(8, 7))

# Off-diagonal mask for colormap
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

# Plot off-diagonal cells with Blues colormap
im = ax.imshow(off_diag, cmap="Blues", aspect="equal",
               vmin=0, vmax=np.nanmax(off_diag))

# Plot diagonal cells with a dark overlay (viridis high end)
diag_vals = np.diag(matrix)
diag_norm = (diag_vals - diag_vals.min()) / (diag_vals.max() - diag_vals.min() + 1e-9)
viridis = plt.cm.viridis

for i in range(len(matrix)):
    color = viridis(0.4 + 0.5 * diag_norm[i])
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, color=color, zorder=2))

# Annotate all cells
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        val = matrix[i, j]
        if i == j:
            # White text on dark diagonal
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=10, fontweight="bold", color="white", zorder=3)
        else:
            # Dark text on light off-diagonal; use white if cell is dark
            bg_norm = val / (np.nanmax(off_diag) + 1e-9)
            txt_color = "white" if bg_norm > 0.6 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=txt_color)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=10)
ax.set_xlabel(data.get("x_axis", "Predicted"), fontsize=12, labelpad=8)
ax.set_ylabel(data.get("y_axis", "True"), fontsize=12, labelpad=8)
ax.set_title("Confusion Matrix (counts)", fontsize=13, pad=12)

# Colorbar for off-diagonal
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Off-diagonal count", fontsize=10)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
