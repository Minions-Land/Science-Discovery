import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores_data = data["scores"]

# Color palette — distinct, print-friendly
COLORS = {
    "Baseline":  "#888888",
    "Method-A":  "#2196F3",
    "Method-B":  "#FF9800",
    "OursModel": "#E53935",
}
STYLES = {
    "Baseline":  (1.5, (4, 2)),
    "Method-A":  (1.8, (2, 1.5)),
    "Method-B":  (1.8, (1, 0)),
    "OursModel": (2.2, (1, 0)),
}

fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))

legend_handles = []

for method in methods:
    pos = np.array(scores_data[method]["positive"])
    neg = np.array(scores_data[method]["negative"])
    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    lw, dash = STYLES[method]
    c = COLORS[method]
    ls = "--" if method == "Baseline" else "-"

    axes[0].plot(fpr, tpr, color=c, lw=lw, linestyle=ls,
                 label=f"{method} (AUROC={auroc:.3f})")
    axes[1].plot(recall, precision, color=c, lw=lw, linestyle=ls,
                 label=f"{method} (AP={ap:.3f})")

    legend_handles.append(
        Line2D([0], [0], color=c, lw=lw, linestyle=ls,
               label=f"{method}  AUROC={auroc:.3f}  AP={ap:.3f}")
    )

# ROC diagonal reference
axes[0].plot([0, 1], [0, 1], color="#cccccc", lw=1.2, linestyle=":", zorder=0)
axes[0].set_xlabel("False Positive Rate", fontsize=11)
axes[0].set_ylabel("True Positive Rate", fontsize=11)
axes[0].set_title("ROC Curve", fontsize=12, fontweight="bold")
axes[0].set_xlim(-0.02, 1.02)
axes[0].set_ylim(-0.02, 1.05)
axes[0].legend(fontsize=8.5, loc="lower right", framealpha=0.9)

# PRC prevalence baseline
n_pos_total = sum(len(scores_data[m]["positive"]) for m in methods)
n_total = n_pos_total + sum(len(scores_data[m]["negative"]) for m in methods)
# Use per-method average (all methods have same class sizes here)
prevalence = len(scores_data["Baseline"]["positive"]) / (
    len(scores_data["Baseline"]["positive"]) + len(scores_data["Baseline"]["negative"])
)
axes[1].axhline(prevalence, color="#cccccc", lw=1.2, linestyle=":",
                zorder=0, label=f"Prevalence ({prevalence:.2f})")
axes[1].set_xlabel("Recall", fontsize=11)
axes[1].set_ylabel("Precision", fontsize=11)
axes[1].set_title("Precision-Recall Curve", fontsize=12, fontweight="bold")
axes[1].set_xlim(-0.02, 1.02)
axes[1].set_ylim(-0.02, 1.05)
axes[1].legend(fontsize=8.5, loc="upper right", framealpha=0.9)

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)

fig.tight_layout(pad=1.5)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
