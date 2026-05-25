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
x_axis = d.get("x_axis", "Predicted")
y_axis = d.get("y_axis", "True")

fig, ax = plt.subplots(figsize=(7, 6))

# Mask diagonal so it doesn't drive the off-diagonal color scale
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)
vmin = np.nanmin(off_diag)
vmax = np.nanmax(off_diag)

cmap = plt.cm.Blues

# Draw off-diagonal cells
im = ax.imshow(off_diag, cmap=cmap, vmin=vmin, vmax=vmax, aspect="equal")

# Draw diagonal cells with a distinct fixed color (dark teal / viridis high end)
diag_cmap = plt.cm.viridis
diag_vmin = matrix.diagonal().min()
diag_vmax = matrix.diagonal().max()
diag_norm = mcolors.Normalize(vmin=diag_vmin, vmax=diag_vmax)

for i in range(len(matrix)):
    color = diag_cmap(diag_norm(matrix[i, i]))
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, color=color, zorder=2))

# Annotate all cells
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        val = matrix[i, j]
        if i == j:
            # white text on dark diagonal cells for readability
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white", zorder=3)
        else:
            # choose text color based on cell brightness
            cell_val = off_diag[i, j] if not np.isnan(off_diag[i, j]) else 0
            norm_val = (cell_val - vmin) / (vmax - vmin + 1e-9)
            text_color = "white" if norm_val > 0.65 else "black"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=8, color=text_color)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel(x_axis.capitalize(), fontsize=10, labelpad=6)
ax.set_ylabel(y_axis.capitalize(), fontsize=10, labelpad=6)
ax.set_title("Confusion Matrix (10 Classes)", fontsize=11, pad=10)

# Colorbar for off-diagonal counts
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Off-diagonal count", fontsize=8)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
