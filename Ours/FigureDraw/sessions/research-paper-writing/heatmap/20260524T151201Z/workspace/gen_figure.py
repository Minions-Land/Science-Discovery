import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data.json") as f:
    d = json.load(f)

matrix = np.array(d["matrix"])
x_labels = d["x_labels"]
y_labels = d["y_labels"]

fig, ax = plt.subplots(figsize=(7, 6))

# Off-diagonal: Blues colormap; diagonal will still use same cmap but text forced white/black
im = ax.imshow(matrix, cmap="Blues", aspect="equal")

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Count", fontsize=10)

# Annotate all cells; diagonal gets bold white text, off-diagonal gets standard text
vmax = matrix.max()
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        val = matrix[i, j]
        on_diag = (i == j)
        # Choose text color based on cell brightness
        normed = val / vmax
        text_color = "white" if normed > 0.55 else "black"
        weight = "bold" if on_diag else "normal"
        ax.text(j, i, str(val), ha="center", va="center",
                fontsize=8, color=text_color, fontweight=weight)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, fontsize=9)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel("Predicted class", fontsize=10)
ax.set_ylabel("True class", fontsize=10)
ax.set_title("Confusion Matrix (10-class classifier)", fontsize=11, pad=10)

# Highlight diagonal with a thin border
for i in range(matrix.shape[0]):
    rect = plt.Rectangle((i - 0.5, i - 0.5), 1, 1,
                          linewidth=1.2, edgecolor="white", facecolor="none")
    ax.add_patch(rect)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
