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

log2fc   = np.array(d["log2fc"])
nlp      = np.array(d["neg_log10_p"])
fc_thr   = d["thresholds"]["abs_log2fc"]   # 1.0
p_thr    = d["thresholds"]["neg_log10_p"]  # 2.0

# ── classify ───────────────────────────────────────────────────────────────
up   = (log2fc >  fc_thr) & (nlp > p_thr)
down = (log2fc < -fc_thr) & (nlp > p_thr)
ns   = ~up & ~down

# ── top-5 by neg_log10_p ───────────────────────────────────────────────────
top5_idx = np.argsort(nlp)[-5:][::-1]

# ── figure ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 5))

ALPHA = 0.45
S     = 8

ax.scatter(log2fc[ns],   nlp[ns],   s=S, c="#aaaaaa", alpha=ALPHA, linewidths=0, rasterized=True, label=f"Non-sig (n={ns.sum()})")
ax.scatter(log2fc[down], nlp[down], s=S, c="#4477AA", alpha=0.7,   linewidths=0, rasterized=True, label=f"Down (n={down.sum()})")
ax.scatter(log2fc[up],   nlp[up],   s=S, c="#CC3311", alpha=0.7,   linewidths=0, rasterized=True, label=f"Up (n={up.sum()})")

# threshold lines
ax.axvline( fc_thr, color="#555555", lw=0.8, ls="--", alpha=0.6)
ax.axvline(-fc_thr, color="#555555", lw=0.8, ls="--", alpha=0.6)
ax.axhline( p_thr,  color="#555555", lw=0.8, ls="--", alpha=0.6)

# annotate top-5
texts = []
for i in top5_idx:
    label = f"G{i+1}"
    t = ax.text(
        log2fc[i], nlp[i], label,
        fontsize=6.5, fontweight="bold",
        color="black",
        path_effects=[pe.withStroke(linewidth=1.8, foreground="white")],
    )
    texts.append(t)

if HAS_ADJUSTTEXT:
    try:
        adjust_text(texts, ax=ax,
                    arrowprops=dict(arrowstyle="-", color="black", lw=0.6),
                    expand_points=(1.4, 1.4))
    except Exception:
        pass

ax.set_xlabel(r"$\log_2$ fold change", fontsize=11)
ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=11)
ax.set_title("Differential Expression Volcano Plot", fontsize=12, pad=8)

leg = ax.legend(fontsize=8, framealpha=0.85, loc="upper left",
                markerscale=1.6, handletextpad=0.4)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

fig.savefig("figure.pdf", dpi=300, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print(f"Up: {up.sum()}  Down: {down.sum()}  Non-sig: {ns.sum()}")
print("Saved figure.pdf, figure.png, figure.svg")
