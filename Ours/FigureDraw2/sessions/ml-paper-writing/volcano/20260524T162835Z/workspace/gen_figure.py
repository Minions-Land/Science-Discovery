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
thr_fc = data["thresholds"]["abs_log2fc"]   # 1.0
thr_p  = data["thresholds"]["neg_log10_p"]  # 2.0

# Classify
up   = (log2fc >  thr_fc) & (nlp > thr_p)
down = (log2fc < -thr_fc) & (nlp > thr_p)
ns   = ~(up | down)

colors = {"ns": "#AAAAAA", "up": "#D62728", "down": "#1F77B4"}
alpha  = {"ns": 0.35,      "up": 0.75,      "down": 0.75}
size   = {"ns": 6,         "up": 8,         "down": 8}

fig, ax = plt.subplots(figsize=(7, 5.5))

for mask, key in [(ns, "ns"), (down, "down"), (up, "up")]:
    ax.scatter(log2fc[mask], nlp[mask],
               c=colors[key], alpha=alpha[key], s=size[key],
               linewidths=0, rasterized=True,
               label=f"{key.capitalize()} ({mask.sum()})" if key != "ns"
                     else f"Not sig. ({mask.sum()})")

# Threshold lines
ax.axvline( thr_fc, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-thr_fc, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axhline( thr_p,  color="black", lw=0.8, ls="--", alpha=0.6)

# Annotate top-5 by neg_log10_p among significant genes
sig_idx = np.where(up | down)[0]
top5 = sig_idx[np.argsort(nlp[sig_idx])[::-1][:5]]
for i, idx in enumerate(top5):
    ax.annotate(f"Gene{idx+1}",
                xy=(log2fc[idx], nlp[idx]),
                xytext=(log2fc[idx] + (0.25 if log2fc[idx] > 0 else -0.25),
                        nlp[idx] + 0.15),
                fontsize=7, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="black"),
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])

ax.set_xlabel(r"$\log_2$ Fold Change", fontsize=12)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=12)
ax.set_title("Volcano Plot", fontsize=13, fontweight="bold")
ax.legend(framealpha=0.8, fontsize=9, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
plt.savefig("figure.pdf", dpi=300, bbox_inches="tight")
plt.savefig("figure.png", dpi=150, bbox_inches="tight")
plt.savefig("figure.svg", bbox_inches="tight")
print("Done. up:", up.sum(), "down:", down.sum(), "ns:", ns.sum())
