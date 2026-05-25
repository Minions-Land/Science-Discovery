import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

# Load data
with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores = data["scores"]

# Colour / style map
colors = {
    "Baseline":   "#888888",
    "Method-A":   "#4477AA",
    "Method-B":   "#EE6677",
    "OursModel":  "#228833",
}
lw = 1.6

fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))

for method in methods:
    pos = np.array(scores[method]["positive"])
    neg = np.array(scores[method]["negative"])

    y_true  = np.concatenate([np.ones(len(pos)),  np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # --- ROC ---
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # --- PRC ---
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    color = colors[method]
    label_roc = f"{method}  (AUC={auroc:.3f})"
    label_prc = f"{method}  (AP={ap:.3f})"

    axes[0].plot(fpr, tpr, color=color, lw=lw, label=label_roc)
    axes[1].plot(rec, prec, color=color, lw=lw, label=label_prc)

# Prevalence for PRC baseline
n_pos_total = sum(len(scores[m]["positive"]) for m in methods)
n_neg_total = sum(len(scores[m]["negative"]) for m in methods)
prevalence  = n_pos_total / (n_pos_total + n_neg_total)   # per-method equal, = 0.5

# ROC diagonal
axes[0].plot([0, 1], [0, 1], "k--", lw=0.9, label="Random (AUC=0.500)")
axes[0].set_xlabel("False Positive Rate")
axes[0].set_ylabel("True Positive Rate")
axes[0].set_title("ROC Curve")
axes[0].set_xlim(0, 1); axes[0].set_ylim(0, 1.01)
axes[0].legend(fontsize=7.5, framealpha=0.9, loc="lower right")
axes[0].set_aspect("equal")

# PRC prevalence baseline
axes[1].axhline(prevalence, color="k", ls="--", lw=0.9,
                label=f"Random (AP={prevalence:.3f})")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precision")
axes[1].set_title("Precision–Recall Curve")
axes[1].set_xlim(0, 1); axes[1].set_ylim(0, 1.01)
axes[1].legend(fontsize=7.5, framealpha=0.9, loc="lower left")
axes[1].set_aspect("equal")

fig.tight_layout(pad=1.2)

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
