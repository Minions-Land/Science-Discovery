"""
gen_figure.py — violin + box overlay with jittered points and significance brackets.
Data source: data.json (4 conditions × 100 samples, metric: relative cell viability).
"""

import json, pathlib, sys, re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import mannwhitneyu

# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.
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
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

# Okabe-Ito colorblind-safe palette; one hue per condition
PALETTE = {
    "Control":       "#0072B2",
    "Drug-A 10uM":   "#E69F00",
    "Drug-A 50uM":   "#D55E00",
    "Combo":         "#CC79A7",
}

rng = np.random.default_rng(42)

data_path = pathlib.Path("data.json")
raw = json.loads(data_path.read_text())

ORDER = ["Control", "Drug-A 10uM", "Drug-A 50uM", "Combo"]
LABELS = ["Control", "Drug-A\n10 µM", "Drug-A\n50 µM", "Combo"]
samples = {c: np.array(raw["samples"][c]) for c in ORDER}

fig, ax = plt.subplots(figsize=(7, 4.5))

xs = np.arange(1, len(ORDER) + 1)

for i, (cond, x) in enumerate(zip(ORDER, xs)):
    vals = samples[cond]
    color = PALETTE[cond]

    # Violin
    vp = ax.violinplot(vals, positions=[x], widths=0.55,
                       showmeans=False, showmedians=False, showextrema=False)
    for body in vp["bodies"]:
        body.set_facecolor(color)
        body.set_alpha(0.35)
        body.set_edgecolor(color)
        body.set_linewidth(0.8)

    # Box
    q1, med, q3 = np.percentile(vals, [25, 50, 75])
    iqr = q3 - q1
    lo_wh = max(vals[vals >= q1 - 1.5 * iqr].min(), vals.min())
    hi_wh = min(vals[vals <= q3 + 1.5 * iqr].max(), vals.max())

    box = mpatches.FancyBboxPatch(
        (x - 0.12, q1), 0.24, iqr,
        boxstyle="square,pad=0", linewidth=1.0,
        edgecolor=color, facecolor="white", zorder=3
    )
    ax.add_patch(box)
    # Whiskers
    ax.plot([x, x], [lo_wh, q1], color=color, lw=1.0, zorder=3)
    ax.plot([x, x], [hi_wh, q3], color=color, lw=1.0, zorder=3)
    ax.plot([x - 0.08, x + 0.08], [lo_wh, lo_wh], color=color, lw=1.0, zorder=3)
    ax.plot([x - 0.08, x + 0.08], [hi_wh, hi_wh], color=color, lw=1.0, zorder=3)
    # Median line
    ax.plot([x - 0.12, x + 0.12], [med, med], color=color, lw=2.0, zorder=4)

    # Jittered points
    jitter = rng.uniform(-0.18, 0.18, size=len(vals))
    ax.scatter(x + jitter, vals, s=12, color=color, alpha=0.35,
               linewidths=0, zorder=2)

# Mann-Whitney U significance brackets (vs Control)
ctrl = samples["Control"]
comparisons = [
    ("Drug-A 10uM", 2, "ns"),
    ("Drug-A 50uM", 3, "***"),
    ("Combo",       4, "***"),
]

bracket_y_start = max(v.max() for v in samples.values()) + 0.08
bracket_step = 0.18

for idx, (cond, x2, _) in enumerate(comparisons):
    stat, p = mannwhitneyu(ctrl, samples[cond], alternative="two-sided")
    if p < 0.001:
        stars = "***"
    elif p < 0.01:
        stars = "**"
    elif p < 0.05:
        stars = "*"
    else:
        stars = "ns"

    y = bracket_y_start + idx * bracket_step
    ax.plot([1, 1, x2, x2], [y - 0.02, y, y, y - 0.02],
            color="#444444", lw=0.8)
    ax.text((1 + x2) / 2, y + 0.01, stars,
            ha="center", va="bottom", fontsize=8.5, color="#444444")

ax.set_xlim(0.35, len(ORDER) + 0.65)
ax.set_ylim(bottom=0)
ax.set_xticks(xs)
ax.set_xticklabels(LABELS)
ax.set_ylabel("Relative cell viability")
ax.tick_params(direction="out", length=2.5, width=0.6)
ax.spines["bottom"].set_linewidth(0.8)
ax.spines["left"].set_linewidth(0.8)

fig.tight_layout()

out_pdf = pathlib.Path("figure.pdf")
out_png = pathlib.Path("figure.png")
out_svg = pathlib.Path("figure.svg")

fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
fig.savefig(out_svg, bbox_inches="tight")
plt.close(fig)

# Post-save font verification
try:
    import subprocess
    res = subprocess.run(["pdffonts", str(out_pdf)], capture_output=True, text=True, check=False)
    if "Type 3" in res.stdout:
        sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{res.stdout}\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type 3 fonts in {out_pdf}")
except FileNotFoundError:
    raw_bytes = out_pdf.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw_bytes):
        sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
        sys.exit(2)
    print("[fonttype-check] OK (pdffonts unavailable; byte-scan passed)")

print("Done: figure.pdf  figure.png  figure.svg")
