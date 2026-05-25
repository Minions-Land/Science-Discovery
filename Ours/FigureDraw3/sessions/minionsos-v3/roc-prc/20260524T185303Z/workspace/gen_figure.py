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
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "font.size": 9,
})
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

# Okabe-Ito colorblind-safe palette
PALETTE = {
    "Baseline":   "#767676",
    "Method-A":   "#56B4E9",
    "Method-B":   "#E69F00",
    "OursModel":  "#0072B2",
}
LINESTYLE = {
    "Baseline":  (0, (4, 2)),
    "Method-A":  (0, (2, 1)),
    "Method-B":  "--",
    "OursModel": "-",
}
LINEWIDTH = {
    "Baseline":  1.2,
    "Method-A":  1.2,
    "Method-B":  1.2,
    "OursModel": 2.0,
}

with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores  = data["scores"]

# Build labels + score arrays
def build_arrays(method):
    pos = scores[method]["positive"]
    neg = scores[method]["negative"]
    y_true  = np.array([1]*len(pos) + [0]*len(neg))
    y_score = np.array(pos + neg)
    return y_true, y_score

prevalence = None  # computed from first method (same for all)

fig, (ax_roc, ax_prc) = plt.subplots(1, 2, figsize=(10, 4))

for method in methods:
    y_true, y_score = build_arrays(method)
    if prevalence is None:
        prevalence = y_true.mean()

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)
    ax_roc.plot(fpr, tpr,
                color=LINESTYLE[method] and PALETTE[method],
                linestyle=LINESTYLE[method],
                linewidth=LINEWIDTH[method],
                label=f"{method}  AUROC={auroc:.3f}")

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)
    ax_prc.plot(rec, prec,
                color=PALETTE[method],
                linestyle=LINESTYLE[method],
                linewidth=LINEWIDTH[method],
                label=f"{method}  AP={ap:.3f}")

# ROC reference diagonal
ax_roc.plot([0, 1], [0, 1], color="#AAAAAA", linewidth=0.8, linestyle=":", zorder=0)
ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.02)
ax_roc.set_xlabel("False Positive Rate", fontsize=9)
ax_roc.set_ylabel("True Positive Rate", fontsize=9)
ax_roc.set_title("ROC Curve", fontsize=10, fontweight="bold")
ax_roc.tick_params(direction="out", length=2.2, width=0.6)
ax_roc.legend(loc="lower right", fontsize=7.5)

# PRC prevalence baseline
ax_prc.axhline(prevalence, color="#AAAAAA", linewidth=0.8, linestyle=":",
               zorder=0, label=f"Random  (prev={prevalence:.2f})")
ax_prc.set_xlim(-0.02, 1.02)
ax_prc.set_ylim(-0.02, 1.02)
ax_prc.set_xlabel("Recall", fontsize=9)
ax_prc.set_ylabel("Precision", fontsize=9)
ax_prc.set_title("Precision-Recall Curve", fontsize=10, fontweight="bold")
ax_prc.tick_params(direction="out", length=2.2, width=0.6)
ax_prc.legend(loc="upper right", fontsize=7.5)

# Panel labels
for ax, letter in [(ax_roc, "a"), (ax_prc, "b")]:
    ax.text(-0.12, 1.04, letter, transform=ax.transAxes,
            fontsize=10, fontweight="bold", va="top", ha="left")

fig.tight_layout(pad=1.2)

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
