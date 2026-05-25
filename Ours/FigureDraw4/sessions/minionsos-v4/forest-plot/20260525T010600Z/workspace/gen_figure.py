"""
Forest plot — 12 studies + pooled estimate (inverse-variance weighting).
Data source: data.json in the same directory.
"""

import json
import pathlib
import subprocess
import sys

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

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

PALETTE = {
    "signal":       "#0F4D92",
    "signal_soft":  "#B4C0E4",
    "neutral":      "#767676",
    "neutral_light": "#D8D8D8",
    "pooled":       "#1A1A1A",
    "null_line":    "#AAAAAA",
}

# ── Load data ────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    d = json.load(f)

studies = d["studies"]          # list of 12 names
effects = np.array(d["effects"])
se      = np.array(d["se"])
xlabel  = d["label"]

n = len(studies)
assert n == 12

# ── Pooled estimate (inverse-variance fixed-effects) ─────────────────────────
weights      = 1.0 / se**2
pooled_eff   = np.sum(weights * effects) / np.sum(weights)
pooled_se    = np.sqrt(1.0 / np.sum(weights))
pooled_lo    = pooled_eff - 1.96 * pooled_se
pooled_hi    = pooled_eff + 1.96 * pooled_se

# ── Per-study 95% CIs ────────────────────────────────────────────────────────
ci_lo = effects - 1.96 * se
ci_hi = effects + 1.96 * se

# ── Layout ───────────────────────────────────────────────────────────────────
# Single panel; studies top-to-bottom, pooled at bottom with a separator gap.
# y positions: study 0 at top (y = n-1), study n-1 at y=0; pooled at y=-1.5
y_studies = np.arange(n - 1, -1, -1, dtype=float)   # n-1 … 0
y_pooled  = -1.8

fig, ax = plt.subplots(figsize=(7, 6))

# Marker size proportional to weight (visual weight ∝ sqrt(w) for readability)
w_norm   = weights / weights.max()
sq_sizes = 40 + 120 * w_norm   # pt²; range ~40–160

# ── Study rows ───────────────────────────────────────────────────────────────
for i, (y, eff, lo, hi, sz) in enumerate(
        zip(y_studies, effects, ci_lo, ci_hi, sq_sizes)):
    ax.plot([lo, hi], [y, y], color=PALETTE["signal"], lw=1.2, solid_capstyle="round")
    ax.scatter([eff], [y], s=sz, color=PALETTE["signal"],
               zorder=3, linewidths=0)

# ── Separator line ────────────────────────────────────────────────────────────
ax.axhline(y=-0.8, color=PALETTE["neutral_light"], lw=0.8, ls="--")

# ── Pooled diamond ────────────────────────────────────────────────────────────
dh = 0.35   # half-height of diamond
diamond = mpatches.FancyArrow(0, 0, 0, 0)   # placeholder; draw as Polygon
diamond_xy = np.array([
    [pooled_lo,  y_pooled],
    [pooled_eff, y_pooled + dh],
    [pooled_hi,  y_pooled],
    [pooled_eff, y_pooled - dh],
])
diamond_patch = mpatches.Polygon(
    diamond_xy, closed=True,
    facecolor=PALETTE["pooled"], edgecolor=PALETTE["pooled"], zorder=4
)
ax.add_patch(diamond_patch)

# ── Null line ─────────────────────────────────────────────────────────────────
ax.axvline(0, color=PALETTE["null_line"], lw=0.9, ls="--", zorder=0)

# ── Axis labels ───────────────────────────────────────────────────────────────
ax.set_yticks(list(y_studies) + [y_pooled])
ax.set_yticklabels(studies + ["Pooled (IV)"], fontsize=8)
ax.set_xlabel(xlabel, fontsize=9)
ax.tick_params(axis="x", direction="out", length=2.2, width=0.6, labelsize=8)
ax.tick_params(axis="y", length=0)

# ── Annotate pooled estimate ──────────────────────────────────────────────────
ax.text(
    pooled_hi + 0.02, y_pooled,
    f"{pooled_eff:.3f} [{pooled_lo:.3f}, {pooled_hi:.3f}]",
    va="center", ha="left", fontsize=7.5, color=PALETTE["pooled"]
)

# ── x-axis range ─────────────────────────────────────────────────────────────
x_all = np.concatenate([ci_lo, ci_hi, [pooled_lo, pooled_hi]])
pad   = 0.08 * (x_all.max() - x_all.min())
ax.set_xlim(x_all.min() - pad, x_all.max() + pad + 0.55)  # extra right for annotation

# ── y-axis range ─────────────────────────────────────────────────────────────
ax.set_ylim(y_pooled - 0.7, y_studies[0] + 0.7)
ax.spines["left"].set_visible(False)

# ── Favour / harm labels ──────────────────────────────────────────────────────
y_label = y_pooled - 0.55
ax.text(-0.01, y_label, "← Favours control", ha="right", va="top",
        fontsize=7, color=PALETTE["neutral"], style="italic")
ax.text(0.01, y_label, "Favours intervention →", ha="left", va="top",
        fontsize=7, color=PALETTE["neutral"], style="italic")

fig.tight_layout()

# ── Save ──────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {pdf_path}, {png_path}, {svg_path}")
print(f"Pooled estimate: {pooled_eff:.3f} (95% CI [{pooled_lo:.3f}, {pooled_hi:.3f}])")

# ── Font-type verification ────────────────────────────────────────────────────
result = subprocess.run(
    ["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False
)
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
    import re
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (raw-bytes fallback) — no /Type3 in figure.pdf")
