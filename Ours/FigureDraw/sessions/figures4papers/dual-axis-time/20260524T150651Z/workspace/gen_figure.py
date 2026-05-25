import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from pathlib import Path

# ── Palette (from skill api.md) ──────────────────────────────────────────────
LOSS_COLOR = "#0F4D92"   # blue_main  — training loss
LR_COLOR   = "#B64342"   # red_strong — learning rate

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
    "font.size": 14,
    "axes.linewidth": 2.0,
    "axes.spines.top": False,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
    "xtick.minor.width": 1.0,
    "ytick.minor.width": 1.0,
    "lines.linewidth": 2.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.dpi": 300,
})

# ── Data ─────────────────────────────────────────────────────────────────────
cwd = Path(__file__).parent
with open(cwd / "data.json") as f:
    d = json.load(f)

steps = np.array(d["steps"])
loss  = np.array(d["loss"])
lr    = np.array(d["lr"])

# ── Figure ───────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(7, 4))

# Left axis — training loss (log scale)
ax1.semilogy(steps, loss, color=LOSS_COLOR, linewidth=2.2, zorder=3, label="Training loss")
ax1.set_xlabel("Training step", fontsize=14)
ax1.set_ylabel("Training loss (log scale)", color=LOSS_COLOR, fontsize=14)
ax1.tick_params(axis="y", colors=LOSS_COLOR, which="both")
ax1.spines["left"].set_color(LOSS_COLOR)
ax1.spines["right"].set_visible(False)   # will be set by ax2 below
ax1.yaxis.set_minor_locator(ticker.LogLocator(subs="all", numticks=10))
ax1.yaxis.set_minor_formatter(ticker.NullFormatter())
ax1.set_xlim(steps[0], steps[-1])

# Right axis — learning rate (linear)
ax2 = ax1.twinx()
ax2.plot(steps, lr * 1e3, color=LR_COLOR, linewidth=2.0,
         linestyle="--", zorder=2, label="Learning rate")
ax2.set_ylabel("Learning rate (×10⁻³)", color=LR_COLOR, fontsize=14)
ax2.tick_params(axis="y", colors=LR_COLOR)
ax2.spines["right"].set_color(LR_COLOR)
ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_linewidth(2.0)
ax2.spines["top"].set_visible(False)
ax2.set_xlim(steps[0], steps[-1])
ax2.set_ylim(bottom=0)

# Legend (combined, top-right inside)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
           loc="upper right", frameon=False, fontsize=12)

fig.tight_layout(pad=0.8)

# ── Export ───────────────────────────────────────────────────────────────────
for ext in ("pdf", "png", "svg"):
    fig.savefig(cwd / f"figure.{ext}", dpi=300, bbox_inches="tight")

plt.close(fig)
print("Saved figure.pdf, figure.png, figure.svg")
