import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
from scipy.special import expit  # sigmoid for converting raw scores to probabilities

# ── load data ──────────────────────────────────────────────────────────────────
with open('data.json') as f:
    data = json.load(f)

methods = data['methods']

# colour palette — distinct, print-safe
COLORS = {
    'Baseline':   '#4878CF',
    'Method-A':   '#6ACC65',
    'Method-B':   '#D65F5F',
    'OursModel':  '#B47CC7',
}
LINESTYLES = {
    'Baseline':   '--',
    'Method-A':   '-.',
    'Method-B':   ':',
    'OursModel':  '-',
}
LINEWIDTHS = {
    'Baseline':   1.4,
    'Method-A':   1.4,
    'Method-B':   1.4,
    'OursModel':  2.0,
}

fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))

# compute global prevalence (equal pos/neg counts across methods assumed,
# but derive from actual data)
total_pos = sum(len(data['scores'][m]['positive']) for m in methods)
total_neg = sum(len(data['scores'][m]['negative']) for m in methods)
# per-method prevalence (same for all here; just use first)
n_pos = len(data['scores'][methods[0]]['positive'])
n_neg = len(data['scores'][methods[0]]['negative'])
prevalence = n_pos / (n_pos + n_neg)

for method in methods:
    pos_scores = np.array(data['scores'][method]['positive'])
    neg_scores = np.array(data['scores'][method]['negative'])

    scores = np.concatenate([pos_scores, neg_scores])
    labels = np.concatenate([np.ones(len(pos_scores)), np.zeros(len(neg_scores))])

    # ── ROC ──
    fpr, tpr, _ = roc_curve(labels, scores)
    auroc = auc(fpr, tpr)

    # ── PRC ──
    prec, rec, _ = precision_recall_curve(labels, scores)
    ap = average_precision_score(labels, scores)

    label_roc = f'{method} (AUC={auroc:.3f})'
    label_prc = f'{method} (AP={ap:.3f})'

    kw = dict(color=COLORS[method], ls=LINESTYLES[method], lw=LINEWIDTHS[method])
    axes[0].plot(fpr, tpr, label=label_roc, **kw)
    axes[1].plot(rec, prec, label=label_prc, **kw)

# ── ROC panel ──
axes[0].plot([0, 1], [0, 1], 'k--', lw=0.8, alpha=0.5, label='Chance')
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curve')
axes[0].set_xlim(-0.02, 1.02)
axes[0].set_ylim(-0.02, 1.02)
axes[0].legend(fontsize=6.5, loc='lower right', framealpha=0.9)
axes[0].set_aspect('equal', adjustable='box')

# ── PRC panel ──
axes[1].axhline(prevalence, color='k', ls='--', lw=0.8, alpha=0.5,
                label=f'Prevalence ({prevalence:.2f})')
axes[1].set_xlabel('Recall')
axes[1].set_ylabel('Precision')
axes[1].set_title('Precision-Recall Curve')
axes[1].set_xlim(-0.02, 1.02)
axes[1].set_ylim(-0.02, 1.02)
axes[1].legend(fontsize=6.5, loc='lower left', framealpha=0.9)
axes[1].set_aspect('equal', adjustable='box')

for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, lw=0.4, alpha=0.4)

plt.tight_layout(pad=1.2)

plt.savefig('figure.pdf', bbox_inches='tight', dpi=300)
plt.savefig('figure.png', bbox_inches='tight', dpi=200)
plt.savefig('figure.svg', bbox_inches='tight')
print("Saved figure.pdf, figure.png, figure.svg")
