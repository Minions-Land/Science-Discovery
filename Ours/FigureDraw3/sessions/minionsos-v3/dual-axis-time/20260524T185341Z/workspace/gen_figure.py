"""
Dual-axis time series: training loss (log y, left) + cosine LR schedule (right).
Data source: data.json — {steps, loss, lr}
"""

import json
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── colors ────────────────────────────────────────────────────────────────────
COLOR_LOSS = "#0F4D92"   # deep blue  — left axis / training loss
COLOR_LR   = "#9A4D8E"  # plum       — right axis / LR schedule

# ── load data ─────────────────────────────────────────────────────────────────
with open("data.json") as f:
    d = json.load(f)

steps = np.array(d["steps"])
loss  = np.array(d["loss"])
lr    = np.array(d["lr"])

# ── figure ────────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(6, 4))

# — left axis: loss (log scale) ———————————————————————————————————————————————
ax1.set_yscale("log")
ax1.plot(steps, loss, color=COLOR_LOSS, linewidth=1.6, zorder=3)

ax1.set_xlabel("Training step", fontsize=9)
ax1.set_ylabel("Training loss (log scale)", color=COLOR_LOSS, fontsize=9)
ax1.tick_params(axis="y", colors=COLOR_LOSS, direction="out", length=2.2, width=0.6)
ax1.tick_params(axis="x", direction="out", length=2.2, width=0.6)
ax1.spines["left"].set_color(COLOR_LOSS)
ax1.spines["bottom"].set_color("#272727")
ax1.yaxis.set_minor_locator(ticker.NullLocator())  # suppress minor log ticks

# — right axis: LR schedule ———————————————————————————————————————————————————
ax2 = ax1.twinx()
ax2.spines["right"].set_visible(True)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["right"].set_color(COLOR_LR)
ax2.spines["right"].set_linewidth(0.8)

ax2.plot(steps, lr * 1e3, color=COLOR_LR, linewidth=1.6,
         linestyle="--", alpha=0.85, zorder=2)

ax2.set_ylabel("Learning rate ($\\times 10^{-3}$)", color=COLOR_LR, fontsize=9)
ax2.tick_params(axis="y", colors=COLOR_LR, direction="out", length=2.2, width=0.6)
ax2.set_ylim(bottom=0)

# — legend (inside axes, lower-left) ——————————————————————————————————————————
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=COLOR_LOSS, linewidth=1.6, label="Training loss"),
    Line2D([0], [0], color=COLOR_LR,   linewidth=1.6, linestyle="--",
           alpha=0.85, label="LR schedule (cosine decay)"),
]
ax1.legend(handles=legend_elements, loc="lower left", fontsize=8)

# — final-step annotation ——————————————————————————————————————————————————————
final_loss = loss[-1]
ax1.annotate(
    f"loss={final_loss:.3f}",
    xy=(steps[-1], final_loss),
    xytext=(-48, 6), textcoords="offset points",
    fontsize=7.5, color=COLOR_LOSS,
    arrowprops=dict(arrowstyle="-", color=COLOR_LOSS, lw=0.6),
)

fig.tight_layout()

# ── export ────────────────────────────────────────────────────────────────────
fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved: figure.pdf  figure.png  figure.svg")
