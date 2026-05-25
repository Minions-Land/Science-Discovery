import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Load data
with open("data.json") as f:
    data = json.load(f)

log2fc = np.array(data["log2fc"])
nlp    = np.array(data["neg_log10_p"])
fc_thr = data["thresholds"]["abs_log2fc"]
p_thr  = data["thresholds"]["neg_log10_p"]

# Classify
up   = (log2fc >=  fc_thr) & (nlp >= p_thr)
down = (log2fc <= -fc_thr) & (nlp >= p_thr)
ns   = ~up & ~down

# Colors
C_UP   = "#d62728"   # red
C_DOWN = "#1f77b4"   # blue
C_NS   = "#aaaaaa"   # grey

fig, ax = plt.subplots(figsize=(6, 5))

ax.scatter(log2fc[ns],   nlp[ns],   s=4,  c=C_NS,   alpha=0.5, linewidths=0, rasterized=True, label=f"NS ({ns.sum():,})")
ax.scatter(log2fc[down], nlp[down], s=6,  c=C_DOWN, alpha=0.75, linewidths=0, rasterized=True, label=f"Down ({down.sum():,})")
ax.scatter(log2fc[up],   nlp[up],   s=6,  c=C_UP,   alpha=0.75, linewidths=0, rasterized=True, label=f"Up ({up.sum():,})")

# Threshold lines
ax.axvline( fc_thr, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thr, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axhline( p_thr,  color="black", lw=0.8, ls="--", alpha=0.6)

# Annotate top-5 by neg_log10_p
top5_idx = np.argsort(nlp)[-5:][::-1]
for i in top5_idx:
    label = f"G{i}"
    ax.annotate(
        label,
        xy=(log2fc[i], nlp[i]),
        xytext=(4, 4),
        textcoords="offset points",
        fontsize=6,
        color="black",
        path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
    )

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano plot", fontsize=12)
ax.legend(markerscale=2, fontsize=8, framealpha=0.8, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
