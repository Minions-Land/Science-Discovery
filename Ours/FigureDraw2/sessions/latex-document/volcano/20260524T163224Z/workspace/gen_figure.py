import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False

# Load data
with open("data.json") as f:
    data = json.load(f)

log2fc = np.array(data["log2fc"])
neg_log10_p = np.array(data["neg_log10_p"])
fc_thresh = data["thresholds"]["abs_log2fc"]
p_thresh = data["thresholds"]["neg_log10_p"]

# Classify genes
up   = (log2fc >  fc_thresh) & (neg_log10_p > p_thresh)
down = (log2fc < -fc_thresh) & (neg_log10_p > p_thresh)
ns   = ~up & ~down

colors = np.where(up, "#E64B35", np.where(down, "#4DBBD5", "#AAAAAA"))

# Figure
fig, ax = plt.subplots(figsize=(7, 5.5))

# Plot non-sig first (bottom layer)
ax.scatter(log2fc[ns], neg_log10_p[ns], c="#CCCCCC", s=8, alpha=0.5,
           linewidths=0, rasterized=True)
ax.scatter(log2fc[down], neg_log10_p[down], c="#4DBBD5", s=10, alpha=0.75,
           linewidths=0, rasterized=True)
ax.scatter(log2fc[up], neg_log10_p[up], c="#E64B35", s=10, alpha=0.75,
           linewidths=0, rasterized=True)

# Threshold lines
ax.axhline(p_thresh,  color="black", linewidth=0.8, linestyle="--", alpha=0.6)
ax.axvline( fc_thresh, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
ax.axvline(-fc_thresh, color="black", linewidth=0.8, linestyle="--", alpha=0.6)

# Annotate top-5 by neg_log10_p
sig_idx = np.where(up | down)[0]
if len(sig_idx) > 0:
    top5_idx = sig_idx[np.argsort(neg_log10_p[sig_idx])[-5:]]
    texts = []
    for i in top5_idx:
        label = f"Gene{i+1}"
        txt = ax.text(log2fc[i], neg_log10_p[i], label,
                      fontsize=6.5, ha="center", va="bottom")
        texts.append(txt)
    if HAS_ADJUST_TEXT:
        try:
            adjust_text(texts, ax=ax,
                        arrowprops=dict(arrowstyle="-", color="grey", lw=0.5),
                        expand_points=(1.3, 1.5))
        except Exception:
            pass

# Labels and legend
ax.set_xlabel(r"$\log_2$ Fold Change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}$ $p$-value", fontsize=11)
ax.set_title("Differential Expression Volcano Plot", fontsize=12, fontweight="bold")

n_up   = int(up.sum())
n_down = int(down.sum())
n_ns   = int(ns.sum())

patches = [
    mpatches.Patch(color="#E64B35", label=f"Up-regulated ({n_up})"),
    mpatches.Patch(color="#4DBBD5", label=f"Down-regulated ({n_down})"),
    mpatches.Patch(color="#CCCCCC", label=f"Not significant ({n_ns})"),
]
ax.legend(handles=patches, fontsize=8, framealpha=0.9, loc="upper left")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout(pad=1.5)

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Saved. Up={n_up}, Down={n_down}, NS={n_ns}")
