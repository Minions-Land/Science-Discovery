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
from matplotlib.patches import Patch

try:
    from scipy import stats
except Exception:  # pragma: no cover
    stats = None


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["legend.frameon"] = False


DATA_PATH = Path("/Users/mjm/Skill/SkillTest/fixtures/figures/data/bar-ablation.csv")
OUT_DIR = Path(__file__).resolve().parent

METHODS = ["Full", "-A", "-B", "-C"]
METHOD_LABELS = {"Full": "Full", "-A": "-A", "-B": "-B", "-C": "-C"}
BASE_BLUE = (0.216, 0.459, 0.729)
METHOD_COLORS = {
    "Full": (BASE_BLUE[0], BASE_BLUE[1], BASE_BLUE[2], 1.00),
    "-A": (BASE_BLUE[0], BASE_BLUE[1], BASE_BLUE[2], 0.68),
    "-B": (BASE_BLUE[0], BASE_BLUE[1], BASE_BLUE[2], 0.46),
    "-C": (BASE_BLUE[0], BASE_BLUE[1], BASE_BLUE[2], 0.26),
}
HATCHES = {"Full": "", "-A": "//", "-B": "\\\\", "-C": ".."}


def sig_marker(full_values, ablated_values):
    if stats is None:
        return ""
    p_value = stats.ttest_ind(full_values, ablated_values, equal_var=False).pvalue
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "n.s."


def main():
    df = pd.read_csv(DATA_PATH)
    datasets = ["Dataset-1", "Dataset-2", "Dataset-3"]
    summary = df.groupby(["dataset", "method"])["accuracy"].agg(["mean", "std"])

    fig, ax = plt.subplots(figsize=(85 / 25.4, 58 / 25.4), constrained_layout=True)
    x = np.arange(len(datasets))
    width = 0.18

    for method_i, method in enumerate(METHODS):
        offset = (method_i - (len(METHODS) - 1) / 2) * width
        means = [summary.loc[(dataset, method), "mean"] for dataset in datasets]
        sds = [summary.loc[(dataset, method), "std"] for dataset in datasets]
        bars = ax.bar(
            x + offset,
            means,
            width=width,
            yerr=sds,
            color=METHOD_COLORS[method],
            edgecolor="#272727",
            linewidth=0.55,
            capsize=2.0,
            error_kw={"elinewidth": 0.65, "capthick": 0.65},
            zorder=3,
        )
        for bar in bars:
            bar.set_hatch(HATCHES[method])

    for xpos, dataset in zip(x, datasets):
        baseline = df.loc[df["dataset"] == dataset, "external_baseline"].iloc[0]
        ax.hlines(
            baseline,
            xpos - 0.46,
            xpos + 0.46,
            colors="#606060",
            linestyles=(0, (3, 2)),
            linewidth=0.8,
            zorder=2,
        )
        full = df[(df["dataset"] == dataset) & (df["method"] == "Full")]["accuracy"]
        minus_c = df[(df["dataset"] == dataset) & (df["method"] == "-C")]["accuracy"]
        marker = sig_marker(full, minus_c)
        y = min(0.975, max(full.mean() + full.std(), minus_c.mean() + minus_c.std()) + 0.028)
        ax.plot([xpos - 1.5 * width, xpos + 1.5 * width], [y, y], color="#272727", lw=0.65, clip_on=False)
        ax.text(xpos, y + 0.010, marker, ha="center", va="bottom", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.linspace(0, 1.0, 6))
    ax.tick_params(axis="both", direction="out", length=2.5, width=0.7)

    legend_handles = [
        Patch(facecolor=METHOD_COLORS[m], edgecolor="#272727", hatch=HATCHES[m], label=METHOD_LABELS[m], linewidth=0.55)
        for m in METHODS
    ]
    ax.legend(
        handles=legend_handles,
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.18),
        handlelength=1.2,
        columnspacing=0.8,
        borderaxespad=0.0,
    )
    ax.text(
        0.0,
        -0.26,
        "Mean accuracy +/- 1 SD (n=5 seeds); dashed segment, strongest external baseline. Full vs -C: * P<0.05, ** P<0.01.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=5.8,
    )

    for ext in ("svg", "pdf", "png"):
        kwargs = {"dpi": 600} if ext == "png" else {}
        fig.savefig(OUT_DIR / f"candidate.{ext}", bbox_inches="tight", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
