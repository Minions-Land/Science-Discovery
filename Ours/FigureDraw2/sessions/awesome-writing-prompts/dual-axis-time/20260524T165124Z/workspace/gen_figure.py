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

l1, = ax1.plot(steps, loss, color=LOSS_COLOR, linewidth=1.6, label="Training loss")
ax1.set_yscale("log")
ax1.set_xlabel("Step", fontsize=11)
ax1.set_ylabel("Training loss (log scale)", color=LOSS_COLOR, fontsize=11)
ax1.tick_params(axis="y", colors=LOSS_COLOR, labelsize=9)
ax1.tick_params(axis="x", labelsize=9)
ax1.spines["left"].set_color(LOSS_COLOR)
ax1.set_xlim(steps[0], steps[-1])

ax2 = ax1.twinx()
l2, = ax2.plot(steps, lr * 1e3, color=LR_COLOR, linewidth=1.6,
               linestyle="--", label="LR ×10⁻³")
ax2.set_ylabel("Learning rate (×10⁻³)", color=LR_COLOR, fontsize=11)
ax2.tick_params(axis="y", colors=LR_COLOR, labelsize=9)
ax2.spines["right"].set_color(LR_COLOR)
ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))

# Suppress default spines coloring on left side for ax2
ax2.spines["left"].set_visible(False)
ax1.spines["right"].set_visible(False)

lines = [l1, l2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=9, framealpha=0.85)

ax1.set_title("Training Loss and Cosine LR Schedule", fontsize=12, pad=8)

fig.tight_layout()
fig.savefig("figure.pdf", dpi=150, bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")
print("Saved figure.pdf, figure.png, figure.svg")
