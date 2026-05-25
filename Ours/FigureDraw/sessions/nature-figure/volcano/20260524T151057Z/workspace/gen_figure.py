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
thr_fc = d["thresholds"]["abs_log2fc"]
thr_p = d["thresholds"]["neg_log10_p"]

# Classify
up   = (log2fc >  thr_fc) & (nlp > thr_p)
down = (log2fc < -thr_fc) & (nlp > thr_p)
ns   = ~(up | down)

n_up   = up.sum()
n_down = down.sum()
n_ns   = ns.sum()

# Colors
C_UP   = "#d62728"
C_DOWN = "#1f77b4"
C_NS   = "#aaaaaa"

fig, ax = plt.subplots(figsize=(5.5, 5))

ax.scatter(log2fc[ns],   nlp[ns],   s=6,  c=C_NS,   alpha=0.5, linewidths=0, rasterized=True, label=f"NS ({n_ns})")
ax.scatter(log2fc[down], nlp[down], s=8,  c=C_DOWN, alpha=0.75, linewidths=0, rasterized=True, label=f"Down ({n_down})")
ax.scatter(log2fc[up],   nlp[up],   s=8,  c=C_UP,   alpha=0.75, linewidths=0, rasterized=True, label=f"Up ({n_up})")

# Threshold lines
ax.axvline( thr_fc, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-thr_fc, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axhline( thr_p,  color="black", lw=0.8, ls="--", alpha=0.6)

# Annotate top-5 by neg_log10_p
top5_idx = np.argsort(nlp)[-5:][::-1]
for i in top5_idx:
    label = f"g{i}"
    ax.annotate(
        label,
        xy=(log2fc[i], nlp[i]),
        xytext=(4, 4),
        textcoords="offset points",
        fontsize=6.5,
        color="black",
        path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
    )

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano plot", fontsize=12, fontweight="bold")

legend = ax.legend(frameon=True, fontsize=8, loc="upper left",
                   markerscale=1.4, handletextpad=0.4)
legend.get_frame().set_linewidth(0.5)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Done.")
