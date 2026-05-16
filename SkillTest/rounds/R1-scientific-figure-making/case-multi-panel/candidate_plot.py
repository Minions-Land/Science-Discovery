import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures" / "data"
OUT = Path(__file__).resolve().parent

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
    "dark": "#272727",
    "mid": "#767676",
}


def apply_publication_style(font_size=7, axes_linewidth=1.0):
    plt.rcParams.update(
        {
            "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": font_size,
            "axes.labelsize": font_size,
            "axes.titlesize": font_size,
            "xtick.labelsize": font_size,
            "ytick.labelsize": font_size,
            "legend.fontsize": font_size,
            "axes.linewidth": axes_linewidth,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )


def finalize_figure(fig, basename):
    fig.savefig(OUT / f"{basename}.svg", bbox_inches="tight", pad_inches=0.06)
    fig.savefig(OUT / f"{basename}.pdf", bbox_inches="tight", pad_inches=0.06)
    fig.savefig(
        OUT / f"{basename}.png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.06,
        facecolor="white",
    )


def read_rows(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def mean_ci(values):
    arr = np.asarray(values, dtype=float)
    mean = arr.mean()
    sem = arr.std(ddof=1) / np.sqrt(len(arr))
    return mean, 1.96 * sem


def dose_summary():
    rows = read_rows(DATA / "multi-panel-A-dose.csv")
    grouped = {}
    for row in rows:
        key = (row["compound"], float(row["dose_uM"]))
        grouped.setdefault(key, []).append(float(row["response_pct"]))
    by_compound = {}
    for (compound, dose), vals in grouped.items():
        mean, ci = mean_ci(vals)
        by_compound.setdefault(compound, []).append((dose, mean, ci))
    return {compound: sorted(vals) for compound, vals in by_compound.items()}


def scatter_rows():
    rows = read_rows(DATA / "multi-panel-B-scatter.csv")
    return [
        (row["group"], float(row["measured_pK"]), float(row["predicted_pK"]))
        for row in rows
    ]


def time_summary():
    rows = read_rows(DATA / "multi-panel-C-timecourse.csv")
    grouped = {}
    for row in rows:
        key = (row["biomarker"], float(row["time_h"]))
        grouped.setdefault(key, []).append(float(row["value"]))
    by_biomarker = {}
    for (biomarker, time), vals in grouped.items():
        arr = np.asarray(vals, dtype=float)
        by_biomarker.setdefault(biomarker, []).append(
            (time, arr.mean(), arr.std(ddof=1) / np.sqrt(len(arr)))
        )
    return {biomarker: sorted(vals) for biomarker, vals in by_biomarker.items()}


def fraction_rows():
    rows = read_rows(DATA / "multi-panel-D-fraction.csv")
    grouped = {}
    for row in rows:
        grouped.setdefault(row["genotype"], []).append(float(row["fraction_responding"]))
    return grouped


def p_to_stars(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "n.s."


def normal_p_from_welch(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    if se == 0:
        return 1.0
    z = abs((a.mean() - b.mean()) / se)
    return math.erfc(z / math.sqrt(2.0))


def add_panel_label(ax, label):
    ax.text(
        -0.13,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=8,
        fontweight="bold",
        va="top",
        ha="left",
    )


def main():
    apply_publication_style(font_size=7, axes_linewidth=0.9)

    fig = plt.figure(figsize=(8.0, 6.2))
    gs = fig.add_gridspec(
        3,
        3,
        width_ratios=[2.0, 1.0, 1.0],
        height_ratios=[1.05, 1.05, 0.95],
        wspace=0.55,
        hspace=0.72,
    )
    ax_a = fig.add_subplot(gs[0:2, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    ax_d = fig.add_subplot(gs[2, :])
    ax_legend = fig.add_subplot(gs[1, 1:])
    ax_legend.set_axis_off()

    compound_colors = {"CompoundX": PALETTE["blue_main"], "CompoundY": PALETTE["neutral"]}
    for compound, vals in dose_summary().items():
        dose = np.array([v[0] for v in vals])
        mean = np.array([v[1] for v in vals])
        ci = np.array([v[2] for v in vals])
        color = compound_colors.get(compound, PALETTE["blue_secondary"])
        ax_a.plot(dose, mean, marker="o", markersize=3.2, lw=1.7, color=color, label=compound)
        ax_a.fill_between(dose, mean - ci, mean + ci, color=color, alpha=0.18, linewidth=0)
        half = mean.max() / 2
        ec50 = dose[np.argmin(np.abs(mean - half))]
        ax_a.axvline(ec50, color=color, linestyle=":", linewidth=0.9, alpha=0.85)
        ax_a.text(ec50, ax_a.get_ylim()[1] * 0.92, "EC50", rotation=90, color=color, va="top", ha="right")
    ax_a.set_xscale("log")
    ax_a.set_xlabel("Dose (uM)")
    ax_a.set_ylabel("Response (%)")
    ax_a.set_title("Dose response with 95% CI", loc="left", pad=3)
    ax_a.grid(axis="y", color="#E6E6E6", linewidth=0.5)
    add_panel_label(ax_a, "A")

    scatter = scatter_rows()
    group_colors = {"kinase": PALETTE["teal"], "GPCR": PALETTE["violet"]}
    lo = min(min(r[1], r[2]) for r in scatter) - 0.2
    hi = max(max(r[1], r[2]) for r in scatter) + 0.2
    for group in ("kinase", "GPCR"):
        x = np.array([r[1] for r in scatter if r[0] == group])
        y = np.array([r[2] for r in scatter if r[0] == group])
        ax_b.scatter(x, y, s=16, color=group_colors[group], alpha=0.75, label=group, edgecolor="none")
        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.array([lo, hi])
        ax_b.plot(x_line, slope * x_line + intercept, color=group_colors[group], linewidth=1.0)
        ax_b.text(0.04, 0.93 if group == "kinase" else 0.82, f"{group} slope={slope:.2f}", transform=ax_b.transAxes, color=group_colors[group])
    ax_b.plot([lo, hi], [lo, hi], color=PALETTE["mid"], linestyle="--", linewidth=0.9)
    ax_b.set_xlim(lo, hi)
    ax_b.set_ylim(lo, hi)
    ax_b.set_xlabel("Measured pK")
    ax_b.set_ylabel("Predicted pK")
    ax_b.set_title("Prediction calibration", loc="left", pad=3)
    add_panel_label(ax_b, "B")

    biomarker_colors = {"IL6": PALETTE["red_strong"], "TNFa": PALETTE["blue_secondary"], "IL10": PALETTE["green_3"]}
    for biomarker, vals in time_summary().items():
        time = np.array([v[0] for v in vals])
        mean = np.array([v[1] for v in vals])
        sem = np.array([v[2] for v in vals])
        color = biomarker_colors.get(biomarker, PALETTE["dark"])
        ax_c.errorbar(time, mean, yerr=sem, marker="o", markersize=3.0, lw=1.4, capsize=2.0, color=color, label=biomarker)
    ax_c.set_xlabel("Time (h)")
    ax_c.set_ylabel("Mean response")
    ax_c.set_title("Cytokine time course", loc="left", pad=3)
    ax_c.grid(axis="y", color="#E6E6E6", linewidth=0.5)
    add_panel_label(ax_c, "C")

    handles, labels = [], []
    for ax in (ax_a, ax_b, ax_c):
        h, lab = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(lab)
    ax_legend.legend(handles, labels, loc="center", ncol=4, handlelength=1.8, columnspacing=1.3)

    grouped = fraction_rows()
    genotypes = ["WT", "Het", "KO"]
    genotype_colors = {"WT": PALETTE["neutral"], "Het": PALETTE["green_2"], "KO": PALETTE["blue_main"]}
    x = np.arange(len(genotypes))
    means = [np.mean(grouped[g]) for g in genotypes]
    sems = [np.std(grouped[g], ddof=1) / np.sqrt(len(grouped[g])) for g in genotypes]
    bars = ax_d.bar(
        x,
        means,
        yerr=sems,
        capsize=3,
        color=[genotype_colors[g] for g in genotypes],
        edgecolor="black",
        linewidth=0.8,
        width=0.58,
    )
    rng = np.random.default_rng(7)
    for i, genotype in enumerate(genotypes):
        y = np.asarray(grouped[genotype], dtype=float)
        jitter = rng.uniform(-0.10, 0.10, len(y))
        ax_d.scatter(np.full(len(y), i) + jitter, y, s=15, color="white", edgecolor=PALETTE["dark"], linewidth=0.5, zorder=3)
    wt = grouped["WT"]
    y_base = max(max(v) for v in grouped.values()) + 0.045
    for offset, genotype in enumerate(["Het", "KO"]):
        i = genotypes.index(genotype)
        p = normal_p_from_welch(wt, grouped[genotype])
        y = y_base + offset * 0.055
        ax_d.plot([0, 0, i, i], [y - 0.012, y, y, y - 0.012], color=PALETTE["dark"], linewidth=0.8)
        ax_d.text(i / 2, y + 0.008, p_to_stars(p), ha="center", va="bottom")
    ax_d.set_xticks(x)
    ax_d.set_xticklabels(genotypes)
    ax_d.set_ylabel("Fraction responding")
    ax_d.set_ylim(0, y_base + 0.14)
    ax_d.set_title("Cell-resolution genotype rescue (n=8 mice/group)", loc="left", pad=3)
    ax_d.grid(axis="y", color="#E6E6E6", linewidth=0.5)
    add_panel_label(ax_d, "D")

    caption = (
        "Source data: panel A -> multi-panel-A-dose.csv; B -> multi-panel-B-scatter.csv; "
        "C -> multi-panel-C-timecourse.csv; D -> multi-panel-D-fraction.csv."
    )
    fig.text(0.02, 0.012, caption, ha="left", va="bottom", fontsize=6, color=PALETTE["dark"])

    finalize_figure(fig, "candidate")
    plt.close(fig)


if __name__ == "__main__":
    main()
