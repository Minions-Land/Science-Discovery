"""
gen_figure.py — Chinchilla-style scaling law scatter + OLS fit
Data source: data.json (x=log10(parameters), y=log10(validation loss))
"""
import json
import pathlib
import numpy as np
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
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
from scipy import stats

PALETTE = {
    "scatter": "#B4C0E4",
    "fit_line": "#0F4D92",
    "ours": "#D55E00",
    "annotation": "#272727",
    "neutral": "#767676",
}

cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

x = np.array(data["x"])
y = np.array(data["y"])
x_label = data["x_label"]
y_label = data["y_label"]

# OLS fit
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r2 = r_value ** 2

# Find closest data point to OursModel target (~9.4, ~0.205)
target_x, target_y = 9.4, 0.205
dists = np.sqrt((x - target_x) ** 2 + (y - target_y) ** 2)
ours_idx = int(np.argmin(dists))
ours_x, ours_y = x[ours_idx], y[ours_idx]

# Fit line range
x_fit = np.linspace(x.min() - 0.1, x.max() + 0.1, 200)
y_fit = slope * x_fit + intercept

fig, ax = plt.subplots(figsize=(6, 4))

# Scatter — all points except OursModel
mask = np.ones(len(x), dtype=bool)
mask[ours_idx] = False
ax.scatter(x[mask], y[mask], s=22, color=PALETTE["scatter"],
           edgecolors=PALETTE["fit_line"], linewidths=0.4, alpha=0.85, zorder=2)

# OLS fit line
ax.plot(x_fit, y_fit, color=PALETTE["fit_line"], linewidth=1.8, zorder=3,
        label=f"OLS fit")

# OursModel point
ax.scatter([ours_x], [ours_y], s=70, color=PALETTE["ours"],
           edgecolors="white", linewidths=0.8, zorder=5, label="OursModel")
ax.annotate(
    "OursModel",
    xy=(ours_x, ours_y),
    xytext=(ours_x + 0.25, ours_y + 0.012),
    fontsize=8,
    color=PALETTE["ours"],
    arrowprops=dict(arrowstyle="-", color=PALETTE["ours"], lw=0.8),
)

# Annotation box: slope, intercept, R²
annot_text = (
    f"$y = {slope:.4f}x + {intercept:.3f}$\n"
    f"$R^2 = {r2:.3f}$"
)
ax.text(
    0.97, 0.97, annot_text,
    transform=ax.transAxes,
    fontsize=8,
    va="top", ha="right",
    color=PALETTE["annotation"],
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
              edgecolor=PALETTE["neutral"], linewidth=0.5, alpha=0.85),
)

ax.set_xlabel(x_label, fontsize=9)
ax.set_ylabel(y_label, fontsize=9)
ax.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)
ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(0.97, 0.78))

fig.tight_layout()

out_pdf = cwd / "figure.pdf"
out_png = cwd / "figure.png"
out_svg = cwd / "figure.svg"
fig.savefig(out_pdf, bbox_inches="tight")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
fig.savefig(out_svg, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {out_pdf}, {out_png}, {out_svg}")
print(f"OLS: slope={slope:.4f}, intercept={intercept:.4f}, R²={r2:.4f}")
print(f"OursModel point: ({ours_x}, {ours_y})")

# Mandatory font-type verification
import subprocess, sys
out = subprocess.run(["pdffonts", str(out_pdf)], capture_output=True, text=True, check=False)
if out.returncode == 0:
    if "Type 3" in out.stdout:
        sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {out_pdf}")
else:
    import re
    raw = out_pdf.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (pdffonts unavailable; byte-scan passed)")
