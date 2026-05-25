import json
import pathlib
import subprocess
import sys

import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

cwd = pathlib.Path(__file__).parent

with open(cwd / "data.json") as f:
    data = json.load(f)

matrix = np.array(data["matrix"], dtype=float)
x_labels = data["x_labels"]
y_labels = data["y_labels"]
n = len(x_labels)

# Row-normalize to show per-class confusion proportions
row_sums = matrix.sum(axis=1, keepdims=True)
norm_matrix = matrix / row_sums

fig, ax = plt.subplots(figsize=(7, 6))

im = ax.imshow(norm_matrix, cmap="Blues", vmin=0, vmax=1, aspect="equal")

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Fraction of true-class samples", fontsize=9)
cbar.ax.tick_params(labelsize=8)

# Annotate every cell; diagonal gets raw count in white, off-diagonal in grey
for i in range(n):
    for j in range(n):
        raw = int(matrix[i, j])
        frac = norm_matrix[i, j]
        if i == j:
            color = "white"
            text = f"{raw}"
            weight = "bold"
        else:
            color = "#444444" if frac < 0.15 else "white"
            text = f"{raw}" if raw > 0 else ""
            weight = "normal"
        if text:
            ax.text(j, i, text, ha="center", va="center",
                    fontsize=7.5, color=color, fontweight=weight)

ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(x_labels, fontsize=8)
ax.set_yticklabels(y_labels, fontsize=8)
ax.tick_params(axis="both", direction="out", length=2.2, width=0.6)
ax.set_xlabel("Predicted class", fontsize=9, labelpad=6)
ax.set_ylabel("True class", fontsize=9, labelpad=6)
ax.set_title("Confusion matrix (10-class)", fontsize=10, pad=10)

# Minor grid to separate cells
ax.set_xticks(np.arange(n) - 0.5, minor=True)
ax.set_yticks(np.arange(n) - 0.5, minor=True)
ax.grid(which="minor", color="white", linewidth=0.8)
ax.tick_params(which="minor", bottom=False, left=False)

fig.tight_layout()

pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path)
fig.savefig(png_path, dpi=300)
fig.savefig(svg_path)

plt.close(fig)

# Font-type verification
pdf_bytes = pdf_path.read_bytes()
import re
if re.search(rb"/Subtype\s*/Type3\b", pdf_bytes):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)

out = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if out.returncode == 0 and "Type 3" in out.stdout:
    sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n")
    sys.exit(2)

print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")
print(f"Saved: {pdf_path}, {png_path}, {svg_path}")
