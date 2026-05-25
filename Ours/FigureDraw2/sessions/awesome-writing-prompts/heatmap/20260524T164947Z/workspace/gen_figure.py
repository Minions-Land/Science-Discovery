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

# Off-diagonal mask: use Blues colormap, diagonal handled separately
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

diag_vals = np.diag(matrix)

# Plot off-diagonal cells with Blues
im = ax.imshow(off_diag, cmap="Blues", aspect="equal",
               vmin=0, vmax=np.nanmax(off_diag))

# Overlay diagonal cells with a distinct dark color (viridis high end)
diag_cmap = plt.cm.YlOrRd
diag_norm = mcolors.Normalize(vmin=min(diag_vals), vmax=max(diag_vals))

for i in range(len(matrix)):
    color = diag_cmap(diag_norm(diag_vals[i]))
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1,
                                color=color, zorder=2))

# Annotate all cells
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        val = matrix[i, j]
        if i == j:
            # White text on dark diagonal cells
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white", zorder=3)
        else:
            # Dark text on light off-diagonal cells
            bg = off_diag[i, j]
            norm_val = bg / np.nanmax(off_diag) if np.nanmax(off_diag) > 0 else 0
            text_color = "white" if norm_val > 0.6 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=text_color, zorder=3)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=10)
ax.set_xlabel("Predicted class", fontsize=11)
ax.set_ylabel("True class", fontsize=11)
ax.set_title("10-class Confusion Matrix", fontsize=13, fontweight="bold")

# Colorbar for off-diagonal
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Off-diagonal count", fontsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
