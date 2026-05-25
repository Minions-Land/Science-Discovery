import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# --- Style constants (from skill api.md) ---
PALETTE = {
    "blue_main":      "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_3":        "#8BCF8B",
    "red_strong":     "#B64342",
    "neutral":        "#CFCECE",
    "highlight":      "#FFD700",
    "teal":           "#42949E",
}

FONT_SIZE      = 15
AXES_LINEWIDTH = 2.0

def apply_publication_style():
    plt.rcParams.update({
        "font.family":        "sans-serif",
        "font.sans-serif":    ["DejaVu Sans", "Helvetica", "Arial"],
        "font.size":          FONT_SIZE,
        "axes.linewidth":     AXES_LINEWIDTH,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "legend.frameon":     False,
        "pdf.fonttype":       42,
        "ps.fonttype":        42,
        "figure.dpi":         150,
    })

# --- Load data ---
cwd = Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

steps   = np.array(data["steps"])
methods = data["methods"]
curves  = data["curves"]

# Color assignment: OursModel=blue (proposed), Method-A=teal, Baseline=red
COLOR_MAP = {
    "OursModel": PALETTE["blue_main"],
    "Method-A":  PALETTE["teal"],
    "Baseline":  PALETTE["red_strong"],
}
ALPHA_BAND = 0.18

apply_publication_style()

fig, ax = plt.subplots(figsize=(7, 4.5))

for method in methods:
    mean    = np.array(curves[method]["mean"])
    ci_half = np.array(curves[method]["ci_half"])
    color   = COLOR_MAP[method]
    lw      = 2.5 if method == "OursModel" else 1.8
    zorder  = 3 if method == "OursModel" else 2

    ax.fill_between(steps, mean - ci_half, mean + ci_half,
                    color=color, alpha=ALPHA_BAND, linewidth=0, zorder=zorder - 1)
    ax.plot(steps, mean, color=color, linewidth=lw,
            label=method, zorder=zorder)

# --- Highlight gap at final step ---
final_step = steps[-1]
vals = {m: curves[m]["mean"][-1] for m in methods}
ours_val     = vals["OursModel"]
baseline_val = vals["Baseline"]
methoda_val  = vals["Method-A"]

# Bracket between OursModel and Baseline (largest gap)
ax.annotate("", xy=(final_step + 0.6, ours_val),
            xytext=(final_step + 0.6, baseline_val),
            arrowprops=dict(arrowstyle="<->", color=PALETTE["highlight"],
                            lw=2.0))
ax.text(final_step + 1.2,
        (ours_val + baseline_val) / 2,
        f"{baseline_val - ours_val:.2f}",
        va="center", ha="left",
        fontsize=11, color=PALETTE["highlight"],
        fontweight="bold")

# --- Axes labels and limits ---
ax.set_xlabel(data["x_label"].capitalize(), fontsize=FONT_SIZE)
ax.set_ylabel(data["y_label"].capitalize(), fontsize=FONT_SIZE)
ax.set_xlim(steps[0] - 0.5, steps[-1] + 4)
ax.set_yscale("log")
ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.1f"))
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

# --- Legend ---
ax.legend(loc="upper right", fontsize=12)

fig.tight_layout(pad=0.5)

# --- Save ---
for fmt in ("pdf", "png", "svg"):
    fig.savefig(cwd / f"figure.{fmt}", dpi=300,
                bbox_inches="tight")

plt.close(fig)
print("Saved figure.pdf, figure.png, figure.svg")
