"""Volcano plot — data.json (3000 genes), thresholds from data."""
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "font.size": 9,
})

PALETTE = {
    "up":      "#C0392B",   # red — upregulated
    "down":    "#2471A3",   # blue — downregulated
    "ns":      "#AAAAAA",   # grey — non-significant
    "thresh":  "#555555",   # dashed threshold lines
    "annot":   "#1A1A1A",   # annotation text
}

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

x = np.array(d["log2fc"])
y = np.array(d["neg_log10_p"])
fc_thresh  = d["thresholds"]["abs_log2fc"]      # 1.0
p_thresh   = d["thresholds"]["neg_log10_p"]     # 2.0

# ── classify ───────────────────────────────────────────────────────────────
sig = y >= p_thresh
up   = sig & (x >  fc_thresh)
down = sig & (x < -fc_thresh)
ns   = ~(up | down)

# ── top-5 by neg_log10_p (among significant) ───────────────────────────────
sig_idx = np.where(sig)[0]
top5_idx = sig_idx[np.argsort(y[sig_idx])[::-1][:5]]

# ── figure ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))

# scatter layers: ns first, then coloured on top
ax.scatter(x[ns],   y[ns],   s=5,  c=PALETTE["ns"],   alpha=0.45, linewidths=0, rasterized=True, zorder=1)
ax.scatter(x[down], y[down], s=7,  c=PALETTE["down"],  alpha=0.75, linewidths=0, rasterized=True, zorder=2)
ax.scatter(x[up],   y[up],   s=7,  c=PALETTE["up"],    alpha=0.75, linewidths=0, rasterized=True, zorder=2)

# threshold lines
ax.axhline(p_thresh,  color=PALETTE["thresh"], lw=0.8, ls="--", zorder=0)
ax.axvline( fc_thresh, color=PALETTE["thresh"], lw=0.8, ls="--", zorder=0)
ax.axvline(-fc_thresh, color=PALETTE["thresh"], lw=0.8, ls="--", zorder=0)

# annotate top-5
for i in top5_idx:
    label = f"G{i}"
    ax.annotate(
        label,
        xy=(x[i], y[i]),
        xytext=(4, 3),
        textcoords="offset points",
        fontsize=7,
        color=PALETTE["annot"],
        path_effects=[pe.withStroke(linewidth=1.8, foreground="white")],
        zorder=5,
    )

# counts in corners
n_up   = int(up.sum())
n_down = int(down.sum())
ax.text(0.98, 0.97, f"Up: {n_up}",   transform=ax.transAxes,
        ha="right", va="top", fontsize=8, color=PALETTE["up"])
ax.text(0.02, 0.97, f"Down: {n_down}", transform=ax.transAxes,
        ha="left",  va="top", fontsize=8, color=PALETTE["down"])

# axes
ax.set_xlabel("log$_2$ fold change", fontsize=9)
ax.set_ylabel("$-$log$_{10}$(p)", fontsize=9)
ax.tick_params(direction="out", length=2.5, width=0.6, labelsize=8)

# legend
from matplotlib.lines import Line2D
handles = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["up"],   markersize=6, label=f"Up (FC>{fc_thresh}, p<{10**-p_thresh:.3f})"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["down"], markersize=6, label=f"Down (FC<-{fc_thresh}, p<{10**-p_thresh:.3f})"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=PALETTE["ns"],   markersize=6, label="Non-significant"),
]
ax.legend(handles=handles, fontsize=7.5, loc="upper center",
          bbox_to_anchor=(0.5, -0.13), ncol=3, handletextpad=0.3, columnspacing=0.8)

fig.tight_layout(rect=[0, 0.05, 1, 1])

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print(f"Saved figure.pdf / figure.png / figure.svg  |  up={n_up}  down={n_down}  ns={int(ns.sum())}")
