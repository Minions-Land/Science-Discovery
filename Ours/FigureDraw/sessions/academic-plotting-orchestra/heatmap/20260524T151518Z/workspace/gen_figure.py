import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

with open("data.json") as f:
    d = json.load(f)

matrix = np.array(d["matrix"])
x_labels = d["x_labels"]
y_labels = d["y_labels"]

fig, ax = plt.subplots(figsize=(8, 7))

# Mask diagonal so off-diagonal uses sequential cmap
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

diag_vals = np.diag(matrix)

# Plot off-diagonal with Blues cmap
im = ax.imshow(off_diag, cmap="Blues", aspect="equal",
               vmin=0, vmax=np.nanmax(off_diag))

# Overlay diagonal with a separate neutral dark color
diag_matrix = np.full_like(matrix, np.nan, dtype=float)
np.fill_diagonal(diag_matrix, diag_vals)

# Use a fixed dark color for diagonal cells
diag_cmap = mcolors.ListedColormap(["#2d6a4f"])
diag_norm = mcolors.Normalize(vmin=0, vmax=100)
ax.imshow(diag_matrix, cmap=diag_cmap, aspect="equal",
          norm=diag_norm, alpha=1.0)

n = matrix.shape[0]

# Annotate all cells
for i in range(n):
    for j in range(n):
        val = matrix[i, j]
        if i == j:
            # White text on dark diagonal
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=11, fontweight="bold", color="white")
        else:
            # Dark text on light off-diagonal; use white if cell is dark
            norm_val = val / np.nanmax(off_diag) if np.nanmax(off_diag) > 0 else 0
            text_color = "white" if norm_val > 0.6 else "#1a1a2e"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=text_color)

ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_yticklabels(y_labels, fontsize=10)
ax.set_xlabel("Predicted class", fontsize=12, labelpad=8)
ax.set_ylabel("True class", fontsize=12, labelpad=8)
ax.set_title("10-Class Confusion Matrix", fontsize=13, pad=12)

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Off-diagonal count", fontsize=10)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
