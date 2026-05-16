from pathlib import Path
import os
import sys


os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib-cache-skilltest")
os.environ.setdefault("XDG_CACHE_HOME", "/private/tmp/skilltest-cache")


def ensure_plotting_python():
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
        import matplotlib  # noqa: F401
    except ModuleNotFoundError:
        conda_python = Path("/Users/mjm/miniconda3/bin/python3")
        if conda_python.exists() and Path(sys.executable) != conda_python:
            os.execv(str(conda_python), [str(conda_python), *sys.argv])
        raise


ensure_plotting_python()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["legend.frameon"] = False


DATA_PATH = Path("/Users/mjm/Skill/SkillTest/fixtures/figures/data/heatmap-zscore.csv")
OUT_DIR = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(DATA_PATH)
    value_cols = ["CTRL_1", "CTRL_2", "CTRL_3", "CTRL_4", "TREAT_1", "TREAT_2", "TREAT_3", "TREAT_4"]
    values = df[value_cols].to_numpy()
    vmax = float(np.ceil(np.nanmax(np.abs(values)) * 10) / 10)

    fig = plt.figure(figsize=(115 / 25.4, 96 / 25.4), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[0.06, 1.0, 0.08], wspace=0.02)
    ax_cluster = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[0, 1])
    cax = fig.add_subplot(gs[0, 2])

    cmap = mpl.colormaps["RdBu_r"].copy()
    cmap.set_bad("white")
    norm = mpl.colors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    im = ax.imshow(values, aspect="auto", cmap=cmap, norm=norm, interpolation="nearest")
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("Row-wise z-score", fontsize=7)
    cb.ax.tick_params(labelsize=6, length=2.2, width=0.6, direction="out")

    cluster_codes = df["cluster"].map({"A": 0, "B": 1, "C": 2}).to_numpy()[:, None]
    cluster_cmap = ListedColormap(["#D8D8D8", "#3775BA", "#E4CCD8"])
    ax_cluster.imshow(cluster_codes, aspect="auto", cmap=cluster_cmap, vmin=0, vmax=2, interpolation="nearest")
    ax_cluster.set_xticks([])
    ax_cluster.set_yticks([4.5, 14.5, 24.5])
    ax_cluster.set_yticklabels(["A", "B", "C"], fontsize=6)
    ax_cluster.tick_params(axis="y", length=0, pad=1)
    for spine in ax_cluster.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(len(value_cols)))
    ax.set_xticklabels(value_cols, rotation=45, ha="right", fontsize=6)
    visible_rows = np.arange(0, len(df), 3)
    ax.set_yticks(visible_rows)
    ax.set_yticklabels(df["gene"].iloc[visible_rows], fontsize=6, rotation=0)
    ax.tick_params(axis="both", direction="out", length=2.2, width=0.6)
    ax.set_frame_on(False)
    ax.axvline(3.5, color="#272727", linewidth=0.8)

    for boundary in [9.5, 19.5]:
        ax.axhline(boundary, color="#272727", linewidth=0.45)
        ax_cluster.axhline(boundary, color="#272727", linewidth=0.45)

    ax.text(
        0.5,
        -0.18,
        "CTRL and TREAT columns are separated by the vertical rule; left side bar denotes clusters A-C.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=5.8,
    )

    for ext in ("svg", "pdf", "png"):
        kwargs = {"dpi": 600} if ext == "png" else {}
        fig.savefig(OUT_DIR / f"candidate.{ext}", bbox_inches="tight", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
