import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data.json") as f:
    d = json.load(f)

steps = np.array(d["steps"])
loss  = np.array(d["loss"])
lr    = np.array(d["lr"])

LOSS_COLOR = "#1f77b4"   # blue
LR_COLOR   = "#d62728"   # red

fig, ax1 = plt.subplots(figsize=(6.5, 3.8))

line_loss, = ax1.semilogy(steps, loss, color=LOSS_COLOR, linewidth=1.6,
                           label="Training loss")
ax1.set_xlabel("Step", fontsize=11)
ax1.set_ylabel("Training loss (log scale)", fontsize=11, color=LOSS_COLOR)
ax1.tick_params(axis="y", labelcolor=LOSS_COLOR)
ax1.yaxis.set_major_formatter(ticker.LogFormatter(labelOnlyBase=False))
ax1.set_xlim(steps[0], steps[-1])
ax1.grid(True, which="both", axis="y", linestyle="--", linewidth=0.4,
         alpha=0.5, color=LOSS_COLOR)

ax2 = ax1.twinx()
line_lr, = ax2.plot(steps, lr * 1e3, color=LR_COLOR, linewidth=1.4,
                    linestyle="--", label="Learning rate")
ax2.set_ylabel(r"Learning rate ($\times 10^{-3}$)", fontsize=11, color=LR_COLOR)
ax2.tick_params(axis="y", labelcolor=LR_COLOR)
ax2.set_ylim(bottom=0)

# combined legend
lines = [line_loss, line_lr]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=9, framealpha=0.85)

fig.tight_layout()

fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
