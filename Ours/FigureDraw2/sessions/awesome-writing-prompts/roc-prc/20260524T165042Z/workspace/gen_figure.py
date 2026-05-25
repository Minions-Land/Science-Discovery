import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from matplotlib.lines import Line2D

with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores = data["scores"]

colors = {
    "Baseline":  "#888888",
    "Method-A":  "#4878CF",
    "Method-B":  "#6ACC65",
    "OursModel": "#D65F5F",
}
linestyles = {
    "Baseline":  (0, (4, 2)),
    "Method-A":  (0, (2, 1)),
    "Method-B":  "dashdot",
    "OursModel": "solid",
}

fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
fig.subplots_adjust(left=0.07, right=0.97, bottom=0.13, top=0.93, wspace=0.32)

all_n_pos = []
all_n_neg = []
for m in methods:
    all_n_pos.append(len(scores[m]["positive"]))
    all_n_neg.append(len(scores[m]["negative"]))

# assume same prevalence for all methods (they share ground truth labels)
n_pos = all_n_pos[0]
n_neg = all_n_neg[0]
prevalence = n_pos / (n_pos + n_neg)

legend_handles_roc = []
legend_handles_prc = []

for m in methods:
    pos = np.array(scores[m]["positive"])
    neg = np.array(scores[m]["negative"])
    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    lw = 2.2 if m == "OursModel" else 1.6
    c = colors[m]
    ls = linestyles[m]

    axes[0].plot(fpr, tpr, color=c, lw=lw, linestyle=ls)
    axes[1].plot(rec, prec, color=c, lw=lw, linestyle=ls)

    label_roc = f"{m}  (AUROC={auroc:.3f})"
    label_prc = f"{m}  (AP={ap:.3f})"
    legend_handles_roc.append(Line2D([0], [0], color=c, lw=lw, linestyle=ls, label=label_roc))
    legend_handles_prc.append(Line2D([0], [0], color=c, lw=lw, linestyle=ls, label=label_prc))

# ROC panel
axes[0].plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5, label="Random (AUROC=0.500)")
axes[0].set_xlabel("False Positive Rate", fontsize=11)
axes[0].set_ylabel("True Positive Rate", fontsize=11)
axes[0].set_title("ROC Curve", fontsize=12, fontweight="bold")
axes[0].set_xlim(-0.01, 1.01)
axes[0].set_ylim(-0.01, 1.02)
axes[0].legend(handles=legend_handles_roc + [Line2D([0],[0],color="k",lw=1,linestyle="--",alpha=0.5,label="Random (AUROC=0.500)")],
               fontsize=7.5, loc="lower right", framealpha=0.9)

# PRC panel
axes[1].axhline(prevalence, color="k", lw=1, linestyle="--", alpha=0.5,
                label=f"Prevalence baseline (P={prevalence:.2f})")
axes[1].set_xlabel("Recall", fontsize=11)
axes[1].set_ylabel("Precision", fontsize=11)
axes[1].set_title("Precision-Recall Curve", fontsize=12, fontweight="bold")
axes[1].set_xlim(-0.01, 1.01)
axes[1].set_ylim(-0.01, 1.02)
axes[1].legend(handles=legend_handles_prc + [Line2D([0],[0],color="k",lw=1,linestyle="--",alpha=0.5,
               label=f"Prevalence baseline (P={prevalence:.2f})")],
               fontsize=7.5, loc="upper right", framealpha=0.9)

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
