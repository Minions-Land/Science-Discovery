import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from scipy.special import expit  # sigmoid for score -> prob

# ── data ────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

methods  = data["methods"]
scores_d = data["scores"]

# ── style ────────────────────────────────────────────────────────────────────
COLORS = {
    "Baseline":  "#9E9E9E",
    "Method-A":  "#4C9BE8",
    "Method-B":  "#E87A4C",
    "OursModel": "#2DB37B",
}
STYLES = {
    "Baseline":  (1.2, "--"),
    "Method-A":  (1.6, "-."),
    "Method-B":  (1.6, ":"),
    "OursModel": (2.2, "-"),
}
LABELS = {
    "Baseline":  "Baseline",
    "Method-A":  "Method-A",
    "Method-B":  "Method-B",
    "OursModel": "Ours",
}

matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 9,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
})

fig = plt.figure(figsize=(7.0, 3.2))
gs  = GridSpec(1, 2, figure=fig, wspace=0.32)
ax_roc = fig.add_subplot(gs[0])
ax_prc = fig.add_subplot(gs[1])

# ── compute prevalence for PRC baseline ─────────────────────────────────────
all_pos = sum(len(scores_d[m]["positive"]) for m in methods)
all_neg = sum(len(scores_d[m]["negative"]) for m in methods)
# use OursModel counts (all methods have same n_pos / n_neg)
n_pos = len(scores_d["OursModel"]["positive"])
n_neg = len(scores_d["OursModel"]["negative"])
prevalence = n_pos / (n_pos + n_neg)

# ── plot curves ──────────────────────────────────────────────────────────────
roc_handles, prc_handles = [], []

for m in methods:
    pos = np.array(scores_d[m]["positive"])
    neg = np.array(scores_d[m]["negative"])
    y_true  = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    # PRC
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    lw, ls  = STYLES[m]
    col     = COLORS[m]
    label_r = f"{LABELS[m]}  (AUROC={auroc:.3f})"
    label_p = f"{LABELS[m]}  (AP={ap:.3f})"

    h1, = ax_roc.plot(fpr, tpr, color=col, lw=lw, linestyle=ls, label=label_r, zorder=3)
    h2, = ax_prc.plot(rec, prec, color=col, lw=lw, linestyle=ls, label=label_p, zorder=3)
    roc_handles.append(h1)
    prc_handles.append(h2)

# diagonal reference (ROC)
ax_roc.plot([0, 1], [0, 1], color="#BBBBBB", lw=0.9, linestyle="--", zorder=1)

# prevalence baseline (PRC)
ax_prc.axhline(prevalence, color="#BBBBBB", lw=0.9, linestyle="--", zorder=1,
               label=f"Prevalence ({prevalence:.2f})")

# ── formatting ───────────────────────────────────────────────────────────────
for ax, xlabel, ylabel, title in [
    (ax_roc, "False Positive Rate", "True Positive Rate", "ROC Curve"),
    (ax_prc, "Recall",              "Precision",          "Precision–Recall Curve"),
]:
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.01, 1.01)
    ax.set_aspect("equal")
    ax.grid(True, linewidth=0.4, color="#E0E0E0", zorder=0)
    ax.tick_params(labelsize=8)

ax_roc.legend(handles=roc_handles, fontsize=7.2, loc="lower right",
              framealpha=0.85, edgecolor="#CCCCCC")
ax_prc.legend(handles=prc_handles + [ax_prc.lines[-1]],
              fontsize=7.2, loc="upper right",
              framealpha=0.85, edgecolor="#CCCCCC")

fig.suptitle("Classifier Comparison: ROC and Precision–Recall Curves",
             fontsize=10.5, fontweight="bold", y=1.01)

plt.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight", dpi=150)
fig.savefig("figure.png", bbox_inches="tight", dpi=150)
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
