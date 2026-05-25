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
scores_data = data["scores"]

# Color palette suitable for print and colorblind
colors = {
    "Baseline":  "#888888",
    "Method-A":  "#4477AA",
    "Method-B":  "#EE6677",
    "OursModel": "#228833",
}
linestyles = {
    "Baseline":  (0, (4, 2)),     # dashed
    "Method-A":  (0, (4, 2, 1, 2)),  # dash-dot
    "Method-B":  (0, (2, 1)),     # densely dashed
    "OursModel": "solid",
}
linewidths = {
    "Baseline":  1.5,
    "Method-A":  1.5,
    "Method-B":  1.5,
    "OursModel": 2.2,
}

fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
ax_roc, ax_prc = axes

roc_handles = []
prc_handles = []

all_n_pos = []
all_n_neg = []

for method in methods:
    pos = np.array(scores_data[method]["positive"])
    neg = np.array(scores_data[method]["negative"])
    all_n_pos.append(len(pos))
    all_n_neg.append(len(neg))

    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    line, = ax_roc.plot(
        fpr, tpr,
        color=colors[method],
        linestyle=linestyles[method],
        linewidth=linewidths[method],
        label=f"{method}  (AUROC={auroc:.3f})",
        zorder=3 if method == "OursModel" else 2,
    )
    roc_handles.append(line)

    # PRC
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    line2, = ax_prc.plot(
        recall, precision,
        color=colors[method],
        linestyle=linestyles[method],
        linewidth=linewidths[method],
        label=f"{method}  (AP={ap:.3f})",
        zorder=3 if method == "OursModel" else 2,
    )
    prc_handles.append(line2)

# ROC diagonal reference
ax_roc.plot([0, 1], [0, 1], color="#AAAAAA", linewidth=0.9, linestyle=":", zorder=1, label="_nolegend_")

# PRC prevalence baseline
n_pos_total = sum(all_n_pos)
n_total = n_pos_total + sum(all_n_neg)
prevalence = n_pos_total / n_total
ax_prc.axhline(prevalence, color="#AAAAAA", linewidth=0.9, linestyle=":", zorder=1, label="_nolegend_")
ax_prc.text(0.02, prevalence + 0.015, f"Prevalence={prevalence:.2f}",
            color="#888888", fontsize=7.5, va="bottom")

# Formatting — ROC
ax_roc.set_xlabel("False Positive Rate", fontsize=10)
ax_roc.set_ylabel("True Positive Rate", fontsize=10)
ax_roc.set_title("ROC Curve", fontsize=11, fontweight="bold")
ax_roc.set_xlim(-0.02, 1.02)
ax_roc.set_ylim(-0.02, 1.05)
ax_roc.legend(handles=roc_handles, fontsize=8, loc="lower right",
              framealpha=0.9, edgecolor="#cccccc")
ax_roc.tick_params(labelsize=8.5)
ax_roc.set_aspect("equal")

# Formatting — PRC
ax_prc.set_xlabel("Recall", fontsize=10)
ax_prc.set_ylabel("Precision", fontsize=10)
ax_prc.set_title("Precision-Recall Curve", fontsize=11, fontweight="bold")
ax_prc.set_xlim(-0.02, 1.02)
ax_prc.set_ylim(-0.02, 1.05)
ax_prc.legend(handles=prc_handles, fontsize=8, loc="lower left",
              framealpha=0.9, edgecolor="#cccccc")
ax_prc.tick_params(labelsize=8.5)
ax_prc.set_aspect("equal")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_facecolor("#fafafa")

fig.tight_layout(pad=1.5)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
