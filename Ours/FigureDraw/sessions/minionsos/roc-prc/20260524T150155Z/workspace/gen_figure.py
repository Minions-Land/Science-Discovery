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

# Color palette (colorblind-friendly)
colors = ["#4477AA", "#EE6677", "#228833", "#CCBB44"]
linestyles = ["-", "--", "-.", ":"]

fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))

# Compute prevalence across all methods (same positive/negative counts per method)
# Use first method to get prevalence
n_pos = len(scores[methods[0]]["positive"])
n_neg = len(scores[methods[0]]["negative"])
prevalence = n_pos / (n_pos + n_neg)

# --- Panel A: ROC ---
ax = axes[0]
ax.plot([0, 1], [0, 1], color="gray", lw=0.8, linestyle="--", zorder=0, label="_nolegend_")

for method, color, ls in zip(methods, colors, linestyles):
    pos = np.array(scores[method]["positive"])
    neg = np.array(scores[method]["negative"])
    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=color, lw=1.8, linestyle=ls,
            label=f"{method}  (AUROC={auroc:.3f})")

ax.set_xlabel("False Positive Rate", fontsize=10)
ax.set_ylabel("True Positive Rate", fontsize=10)
ax.set_title("ROC Curve", fontsize=11, fontweight="bold")
ax.legend(fontsize=7.5, loc="lower right", framealpha=0.9)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect("equal")
ax.text(0.03, 0.93, "(a)", transform=ax.transAxes, fontsize=11, fontweight="bold")

# --- Panel B: Precision-Recall ---
ax = axes[1]
ax.axhline(prevalence, color="gray", lw=0.8, linestyle="--", zorder=0,
           label=f"Prevalence ({prevalence:.2f})")

for method, color, ls in zip(methods, colors, linestyles):
    pos = np.array(scores[method]["positive"])
    neg = np.array(scores[method]["negative"])
    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)
    ax.plot(recall, precision, color=color, lw=1.8, linestyle=ls,
            label=f"{method}  (AP={ap:.3f})")

ax.set_xlabel("Recall", fontsize=10)
ax.set_ylabel("Precision", fontsize=10)
ax.set_title("Precision-Recall Curve", fontsize=11, fontweight="bold")
ax.legend(fontsize=7.5, loc="upper right", framealpha=0.9)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect("equal")
ax.text(0.03, 0.93, "(b)", transform=ax.transAxes, fontsize=11, fontweight="bold")

fig.tight_layout(pad=1.5)

fig.savefig("figure.pdf", bbox_inches="tight", dpi=300)
fig.savefig("figure.png", bbox_inches="tight", dpi=300)
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
