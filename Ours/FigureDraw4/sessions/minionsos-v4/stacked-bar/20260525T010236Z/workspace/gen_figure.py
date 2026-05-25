"""
Stacked bar chart: 4-class proportions across 5 conditions.
Data source: data.json
"""
import json
import pathlib
import re
import subprocess
import sys

import matplotlib as mpl

mpl.rcParams.update({
    # Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
    # Do NOT override per element — all text inherits from here.
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
import numpy as np

# Okabe-Ito colorblind-safe palette (4 of 7)
PALETTE = {
    "A": "#0072B2",   # blue
    "B": "#E69F00",   # orange
    "C": "#009E73",   # green
    "D": "#CC79A7",   # pink/purple
}

# Load data
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

classes = data["classes"]       # ["Class A", "Class B", "Class C", "Class D"]
conditions = data["conditions"] # ["Cond1", ..., "Cond5"]
proportions = data["proportions"]

colors = [PALETTE["A"], PALETTE["B"], PALETTE["C"], PALETTE["D"]]

# Build matrix: shape (n_classes, n_conditions)
mat = np.array([proportions[c] for c in conditions]).T  # (4, 5)

x = np.arange(len(conditions))
bar_width = 0.55

fig, ax = plt.subplots(figsize=(6, 4))

bottoms = np.zeros(len(conditions))
bars = []
for i, (cls, color) in enumerate(zip(classes, colors)):
    b = ax.bar(x, mat[i], bar_width, bottom=bottoms, color=color, label=cls,
               linewidth=0)
    bars.append(b)
    bottoms += mat[i]

# Axes
ax.set_xlim(-0.5, len(conditions) - 0.5)
ax.set_ylim(0, 1.0)
ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=8)
ax.set_yticks([0, 0.25, 0.50, 0.75, 1.00])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=8)
ax.set_ylabel("Proportion", fontsize=9)
ax.tick_params(direction="out", length=2.2, width=0.6)
ax.spines["left"].set_linewidth(0.8)
ax.spines["bottom"].set_linewidth(0.8)

# Legend inside axes, top-right, away from data
ax.legend(loc="upper right", fontsize=8, handlelength=1.2, handletextpad=0.5,
          borderpad=0.4, labelspacing=0.3)

fig.tight_layout(pad=0.6)

# Save
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path)
fig.savefig(png_path, dpi=300)
fig.savefig(svg_path)
plt.close(fig)

# Post-save font verification (mandatory per academic-plotting skill)
result = subprocess.run(["pdffonts", str(pdf_path)],
                        capture_output=True, text=True, check=False)
if result.returncode == 0:
    if "Type 3" in result.stdout:
        sys.stderr.write(
            f"FATAL: figure.pdf contains Type-3 bitmap fonts; rcParams not honored.\n"
            f"{result.stdout}\n"
        )
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    # pdffonts not available; fall back to raw-bytes check
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (raw-bytes fallback) — no /Type3 in figure.pdf")

print(f"Saved: {pdf_path}, {png_path}, {svg_path}")
