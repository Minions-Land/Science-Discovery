import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from scipy.special import expit  # sigmoid for score -> prob conversion

# ── data ──────────────────────────────────────────────────────────────────────
with open("data.json") as f:
    data = json.load(f)

methods = data["methods"]

# palette: colourblind-friendly (Wong 2011)
COLORS = {
    "Baseline":  "#E69F00",
    "Method-A":  "#56B4E9",
    "Method-B":  "#009E73",
    "OursModel": "#CC79A7",
}
LINESTYLES = {
    "Baseline":  (0, (4, 2)),       # dashed
    "Method-A":  (0, (2, 1, 2, 1)), # dash-dot
    "Method-B":  (0, (1, 1)),       # dotted
    "OursModel": "-",               # solid
}
LW = 1.6

# ── compute curves ─────────────────────────────────────────────────────────────
roc_data, prc_data = {}, {}
total_pos, total_neg = 0, 0

for m in methods:
    pos = np.array(data["scores"][m]["positive"])
    neg = np.array(data["scores"][m]["negative"])
    y_true = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
    y_score = np.concatenate([pos, neg])

    fpr, tpr, _ = roc_curve(y_true, y_score)
    auroc = auc(fpr, tpr)

    prec, rec, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    roc_data[m] = (fpr, tpr, auroc)
    prc_data[m] = (rec, prec, ap)

    total_pos += len(pos)
    total_neg += len(neg)

prevalence = total_pos / (total_pos + total_neg) / len(methods)

# ── figure ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3), constrained_layout=True)

for ax in axes:
    ax.tick_params(direction="in", which="both", top=True, right=True, labelsize=8)
    for spine in ax.spines.values():
        spine.set_linewidth(0.7)
    ax.grid(True, linewidth=0.35, alpha=0.5, color="#cccccc")

# ── left: ROC ─────────────────────────────────────────────────────────────────
ax = axes[0]
ax.plot([0, 1], [0, 1], color="#aaaaaa", lw=0.8, ls="--", zorder=1)

for m in methods:
    fpr, tpr, auroc = roc_data[m]
    label = f"{m}  (AUROC = {auroc:.3f})"
    ax.plot(fpr, tpr, color=COLORS[m], ls=LINESTYLES[m], lw=LW, label=label, zorder=2)

ax.set_xlabel("False positive rate", fontsize=9)
ax.set_ylabel("True positive rate", fontsize=9)
ax.set_title("ROC curve", fontsize=9, fontweight="bold")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.25))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
ax.legend(fontsize=6.5, loc="lower right", framealpha=0.85, edgecolor="#bbbbbb",
          handlelength=2.0, borderpad=0.6)

# ── right: PRC ────────────────────────────────────────────────────────────────
ax = axes[1]
prev_line = total_pos / (total_pos + total_neg) / len(methods) * len(methods)
# use per-method average prevalence for the baseline
all_prev = [
    len(data["scores"][m]["positive"]) /
    (len(data["scores"][m]["positive"]) + len(data["scores"][m]["negative"]))
    for m in methods
]
mean_prev = np.mean(all_prev)
ax.axhline(mean_prev, color="#aaaaaa", lw=0.8, ls="--", zorder=1,
           label=f"Chance  (prev = {mean_prev:.2f})")

for m in methods:
    rec, prec, ap = prc_data[m]
    label = f"{m}  (AP = {ap:.3f})"
    ax.plot(rec, prec, color=COLORS[m], ls=LINESTYLES[m], lw=LW, label=label, zorder=2)

ax.set_xlabel("Recall", fontsize=9)
ax.set_ylabel("Precision", fontsize=9)
ax.set_title("Precision–Recall curve", fontsize=9, fontweight="bold")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.25))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
ax.legend(fontsize=6.5, loc="upper right", framealpha=0.85, edgecolor="#bbbbbb",
          handlelength=2.0, borderpad=0.6)

# ── save ───────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
