import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATA_DIR = "/Users/mjm/Skill/SkillTest/fixtures/figures-5panel/data"
OUT_DIR = "/Users/mjm/Skill/SkillTest/rounds/R4-5-panel-figure/case-pharma-pipeline"


def sem(x):
    x = np.asarray(x, dtype=float)
    return x.std(ddof=1) / np.sqrt(len(x))


def logistic4(x, top, bottom, ic50, hill=1.0):
    return bottom + (top - bottom) / (1 + (x / ic50) ** hill)


def add_panel_label(ax, label):
    ax.text(-0.12, 1.05, label, transform=ax.transAxes, fontweight="bold", va="bottom")


def main():
    a = pd.read_csv(os.path.join(DATA_DIR, "panel-A-efficacy.csv"))
    b = pd.read_csv(os.path.join(DATA_DIR, "panel-B-doseresponse.csv"))
    c = pd.read_csv(os.path.join(DATA_DIR, "panel-C-admet.csv"))
    d = pd.read_csv(os.path.join(DATA_DIR, "panel-D-engagement.csv"))
    e = pd.read_csv(os.path.join(DATA_DIR, "panel-E-safety.csv"))

    fig = plt.figure(figsize=(10, 7.5))
    gs = fig.add_gridspec(3, 3)
    ax_a = fig.add_subplot(gs[0:2, 0:2])
    ax_b = fig.add_subplot(gs[0, 2])
    ax_c = fig.add_subplot(gs[1, 2])
    ax_d = fig.add_subplot(gs[2, 0])
    ax_e = fig.add_subplot(gs[2, 1:3])

    # A: grouped bar
    cancer_types = list(a["cancer_type"].drop_duplicates())
    compounds = list(a["compound"].drop_duplicates())
    x = np.arange(len(cancer_types))
    width = 0.35
    for i, compound in enumerate(compounds):
        vals = []
        errs = []
        for cancer_type in cancer_types:
            y = a[(a["cancer_type"] == cancer_type) & (a["compound"] == compound)]["tumor_volume_reduction_pct"]
            vals.append(y.mean())
            errs.append(y.std(ddof=1))
        xpos = x + (i - 0.5) * width
        ax_a.bar(xpos, vals, width=width, yerr=errs, capsize=4, label=compound)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(cancer_types, rotation=20, ha="right")
    ax_a.set_ylabel("Tumour volume reduction (%)")
    ax_a.set_title("Efficacy")
    ax_a.legend()
    ymax = ax_a.get_ylim()[1]
    for xi in x:
        ax_a.text(xi, ymax * 0.92, "**", ha="center")
    add_panel_label(ax_a, "A")

    # B: dose-response
    doses = np.sort(b["dose_uM"].unique())
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for i, compound in enumerate(sorted(b["compound"].unique())):
        sub = b[b["compound"] == compound]
        means = sub.groupby("dose_uM")["viability_pct"].mean().reindex(doses)
        ax_b.plot(doses, means, marker="o", label=compound, color=colors[i % len(colors)])
        yvals = means.to_numpy()
        ic50 = np.interp(50, yvals[::-1], doses[::-1]) if yvals.min() <= 50 <= yvals.max() else doses[np.argmin(np.abs(yvals - 50))]
        ax_b.axvline(ic50, color=colors[i % len(colors)], alpha=0.25)
    ax_b.set_xscale("log")
    ax_b.set_xlabel("Dose (uM)")
    ax_b.set_ylabel("Viability (%)")
    ax_b.set_title("Dose response")
    ax_b.legend(fontsize=7)
    add_panel_label(ax_b, "B")

    # C: compact violin small multiples
    metrics = list(c["metric"].drop_duplicates())
    positions = np.arange(len(metrics))
    for j, compound in enumerate(sorted(c["compound"].unique())):
        data = [c[(c["compound"] == compound) & (c["metric"] == metric)]["value"].to_numpy() for metric in metrics]
        parts = ax_c.violinplot(data, positions=positions + (j - 1) * 0.22, widths=0.18, showmedians=True)
        for body in parts["bodies"]:
            body.set_alpha(0.35)
    ax_c.set_xticks(positions)
    ax_c.set_xticklabels(["CLint", "Vd", "F%", "t1/2"], rotation=25, ha="right")
    ax_c.set_ylabel("Value")
    ax_c.set_title("ADMET")
    add_panel_label(ax_c, "C")

    # D: engagement time course
    for treatment in d["treatment"].drop_duplicates():
        sub = d[d["treatment"] == treatment]
        stats = sub.groupby("time_h")["engagement_pct"].agg(["mean", sem]).reset_index()
        ax_d.errorbar(stats["time_h"], stats["mean"], yerr=stats["sem"], marker="o", capsize=3, label=treatment)
    ax_d.set_xlabel("Time (h)")
    ax_d.set_ylabel("Engagement (%)")
    ax_d.set_title("Target engagement")
    ax_d.legend()
    add_panel_label(ax_d, "D")

    # E: toxicity grouped bars
    organs = list(e["organ"].drop_duplicates())
    groups = list(e["group"].drop_duplicates())
    x = np.arange(len(organs))
    width = 0.25
    for i, group in enumerate(groups):
        means = []
        errs = []
        for organ in organs:
            y = e[(e["organ"] == organ) & (e["group"] == group)]["toxicity_score"]
            means.append(y.mean())
            errs.append(y.std(ddof=1))
        ax_e.bar(x + (i - 1) * width, means, width=width, yerr=errs, capsize=3, label=group)
    ax_e.set_xticks(x)
    ax_e.set_xticklabels(organs, rotation=25, ha="right")
    ax_e.set_ylabel("Toxicity score")
    ax_e.set_title("Safety")
    ax_e.legend()
    top = ax_e.get_ylim()[1]
    for xi in x:
        ax_e.text(xi + width, top * 0.91, "*", ha="center")
    add_panel_label(ax_e, "E")

    fig.tight_layout()
    base = os.path.join(OUT_DIR, "baseline")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".pdf")
    fig.savefig(base + ".png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
