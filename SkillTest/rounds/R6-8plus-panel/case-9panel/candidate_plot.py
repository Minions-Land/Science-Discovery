#!/usr/bin/env python3
import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures-8plus" / "data"
OUT = Path(__file__).resolve().parent


PALETTE = {
    "compound": "#2563A9",
    "vehicle": "#5B6673",
    "support": "#2A8C82",
    "dose": "#D9772B",
    "accent": "#B8323B",
    "soft": "#E6EDF3",
}


def rows(name):
    with (DATA / name).open(newline="") as f:
        return list(csv.DictReader(f))


def mean_sem(values):
    arr = np.asarray(values, dtype=float)
    sem = arr.std(ddof=1) / math.sqrt(len(arr)) if len(arr) > 1 else 0
    return arr.mean(), sem


def label(ax, text):
    ax.text(-0.11, 1.055, text, transform=ax.transAxes, fontsize=8,
            fontweight="bold", va="top", ha="left")


def style(ax):
    ax.tick_params(labelsize=7, length=2.5, width=0.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for spine in ax.spines.values():
        spine.set_linewidth(0.6)


def panel_a(ax):
    data = rows("9p-A-efficacy.csv")
    cancers = list(dict.fromkeys(r["cancer_type"] for r in data))
    x = np.arange(len(cancers))
    width = 0.36
    for idx, compound in enumerate(["Vehicle", "CompoundX"]):
        means, sems = zip(*(mean_sem([float(r["tumor_volume_pct"]) for r in data
                                      if r["cancer_type"] == cancer and r["compound"] == compound])
                            for cancer in cancers))
        ax.bar(x + (idx - 0.5) * width, means, width, yerr=sems, capsize=2,
               color=PALETTE["vehicle"] if compound == "Vehicle" else PALETTE["compound"],
               label=compound, edgecolor="white", linewidth=0.5)
    ax.set_title("Tumour volume reduction", fontsize=8)
    ax.set_ylabel("Tumour volume (%)", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(cancers, rotation=25, ha="right")
    ax.legend(frameon=False, fontsize=7, ncol=2, loc="upper right")
    label(ax, "A")
    style(ax)


def panel_b(ax):
    data = rows("9p-B-doseresponse.csv")
    colors = [PALETTE["compound"], PALETTE["support"], PALETTE["dose"]]
    for color, compound in zip(colors, sorted(set(r["compound"] for r in data))):
        doses = sorted({float(r["dose_uM"]) for r in data if r["compound"] == compound})
        means = [mean_sem([float(r["viability_pct"]) for r in data
                           if r["compound"] == compound and float(r["dose_uM"]) == dose])[0]
                 for dose in doses]
        ax.plot(doses, means, marker="o", markersize=3, linewidth=1, color=color, label=compound)
    ax.set_xscale("log")
    ax.set_title("In vitro potency", fontsize=8)
    ax.set_xlabel("Dose (uM)", fontsize=7)
    ax.set_ylabel("Viability (%)", fontsize=7)
    ax.legend(frameon=False, fontsize=6, loc="lower left")
    label(ax, "B")
    style(ax)


def panel_c(ax):
    data = rows("9p-C-admet.csv")
    metrics = list(dict.fromkeys(r["metric"] for r in data))
    compounds = sorted(set(r["compound"] for r in data))
    positions, values, colors = [], [], []
    for mi, metric in enumerate(metrics):
        for ci, compound in enumerate(compounds):
            positions.append(mi * 4 + ci)
            values.append([float(r["value"]) for r in data
                           if r["metric"] == metric and r["compound"] == compound])
            colors.append([PALETTE["compound"], PALETTE["support"], PALETTE["dose"]][ci])
    parts = ax.violinplot(values, positions=positions, widths=0.72, showextrema=False)
    for body, color in zip(parts["bodies"], colors):
        body.set_facecolor(color)
        body.set_alpha(0.66)
        body.set_edgecolor("none")
    metric_labels = {"CL_int": "CL", "fu": "fu", "L_kg_pct": "L/kg"}
    ax.set_xticks([1, 5, 9])
    ax.set_xticklabels([metric_labels.get(m, m) for m in metrics], rotation=25, ha="right", fontsize=6)
    ax.set_title("ADMET profile", fontsize=8)
    ax.set_ylabel("Value", fontsize=7)
    ax.text(0.98, 0.95, "X1 X2 X3", transform=ax.transAxes, ha="right", va="top", fontsize=6)
    label(ax, "C")
    style(ax)


def panel_d(ax):
    data = rows("9p-D-engagement.csv")
    for treatment, color in [("CompoundX", PALETTE["compound"]), ("Vehicle", PALETTE["vehicle"])]:
        times = sorted({float(r["time_h"]) for r in data if r["treatment"] == treatment})
        means, sems = zip(*(mean_sem([float(r["engagement_pct"]) for r in data
                                      if r["treatment"] == treatment and float(r["time_h"]) == time])
                            for time in times))
        ax.errorbar(times, means, yerr=sems, marker="o", markersize=3, linewidth=1,
                    color=color, capsize=2, label=treatment)
    ax.set_title("Target engagement", fontsize=8)
    ax.set_xlabel("Time (h)", fontsize=7)
    ax.set_ylabel("Engagement (%)", fontsize=7)
    ax.legend(frameon=False, fontsize=6)
    label(ax, "D")
    style(ax)


def panel_e(ax):
    data = rows("9p-E-safety.csv")
    organs = list(dict.fromkeys(r["organ"] for r in data))
    groups = list(dict.fromkeys(r["group"] for r in data))
    x = np.arange(len(organs))
    width = 0.24
    for idx, group in enumerate(groups):
        means = [mean_sem([float(r["toxicity_score"]) for r in data
                           if r["organ"] == organ and r["group"] == group])[0]
                 for organ in organs]
        ax.bar(x + (idx - 1) * width, means, width,
               color=[PALETTE["vehicle"], PALETTE["support"], PALETTE["dose"]][idx],
               label=group)
    ax.set_title("Safety by organ", fontsize=8)
    ax.set_ylabel("Toxicity score", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(organs, rotation=25, ha="right")
    ax.legend(frameon=False, fontsize=5.2, loc="upper left", ncol=1)
    label(ax, "E")
    style(ax)


def km(times, events):
    order = np.argsort(times)
    times = np.asarray(times)[order]
    events = np.asarray(events)[order]
    at_risk = len(times)
    survival = 1.0
    xs, ys = [0], [1.0]
    for time, event in zip(times, events):
        xs.extend([time, time])
        next_survival = survival * (1 - event / at_risk)
        ys.extend([survival, next_survival])
        survival = next_survival
        at_risk -= 1
    return xs, ys


def panel_f(ax):
    data = rows("9p-F-survival.csv")
    for group, color in [("CompoundX", PALETTE["compound"]), ("Vehicle", PALETTE["vehicle"])]:
        subset = [r for r in data if r["group"] == group]
        xs, ys = km([float(r["time_days"]) for r in subset], [int(r["event"]) for r in subset])
        ax.step(xs, ys, where="post", linewidth=1.2, color=color, label=group)
    ax.set_title("Survival benefit", fontsize=8)
    ax.set_xlabel("Days", fontsize=7)
    ax.set_ylabel("Survival", fontsize=7)
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, fontsize=6)
    label(ax, "F")
    style(ax)


def panel_g(ax):
    data = rows("9p-G-correlation.csv")
    x = np.array([float(r["biomarker_X"]) for r in data])
    y = np.array([float(r["clinical_response_pct"]) for r in data])
    ax.scatter(x, y, s=12, color=PALETTE["support"], alpha=0.75, linewidth=0)
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 50)
    ax.plot(xx, slope * xx + intercept, color=PALETTE["accent"], linewidth=1)
    ax.set_title("Biomarker correlation", fontsize=8)
    ax.set_xlabel("Biomarker X", fontsize=7)
    ax.set_ylabel("Response (%)", fontsize=7)
    label(ax, "G")
    style(ax)


def panel_h(ax):
    data = rows("9p-H-biomarker.csv")
    for status, color in [("Responder", PALETTE["compound"]), ("Non-responder", PALETTE["dose"])]:
        weeks = sorted({float(r["week"]) for r in data if r["responder_status"] == status})
        means, sems = zip(*(mean_sem([float(r["biomarker_pct"]) for r in data
                                      if r["responder_status"] == status and float(r["week"]) == week])
                            for week in weeks))
        ax.errorbar(weeks, means, yerr=sems, marker="o", markersize=3, linewidth=1,
                    capsize=2, color=color, label=status)
    ax.set_title("Biomarker dynamics", fontsize=8)
    ax.set_xlabel("Week", fontsize=7)
    ax.set_ylabel("Biomarker (%)", fontsize=7)
    ax.legend(frameon=False, fontsize=6)
    label(ax, "H")
    style(ax)


def panel_i(ax):
    data = rows("9p-I-subset.csv")
    y = np.arange(len(data))[::-1]
    rates = np.array([float(r["response_rate"]) for r in data])
    lo = np.array([float(r["ci_lo"]) for r in data])
    hi = np.array([float(r["ci_hi"]) for r in data])
    ax.errorbar(rates, y, xerr=[rates - lo, hi - rates], fmt="o",
                color=PALETTE["compound"], ecolor=PALETTE["vehicle"],
                elinewidth=1, capsize=2, markersize=3)
    ax.axvline(rates[0], color=PALETTE["soft"], linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels([r["subset"] for r in data], fontsize=6)
    ax.set_xlim(0.15, 0.75)
    ax.set_title("Subset response", fontsize=8)
    ax.set_xlabel("Response rate", fontsize=7)
    label(ax, "I")
    style(ax)


def main():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "font.size": 7,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "axes.linewidth": 0.6,
    })
    # layout: gridspec(4, 4), hero=gs[0:2,0:2], contiguous remainder fills every cell.
    fig = plt.figure(figsize=(10.5, 12.5), constrained_layout=True)
    gs = fig.add_gridspec(4, 4, wspace=0.25, hspace=0.28)
    axes = {
        "A": fig.add_subplot(gs[0:2, 0:2]),
        "B": fig.add_subplot(gs[0, 2]),
        "C": fig.add_subplot(gs[0, 3]),
        "D": fig.add_subplot(gs[1, 2]),
        "E": fig.add_subplot(gs[1, 3]),
        "F": fig.add_subplot(gs[2, 0:2]),
        "G": fig.add_subplot(gs[2, 2:4]),
        "H": fig.add_subplot(gs[3, 0:2]),
        "I": fig.add_subplot(gs[3, 2:4]),
    }
    for key, func in zip("ABCDEFGHI", [panel_a, panel_b, panel_c, panel_d, panel_e, panel_f, panel_g, panel_h, panel_i]):
        func(axes[key])
    for ext in ("svg", "pdf", "png"):
        kwargs = {"dpi": 300} if ext == "png" else {}
        fig.savefig(OUT / f"candidate.{ext}", bbox_inches="tight", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
