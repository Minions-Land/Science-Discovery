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

# Mask diagonal to color off-diagonal only
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

im = ax.imshow(off_diag, cmap="Blues", aspect="equal",
               vmin=0, vmax=np.nanmax(off_diag))

# Annotate all cells
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        if i == j:
            # Diagonal: white text on a dark teal background
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                       color="#1a5276", zorder=2))
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white", zorder=3)
        else:
            # Off-diagonal: dark text, color from Blues cmap
            norm_val = val / np.nanmax(off_diag)
            text_color = "white" if norm_val > 0.6 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=text_color)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=11)
ax.set_ylabel("True class", fontsize=11)
ax.set_title("10×10 Confusion Matrix", fontsize=13, pad=10)

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Count (off-diagonal)", fontsize=9)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
