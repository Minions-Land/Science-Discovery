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
thr_fc = d["thresholds"]["abs_log2fc"]
thr_p = d["thresholds"]["neg_log10_p"]

up   = (log2fc >= thr_fc)  & (neg_log10_p >= thr_p)
down = (log2fc <= -thr_fc) & (neg_log10_p >= thr_p)
ns   = ~up & ~down

n_up   = up.sum()
n_down = down.sum()
n_ns   = ns.sum()

fig, ax = plt.subplots(figsize=(6.5, 5.5))

ax.scatter(log2fc[ns],   neg_log10_p[ns],   c="#AAAAAA", s=5, alpha=0.5, linewidths=0, rasterized=True, label=f"NS ({n_ns})")
ax.scatter(log2fc[down], neg_log10_p[down], c="#3182BD", s=8, alpha=0.75, linewidths=0, rasterized=True, label=f"Down ({n_down})")
ax.scatter(log2fc[up],   neg_log10_p[up],   c="#E6550D", s=8, alpha=0.75, linewidths=0, rasterized=True, label=f"Up ({n_up})")

# threshold lines
ax.axvline(-thr_fc, color="#3182BD", lw=0.8, ls="--", alpha=0.7)
ax.axvline( thr_fc, color="#E6550D", lw=0.8, ls="--", alpha=0.7)
ax.axhline( thr_p,  color="#636363", lw=0.8, ls="--", alpha=0.7)

# annotate top-5 by neg_log10_p among significant genes
sig_mask = up | down
sig_idx = np.where(sig_mask)[0]
top5_idx = sig_idx[np.argsort(neg_log10_p[sig_mask])[-5:]]

for i in top5_idx:
    label = f"g{i}"
    x, y = log2fc[i], neg_log10_p[i]
    dx = 0.15 if x > 0 else -0.15
    txt = ax.text(x + dx, y + 0.08, label, fontsize=6.5, ha="left" if x > 0 else "right",
                  color="#222222", zorder=5)
    txt.set_path_effects([pe.withStroke(linewidth=2, foreground="white")])

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}$ $p$-value", fontsize=11)
ax.set_title("Volcano plot  ·  3,000 genes", fontsize=12, fontweight="bold")

legend = ax.legend(title="", frameon=True, fontsize=9, markerscale=1.6,
                   loc="upper left", framealpha=0.85, edgecolor="#CCCCCC")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Saved: up={n_up}, down={n_down}, ns={n_ns}")
