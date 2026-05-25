#!/usr/bin/env python3
"""
gen_figure.py — validation-loss training curves with 95% CI bands.
Data source: data.json (3 methods × 50 steps, n_seeds=5)
"""

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

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import numpy as np

# ── Palette (Okabe-Ito colorblind-safe) ─────────────────────────────────────
PALETTE = {
    "Baseline":   "#767676",   # neutral grey
    "Method-A":   "#E69F00",   # amber
    "OursModel":  "#0072B2",   # deep blue — accent for our method
    "Baseline_band":  "#D8D8D8",
    "Method-A_band":  "#F5DFA0",
    "OursModel_band": "#B4C0E4",
}

# ── Load data ────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

steps   = np.array(data["steps"])
methods = data["methods"]   # ["Baseline", "Method-A", "OursModel"]
curves  = data["curves"]

# ── Figure ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))

for method in methods:
    mean    = np.array(curves[method]["mean"])
    ci_half = np.array(curves[method]["ci_half"])
    color   = PALETTE[method]
    band    = PALETTE.get(f"{method}_band", color)
    lw      = 2.0 if method == "OursModel" else 1.6
    zorder  = 3 if method == "OursModel" else 2

    ax.fill_between(steps, mean - ci_half, mean + ci_half,
                    color=band, alpha=0.25, linewidth=0, zorder=zorder - 1)
    ax.plot(steps, mean,
            color=color, linewidth=lw, label=method, zorder=zorder)

# ── Final-step gap annotation ────────────────────────────────────────────────
last = steps[-1]
ours_final    = curves["OursModel"]["mean"][-1]
methodA_final = curves["Method-A"]["mean"][-1]
gap = methodA_final - ours_final   # how much lower OursModel is

ax.annotate(
    f"−{gap:.2f}",
    xy=(last, ours_final),
    xytext=(6, -2),
    textcoords="offset points",
    fontsize=8,
    color=PALETTE["OursModel"],
    va="top",
)

# Bracket lines from Method-A to OursModel at final step
ax.annotate(
    "",
    xy=(last, ours_final),
    xytext=(last, methodA_final),
    arrowprops=dict(arrowstyle="-", color="#999999", lw=0.8,
                    connectionstyle="arc3,rad=0"),
)

# ── Axes ─────────────────────────────────────────────────────────────────────
ax.set_yscale("log")
ax.set_xlabel("Training step", fontsize=10)
ax.set_ylabel("Validation loss", fontsize=10)
ax.tick_params(axis="both", labelsize=8, direction="out", length=2.2, width=0.6)
ax.set_xlim(-1, steps[-1] + 2)

# ── Legend inside axes, upper right ─────────────────────────────────────────
ax.legend(loc="upper right", fontsize=9, frameon=False,
          handlelength=1.6, handletextpad=0.5)

fig.tight_layout()

# ── Save ─────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
print(f"Saved: {pdf_path}, {png_path}, {svg_path}")

# ── Font-type verification ────────────────────────────────────────────────────
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
    # pdffonts not available — fallback to raw bytes scan
    raw = pdf_path.read_bytes()
    import re
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (bytes scan) — no /Type3 in figure.pdf")
