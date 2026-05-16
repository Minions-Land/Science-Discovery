from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats


DATA = "fixtures/figures/data/bar-ablation.csv"
OUT = "rounds/R1-scientific-figure-making/case-bar/candidate"
ORDER = ["Full", "-A", "-B", "-C"]
PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_2": "#AADCA9",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
}


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 7
    axes_linewidth: float = 0.8
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
datasets = list(df["dataset"].drop_duplicates())
summary = df.groupby(["dataset", "method"])["accuracy"].agg(["mean", "std"]).reset_index()

fig, ax = plt.subplots(figsize=(5.2, 3.0))
x = np.arange(len(datasets))
width = 0.18
colors = [PALETTE["blue_main"], PALETTE["green_2"], PALETTE["red_2"], PALETTE["neutral"]]
hatches = ["", "//", "\\\\", ".."]

for i, method in enumerate(ORDER):
    rows = summary[summary["method"] == method].set_index("dataset").loc[datasets]
    ax.bar(
        x + (i - 1.5) * width,
        rows["mean"],
        width,
        yerr=rows["std"],
        error_kw={"elinewidth": 0.8, "capthick": 0.8},
        capsize=2.5,
        label=method,
        color=colors[i],
        edgecolor="black",
        linewidth=0.5,
        hatch=hatches[i],
    )

for j, dataset in enumerate(datasets):
    base = float(df[df["dataset"] == dataset]["external_baseline"].iloc[0])
    ax.hlines(
        base,
        j - 0.44,
        j + 0.44,
        linestyles=(0, (3, 2)),
        colors="#4D4D4D",
        linewidth=0.8,
    )
    full = df[(df["dataset"] == dataset) & (df["method"] == "Full")]["accuracy"]
    minus_c = df[(df["dataset"] == dataset) & (df["method"] == "-C")]["accuracy"]
    p = stats.ttest_ind(full, minus_c, equal_var=False).pvalue
    mark = "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
    x1 = j + (0 - 1.5) * width
    x2 = j + (3 - 1.5) * width
    y = max(full.mean() + full.std(), minus_c.mean() + minus_c.std()) + 0.035
    ax.plot([x1, x1, x2, x2], [y - 0.008, y, y, y - 0.008], color="black", linewidth=0.7)
    ax.text((x1 + x2) / 2, y + 0.006, mark, ha="center", va="bottom", fontsize=7)

ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.set_ylabel("Accuracy (mean +/- SD, n=5)")
ax.set_ylim(0, 1.0)
ax.set_xlim(-0.55, len(datasets) - 0.25)
handles, labels = ax.get_legend_handles_labels()
handles.append(Line2D([0], [0], color="#4D4D4D", linewidth=0.8, linestyle=(0, (3, 2))))
labels.append("External baseline")
ax.legend(handles, labels, ncols=5, loc="upper center", bbox_to_anchor=(0.5, 1.18), handlelength=1.4, columnspacing=1.0)
ax.tick_params(direction="out", length=3, width=0.8)
finalize_figure(fig, OUT)
