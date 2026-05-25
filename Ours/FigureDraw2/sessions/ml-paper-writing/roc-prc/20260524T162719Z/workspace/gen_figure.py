import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
scores  = data["scores"]

COLORS = {
    "Baseline":   "#888888",
    "Method-A":   "#4477AA",
    "Method-B":   "#EE6677",
    "OursModel":  "#228833",
}
STYLES = {
    "Baseline":   (2.0, (0, (6, 2))),
    "Method-A":   (1.8, (0, (4, 1.5))),
    "Method-B":   (1.8, (0, (2, 1))),
    "OursModel":  (2.4, "solid"),
}

# ── figure layout ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
fig.subplots_adjust(left=0.08, right=0.97, bottom=0.13, top=0.93, wspace=0.32)

ax_roc, ax_prc = axes

for method in methods:
    pos = np.array(scores[method]["positive"])
    neg = np.array(scores[method]["negative"])

    y_true  = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    lw, ls = STYLES[method]
    col     = COLORS[method]
    label_roc = f"{method}  (AUROC={auroc:.3f})"
    label_prc = f"{method}  (AP={ap:.3f})"

    ax_roc.plot(fpr, tpr, color=col, lw=lw, linestyle=ls, label=label_roc)
    ax_prc.plot(rec, prec, color=col, lw=lw, linestyle=ls, label=label_prc)

# ── ROC reference diagonal ────────────────────────────────────────────────────
ax_roc.plot([0, 1], [0, 1], color="#bbbbbb", lw=1.2, linestyle="--", zorder=0)

# ── PRC prevalence baseline ───────────────────────────────────────────────────
# prevalence = fraction of positives across all methods (each method has same
# number of pos/neg, so prevalence = 0.5 per method; use the first method)
first = methods[0]
n_pos = len(scores[first]["positive"])
n_neg = len(scores[first]["negative"])
prevalence = n_pos / (n_pos + n_neg)
ax_prc.axhline(prevalence, color="#bbbbbb", lw=1.2, linestyle="--", zorder=0,
               label=f"Prevalence ({prevalence:.2f})")

# ── cosmetics ─────────────────────────────────────────────────────────────────
for ax, xlabel, ylabel, title in [
    (ax_roc, "False Positive Rate", "True Positive Rate", "ROC Curve"),
    (ax_prc, "Recall",              "Precision",          "Precision–Recall Curve"),
]:
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.05)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax.tick_params(labelsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7.5, loc="lower right" if ax is ax_roc else "lower left",
              framealpha=0.85, edgecolor="#cccccc")

# ── save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
