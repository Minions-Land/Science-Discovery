import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Load data
with open("data.json") as f:
    d = json.load(f)

log2fc = np.array(d["log2fc"])
neg_log10_p = np.array(d["neg_log10_p"])
fc_thresh = d["thresholds"]["abs_log2fc"]
p_thresh = d["thresholds"]["neg_log10_p"]

# Classify genes
up   = (log2fc >= fc_thresh)  & (neg_log10_p >= p_thresh)
down = (log2fc <= -fc_thresh) & (neg_log10_p >= p_thresh)
ns   = ~(up | down)

colors = {"ns": "#AAAAAA", "up": "#D62728", "down": "#1F77B4"}
sizes  = {"ns": 6, "up": 8, "down": 8}
alpha  = {"ns": 0.35, "up": 0.75, "down": 0.75}

fig, ax = plt.subplots(figsize=(6, 5))

ax.scatter(log2fc[ns],   neg_log10_p[ns],   c=colors["ns"],   s=sizes["ns"],
           alpha=alpha["ns"],   linewidths=0, rasterized=True, label=f"Non-sig (n={ns.sum()})")
ax.scatter(log2fc[down], neg_log10_p[down], c=colors["down"], s=sizes["down"],
           alpha=alpha["down"], linewidths=0, rasterized=True, label=f"Down (n={down.sum()})")
ax.scatter(log2fc[up],   neg_log10_p[up],   c=colors["up"],   s=sizes["up"],
           alpha=alpha["up"],   linewidths=0, rasterized=True, label=f"Up (n={up.sum()})")

# Threshold lines
ax.axvline( fc_thresh, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thresh, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axhline( p_thresh,  color="black", lw=0.8, ls="--", alpha=0.6)

# Annotate top-5 by neg_log10_p (among sig genes)
sig_mask = up | down
if sig_mask.sum() > 0:
    sig_idx = np.where(sig_mask)[0]
    top5 = sig_idx[np.argsort(neg_log10_p[sig_idx])[-5:]]
    for i, idx in enumerate(top5):
        ax.annotate(
            f"gene{idx}",
            xy=(log2fc[idx], neg_log10_p[idx]),
            xytext=(4, 2), textcoords="offset points",
            fontsize=6.5, color="black",
            path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
        )

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano Plot", fontsize=12, fontweight="bold")
ax.legend(fontsize=8, framealpha=0.8, markerscale=1.4)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
print(f"Up: {up.sum()}, Down: {down.sum()}, Non-sig: {ns.sum()}")
