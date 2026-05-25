#!/usr/bin/env python3
"""Generate two-panel ROC + Precision-Recall figure for 4 binary classifiers."""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

# --- Publication styling ---
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "legend.fontsize": 7.5,
    "legend.frameon": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.15,
    "grid.linestyle": "-",
    "lines.linewidth": 1.6,
})

# Colorblind-safe "Ocean Dusk" palette; OursModel gets coral
COLORS = {
    "Baseline":  "#8C8C8C",   # gray — recedes
    "Method-A":  "#2A9D8F",   # teal
    "Method-B":  "#0072B2",   # blue
    "OursModel": "#E76F51",   # coral — stands out
}
MARKERS = {
    "Baseline":  "s",
    "Method-A":  "^",
    "Method-B":  "D",
    "OursModel": "o",
}
LINESTYLES = {
    "Baseline":  "--",
    "Method-A":  "-.",
    "Method-B":  ":",
    "OursModel": "-",
}

# Load data
with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores_data = data["scores"]

# Build labels + scores arrays
def get_labels_scores(method):
    pos = scores_data[method]["positive"]
    neg = scores_data[method]["negative"]
    y_true = np.array([1] * len(pos) + [0] * len(neg))
    y_score = np.array(pos + neg)
    return y_true, y_score

# Compute prevalence (same for all methods since same pos/neg counts)
y_true_ref, _ = get_labels_scores(methods[0])
prevalence = y_true_ref.mean()

# --- Figure layout ---
fig, axes = plt.subplots(1, 2, figsize=(6.75, 2.9))
ax_roc, ax_prc = axes

# Panel labels
for i, ax in enumerate(axes):
    ax.text(-0.12, 1.04, f"({'ab'[i]})", transform=ax.transAxes,
            fontsize=11, fontweight="bold", va="top")

# --- ROC panel ---
ax_roc.plot([0, 1], [0, 1], color="#AAAAAA", linewidth=1.0, linestyle="--",
            zorder=1, label="Random (AUROC = 0.50)")

for method in methods:
    y_true, y_score = get_labels_scores(method)
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)
    color = COLORS[method]
    lw = 2.2 if method == "OursModel" else 1.5
    zorder = 4 if method == "OursModel" else 2
    ax_roc.plot(fpr, tpr,
                color=color,
                linewidth=lw,
                linestyle=LINESTYLES[method],
                zorder=zorder,
                label=f"{method} (AUROC = {auroc:.3f})")

ax_roc.set_xlabel("False Positive Rate")
ax_roc.set_ylabel("True Positive Rate")
ax_roc.set_title("(a) ROC Curve", loc="left", pad=4)
ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.05)
ax_roc.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax_roc.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax_roc.legend(loc="lower right", handlelength=1.8, fontsize=7.2)

# --- PRC panel ---
ax_prc.axhline(y=prevalence, color="#AAAAAA", linewidth=1.0, linestyle="--",
               zorder=1, label=f"Prevalence baseline (AP = {prevalence:.3f})")

for method in methods:
    y_true, y_score = get_labels_scores(method)
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)
    color = COLORS[method]
    lw = 2.2 if method == "OursModel" else 1.5
    zorder = 4 if method == "OursModel" else 2
    ax_prc.plot(recall, precision,
                color=color,
                linewidth=lw,
                linestyle=LINESTYLES[method],
                zorder=zorder,
                label=f"{method} (AP = {ap:.3f})")

ax_prc.set_xlabel("Recall")
ax_prc.set_ylabel("Precision")
ax_prc.set_title("(b) Precision-Recall Curve", loc="left", pad=4)
ax_prc.set_xlim(-0.02, 1.02)
ax_prc.set_ylim(-0.02, 1.05)
ax_prc.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax_prc.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax_prc.legend(loc="upper right", handlelength=1.8, fontsize=7.2)

plt.tight_layout(pad=0.8, w_pad=1.2)

fig.savefig("figure.pdf")
fig.savefig("figure.png", dpi=300)
try:
    fig.savefig("figure.svg")
except Exception:
    pass

print("Saved: figure.pdf, figure.png, figure.svg")
plt.close()
