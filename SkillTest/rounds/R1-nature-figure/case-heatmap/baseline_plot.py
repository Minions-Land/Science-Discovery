from pathlib import Path
import os
import sys


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
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/matplotlib-cache-skilltest")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


DATA_PATH = Path("/Users/mjm/Skill/SkillTest/fixtures/figures/data/heatmap-zscore.csv")
OUT_DIR = Path(__file__).resolve().parent


def main():
    df = pd.read_csv(DATA_PATH)
    value_cols = ["CTRL_1", "CTRL_2", "CTRL_3", "CTRL_4", "TREAT_1", "TREAT_2", "TREAT_3", "TREAT_4"]
    values = df[value_cols].to_numpy()

    fig = plt.figure(figsize=(7.0, 7.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[0.15, 1, 0.08], wspace=0.05)
    ax_cluster = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[0, 1])
    cax = fig.add_subplot(gs[0, 2])

    vmax = float(np.nanmax(np.abs(values)))
    image = ax.imshow(values, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    fig.colorbar(image, cax=cax, label="row-wise z-score")

    ax.set_xticks(np.arange(len(value_cols)))
    ax.set_xticklabels(value_cols, rotation=45, ha="right")
    ax.set_yticks(np.arange(0, len(df), 2))
    ax.set_yticklabels(df["gene"].iloc[::2])
    ax.axvline(3.5, color="black", linewidth=1.2)
    ax.set_title("Expression z-scores by condition")
    ax.tick_params(direction="out")

    clusters = df["cluster"].map({"A": 0, "B": 1, "C": 2}).to_numpy()[:, None]
    cluster_cmap = ListedColormap(["#4C72B0", "#55A868", "#C44E52"])
    ax_cluster.imshow(clusters, aspect="auto", cmap=cluster_cmap, vmin=0, vmax=2)
    ax_cluster.set_xticks([])
    ax_cluster.set_yticks([4.5, 14.5, 24.5])
    ax_cluster.set_yticklabels(["A", "B", "C"])
    ax_cluster.tick_params(length=0)

    for boundary in [9.5, 19.5]:
        ax.axhline(boundary, color="black", linewidth=0.8)
        ax_cluster.axhline(boundary, color="black", linewidth=0.8)

    fig.tight_layout()
    for ext in ("svg", "pdf", "png"):
        kwargs = {"dpi": 300} if ext == "png" else {}
        fig.savefig(OUT_DIR / f"baseline.{ext}", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
