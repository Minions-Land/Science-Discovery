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

fig, ax1 = plt.subplots(figsize=(7, 4))

line1, = ax1.semilogy(steps, loss, color=LOSS_COLOR, linewidth=1.4,
                      label="Training loss")
ax1.set_xlabel("Step", fontsize=11)
ax1.set_ylabel("Training loss (log scale)", color=LOSS_COLOR, fontsize=11)
ax1.tick_params(axis="y", labelcolor=LOSS_COLOR)
ax1.yaxis.set_major_formatter(ticker.LogFormatterSciNotation(labelOnlyBase=False))
ax1.set_xlim(steps[0], steps[-1])

ax2 = ax1.twinx()
line2, = ax2.plot(steps, lr * 1e3, color=LR_COLOR, linewidth=1.4,
                  linestyle="--", label="Learning rate (×10⁻³)")
ax2.set_ylabel("Learning rate (×10⁻³)", color=LR_COLOR, fontsize=11)
ax2.tick_params(axis="y", labelcolor=LR_COLOR)
ax2.set_ylim(bottom=0)

lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=9, framealpha=0.85)

ax1.set_title("Training loss and cosine LR schedule", fontsize=12, pad=8)
fig.tight_layout()

fig.savefig("figure.pdf", dpi=150)
fig.savefig("figure.png", dpi=150)
fig.savefig("figure.svg")
print("Saved figure.pdf, figure.png, figure.svg")
