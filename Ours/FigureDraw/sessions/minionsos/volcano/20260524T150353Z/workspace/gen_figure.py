import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

with open("data.json") as f:
    d = json.load(f)

log2fc = np.array(d["log2fc"])
nlp = np.array(d["neg_log10_p"])
fc_thresh = d["thresholds"]["abs_log2fc"]
p_thresh = d["thresholds"]["neg_log10_p"]

up   = (log2fc >  fc_thresh) & (nlp > p_thresh)
down = (log2fc < -fc_thresh) & (nlp > p_thresh)
ns   = ~up & ~down

colors = {"ns": "#AAAAAA", "up": "#D62728", "down": "#1F77B4"}

fig, ax = plt.subplots(figsize=(7, 5.5))

ax.scatter(log2fc[ns],   nlp[ns],   s=6, c=colors["ns"],   alpha=0.45, linewidths=0, rasterized=True, label=f"Non-sig (n={ns.sum()})")
ax.scatter(log2fc[down], nlp[down], s=8, c=colors["down"], alpha=0.75, linewidths=0, rasterized=True, label=f"Down (n={down.sum()})")
ax.scatter(log2fc[up],   nlp[up],   s=8, c=colors["up"],   alpha=0.75, linewidths=0, rasterized=True, label=f"Up (n={up.sum()})")

ax.axvline( fc_thresh, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thresh, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axhline(p_thresh,   color="black", lw=0.8, ls="--", alpha=0.6)

# Annotate top-5 by neg_log10_p (any category)
sig_mask = up | down
if sig_mask.sum() > 0:
    sig_idx = np.where(sig_mask)[0]
    top5 = sig_idx[np.argsort(nlp[sig_idx])[::-1][:5]]
    for i, idx in enumerate(top5):
        label = f"Gene{idx+1}"
        ax.annotate(
            label,
            xy=(log2fc[idx], nlp[idx]),
            xytext=(5, 3),
            textcoords="offset points",
            fontsize=6.5,
            color="black",
            path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
        )

ax.set_xlabel(r"$\log_2$ Fold Change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano Plot", fontsize=13, fontweight="bold")
ax.legend(loc="upper right", fontsize=8, framealpha=0.8, markerscale=1.5)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"Up: {up.sum()}, Down: {down.sum()}, Non-sig: {ns.sum()}")
