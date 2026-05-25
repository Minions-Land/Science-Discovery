import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
try:
    from adjustText import adjust_text
    HAS_ADJUSTTEXT = True
except ImportError:
    HAS_ADJUSTTEXT = False

# ── load data ─────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

log2fc = np.array(d["log2fc"])
nlp    = np.array(d["neg_log10_p"])
thr_fc = d["thresholds"]["abs_log2fc"]
thr_p  = d["thresholds"]["neg_log10_p"]

# ── classify ──────────────────────────────────────────────────────────────────
sig   = nlp > thr_p
up    = sig & (log2fc >  thr_fc)
down  = sig & (log2fc < -thr_fc)
ns    = ~(up | down)

n_up   = up.sum()
n_down = down.sum()
n_ns   = ns.sum()

# ── colour palette (publication-friendly) ─────────────────────────────────────
C_UP   = "#D62728"   # red
C_DOWN = "#1F77B4"   # blue
C_NS   = "#AAAAAA"   # grey

# ── figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 5.5))

ax.scatter(log2fc[ns],   nlp[ns],   s=4,  c=C_NS,   alpha=0.5, linewidths=0, rasterized=True)
ax.scatter(log2fc[down], nlp[down], s=8,  c=C_DOWN, alpha=0.8, linewidths=0, rasterized=True)
ax.scatter(log2fc[up],   nlp[up],   s=8,  c=C_UP,   alpha=0.8, linewidths=0, rasterized=True)

# threshold lines
ax.axvline( thr_fc, color="#555555", lw=0.8, ls="--", alpha=0.7)
ax.axvline(-thr_fc, color="#555555", lw=0.8, ls="--", alpha=0.7)
ax.axhline( thr_p,  color="#555555", lw=0.8, ls="--", alpha=0.7)

# ── annotate top-5 by neg_log10_p (from sig genes only) ──────────────────────
sig_idx = np.where(up | down)[0]
if len(sig_idx) >= 5:
    top5 = sig_idx[np.argsort(nlp[sig_idx])[-5:]]
else:
    top5 = sig_idx

texts = []
for i in top5:
    col = C_UP if log2fc[i] > 0 else C_DOWN
    t = ax.text(log2fc[i], nlp[i], f"gene{i+1}",
                fontsize=6.5, color=col, fontweight="bold", ha="center")
    texts.append(t)

if HAS_ADJUSTTEXT:
    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color="#444444", lw=0.5),
                expand_text=(1.2, 1.4))

# ── legend ────────────────────────────────────────────────────────────────────
patches = [
    mpatches.Patch(color=C_DOWN, label=f"Down ({n_down})"),
    mpatches.Patch(color=C_NS,   label=f"NS ({n_ns})"),
    mpatches.Patch(color=C_UP,   label=f"Up ({n_up})"),
]
ax.legend(handles=patches, loc="upper right", fontsize=8, framealpha=0.85,
          edgecolor="#CCCCCC", handlelength=1.2)

# ── labels / style ────────────────────────────────────────────────────────────
ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$",      fontsize=11)
ax.set_title("Volcano Plot", fontsize=12, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=9)

plt.tight_layout()

# ── save ──────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"Saved: figure.pdf, figure.png, figure.svg")
print(f"Up: {n_up}  Down: {n_down}  NS: {n_ns}")
