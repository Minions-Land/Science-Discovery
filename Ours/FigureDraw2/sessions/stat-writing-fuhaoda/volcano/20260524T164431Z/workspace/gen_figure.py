import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

with open("data.json") as f:
    d = json.load(f)

log2fc = np.array(d["log2fc"])
neg_log10_p = np.array(d["neg_log10_p"])
fc_thresh = d["thresholds"]["abs_log2fc"]
p_thresh = d["thresholds"]["neg_log10_p"]

up   = (log2fc >  fc_thresh) & (neg_log10_p > p_thresh)
down = (log2fc < -fc_thresh) & (neg_log10_p > p_thresh)
ns   = ~up & ~down

colors = {"ns": "#AAAAAA", "up": "#D62728", "down": "#1F77B4"}

fig, ax = plt.subplots(figsize=(7, 5.5))

ax.scatter(log2fc[ns],   neg_log10_p[ns],   s=6, color=colors["ns"],   alpha=0.5, linewidths=0, label=f"Non-sig (n={ns.sum()})")
ax.scatter(log2fc[down], neg_log10_p[down], s=8, color=colors["down"], alpha=0.75, linewidths=0, label=f"Down (n={down.sum()})")
ax.scatter(log2fc[up],   neg_log10_p[up],   s=8, color=colors["up"],   alpha=0.75, linewidths=0, label=f"Up (n={up.sum()})")

# Threshold lines
ax.axvline( fc_thresh, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thresh, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axhline(p_thresh,   color="black", lw=0.8, ls="--", alpha=0.6)

# Annotate top-5 genes by neg_log10_p
sig = up | down
if sig.sum() > 0:
    sig_idx = np.where(sig)[0]
    top5 = sig_idx[np.argsort(neg_log10_p[sig_idx])[-5:]]
    for i in top5:
        ax.annotate(
            f"gene{i}",
            xy=(log2fc[i], neg_log10_p[i]),
            xytext=(4, 4), textcoords="offset points",
            fontsize=6.5,
            path_effects=[pe.withStroke(linewidth=2, foreground="white")],
        )

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano Plot", fontsize=13, fontweight="bold")
ax.legend(loc="upper right", fontsize=8, framealpha=0.8, markerscale=1.5)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
