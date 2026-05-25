"""
gen_figure.py — grouped bar chart: 4 methods × 5 benchmarks
Data source: data.json (same directory)
"""

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
# Font stack: Arial → Helvetica → DejaVu Sans → Liberation Sans
# Do NOT override per element — all text inherits from here.

import matplotlib.pyplot as plt
import numpy as np

# ── palette ──────────────────────────────────────────────────────────────────
# Okabe-Ito colorblind-safe; OursModel gets the saturated signal blue accent
PALETTE = {
    "Baseline":  "#959595",   # neutral grey
    "Method-A":  "#56B4E9",   # sky blue
    "Method-B":  "#E69F00",   # amber
    "OursModel": "#0072B2",   # deep signal blue (accent / winner)
}
HATCHES = {
    "Baseline":  "",
    "Method-A":  "///",
    "Method-B":  "...",
    "OursModel": "",
}

# ── data ─────────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
with open(cwd / "data.json") as f:
    data = json.load(f)

benchmarks = data["benchmarks"]   # 5 items
methods    = data["methods"]       # 4 items
values     = data["values"]

means = {m: [values[m][b]["mean"] for b in benchmarks] for m in methods}
stds  = {m: [values[m][b]["std"]  for b in benchmarks] for m in methods}

# ── layout ───────────────────────────────────────────────────────────────────
n_benchmarks = len(benchmarks)
n_methods    = len(methods)
bar_width    = 0.18          # fraction of slot
group_width  = 1.0
offsets = np.linspace(
    -(n_methods - 1) / 2 * bar_width,
     (n_methods - 1) / 2 * bar_width,
    n_methods,
)
x = np.arange(n_benchmarks)

fig, ax = plt.subplots(figsize=(7, 4))

for i, method in enumerate(methods):
    bars = ax.bar(
        x + offsets[i],
        means[method],
        width=bar_width * 0.92,
        yerr=stds[method],
        error_kw=dict(elinewidth=0.8, capsize=2.5, ecolor="#555555"),
        color=PALETTE[method],
        hatch=HATCHES[method],
        label=method,
        zorder=3,
    )
    # value labels above each bar
    for bar, mean_val in zip(bars, means[method]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(stds[method]) + 0.6,
            f"{mean_val:.1f}",
            ha="center", va="bottom",
            fontsize=6.5, color="#444444",
        )

# ── axes ─────────────────────────────────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=9)
ax.set_ylabel("Accuracy (%)", fontsize=9)
ax.tick_params(axis="both", direction="out", length=2.2, width=0.6, labelsize=8)

# zoom y-axis to data range (brief hint: don't start at 0 if all > 60)
all_means = [v for m in methods for v in means[m]]
all_stds  = [v for m in methods for v in stds[m]]
data_min  = min(all_means) - max(all_stds)
data_max  = max(all_means) + max(all_stds)
span      = data_max - data_min
ax.set_ylim(data_min - 0.10 * span, data_max + 0.22 * span)

# light horizontal grid behind bars
ax.yaxis.grid(True, linewidth=0.4, color="#dddddd", zorder=0)
ax.set_axisbelow(True)

# ── legend ───────────────────────────────────────────────────────────────────
# inside axes, upper-left, away from tallest bars (OursModel is rightmost)
legend = ax.legend(
    loc="upper left",
    fontsize=8,
    handlelength=1.4,
    handleheight=0.9,
    borderpad=0.5,
    labelspacing=0.35,
)

# bold the winner label
for text in legend.get_texts():
    if text.get_text() == "OursModel":
        text.set_fontweight("bold")

fig.tight_layout(pad=0.6)

# ── save ─────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
print(f"Saved: {pdf_path}, {png_path}, {svg_path}")

# ── font-type verification ────────────────────────────────────────────────────
import re
raw = pdf_path.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)

out = subprocess.run(
    ["pdffonts", str(pdf_path)],
    capture_output=True, text=True, check=False,
)
if out.returncode == 0 and "Type 3" in out.stdout:
    sys.stderr.write(
        f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n"
    )
    sys.exit(2)

print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")
