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

# --- Training loss (left, log scale) ---
ax1.plot(steps, loss, color=LOSS_COLOR, linewidth=1.5, label="Training loss")
ax1.set_yscale("log")
ax1.set_xlabel("Training step", fontsize=11)
ax1.set_ylabel("Training loss (log scale)", color=LOSS_COLOR, fontsize=11)
ax1.tick_params(axis="y", labelcolor=LOSS_COLOR)
ax1.tick_params(axis="x")
ax1.yaxis.set_major_formatter(ticker.LogFormatterSciNotation(labelOnlyBase=False))
ax1.set_xlim(steps[0], steps[-1])

# --- Cosine LR schedule (right axis) ---
ax2 = ax1.twinx()
ax2.plot(steps, lr * 1e3, color=LR_COLOR, linewidth=1.5,
         linestyle="--", label="Learning rate")
ax2.set_ylabel(r"Learning rate ($\times 10^{-3}$)", color=LR_COLOR, fontsize=11)
ax2.tick_params(axis="y", labelcolor=LR_COLOR)
ax2.set_ylim(bottom=0)

# --- Legend (combined) ---
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=9)

# Spine colour hints
ax1.spines["left"].set_color(LOSS_COLOR)
ax2.spines["right"].set_color(LR_COLOR)

plt.title("Training dynamics: loss and cosine LR schedule", fontsize=12)
fig.tight_layout()

fig.savefig("figure.pdf", bbox_inches="tight")
fig.savefig("figure.png", dpi=150, bbox_inches="tight")
fig.savefig("figure.svg", bbox_inches="tight")

print("Saved figure.pdf, figure.png, figure.svg")
