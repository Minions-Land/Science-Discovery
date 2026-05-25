"""
gen_figure.py — 10×10 confusion-matrix heatmap
Data source: data.json (matrix[i][j] = predictions of true class i as class j)
"""

import json
import numpy as np
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ── Load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

matrix = np.array(data["matrix"], dtype=float)
x_labels = data["x_labels"]
y_labels = data["y_labels"]
x_axis   = data.get("x_axis", "Predicted")
y_axis   = data.get("y_axis", "True")
n = matrix.shape[0]

# ── Normalise rows to percent for the off-diagonal colourmap ───────────────
row_sums = matrix.sum(axis=1, keepdims=True)
matrix_norm = matrix / row_sums * 100  # percent of true-class samples

# ── Build masked arrays: diagonal vs off-diagonal ─────────────────────────
diag_mask = np.eye(n, dtype=bool)
off_diag = np.ma.array(matrix_norm, mask=diag_mask)   # colour by sequential cmap
diag_vals = np.ma.array(matrix_norm, mask=~diag_mask)  # diagonal overlay

# ── Figure ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))

# Off-diagonal: Blues sequential cmap
cmap_off = plt.cm.Blues
im_off = ax.imshow(off_diag, cmap=cmap_off, vmin=0, vmax=15, aspect="equal")

# Diagonal: fixed dark colour (Viridis high-value) to distinguish clearly
diag_color = "#1f77b4"  # strong blue — not green/red (no directional signal)
diag_display = np.ma.filled(diag_vals, np.nan)
# Overlay diagonal as a separate image layer with a single-hue sequential map
diag_cmap = mcolors.LinearSegmentedColormap.from_list(
    "diag_cmap", ["#4A90D9", "#003399"], N=256
)
im_diag = ax.imshow(diag_vals, cmap=diag_cmap, vmin=60, vmax=100, aspect="equal")

# ── Annotate every cell ────────────────────────────────────────────────────
for i in range(n):
    for j in range(n):
        val = matrix_norm[i, j]
        raw = int(matrix[i, j])
        if i == j:
            # Diagonal: always white text for readability on dark cell
            ax.text(j, i, f"{val:.0f}%\n({raw})",
                    ha="center", va="center", fontsize=7.5,
                    color="white", fontweight="bold")
        else:
            # Off-diagonal: dark text on light cells, white on dark
            text_color = "white" if val > 8 else "#272727"
            ax.text(j, i, f"{val:.0f}",
                    ha="center", va="center", fontsize=6.5,
                    color=text_color)

# ── Tick labels ────────────────────────────────────────────────────────────
ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_yticklabels(y_labels, fontsize=8)
ax.xaxis.set_ticks_position("bottom")
ax.yaxis.set_ticks_position("left")
ax.tick_params(axis="both", which="both", length=0)

ax.set_xlabel(x_axis.capitalize() + " class", fontsize=9, labelpad=8)
ax.set_ylabel(y_axis.capitalize() + " class", fontsize=9, labelpad=8)

# ── Colourbar for off-diagonal ─────────────────────────────────────────────
cbar = fig.colorbar(im_off, ax=ax, fraction=0.035, pad=0.03, shrink=0.85)
cbar.set_label("Misclassification (%)", fontsize=8)
cbar.ax.tick_params(labelsize=7, length=2, width=0.6)
cbar.outline.set_linewidth(0.5)

ax.set_title("Confusion Matrix", fontsize=11, pad=10, fontweight="semibold")

fig.tight_layout()

# ── Save ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved: figure.pdf, figure.png, figure.svg")
