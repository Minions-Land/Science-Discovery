"""
gen_figure.py — stacked bar of 4-class proportions across 5 conditions.
Data source: data.json (classes, conditions, proportions).
"""

import json
import pathlib
import subprocess
import sys

import matplotlib as mpl

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
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
import numpy as np

# ── Data ──────────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

classes = data["classes"]          # 4 classes
conditions = data["conditions"]    # 5 conditions
proportions = data["proportions"]  # dict: condition → [4 floats]

# Build matrix: shape (n_classes, n_conditions)
n_cls = len(classes)
n_cond = len(conditions)
mat = np.array([proportions[c] for c in conditions]).T  # (4, 5)

# ── Palette — cool-warm pastel family, ~25-30% saturation, P1+P2 compliant ──
# 4 distinct hues, family-coherent (all desaturated), distinguishable
PALETTE = [
    "#5B8DB8",   # muted blue      — Class A
    "#7BBFA5",   # muted teal      — Class B
    "#E8A87C",   # muted amber     — Class C
    "#C47E9E",   # muted mauve     — Class D
]

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))

x = np.arange(n_cond)
bar_width = 0.55

bottoms = np.zeros(n_cond)
bars = []
for i, (cls, color) in enumerate(zip(classes, PALETTE)):
    b = ax.bar(x, mat[i], bar_width, bottom=bottoms,
               color=color, label=cls, linewidth=0)
    bars.append(b)
    bottoms += mat[i]

# ── Axes ──────────────────────────────────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=9)
ax.set_ylim(0, 1.0)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=8)
ax.set_ylabel("Proportion", fontsize=9)
ax.tick_params(direction="out", length=2.2, width=0.6)
ax.spines["left"].set_linewidth(0.8)
ax.spines["bottom"].set_linewidth(0.8)

# ── Legend — outside plot area, right side (P7: legend off data) ──────────────
ax.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=8,
    frameon=False,
    handlelength=1.2,
    handleheight=1.0,
    borderpad=0,
    labelspacing=0.5,
)

fig.tight_layout(rect=[0, 0, 0.85, 1])

# ── Save ──────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
print(f"Saved: {pdf_path}, {png_path}, {svg_path}")

# ── Font verification (mandatory post-save check) ─────────────────────────────
out = subprocess.run(
    ["pdffonts", str(pdf_path)],
    capture_output=True, text=True, check=False,
)
if out.returncode == 0:
    if "Type 3" in out.stdout:
        sys.stderr.write(
            f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n"
        )
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    # pdffonts not available — fall back to raw byte scan
    import re
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (byte-scan fallback) — no /Type3 in figure.pdf")
