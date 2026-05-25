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
x_axis = data.get("x_axis", "Predicted")
y_axis = data.get("y_axis", "True")

fig, ax = plt.subplots(figsize=(7, 6))

# Mask diagonal for off-diagonal colormapping
off_diag = matrix.astype(float).copy()
np.fill_diagonal(off_diag, np.nan)

# Plot off-diagonal cells with Blues cmap
im = ax.imshow(off_diag, cmap="Blues", aspect="equal",
               vmin=0, vmax=np.nanmax(off_diag))

# Overlay diagonal cells in a contrasting color (dark viridis / gold)
diag_vals = np.diag(matrix)
diag_norm = (diag_vals - diag_vals.min()) / (diag_vals.max() - diag_vals.min() + 1e-9)
diag_cmap = plt.cm.YlOrBr

for i in range(len(matrix)):
    color = diag_cmap(0.4 + 0.5 * diag_norm[i])
    rect = plt.Rectangle([i - 0.5, i - 0.5], 1, 1, color=color)
    ax.add_patch(rect)

# Annotate every cell
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        val = matrix[i, j]
        if i == j:
            # Diagonal — white text for readability on dark cell
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
        else:
            # Off-diagonal — choose text color based on cell brightness
            cell_norm = val / (np.nanmax(off_diag) + 1e-9)
            text_color = "white" if cell_norm > 0.55 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=7.5, color=text_color)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel(x_axis.capitalize() + " label", fontsize=10, labelpad=8)
ax.set_ylabel(y_axis.capitalize() + " label", fontsize=10, labelpad=8)
ax.xaxis.set_label_position("bottom")
ax.set_title("Confusion Matrix (10 classes)", fontsize=11, pad=10)

# Colorbar for off-diagonal intensity
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Off-diagonal count", fontsize=8)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
