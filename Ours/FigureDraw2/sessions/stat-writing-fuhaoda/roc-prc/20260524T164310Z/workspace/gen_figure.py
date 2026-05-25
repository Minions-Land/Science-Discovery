import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores = data["scores"]

# Color palette and line styles
colors = ["#888888", "#2196F3", "#FF9800", "#E53935"]
linestyles = ["--", "-.", ":", "-"]
linewidths = [1.4, 1.6, 1.6, 2.2]

fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))

n_pos_total = 0
n_total = 0

for i, method in enumerate(methods):
    pos = np.array(scores[method]["positive"])
    neg = np.array(scores[method]["negative"])
    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    n_pos_total += len(pos)
    n_total += len(pos) + len(neg)

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    label_roc = f"{method}  (AUROC={auroc:.3f})"
    label_prc = f"{method}  (AP={ap:.3f})"

    axes[0].plot(fpr, tpr, color=colors[i], ls=linestyles[i],
                 lw=linewidths[i], label=label_roc)
    axes[1].plot(rec, prec, color=colors[i], ls=linestyles[i],
                 lw=linewidths[i], label=label_prc)

# ROC diagonal
axes[0].plot([0, 1], [0, 1], color="#bbbbbb", lw=1.0, ls="--", zorder=0)
axes[0].set_xlabel("False Positive Rate", fontsize=11)
axes[0].set_ylabel("True Positive Rate", fontsize=11)
axes[0].set_title("ROC Curve", fontsize=12, fontweight="bold")
axes[0].set_xlim(-0.02, 1.02)
axes[0].set_ylim(-0.02, 1.02)
axes[0].legend(fontsize=8.5, loc="lower right", framealpha=0.9)
axes[0].set_aspect("equal")

# PRC prevalence baseline
prevalence = n_pos_total / n_total
axes[1].axhline(prevalence, color="#bbbbbb", lw=1.0, ls="--", zorder=0,
                label=f"Prevalence ({prevalence:.2f})")
axes[1].set_xlabel("Recall", fontsize=11)
axes[1].set_ylabel("Precision", fontsize=11)
axes[1].set_title("Precision-Recall Curve", fontsize=12, fontweight="bold")
axes[1].set_xlim(-0.02, 1.02)
axes[1].set_ylim(-0.02, 1.02)
axes[1].legend(fontsize=8.5, loc="lower left", framealpha=0.9)
axes[1].set_aspect("equal")

for ax in axes:
    ax.tick_params(labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.tight_layout(pad=1.5)

fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
