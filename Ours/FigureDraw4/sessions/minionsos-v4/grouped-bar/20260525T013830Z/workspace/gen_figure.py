"""
Grouped bar chart: 4 methods × 5 benchmarks.
Data source: data.json (same directory).
"""

import json, pathlib, subprocess, sys
import numpy as np
import matplotlib as mpl

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
})

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Palette (Okabe-Ito colorblind-safe) ──────────────────────────────────────
PALETTE = {
    "Baseline":   "#767676",   # neutral grey
    "Method-A":   "#56B4E9",   # sky blue
    "Method-B":   "#E69F00",   # amber
    "OursModel":  "#0072B2",   # strong blue (signal / "our method")
}

HATCHES = {
    "Baseline":  "",
    "Method-A":  "///",
    "Method-B":  "...",
    "OursModel": "xxx",
}

# ── Load data ─────────────────────────────────────────────────────────────────
cwd = pathlib.Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())

benchmarks = data["benchmarks"]   # 5
methods    = data["methods"]       # 4
values     = data["values"]

n_bench   = len(benchmarks)
n_methods = len(methods)

means = np.array([[values[m][b]["mean"] for b in benchmarks] for m in methods])
stds  = np.array([[values[m][b]["std"]  for b in benchmarks] for m in methods])

# ── Layout ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 3.6))

bar_w   = 0.18
group_w = n_methods * bar_w
offsets = np.linspace(-(group_w - bar_w) / 2, (group_w - bar_w) / 2, n_methods)
x       = np.arange(n_bench)

for i, method in enumerate(methods):
    xpos = x + offsets[i]
    bars = ax.bar(
        xpos,
        means[i],
        width=bar_w,
        bottom=0,
        color=PALETTE[method],
        hatch=HATCHES[method],
        edgecolor="white" if method != "OursModel" else "#004C80",
        linewidth=0.6,
        label=method,
        zorder=3,
    )
    ax.errorbar(
        xpos,
        means[i],
        yerr=stds[i],
        fmt="none",
        ecolor="#272727",
        elinewidth=0.9,
        capsize=2.2,
        capthick=0.9,
        zorder=4,
    )

# ── Axis formatting ───────────────────────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(benchmarks, fontsize=8)
ax.set_ylabel("Accuracy (%)", fontsize=9)
ax.tick_params(direction="out", length=2.2, width=0.6, labelsize=8)

# y-range: all values above 30, min ≈ 31 → start at 25 to avoid wasted space
ymin = max(0, np.min(means - stds) - 5)
ymax = np.max(means + stds) + 5
ax.set_ylim(ymin, ymax)
ax.set_xlim(-0.5, n_bench - 0.5)

# Subtle horizontal grid
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.5, zorder=0)
ax.set_axisbelow(True)

# ── Legend (inside axes, upper-left) ─────────────────────────────────────────
legend_patches = [
    mpatches.Patch(
        facecolor=PALETTE[m],
        hatch=HATCHES[m],
        edgecolor="#555" if m != "OursModel" else "#004C80",
        linewidth=0.6,
        label=m,
    )
    for m in methods
]
ax.legend(
    handles=legend_patches,
    fontsize=8,
    loc="upper left",
    ncol=2,
    handlelength=1.4,
    handleheight=0.9,
    borderpad=0.5,
    labelspacing=0.35,
)

fig.tight_layout(pad=0.5)

# ── Export ────────────────────────────────────────────────────────────────────
pdf_path = cwd / "figure.pdf"
png_path = cwd / "figure.png"
svg_path = cwd / "figure.svg"

fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(svg_path, bbox_inches="tight")
print(f"Saved: {pdf_path}, {png_path}, {svg_path}")

# ── Post-save Type-42 verification ───────────────────────────────────────────
import re
raw = pdf_path.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — rcParams not honored.\n")
    sys.exit(2)

out = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False)
if out.returncode == 0 and "Type 3" in out.stdout:
    sys.stderr.write(f"FATAL: figure.pdf contains Type-3 bitmap fonts.\n{out.stdout}\n")
    sys.exit(2)

print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")
