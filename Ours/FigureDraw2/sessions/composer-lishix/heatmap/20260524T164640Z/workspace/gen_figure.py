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

# Off-diagonal mask for colormap scaling (exclude diagonal)
mask = np.ones_like(matrix, dtype=float)
np.fill_diagonal(mask, np.nan)
off_diag = matrix * mask

vmin = np.nanmin(off_diag)
vmax = np.nanmax(off_diag)

# Draw off-diagonal cells with Blues colormap
cmap = plt.cm.Blues
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

for i in range(10):
    for j in range(10):
        val = matrix[i, j]
        if i == j:
            # Diagonal: dark background, white text
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                       color="#1a5276", zorder=1))
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=10, fontweight="bold", color="white", zorder=2)
        else:
            color = cmap(norm(val))
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                       color=color, zorder=1))
            # Choose text color for readability
            luminance = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
            text_color = "white" if luminance < 0.5 else "#222222"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=text_color, zorder=2)

# Colorbar for off-diagonal
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Count (off-diagonal)", fontsize=9)

ax.set_xlim(-0.5, 9.5)
ax.set_ylim(-0.5, 9.5)
ax.set_xticks(range(10))
ax.set_yticks(range(10))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=11)
ax.set_ylabel("True class", fontsize=11)
ax.set_title("10×10 Confusion Matrix", fontsize=13, fontweight="bold")
ax.invert_yaxis()

# Grid lines
for k in range(11):
    ax.axhline(k - 0.5, color="white", linewidth=0.4, zorder=3)
    ax.axvline(k - 0.5, color="white", linewidth=0.4, zorder=3)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
