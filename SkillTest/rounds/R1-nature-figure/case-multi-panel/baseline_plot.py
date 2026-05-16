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


DATA_DIR = Path("/Users/mjm/Skill/SkillTest/fixtures/figures/data")
OUT_DIR = Path(__file__).resolve().parent


def sem(values):
    values = np.asarray(values, dtype=float)
    return values.std(ddof=1) / np.sqrt(len(values))


def ec50_from_curve(doses, responses):
    order = np.argsort(doses)
    doses = np.asarray(doses)[order]
    responses = np.asarray(responses)[order]
    target = 50.0
    for i in range(1, len(doses)):
        low, high = responses[i - 1], responses[i]
        if (low <= target <= high) or (high <= target <= low):
            frac = (target - low) / (high - low)
            return doses[i - 1] + frac * (doses[i] - doses[i - 1])
    return doses[np.argmin(np.abs(responses - target))]


def add_sig(ax, x1, x2, y, text):
    ax.plot([x1, x1, x2, x2], [y, y + 0.015, y + 0.015, y], color="black", linewidth=1)
    ax.text((x1 + x2) / 2, y + 0.018, text, ha="center", va="bottom")


def marker_vs_wt(wt, other):
    if stats is None:
        return ""
    p_value = stats.ttest_ind(wt, other, equal_var=False).pvalue
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "n.s."


def main():
    dose = pd.read_csv(DATA_DIR / "multi-panel-A-dose.csv")
    scatter = pd.read_csv(DATA_DIR / "multi-panel-B-scatter.csv")
    timecourse = pd.read_csv(DATA_DIR / "multi-panel-C-timecourse.csv")
    fraction = pd.read_csv(DATA_DIR / "multi-panel-D-fraction.csv")

    fig = plt.figure(figsize=(11, 7))
    gs = fig.add_gridspec(2, 3, width_ratios=[2.0, 1.0, 1.0], height_ratios=[1.4, 1.0])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    ax_d = fig.add_subplot(gs[1, :])

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    compound_colors = {"CompoundX": colors[0], "CompoundY": colors[1]}
    for compound, group in dose.groupby("compound"):
        summary = group.groupby("dose_uM")["response_pct"].agg(["mean", sem]).reset_index()
        ci = 1.96 * summary["sem"]
        ax_a.plot(summary["dose_uM"], summary["mean"], marker="o", label=compound, color=compound_colors[compound])
        ax_a.fill_between(
            summary["dose_uM"],
            summary["mean"] - ci,
            summary["mean"] + ci,
            color=compound_colors[compound],
            alpha=0.2,
        )
        ec50 = ec50_from_curve(summary["dose_uM"], summary["mean"])
        ax_a.axvline(ec50, color=compound_colors[compound], linestyle="--", linewidth=1)
    ax_a.set_xscale("log")
    ax_a.set_xlabel("Dose (uM)")
    ax_a.set_ylabel("Response (%)")
    ax_a.set_title("A  Dose response")
    ax_a.legend()

    group_colors = {"kinase": colors[2], "GPCR": colors[3]}
    for group_name, group in scatter.groupby("group"):
        ax_b.scatter(group["measured_pK"], group["predicted_pK"], label=group_name, color=group_colors[group_name], alpha=0.8)
        slope, intercept = np.polyfit(group["measured_pK"], group["predicted_pK"], 1)
        x_pos = 0.05 if group_name == "kinase" else 0.05
        y_pos = 0.95 if group_name == "kinase" else 0.84
        ax_b.text(x_pos, y_pos, f"{group_name}: slope={slope:.2f}", transform=ax_b.transAxes, va="top")
    lo = min(scatter["measured_pK"].min(), scatter["predicted_pK"].min())
    hi = max(scatter["measured_pK"].max(), scatter["predicted_pK"].max())
    ax_b.plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=1)
    ax_b.set_xlabel("Measured pK")
    ax_b.set_ylabel("Predicted pK")
    ax_b.set_title("B  Prediction")
    ax_b.legend()

    for biomarker, group in timecourse.groupby("biomarker"):
        summary = group.groupby("time_h")["value"].agg(["mean", sem]).reset_index()
        ax_c.errorbar(summary["time_h"], summary["mean"], yerr=summary["sem"], marker="o", capsize=3, label=biomarker)
    ax_c.set_xlabel("Time (h)")
    ax_c.set_ylabel("Mean cytokine value")
    ax_c.set_title("C  Cytokines")
    ax_c.legend()

    genotypes = ["WT", "Het", "KO"]
    xpos = np.arange(len(genotypes))
    means = [fraction.loc[fraction["genotype"] == genotype, "fraction_responding"].mean() for genotype in genotypes]
    sds = [fraction.loc[fraction["genotype"] == genotype, "fraction_responding"].std() for genotype in genotypes]
    ax_d.bar(xpos, means, yerr=sds, capsize=4, color=colors[:3])
    rng = np.random.default_rng(3)
    for i, genotype in enumerate(genotypes):
        vals = fraction.loc[fraction["genotype"] == genotype, "fraction_responding"].to_numpy()
        ax_d.scatter(np.full_like(vals, i, dtype=float) + rng.uniform(-0.06, 0.06, len(vals)), vals, color="black", s=18)
    wt = fraction.loc[fraction["genotype"] == "WT", "fraction_responding"]
    y_base = max(means) + max(sds) + 0.03
    for i, genotype in enumerate(["Het", "KO"], start=1):
        vals = fraction.loc[fraction["genotype"] == genotype, "fraction_responding"]
        add_sig(ax_d, 0, i, y_base + (i - 1) * 0.07, marker_vs_wt(wt, vals))
    ax_d.set_xticks(xpos)
    ax_d.set_xticklabels(genotypes)
    ax_d.set_ylim(0, 1.0)
    ax_d.set_ylabel("Fraction responding")
    ax_d.set_title("D  Genotype rescue")

    fig.suptitle("Compound X discovery profile")
    fig.tight_layout()
    for ext in ("svg", "pdf", "png"):
        kwargs = {"dpi": 300} if ext == "png" else {}
        fig.savefig(OUT_DIR / f"baseline.{ext}", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
