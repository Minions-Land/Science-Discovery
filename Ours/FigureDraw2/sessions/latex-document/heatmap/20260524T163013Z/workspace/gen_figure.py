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

fig, ax = plt.subplots(figsize=(7, 6))

# Mask diagonal so off-diagonal gets sequential colormap on its own scale
off_diag = matrix.copy().astype(float)
np.fill_diagonal(off_diag, np.nan)

diag_vals = np.diag(matrix)
diag_min, diag_max = diag_vals.min(), diag_vals.max()
off_min = np.nanmin(off_diag)
off_max = np.nanmax(off_diag)

# Draw off-diagonal cells with Blues cmap
norm_off = mcolors.Normalize(vmin=off_min, vmax=off_max)
cmap_off = plt.get_cmap("Blues")

n = matrix.shape[0]
cell_colors = np.full((n, n, 4), 1.0)  # RGBA white default

for i in range(n):
    for j in range(n):
        if i != j:
            cell_colors[i, j] = cmap_off(norm_off(matrix[i, j]))

ax.imshow(cell_colors, aspect="auto", interpolation="nearest")

# Overlay diagonal cells with a distinct green tint
norm_diag = mcolors.Normalize(vmin=diag_min, vmax=diag_max)
cmap_diag = plt.get_cmap("YlGn")
for i in range(n):
    color = cmap_diag(norm_diag(matrix[i, i]))
    rect = plt.Rectangle([i - 0.5, i - 0.5], 1, 1, color=color, zorder=2)
    ax.add_patch(rect)

# Annotate all cells
for i in range(n):
    for j in range(n):
        val = matrix[i, j]
        if i == j:
            # white text on (potentially dark) diagonal
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white", zorder=3)
        else:
            # dark text on light off-diagonal
            bg = cell_colors[i, j]
            lum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
            txt_color = "white" if lum < 0.5 else "#333333"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=7.5, color=txt_color, zorder=3)

# Axes
ax.set_xticks(range(n))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticks(range(n))
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=10, labelpad=8)
ax.set_ylabel("True class", fontsize=10, labelpad=8)
ax.set_title("10-Class Confusion Matrix", fontsize=11, pad=10)

# Colorbars
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax_off = divider.append_axes("right", size="4%", pad=0.1)
sm_off = plt.cm.ScalarMappable(cmap=cmap_off, norm=norm_off)
sm_off.set_array([])
cb_off = fig.colorbar(sm_off, cax=cax_off)
cb_off.set_label("Off-diag count", fontsize=8)

cax_diag = divider.append_axes("right", size="4%", pad=0.55)
sm_diag = plt.cm.ScalarMappable(cmap=cmap_diag, norm=norm_diag)
sm_diag.set_array([])
cb_diag = fig.colorbar(sm_diag, cax=cax_diag)
cb_diag.set_label("Diagonal count", fontsize=8)

plt.tight_layout()
fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
