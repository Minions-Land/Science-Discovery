"""
gen_figure.py — ROC + Precision-Recall two-panel figure for 4 binary classifiers.
Data source: data.json (positive/negative scores per method).
"""

import json
import pathlib
import subprocess
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

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

# Okabe-Ito colorblind-safe palette; last entry reserved for "OursModel" (bold accent)
PALETTE = {
    "Baseline":   "#767676",   # neutral grey
    "Method-A":   "#56B4E9",   # sky blue
    "Method-B":   "#E69F00",   # amber
    "OursModel":  "#0072B2",   # deep blue (signal / hero)
}
LINEWIDTH = {
    "Baseline":  1.0,
    "Method-A":  1.2,
    "Method-B":  1.2,
    "OursModel": 2.0,
}
LINESTYLE = {
    "Baseline":  "--",
    "Method-A":  "-",
    "Method-B":  "-",
    "OursModel": "-",
}

cwd = pathlib.Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())
methods = data["methods"]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
ax_roc, ax_prc = axes

# ── compute prevalence for PRC baseline ──────────────────────────────────────
# Use first method's counts (all methods share the same test set structure)
first = methods[0]
n_pos = len(data["scores"][first]["positive"])
n_neg = len(data["scores"][first]["negative"])
prevalence = n_pos / (n_pos + n_neg)

for method in methods:
    pos = np.array(data["scores"][method]["positive"])
    neg = np.array(data["scores"][method]["negative"])

    scores = np.concatenate([pos, neg])
    labels = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])

    # ROC
    fpr, tpr, _ = roc_curve(labels, scores)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(labels, scores)
    ap = average_precision_score(labels, scores)

    lw = LINEWIDTH[method]
    ls = LINESTYLE[method]
    color = PALETTE[method]
    label_roc = f"{method}  (AUROC={auroc:.3f})"
    label_prc = f"{method}  (AP={ap:.3f})"

    ax_roc.plot(fpr, tpr, color=color, lw=lw, ls=ls, label=label_roc)
    ax_prc.plot(rec, prec, color=color, lw=lw, ls=ls, label=label_prc)

# ── ROC reference diagonal ────────────────────────────────────────────────────
ax_roc.plot([0, 1], [0, 1], color="#BBBBBB", lw=0.8, ls=":", zorder=0)
ax_roc.set_xlabel("False Positive Rate", fontsize=9)
ax_roc.set_ylabel("True Positive Rate", fontsize=9)
ax_roc.set_title("ROC Curve", fontsize=10, fontweight="bold")
ax_roc.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.02)
ax_roc.legend(fontsize=7.5, loc="lower right")

# ── PRC prevalence baseline ───────────────────────────────────────────────────
ax_prc.axhline(prevalence, color="#BBBBBB", lw=0.8, ls=":", zorder=0,
               label=f"Random (prevalence={prevalence:.2f})")
ax_prc.set_xlabel("Recall", fontsize=9)
ax_prc.set_ylabel("Precision", fontsize=9)
ax_prc.set_title("Precision-Recall Curve", fontsize=10, fontweight="bold")
ax_prc.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax_prc.set_xlim(-0.02, 1.02)
ax_prc.set_ylim(-0.02, 1.02)
ax_prc.legend(fontsize=7.5, loc="lower left")

fig.tight_layout(pad=1.5)

out_pdf = cwd / "figure.pdf"
out_png = cwd / "figure.png"
out_svg = cwd / "figure.svg"

fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
fig.savefig(out_svg)
plt.close(fig)

print(f"Saved: {out_pdf}, {out_png}, {out_svg}")

# ── font-type verification ────────────────────────────────────────────────────
result = subprocess.run(["pdffonts", str(out_pdf)], capture_output=True, text=True, check=False)
if result.returncode == 0:
    if "Type 3" in result.stdout:
        sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{result.stdout}\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {out_pdf}")
else:
    import re
    raw = out_pdf.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (pdffonts unavailable; byte-scan passed)")
