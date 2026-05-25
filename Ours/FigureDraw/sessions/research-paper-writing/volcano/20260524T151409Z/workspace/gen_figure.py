import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
try:
    from adjustText import adjust_text
    HAS_ADJUSTTEXT = True
except ImportError:
    HAS_ADJUSTTEXT = False

# ── load data ──────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

log2fc = np.array(d["log2fc"])
nlp    = np.array(d["neg_log10_p"])
fc_thr = d["thresholds"]["abs_log2fc"]   # 1.0
p_thr  = d["thresholds"]["neg_log10_p"]  # 2.0
n      = d["n"]  # 3000

# ── classify ───────────────────────────────────────────────────────────────
sig_up   = (log2fc  >  fc_thr) & (nlp > p_thr)
sig_down = (log2fc  < -fc_thr) & (nlp > p_thr)
nonsig   = ~(sig_up | sig_down)

colors = np.where(sig_up, "#d62728",
         np.where(sig_down, "#1f77b4", "#aaaaaa"))

# ── top-5 by neg_log10_p (among significant only) ─────────────────────────
sig_mask = sig_up | sig_down
sig_idx  = np.where(sig_mask)[0]
top5_idx = sig_idx[np.argsort(nlp[sig_idx])[-5:]]

# ── figure ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5.5))

# non-sig first (background)
ax.scatter(log2fc[nonsig],   nlp[nonsig],   c="#aaaaaa", s=6,  alpha=0.4,
           linewidths=0, rasterized=True, label="Non-significant")
ax.scatter(log2fc[sig_down], nlp[sig_down], c="#1f77b4", s=8,  alpha=0.75,
           linewidths=0, rasterized=True, label=f"Down  (n={sig_down.sum()})")
ax.scatter(log2fc[sig_up],   nlp[sig_up],   c="#d62728", s=8,  alpha=0.75,
           linewidths=0, rasterized=True, label=f"Up  (n={sig_up.sum()})")

# threshold lines
ax.axhline(p_thr,   color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline( fc_thr, color="black", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thr, color="black", lw=0.8, ls="--", alpha=0.6)

# annotate top-5
texts = []
for i in top5_idx:
    label = f"Gene{i+1}"
    t = ax.text(log2fc[i], nlp[i], label, fontsize=7, fontweight="bold",
                color="black")
    t.set_path_effects([pe.withStroke(linewidth=2, foreground="white")])
    texts.append(t)

if HAS_ADJUSTTEXT:
    try:
        adjust_text(texts, ax=ax,
                    arrowprops=dict(arrowstyle="-", color="black", lw=0.6))
    except Exception:
        pass

# axes / labels
ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Differential Expression Volcano Plot", fontsize=12, pad=8)
ax.legend(loc="upper left", fontsize=8, framealpha=0.8, markerscale=1.5)

# threshold annotations
ax.text(ax.get_xlim()[1] if ax.get_xlim()[1] > 0 else 5,
        p_thr + 0.05, f"p-thr ({p_thr})", va="bottom", ha="right",
        fontsize=7, color="black", alpha=0.7)

ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

# ── save ───────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
print(f"Up: {sig_up.sum()}  Down: {sig_down.sum()}  Non-sig: {nonsig.sum()}")
