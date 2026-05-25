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
fc_thr = d["thresholds"]["abs_log2fc"]
p_thr = d["thresholds"]["neg_log10_p"]

# classify
up   = (log2fc >  fc_thr) & (nlp > p_thr)
down = (log2fc < -fc_thr) & (nlp > p_thr)
ns   = ~(up | down)

fig, ax = plt.subplots(figsize=(7, 5.5))

ax.scatter(log2fc[ns],   nlp[ns],   c="#b0b0b0", s=8,  alpha=0.5, linewidths=0, label=f"NS ({ns.sum()})", rasterized=True)
ax.scatter(log2fc[down], nlp[down], c="#3a86ff", s=12, alpha=0.75, linewidths=0, label=f"Down ({down.sum()})", rasterized=True)
ax.scatter(log2fc[up],   nlp[up],   c="#e63946", s=12, alpha=0.75, linewidths=0, label=f"Up ({up.sum()})", rasterized=True)

# threshold lines
ax.axhline(p_thr,   color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline( fc_thr, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thr, color="black", lw=0.8, ls="--", alpha=0.6)

# annotate top-5 by neg_log10_p
sig = up | down
if sig.any():
    top5_idx = np.argsort(nlp)[-5:][::-1]
    for i in top5_idx:
        ax.annotate(
            f"gene{i}",
            xy=(log2fc[i], nlp[i]),
            xytext=(4, 4), textcoords="offset points",
            fontsize=6.5,
            ha="left",
            path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
        )

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano Plot", fontsize=13, fontweight="bold")
ax.legend(framealpha=0.85, fontsize=9, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done.")
