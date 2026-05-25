"""
Volcano plot for ~3000 genes.
Data source: data.json (log2fc, neg_log10_p, thresholds)
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
import matplotlib.patches as mpatches
import numpy as np

# ── data ──────────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    d = json.load(f)

log2fc = np.array(d["log2fc"])
nlp    = np.array(d["neg_log10_p"])
thr_fc = d["thresholds"]["abs_log2fc"]      # 1.0
thr_p  = d["thresholds"]["neg_log10_p"]     # 2.0

# ── classify ──────────────────────────────────────────────────────────────────
up   = (log2fc >=  thr_fc) & (nlp >= thr_p)
down = (log2fc <= -thr_fc) & (nlp >= thr_p)
ns   = ~up & ~down

# ── palette ───────────────────────────────────────────────────────────────────
PALETTE = {
    "up":      "#C0392B",   # directional red
    "down":    "#2471A3",   # directional blue
    "ns":      "#AAAAAA",   # neutral grey
    "thresh":  "#555555",   # threshold lines
    "label":   "#1A1A1A",   # annotation text
}

# ── figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))

# scatter — non-sig first (bottom layer)
ax.scatter(log2fc[ns],   nlp[ns],   s=5,  c=PALETTE["ns"],   alpha=0.45, linewidths=0, rasterized=True)
ax.scatter(log2fc[down], nlp[down], s=6,  c=PALETTE["down"],  alpha=0.75, linewidths=0, rasterized=True)
ax.scatter(log2fc[up],   nlp[up],   s=6,  c=PALETTE["up"],    alpha=0.75, linewidths=0, rasterized=True)

# threshold lines
ax.axhline(thr_p,   color=PALETTE["thresh"], lw=0.7, ls="--", alpha=0.6)
ax.axvline( thr_fc, color=PALETTE["thresh"], lw=0.7, ls="--", alpha=0.6)
ax.axvline(-thr_fc, color=PALETTE["thresh"], lw=0.7, ls="--", alpha=0.6)

# ── annotate top-5 by neg_log10_p ─────────────────────────────────────────────
sig_mask = up | down
if sig_mask.sum() >= 5:
    sig_idx = np.where(sig_mask)[0]
    top5 = sig_idx[np.argsort(nlp[sig_idx])[-5:]]
else:
    top5 = np.argsort(nlp)[-5:]

for i, idx in enumerate(top5):
    x, y = log2fc[idx], nlp[idx]
    label = f"gene{idx}"
    ax.annotate(
        label,
        xy=(x, y),
        xytext=(x + (0.25 if x > 0 else -0.25), y + 0.18),
        fontsize=6.5,
        color=PALETTE["label"],
        ha="left" if x > 0 else "right",
        arrowprops=dict(arrowstyle="-", color="#888888", lw=0.5),
    )

# ── axes cosmetics ────────────────────────────────────────────────────────────
ax.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax.set_xlabel(r"log$_2$ fold change", fontsize=9)
ax.set_ylabel(r"$-$log$_{10}$(p)", fontsize=9)
ax.set_title("Differential expression — volcano plot", fontsize=10, pad=8)

# counts in corners
n_up   = int(up.sum())
n_down = int(down.sum())
ax.text(0.98, 0.98, f"Up: {n_up}",   transform=ax.transAxes,
        ha="right", va="top", fontsize=8, color=PALETTE["up"])
ax.text(0.02, 0.98, f"Down: {n_down}", transform=ax.transAxes,
        ha="left",  va="top", fontsize=8, color=PALETTE["down"])

# legend
patches = [
    mpatches.Patch(color=PALETTE["up"],   label=f"Up (FC≥{thr_fc}, -log10 p≥{thr_p})"),
    mpatches.Patch(color=PALETTE["down"], label=f"Down (FC≤-{thr_fc}, -log10 p≥{thr_p})"),
    mpatches.Patch(color=PALETTE["ns"],   label="Not significant"),
]
ax.legend(handles=patches, fontsize=7.5, loc="upper center",
          bbox_to_anchor=(0.5, -0.13), ncol=3, handlelength=1.0)

fig.tight_layout()

# ── save ──────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {pdf_path}, {png_path}, {svg_path}")
print(f"  n={len(log2fc)}  up={n_up}  down={n_down}  ns={int(ns.sum())}")

# ── font-type verification ─────────────────────────────────────────────────────
import re
raw = pdf_path.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)

out = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if out.returncode == 0:
    if "Type 3" in out.stdout:
        sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    print("[fonttype-check] pdffonts not available; byte-level check passed.")
