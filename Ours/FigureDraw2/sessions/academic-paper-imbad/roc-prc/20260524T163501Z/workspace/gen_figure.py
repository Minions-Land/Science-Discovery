import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

DATA_PATH = "data.json"

with open(DATA_PATH) as f:
    data = json.load(f)

methods = data["methods"]
scores_raw = data["scores"]

# Color palette: colorblind-friendly
COLORS = {
    "Baseline":  "#666666",
    "Method-A":  "#2166ac",
    "Method-B":  "#d6604d",
    "OursModel": "#1a9641",
}
LINESTYLES = {
    "Baseline":  (0, (3, 1.5)),  # loosely dashed
    "Method-A":  (0, (5, 1)),    # dashed
    "Method-B":  (0, (1, 1)),    # dotted
    "OursModel": "-",
}
LINEWIDTHS = {
    "Baseline":  1.5,
    "Method-A":  1.5,
    "Method-B":  1.5,
    "OursModel": 2.2,
}

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4))

all_n_pos = []
all_n_neg = []

for method in methods:
    pos = np.array(scores_raw[method]["positive"])
    neg = np.array(scores_raw[method]["negative"])
    all_n_pos.append(len(pos))
    all_n_neg.append(len(neg))

    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    label_roc = f"{method} (AUC={auroc:.3f})"
    label_prc = f"{method} (AP={ap:.3f})"

    kw = dict(color=COLORS[method], linestyle=LINESTYLES[method],
              linewidth=LINEWIDTHS[method])

    axes[0].plot(fpr, tpr, label=label_roc, **kw)
    axes[1].plot(rec, prec, label=label_prc, **kw)

# Reference lines
axes[0].plot([0, 1], [0, 1], color="black", lw=0.8, linestyle="--", alpha=0.5,
             label="Random (AUC=0.500)")

n_pos_mean = int(np.mean(all_n_pos))
n_neg_mean = int(np.mean(all_n_neg))
prevalence = n_pos_mean / (n_pos_mean + n_neg_mean)
axes[1].axhline(prevalence, color="black", lw=0.8, linestyle="--", alpha=0.5,
                label=f"Prevalence ({prevalence:.3f})")

# Formatting
for ax, xlabel, ylabel, title in [
    (axes[0], "False Positive Rate", "True Positive Rate", "ROC Curve"),
    (axes[1], "Recall", "Precision",                       "Precision–Recall Curve"),
]:
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=7.2, loc="lower right" if ax is axes[0] else "lower left",
              framealpha=0.85, edgecolor="#cccccc")

fig.tight_layout(pad=1.2)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
