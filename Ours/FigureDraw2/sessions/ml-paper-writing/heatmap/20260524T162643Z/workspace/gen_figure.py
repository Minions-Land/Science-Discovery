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

# Off-diagonal mask: use Blues colormap, but diagonal handled separately
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

diag_vals = np.diag(matrix)

# Plot off-diagonal with Blues
im = ax.imshow(off_diag, cmap="Blues", aspect="equal", vmin=0, vmax=matrix.max())

# Overlay diagonal cells with a distinct dark color
diag_cmap = plt.cm.YlOrRd
diag_norm = mcolors.Normalize(vmin=diag_vals.min() - 10, vmax=diag_vals.max())

for i in range(len(x_labels)):
    color = diag_cmap(diag_norm(diag_vals[i]))
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, color=color, zorder=2))
    ax.text(i, i, str(diag_vals[i]), ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=3)

# Annotate off-diagonal cells
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if i != j and matrix[i, j] > 0:
            val = matrix[i, j]
            # pick text color based on cell brightness
            bg = im.cmap(im.norm(val))
            lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
            txt_color = "white" if lum < 0.5 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=7, color=txt_color)

ax.set_xticks(range(len(x_labels)))
ax.set_yticks(range(len(y_labels)))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=10)
ax.set_ylabel("True class", fontsize=10)
ax.set_title("Confusion Matrix", fontsize=11, fontweight="bold")

# Colorbar for off-diagonal
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Count (off-diagonal)", fontsize=8)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
