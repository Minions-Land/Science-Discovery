from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable


DATA = "fixtures/figures/data/heatmap-zscore.csv"
OUT = "rounds/R1-scientific-figure-making/case-heatmap/candidate"
CLUSTER_COLORS = {"A": "#CFCECE", "B": "#0F4D92", "C": "#AADCA9"}


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 6
    axes_linewidth: float = 0.7
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")


def apply_publication_style(style=FigureStyle()):
    plt.rcParams.update({
        "font.family": list(style.font_family),
        "font.size": style.font_size,
        "axes.labelsize": style.font_size,
        "xtick.labelsize": style.font_size,
        "ytick.labelsize": style.font_size,
        "legend.fontsize": style.font_size,
        "axes.linewidth": style.axes_linewidth,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })


def finalize_figure(fig, out_path, formats=("svg", "pdf", "png"), dpi=300, pad=0.05):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        fig.savefig(f"{out_path}.{fmt}", dpi=dpi, bbox_inches="tight", pad_inches=pad)


apply_publication_style()
df = pd.read_csv(DATA)
conditions = [c for c in df.columns if c not in ("gene", "cluster")]
matrix = df[conditions].to_numpy()
genes = df["gene"].tolist()
clusters = df["cluster"].tolist()

fig, ax = plt.subplots(figsize=(5.4, 5.9))
norm = TwoSlopeNorm(vcenter=0, vmin=-2.5, vmax=2.5)
im = ax.imshow(matrix, cmap="RdBu_r", norm=norm, aspect="auto", interpolation="nearest")

ax.set_xticks(np.arange(len(conditions)))
ax.set_xticklabels(conditions, rotation=35, ha="right", rotation_mode="anchor")
tick_idx = np.arange(0, len(genes), 2)
ax.set_yticks(tick_idx)
ax.set_yticklabels([genes[i] for i in tick_idx], rotation=0)
ax.yaxis.tick_right()
ax.tick_params(axis="both", direction="out", length=2.5, width=0.7, pad=2)
ax.axvline(3.5, color="black", linewidth=0.8)
for y in (9.5, 19.5):
    ax.axhline(y, color="black", linewidth=0.6)
ax.text(1.5, -1.25, "CTRL", ha="center", va="bottom", fontsize=6)
ax.text(5.5, -1.25, "TREAT", ha="center", va="bottom", fontsize=6)

divider = make_axes_locatable(ax)
side = divider.append_axes("left", size="3%", pad=0.05)
cluster_rgb = np.array([[matplotlib.colors.to_rgb(CLUSTER_COLORS[c])] for c in clusters])
side.imshow(cluster_rgb, aspect="auto", interpolation="nearest")
side.set_xticks([])
side.set_yticks([4.5, 14.5, 24.5])
side.set_yticklabels(["A", "B", "C"])
side.tick_params(axis="y", direction="out", length=0, pad=1)
for spine in side.spines.values():
    spine.set_visible(False)

cax = divider.append_axes("right", size="4%", pad=0.55)
cbar = fig.colorbar(im, cax=cax)
cbar.set_label("row-wise z-score")
cbar.ax.tick_params(direction="out", length=2.5, width=0.7)

finalize_figure(fig, OUT)
