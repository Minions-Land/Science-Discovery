import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score

# ── load data ──────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]
colors  = ["#4477AA", "#EE6677", "#228833", "#AA3377"]
markers = ["o", "s", "^", "D"]

# ── figure layout ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
ax_roc, ax_prc = axes

legend_handles = []

all_pos = []
for m in methods:
    all_pos.extend(data["scores"][m]["positive"])
all_neg = []
for m in methods:
    all_neg.extend(data["scores"][m]["negative"])

# prevalence = fraction of positives among all samples for one method
# (same for every method as dataset sizes match)
n_pos = len(data["scores"][methods[0]]["positive"])
n_neg = len(data["scores"][methods[0]]["negative"])
prevalence = n_pos / (n_pos + n_neg)

for i, method in enumerate(methods):
    pos_scores = np.array(data["scores"][method]["positive"])
    neg_scores = np.array(data["scores"][method]["negative"])

    y_true  = np.concatenate([np.ones(len(pos_scores)), np.zeros(len(neg_scores))])
    y_score = np.concatenate([pos_scores, neg_scores])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    lw   = 1.8
    col  = colors[i]
    lbl  = f"{method}  (AUROC={auroc:.3f})"
    lbl2 = f"{method}  (AP={ap:.3f})"

    ax_roc.plot(fpr, tpr, color=col, lw=lw, alpha=0.9)
    ax_prc.plot(rec, prec, color=col, lw=lw, alpha=0.9)

    # shared legend handle with both metrics
    legend_handles.append(
        Line2D([0], [0], color=col, lw=lw,
               label=f"{method}  AUROC={auroc:.3f}  AP={ap:.3f}")
    )

# ── ROC reference diagonal ─────────────────────────────────────────────────────
ax_roc.plot([0, 1], [0, 1], "k--", lw=0.9, alpha=0.5, label="Random")

# ── PRC prevalence baseline ────────────────────────────────────────────────────
ax_prc.axhline(prevalence, color="k", ls="--", lw=0.9, alpha=0.5,
               label=f"Prevalence ({prevalence:.2f})")

# ── axes formatting ────────────────────────────────────────────────────────────
for ax in axes:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.tick_params(labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

ax_roc.set_xlabel("False Positive Rate", fontsize=10)
ax_roc.set_ylabel("True Positive Rate", fontsize=10)
ax_roc.set_title("ROC Curve", fontsize=11, fontweight="bold")

ax_prc.set_xlabel("Recall", fontsize=10)
ax_prc.set_ylabel("Precision", fontsize=10)
ax_prc.set_title("Precision–Recall Curve", fontsize=11, fontweight="bold")

# ── shared legend below both panels ───────────────────────────────────────────
fig.legend(
    handles=legend_handles,
    loc="lower center",
    ncol=2,
    fontsize=8.5,
    frameon=False,
    bbox_to_anchor=(0.5, -0.08),
)

fig.tight_layout(rect=[0, 0.06, 1, 1])

# ── save ───────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=200, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
