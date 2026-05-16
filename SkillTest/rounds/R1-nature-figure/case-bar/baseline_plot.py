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

try:
    from scipy import stats
except Exception:  # pragma: no cover
    stats = None


DATA_PATH = Path("/Users/mjm/Skill/SkillTest/fixtures/figures/data/bar-ablation.csv")
OUT_DIR = Path(__file__).resolve().parent


def p_value_marker(full_values, minus_c_values):
    if stats is None:
        return ""
    p_value = stats.ttest_ind(full_values, minus_c_values, equal_var=False).pvalue
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "n.s."


def main():
    df = pd.read_csv(DATA_PATH)
    datasets = ["Dataset-1", "Dataset-2", "Dataset-3"]
    methods = ["Full", "-A", "-B", "-C"]

    summary = (
        df.groupby(["dataset", "method"])["accuracy"]
        .agg(["mean", "std"])
        .reindex(pd.MultiIndex.from_product([datasets, methods], names=["dataset", "method"]))
    )

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    x = np.arange(len(datasets))
    width = 0.18

    for i, method in enumerate(methods):
        offset = (i - 1.5) * width
        means = [summary.loc[(dataset, method), "mean"] for dataset in datasets]
        sds = [summary.loc[(dataset, method), "std"] for dataset in datasets]
        ax.bar(x + offset, means, width, yerr=sds, capsize=4, label=method)

    for xpos, dataset in zip(x, datasets):
        baseline = df.loc[df["dataset"] == dataset, "external_baseline"].iloc[0]
        ax.hlines(
            baseline,
            xpos - 0.45,
            xpos + 0.45,
            colors="black",
            linestyles="--",
            linewidth=1.0,
        )
        full = df[(df["dataset"] == dataset) & (df["method"] == "Full")]["accuracy"]
        minus_c = df[(df["dataset"] == dataset) & (df["method"] == "-C")]["accuracy"]
        marker = p_value_marker(full, minus_c)
        if marker:
            y = max(full.mean() + full.std(), minus_c.mean() + minus_c.std()) + 0.035
            ax.plot([xpos - 1.5 * width, xpos + 1.5 * width], [y, y], color="black", linewidth=1)
            ax.text(xpos, y + 0.01, marker, ha="center", va="bottom")

    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Accuracy")
    ax.set_title("Ablation study across datasets")
    ax.legend(title="Method")
    ax.text(
        0.01,
        0.02,
        "Bars show mean accuracy; error bars show +/- 1 SD (n=5 seeds). Dashed lines: external baseline.",
        transform=ax.transAxes,
        fontsize=8,
        va="bottom",
    )

    fig.tight_layout()
    for ext in ("svg", "pdf", "png"):
        kwargs = {"dpi": 300} if ext == "png" else {}
        fig.savefig(OUT_DIR / f"baseline.{ext}", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
