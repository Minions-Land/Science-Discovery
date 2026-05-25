import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores_data = data["scores"]

# Color palette
colors = {
    "Baseline":  "#888888",
    "Method-A":  "#4477AA",
    "Method-B":  "#EE6677",
    "OursModel": "#228833",
}
lw = 1.6

fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))

total_pos = 0
total_neg = 0

for method in methods:
    pos = np.array(scores_data[method]["positive"])
    neg = np.array(scores_data[method]["negative"])
    total_pos = len(pos)
    total_neg = len(neg)

    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    label_roc = f"{method} (AUROC={auroc:.3f})"
    label_prc = f"{method} (AP={ap:.3f})"
    c = colors[method]
    ls = "--" if method == "Baseline" else "-"

    axes[0].plot(fpr, tpr, color=c, lw=lw, linestyle=ls, label=label_roc)
    axes[1].plot(rec, prec, color=c, lw=lw, linestyle=ls, label=label_prc)

# Reference lines
axes[0].plot([0, 1], [0, 1], color="black", lw=0.8, linestyle=":", label="Chance")

prevalence = total_pos / (total_pos + total_neg)
axes[1].axhline(prevalence, color="black", lw=0.8, linestyle=":", label=f"Prevalence ({prevalence:.2f})")

for ax, xlabel, ylabel, title in [
    (axes[0], "False Positive Rate", "True Positive Rate", "ROC Curve"),
    (axes[1], "Recall", "Precision", "Precision-Recall Curve"),
]:
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.05])
    ax.legend(fontsize=7.5, loc="lower right" if ax is axes[0] else "upper right",
              framealpha=0.85)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)

fig.tight_layout(pad=1.5)
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
