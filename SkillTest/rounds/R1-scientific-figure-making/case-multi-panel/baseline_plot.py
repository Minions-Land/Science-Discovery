import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures" / "data"
OUT = Path(__file__).resolve().parent


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
    summary = {}
    for row in rows:
        key = (row["compound"], float(row["dose_uM"]))
        summary.setdefault(key, []).append(float(row["response_pct"]))
    by_compound = {}
    for (compound, dose), vals in summary.items():
        mean, ci = mean_ci(vals)
        by_compound.setdefault(compound, []).append((dose, mean, ci))
    return {k: sorted(v) for k, v in by_compound.items()}


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
    return {k: sorted(v) for k, v in by_biomarker.items()}


def fraction_rows():
    rows = read_rows(DATA / "multi-panel-D-fraction.csv")
    grouped = {}
    for row in rows:
        grouped.setdefault(row["genotype"], []).append(float(row["fraction_responding"]))
    return grouped


def main():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    ax_a, ax_b, ax_c, ax_d = axes.ravel()

    for compound, vals in dose_summary().items():
        dose = np.array([v[0] for v in vals])
        mean = np.array([v[1] for v in vals])
        ci = np.array([v[2] for v in vals])
        ax_a.plot(dose, mean, marker="o", label=compound)
        ax_a.fill_between(dose, mean - ci, mean + ci, alpha=0.2)
        half = mean.max() / 2
        ec50 = dose[np.argmin(np.abs(mean - half))]
        ax_a.axvline(ec50, linestyle="--", linewidth=1)
    ax_a.set_xscale("log")
    ax_a.set_xlabel("Dose (uM)")
    ax_a.set_ylabel("Response (%)")
    ax_a.set_title("A Dose response")
    ax_a.legend()

    scatter = scatter_rows()
    for group in sorted({r[0] for r in scatter}):
        x = np.array([r[1] for r in scatter if r[0] == group])
        y = np.array([r[2] for r in scatter if r[0] == group])
        ax_b.scatter(x, y, label=group)
    lo = min(min(r[1], r[2]) for r in scatter)
    hi = max(max(r[1], r[2]) for r in scatter)
    ax_b.plot([lo, hi], [lo, hi], "k--")
    ax_b.set_xlabel("Measured pK")
    ax_b.set_ylabel("Predicted pK")
    ax_b.set_title("B Predictions")
    ax_b.legend()

    for biomarker, vals in time_summary().items():
        time = np.array([v[0] for v in vals])
        mean = np.array([v[1] for v in vals])
        sem = np.array([v[2] for v in vals])
        ax_c.errorbar(time, mean, yerr=sem, marker="o", label=biomarker)
    ax_c.set_xlabel("Time (h)")
    ax_c.set_ylabel("Response")
    ax_c.set_title("C Biomarkers")
    ax_c.legend()

    grouped = fraction_rows()
    labels = list(grouped)
    means = [np.mean(grouped[label]) for label in labels]
    ax_d.bar(labels, means)
    for i, label in enumerate(labels):
        y = grouped[label]
        ax_d.scatter(np.full(len(y), i), y, color="k", s=20)
    ax_d.set_ylabel("Fraction responding")
    ax_d.set_title("D Genotype rescue")

    fig.tight_layout()
    for ext in ("svg", "pdf", "png"):
        fig.savefig(OUT / f"baseline.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    main()
