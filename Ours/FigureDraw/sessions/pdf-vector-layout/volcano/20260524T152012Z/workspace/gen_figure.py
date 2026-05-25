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
nlp = np.array(d["neg_log10_p"])
fc_thresh = d["thresholds"]["abs_log2fc"]   # 1.0
p_thresh = d["thresholds"]["neg_log10_p"]   # 2.0

# Classify
up   = (log2fc >=  fc_thresh) & (nlp >= p_thresh)
down = (log2fc <= -fc_thresh) & (nlp >= p_thresh)
ns   = ~up & ~down

# Colors
C_UP   = "#d62728"   # red
C_DOWN = "#1f77b4"   # blue
C_NS   = "#aaaaaa"   # grey

fig, ax = plt.subplots(figsize=(6, 5))

ax.scatter(log2fc[ns],   nlp[ns],   s=4,  c=C_NS,   alpha=0.5, linewidths=0, rasterized=True, label=f"NS (n={ns.sum()})")
ax.scatter(log2fc[down], nlp[down], s=6,  c=C_DOWN, alpha=0.8, linewidths=0, rasterized=True, label=f"Down (n={down.sum()})")
ax.scatter(log2fc[up],   nlp[up],   s=6,  c=C_UP,   alpha=0.8, linewidths=0, rasterized=True, label=f"Up (n={up.sum()})")

# Threshold lines
ax.axvline( fc_thresh, color="black", lw=0.7, ls="--", alpha=0.6)
ax.axvline(-fc_thresh, color="black", lw=0.7, ls="--", alpha=0.6)
ax.axhline( p_thresh,  color="black", lw=0.7, ls="--", alpha=0.6)

# Annotate top-5 by neg_log10_p
top5_idx = np.argsort(nlp)[-5:][::-1]
for i in top5_idx:
    label = f"G{i}"
    ax.annotate(
        label,
        xy=(log2fc[i], nlp[i]),
        xytext=(4, 3),
        textcoords="offset points",
        fontsize=6,
        color="black",
        path_effects=[pe.withStroke(linewidth=1.5, foreground="white")],
    )

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Volcano plot", fontsize=12)
ax.legend(fontsize=8, markerscale=2, framealpha=0.7)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("figure.pdf", dpi=150)
plt.savefig("figure.png", dpi=150)
plt.savefig("figure.svg")
plt.close()
print("Done.")
