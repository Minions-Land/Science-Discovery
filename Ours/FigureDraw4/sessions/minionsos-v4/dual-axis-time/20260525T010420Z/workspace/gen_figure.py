import json
import pathlib
import subprocess
import sys

import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

import matplotlib.pyplot as plt
import numpy as np

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

# Colors: color-couple each axis to its line (brief requirement)
COLOR_LOSS = "#0F4D92"   # blue — training loss (left axis)
COLOR_LR   = "#D55E00"   # orange-red — learning rate (right axis)

cwd = pathlib.Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())

steps = np.array(data["steps"])
loss  = np.array(data["loss"])
lr    = np.array(data["lr"])

fig, ax1 = plt.subplots(figsize=(7, 4))

# --- Left axis: training loss (log scale) ---
ax1.set_yscale("log")
line1, = ax1.plot(steps, loss, color=COLOR_LOSS, linewidth=1.5, label="Training loss")

ax1.set_xlabel("Step", fontsize=9)
ax1.set_ylabel("Training loss (log scale)", fontsize=9, color=COLOR_LOSS)
ax1.tick_params(axis="y", colors=COLOR_LOSS, direction="out", length=2.2, width=0.6)
ax1.tick_params(axis="x", direction="out", length=2.2, width=0.6)
ax1.spines["left"].set_color(COLOR_LOSS)
ax1.yaxis.label.set_color(COLOR_LOSS)

# --- Right axis: cosine LR schedule ---
ax2 = ax1.twinx()
ax2.spines["right"].set_visible(True)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["right"].set_color(COLOR_LR)
ax2.spines["right"].set_linewidth(0.8)

line2, = ax2.plot(steps, lr * 1e3, color=COLOR_LR, linewidth=1.5,
                  linestyle="--", label="Learning rate")

ax2.set_ylabel(r"Learning rate ($\times 10^{-3}$)", fontsize=9, color=COLOR_LR)
ax2.tick_params(axis="y", colors=COLOR_LR, direction="out", length=2.2, width=0.6)

# Tick labels
ax1.tick_params(labelsize=8)
ax2.tick_params(labelsize=8)

# Combined legend inside axes, top-right
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=8)

fig.tight_layout()

out_pdf = cwd / "figure.pdf"
out_png = cwd / "figure.png"
out_svg = cwd / "figure.svg"

fig.savefig(out_pdf, bbox_inches="tight")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
fig.savefig(out_svg, bbox_inches="tight")
plt.close(fig)

# --- Post-save font verification ---
pdf_path = pathlib.Path(out_pdf)
result = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if result.returncode == 0:
    if "Type 3" in result.stdout:
        sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{result.stdout}\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {pdf_path}")
else:
    # pdffonts not available; fall back to raw bytes check
    import re
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (fallback byte-scan) — no Type 3 fonts")

print(f"Saved: {out_pdf}, {out_png}, {out_svg}")
