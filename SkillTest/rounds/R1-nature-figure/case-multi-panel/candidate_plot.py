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


DATA_DIR = Path("/Users/mjm/Skill/SkillTest/fixtures/figures/data")
OUT_DIR = Path(__file__).resolve().parent

PALETTE = {
    "signal": "#0F4D92",
    "signal_soft": "#B4C0E4",
    "neutral": "#767676",
    "neutral_light": "#D8D8D8",
    "accent": "#E4CCD8",
    "accent_dark": "#9A4D8E",
    "black": "#272727",
}


def sem(values):
    values = np.asarray(values, dtype=float)
    return values.std(ddof=1) / np.sqrt(len(values))


def ec50_from_curve(doses, responses):
    order = np.argsort(doses)
    doses = np.asarray(doses, dtype=float)[order]
    responses = np.asarray(responses, dtype=float)[order]
    target = 50.0
    for i in range(1, len(doses)):
        y0, y1 = responses[i - 1], responses[i]
        if (y0 <= target <= y1) or (y1 <= target <= y0):
            frac = (target - y0) / (y1 - y0)
            log_dose = np.log10(doses[i - 1]) + frac * (np.log10(doses[i]) - np.log10(doses[i - 1]))
            return 10 ** log_dose
    return doses[np.argmin(np.abs(responses - target))]


def add_panel_label(ax, label):
    ax.text(-0.14, 1.08, label, transform=ax.transAxes, fontsize=8, fontweight="bold", ha="left", va="bottom")


def sig_marker(wt, other):
    if stats is None:
        return ""
    p_value = stats.ttest_ind(wt, other, equal_var=False).pvalue
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "n.s."


def add_sig(ax, x1, x2, y, text):
    ax.plot([x1, x1, x2, x2], [y, y + 0.018, y + 0.018, y], color=PALETTE["black"], linewidth=0.7, clip_on=False)
    ax.text((x1 + x2) / 2, y + 0.022, text, ha="center", va="bottom", fontsize=7)


def main():
    dose = pd.read_csv(DATA_DIR / "multi-panel-A-dose.csv")
    scatter = pd.read_csv(DATA_DIR / "multi-panel-B-scatter.csv")
    timecourse = pd.read_csv(DATA_DIR / "multi-panel-C-timecourse.csv")
    fraction = pd.read_csv(DATA_DIR / "multi-panel-D-fraction.csv")

    fig = plt.figure(figsize=(180 / 25.4, 128 / 25.4), constrained_layout=True)
    gs = fig.add_gridspec(3, 4, height_ratios=[1.35, 0.95, 0.85], width_ratios=[1.2, 1.2, 1.0, 1.0])
    ax_a = fig.add_subplot(gs[0:2, 0:2])
    ax_b = fig.add_subplot(gs[0, 2])
    ax_c = fig.add_subplot(gs[0, 3])
    ax_d = fig.add_subplot(gs[1:, 2:])

    compound_colors = {"CompoundX": PALETTE["signal"], "CompoundY": PALETTE["neutral"]}
    for compound in ["CompoundX", "CompoundY"]:
        group = dose[dose["compound"] == compound]
        summary = group.groupby("dose_uM")["response_pct"].agg(["mean", sem]).reset_index()
        ci = 1.96 * summary["sem"]
        ax_a.plot(
            summary["dose_uM"],
            summary["mean"],
            color=compound_colors[compound],
            marker="o",
            markersize=3.2,
            linewidth=1.4,
            label=compound.replace("Compound", "Compound "),
        )
        ax_a.fill_between(
            summary["dose_uM"],
            summary["mean"] - ci,
            summary["mean"] + ci,
            color=compound_colors[compound],
            alpha=0.16,
            linewidth=0,
        )
        ec50 = ec50_from_curve(summary["dose_uM"], summary["mean"])
        ax_a.axvline(ec50, color=compound_colors[compound], linestyle=(0, (2, 2)), linewidth=0.8)
        ax_a.text(ec50, 5, f"EC50\n{ec50:.2g}", color=compound_colors[compound], ha="center", va="bottom", fontsize=5.7)
    ax_a.set_xscale("log")
    ax_a.set_xlabel("Dose (uM)")
    ax_a.set_ylabel("Response (%)")
    ax_a.set_ylim(0, 105)
    ax_a.legend(loc="upper left", handlelength=1.7)
    ax_a.tick_params(direction="out", length=2.5, width=0.7)
    add_panel_label(ax_a, "a")

    group_colors = {"kinase": PALETTE["signal_soft"], "GPCR": PALETTE["accent"]}
    for group_name in ["kinase", "GPCR"]:
        group = scatter[scatter["group"] == group_name]
        ax_b.scatter(
            group["measured_pK"],
            group["predicted_pK"],
            s=16,
            color=group_colors[group_name],
            edgecolor=PALETTE["black"],
            linewidth=0.35,
            label=group_name,
            alpha=0.95,
        )
        slope, intercept = np.polyfit(group["measured_pK"], group["predicted_pK"], 1)
        y_text = 0.96 if group_name == "kinase" else 0.86
        ax_b.text(0.04, y_text, f"{group_name} slope {slope:.2f}", transform=ax_b.transAxes, ha="left", va="top", fontsize=5.8)
    lo = min(scatter["measured_pK"].min(), scatter["predicted_pK"].min()) - 0.2
    hi = max(scatter["measured_pK"].max(), scatter["predicted_pK"].max()) + 0.2
    ax_b.plot([lo, hi], [lo, hi], color=PALETTE["neutral"], linestyle=(0, (2, 2)), linewidth=0.8)
    ax_b.set_xlim(lo, hi)
    ax_b.set_ylim(lo, hi)
    ax_b.set_xlabel("Measured pK")
    ax_b.set_ylabel("Predicted pK")
    ax_b.tick_params(direction="out", length=2.5, width=0.7)
    add_panel_label(ax_b, "b")

    biomarker_colors = {"IL6": PALETTE["signal"], "TNFa": PALETTE["accent_dark"], "IL10": PALETTE["neutral"]}
    for biomarker in ["IL6", "TNFa", "IL10"]:
        group = timecourse[timecourse["biomarker"] == biomarker]
        summary = group.groupby("time_h")["value"].agg(["mean", sem]).reset_index()
        ax_c.errorbar(
            summary["time_h"],
            summary["mean"],
            yerr=summary["sem"],
            color=biomarker_colors[biomarker],
            marker="o",
            markersize=3.0,
            linewidth=1.2,
            elinewidth=0.7,
            capsize=2,
            label=biomarker,
        )
    ax_c.set_xlabel("Time (h)")
    ax_c.set_ylabel("Cytokine value")
    ax_c.legend(loc="upper right", handlelength=1.3)
    ax_c.tick_params(direction="out", length=2.5, width=0.7)
    add_panel_label(ax_c, "c")

    genotypes = ["WT", "Het", "KO"]
    genotype_colors = {"WT": PALETTE["neutral_light"], "Het": PALETTE["accent"], "KO": PALETTE["signal"]}
    xpos = np.arange(len(genotypes))
    means = [fraction.loc[fraction["genotype"] == g, "fraction_responding"].mean() for g in genotypes]
    sds = [fraction.loc[fraction["genotype"] == g, "fraction_responding"].std() for g in genotypes]
    bars = ax_d.bar(
        xpos,
        means,
        yerr=sds,
        capsize=2.5,
        color=[genotype_colors[g] for g in genotypes],
        edgecolor=PALETTE["black"],
        linewidth=0.6,
        error_kw={"elinewidth": 0.7, "capthick": 0.7},
        width=0.62,
        zorder=2,
    )
    for bar, hatch in zip(bars, ["", "//", ""]):
        bar.set_hatch(hatch)
    rng = np.random.default_rng(9)
    for i, genotype in enumerate(genotypes):
        vals = fraction.loc[fraction["genotype"] == genotype, "fraction_responding"].to_numpy()
        jitter = rng.uniform(-0.07, 0.07, len(vals))
        ax_d.scatter(
            np.full(len(vals), i) + jitter,
            vals,
            s=13,
            color="white",
            edgecolor=PALETTE["black"],
            linewidth=0.45,
            zorder=4,
        )
    wt = fraction.loc[fraction["genotype"] == "WT", "fraction_responding"]
    y0 = 0.78
    for i, genotype in enumerate(["Het", "KO"], start=1):
        vals = fraction.loc[fraction["genotype"] == genotype, "fraction_responding"]
        add_sig(ax_d, 0, i, y0 + 0.075 * (i - 1), sig_marker(wt, vals))
    ax_d.set_xticks(xpos)
    ax_d.set_xticklabels(genotypes)
    ax_d.set_ylim(0, 1.0)
    ax_d.set_ylabel("Responding cells (fraction)")
    ax_d.tick_params(direction="out", length=2.5, width=0.7)
    add_panel_label(ax_d, "d")

    fig.text(
        0.01,
        -0.02,
        "Source columns: a, compound/dose_uM/response_pct; b, measured_pK/predicted_pK/group; "
        "c, biomarker/time_h/value; d, genotype/mouse/fraction_responding. "
        "Bands show 95% CI; error bars show SEM in c and SD in d; d tests are pairwise vs WT.",
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
