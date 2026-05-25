import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

with open("data.json") as f:
    data = json.load(f)

log2fc = np.array(data["log2fc"])
nlp = np.array(data["neg_log10_p"])
fc_thresh = data["thresholds"]["abs_log2fc"]
p_thresh = data["thresholds"]["neg_log10_p"]

# Classify each gene
up   = (log2fc >= fc_thresh)  & (nlp >= p_thresh)
down = (log2fc <= -fc_thresh) & (nlp >= p_thresh)
ns   = ~up & ~down

colors = {"ns": "#b0b0b0", "down": "#4C72B0", "up": "#DD4949"}
alpha_ns = 0.35
alpha_sig = 0.7
size_ns = 6
size_sig = 8

fig, ax = plt.subplots(figsize=(7, 5.5))

ax.scatter(log2fc[ns],   nlp[ns],   c=colors["ns"],   s=size_ns,  alpha=alpha_ns, lw=0, rasterized=True, zorder=1)
ax.scatter(log2fc[down], nlp[down], c=colors["down"],  s=size_sig, alpha=alpha_sig, lw=0, rasterized=True, zorder=2, label=f"Down ({down.sum()})")
ax.scatter(log2fc[up],   nlp[up],   c=colors["up"],    s=size_sig, alpha=alpha_sig, lw=0, rasterized=True, zorder=2, label=f"Up ({up.sum()})")

# Threshold lines
ax.axhline(p_thresh,  color="#555555", lw=0.8, ls="--", zorder=3)
ax.axvline( fc_thresh, color="#555555", lw=0.8, ls="--", zorder=3)
ax.axvline(-fc_thresh, color="#555555", lw=0.8, ls="--", zorder=3)

# Annotate top-5 by neg_log10_p (among significant)
sig_mask = up | down
if sig_mask.sum() > 0:
    sig_idx = np.where(sig_mask)[0]
    top5 = sig_idx[np.argsort(nlp[sig_mask])[::-1][:5]]
    for i, idx in enumerate(top5):
        label = f"Gene{idx+1}"
        ax.annotate(
            label,
            xy=(log2fc[idx], nlp[idx]),
            xytext=(log2fc[idx] + (0.25 if log2fc[idx] > 0 else -0.25), nlp[idx] + 0.15),
            fontsize=6.5,
            ha="left" if log2fc[idx] > 0 else "right",
            arrowprops=dict(arrowstyle="-", lw=0.5, color="#444444"),
            color="#222222",
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
        )

ax.set_xlabel(r"$\log_2$ Fold Change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano Plot — Differential Gene Expression", fontsize=12, fontweight="bold")

# Legend with non-sig count
ns_patch = matplotlib.patches.Patch(color=colors["ns"], alpha=0.6, label=f"Non-sig ({ns.sum()})")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=[ns_patch] + handles, fontsize=9, framealpha=0.7, loc="upper left")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
print(f"n={len(log2fc)}  up={up.sum()}  down={down.sum()}  ns={ns.sum()}")
