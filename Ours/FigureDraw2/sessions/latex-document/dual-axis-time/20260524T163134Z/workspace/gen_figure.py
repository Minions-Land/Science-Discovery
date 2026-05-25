import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data.json") as f:
    data = json.load(f)

steps = np.array(data["steps"])
loss  = np.array(data["loss"])
lr    = np.array(data["lr"])

LOSS_COLOR = "#1f77b4"   # blue
LR_COLOR   = "#d62728"   # red

fig, ax1 = plt.subplots(figsize=(7, 4))

ax1.semilogy(steps, loss, color=LOSS_COLOR, linewidth=1.6, label="Training loss")
ax1.set_xlabel("Training step", fontsize=11)
ax1.set_ylabel("Training loss (log scale)", color=LOSS_COLOR, fontsize=11)
ax1.tick_params(axis="y", colors=LOSS_COLOR, labelsize=9)
ax1.tick_params(axis="x", labelsize=9)
ax1.yaxis.set_minor_formatter(ticker.NullFormatter())
ax1.spines["left"].set_color(LOSS_COLOR)

ax2 = ax1.twinx()
ax2.plot(steps, lr * 1e3, color=LR_COLOR, linewidth=1.4,
         linestyle="--", label="Learning rate (×10⁻³)")
ax2.set_ylabel("Learning rate (×10⁻³)", color=LR_COLOR, fontsize=11)
ax2.tick_params(axis="y", colors=LR_COLOR, labelsize=9)
ax2.spines["right"].set_color(LR_COLOR)
ax2.set_ylim(bottom=0)

# combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9,
           loc="upper right", framealpha=0.85)

ax1.set_xlim(steps[0], steps[-1])
fig.tight_layout()

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
