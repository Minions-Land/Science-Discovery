"""
gen_figure.py — 6-cluster ridgeline (joyplot) of expression distributions.
Data source: data.json in the same directory.
"""

import json
import pathlib
import subprocess
import sys
import re

import numpy as np
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
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

HERE = pathlib.Path(__file__).parent

# ── Load data ──────────────────────────────────────────────────────────────
with open(HERE / "data.json") as f:
    data = json.load(f)

clusters = data["clusters"]          # ordered list of 6 names
samples  = data["samples"]           # dict: cluster → list[float]
x_label  = data["x_label"]

# ── Palette: single-blue family, faded-bottom → saturated-top ──────────────
# Matches the ridgeline_population_distributions exemplar annotation.
BLUE_DEEP   = "#154095"
BLUE_MID    = "#2F5EBE"
BLUE_SOFT   = "#406ac0"
BLUE_LIGHT  = "#6B93D1"
BLUE_FAINT  = "#95c0ea"
BLUE_PALE   = "#BDD5F0"

palette = [BLUE_PALE, BLUE_FAINT, BLUE_LIGHT, BLUE_SOFT, BLUE_MID, BLUE_DEEP]
# Cluster 1 (bottom) → faded; Cluster 6 (top) → deep

# ── Layout ─────────────────────────────────────────────────────────────────
N = len(clusters)
OVERLAP = 0.55          # fraction of row height used for vertical overlap
ROW_H   = 0.9           # inches per ridge row (before overlap compression)
FIG_W   = 6.5
FIG_H   = 4.2

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))

# Determine shared x range (trim to 1st–99th percentile of all data)
all_vals = np.concatenate([samples[c] for c in clusters])
x_lo = np.percentile(all_vals, 0.5)
x_hi = np.percentile(all_vals, 99.5)
x_eval = np.linspace(x_lo, x_hi, 400)

# Compute KDE heights so we can normalise
kdes = {}
for c in clusters:
    arr = np.array(samples[c])
    kde = gaussian_kde(arr, bw_method="scott")
    kdes[c] = kde(x_eval)

max_density = max(kdes[c].max() for c in clusters)

# Ridge vertical spacing: each ridge centre is placed at y = i * step
STEP     = 1.0
SCALE    = STEP * (1 - OVERLAP) / max_density   # map density → y-units

for i, cluster in enumerate(clusters):
    y_base  = i * STEP
    density = kdes[cluster]
    y_top   = y_base + density * SCALE

    color = palette[i]
    lw    = 1.6 if i == (N // 2) else 1.0   # emphasise middle ridge

    # Fill with semi-transparent white base then colored layer
    ax.fill_between(x_eval, y_base, y_top,
                    color=color, alpha=0.45, linewidth=0)
    ax.plot(x_eval, y_top, color=color, linewidth=lw)
    # Thin white baseline to visually separate overlapping fills
    ax.plot([x_eval[0], x_eval[-1]], [y_base, y_base],
            color="white", linewidth=0.6, zorder=2)

    # Label on left
    ax.text(x_lo - 0.06 * (x_hi - x_lo), y_base,
            cluster, va="bottom", ha="right",
            fontsize=8.5, color="#333333")

# ── Axes cosmetics ──────────────────────────────────────────────────────────
ax.set_xlim(x_lo - 0.08 * (x_hi - x_lo), x_hi + 0.02 * (x_hi - x_lo))
ax.set_ylim(-0.25 * STEP, (N - 1) * STEP + STEP * 1.1)

ax.set_xlabel(x_label, fontsize=9, labelpad=4)
ax.tick_params(axis="x", direction="out", length=2.2, width=0.6, labelsize=8)
ax.tick_params(axis="y", left=False, labelleft=False)

ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

fig.tight_layout(pad=0.8)

# ── Save ────────────────────────────────────────────────────────────────────
pdf_path = HERE / "figure.pdf"
png_path = HERE / "figure.png"
svg_path = HERE / "figure.svg"

fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {pdf_path}, {png_path}, {svg_path}")

# ── Font verification ────────────────────────────────────────────────────────
result = subprocess.run(["pdffonts", str(pdf_path)],
                        capture_output=True, text=True, check=False)
if result.returncode == 0:
    if "Type 3" in result.stdout:
        sys.stderr.write(
            f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{result.stdout}\n"
        )
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    # pdffonts not available — fall back to raw bytes check
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (raw-bytes fallback) — no /Type3 in figure.pdf")
