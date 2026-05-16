import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams.update({
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.7,
    "legend.frameon": False,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
})

DATA_DIR = "/Users/mjm/Skill/SkillTest/fixtures/figures-5panel/data"
OUT_DIR = "/Users/mjm/Skill/SkillTest/rounds/R4-5-panel-figure/case-pharma-pipeline"

PALETTE = {
    "signal": "#0F4D92",
    "signal_soft": "#B4C0E4",
    "neutral": "#767676",
    "neutral_soft": "#D8D8D8",
    "neutral_dark": "#272727",
    "accent": "#42949E",
    "accent_2": "#9A4D8E",
    "warn": "#B64342",
    "low": "#E4CCD8",
}


def sem(x):
    x = np.asarray(x, dtype=float)
    return x.std(ddof=1) / np.sqrt(len(x))


def add_panel_label(ax, label, x=-0.11, y=1.04):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=8, fontweight="bold",
            ha="left", va="bottom")


def style_axis(ax):
    ax.tick_params(labelsize=7, pad=2)
    ax.grid(axis="y", color="#EAEAEA", linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)


def add_sig_bar(ax, x0, x1, y, text="**", h=1.6):
    ax.plot([x0, x0, x1, x1], [y, y + h, y + h, y], color=PALETTE["neutral_dark"], lw=0.6)
    ax.text((x0 + x1) / 2, y + h * 1.1, text, ha="center", va="bottom", fontsize=7)


def dose_ic50(doses, means):
    doses = np.asarray(doses, dtype=float)
    means = np.asarray(means, dtype=float)
    order = np.argsort(doses)
    doses = doses[order]
    means = means[order]
    if means.min() <= 50 <= means.max():
        return np.interp(50, means[::-1], doses[::-1])
    return doses[np.argmin(np.abs(means - 50))]


def save_figure(fig, base):
    fig.savefig(base + ".svg", bbox_inches="tight")
    fig.savefig(base + ".pdf", bbox_inches="tight")
    fig.savefig(base + ".png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    a = pd.read_csv(os.path.join(DATA_DIR, "panel-A-efficacy.csv"))
    b = pd.read_csv(os.path.join(DATA_DIR, "panel-B-doseresponse.csv"))
    c = pd.read_csv(os.path.join(DATA_DIR, "panel-C-admet.csv"))
    d = pd.read_csv(os.path.join(DATA_DIR, "panel-D-engagement.csv"))
    e = pd.read_csv(os.path.join(DATA_DIR, "panel-E-safety.csv"))

    # Contract: asymmetric mixed-modality quantitative figure; panel A is the
    # primary evidence, with B-E supporting potency, ADMET, PD, and safety.
    fig = plt.figure(figsize=(8.6, 6.8))
    gs = fig.add_gridspec(
        3, 4,
        width_ratios=[1.35, 1.35, 1.0, 1.0],
        height_ratios=[1.25, 1.25, 0.95],
        left=0.07, right=0.985, bottom=0.14, top=0.94,
        wspace=0.48, hspace=0.72,
    )
    ax_a = fig.add_subplot(gs[0:2, 0:2])
    ax_b = fig.add_subplot(gs[0, 2])
    ax_c = fig.add_subplot(gs[0, 3])
    ax_d = fig.add_subplot(gs[1, 2:4])
    ax_e = fig.add_subplot(gs[2, :])

    # A: hero efficacy panel
    cancer_types = list(a["cancer_type"].drop_duplicates())
    compounds = ["Vehicle", "CompoundX"]
    colors = {"Vehicle": PALETTE["neutral_soft"], "CompoundX": PALETTE["signal"]}
    x = np.arange(len(cancer_types))
    bar_w = 0.34
    for i, compound in enumerate(compounds):
        vals, errs = [], []
        for cancer_type in cancer_types:
            y = a[(a["cancer_type"] == cancer_type) & (a["compound"] == compound)]["tumor_volume_reduction_pct"]
            vals.append(y.mean())
            errs.append(y.std(ddof=1))
        xpos = x + (i - 0.5) * bar_w
        ax_a.bar(xpos, vals, yerr=errs, width=bar_w, color=colors[compound],
                 edgecolor=PALETTE["neutral_dark"], linewidth=0.45, capsize=2.5,
                 error_kw={"elinewidth": 0.6, "capthick": 0.6}, label=compound)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(cancer_types, rotation=15, ha="right")
    ax_a.set_ylabel("Tumour volume reduction (%)")
    ax_a.set_title("Antitumour efficacy across models", fontsize=8, loc="left", pad=3)
    ax_a.set_ylim(0, max(82, ax_a.get_ylim()[1]))
    for xi in x:
        add_sig_bar(ax_a, xi - bar_w / 2, xi + bar_w / 2, 73)
    ax_a.add_patch(plt.Rectangle((-0.06, 0.93), 0.028, 0.018, transform=ax_a.transAxes,
                                 color=PALETTE["neutral_soft"], ec=PALETTE["neutral_dark"],
                                 lw=0.4, clip_on=False))
    ax_a.add_patch(plt.Rectangle((-0.06, 0.885), 0.028, 0.018, transform=ax_a.transAxes,
                                 color=PALETTE["signal"], ec=PALETTE["neutral_dark"],
                                 lw=0.4, clip_on=False))
    ax_a.text(-0.025, 0.94, "Vehicle", transform=ax_a.transAxes, fontsize=7, va="center", clip_on=False)
    ax_a.text(-0.025, 0.895, "CompoundX", transform=ax_a.transAxes, fontsize=7, va="center", clip_on=False)
    add_panel_label(ax_a, "A", x=-0.08)
    style_axis(ax_a)

    # B: dose-response with compact direct labels
    compounds_b = sorted(b["compound"].unique())
    dose_colors = ["#0F4D92", "#3775BA", "#7884B4", "#42949E", "#9A4D8E", "#767676"]
    for color, compound in zip(dose_colors, compounds_b):
        sub = b[b["compound"] == compound]
        stats = sub.groupby("dose_uM")["viability_pct"].agg(["mean", sem]).reset_index()
        ic50 = dose_ic50(stats["dose_uM"], stats["mean"])
        ax_b.plot(stats["dose_uM"], stats["mean"], color=color, lw=1.1, marker="o",
                  ms=2.6)
        ax_b.fill_between(stats["dose_uM"], stats["mean"] - stats["sem"],
                          stats["mean"] + stats["sem"], color=color, alpha=0.10, linewidth=0)
        ax_b.axvline(ic50, color=color, lw=0.55, alpha=0.35)
    ax_b.axhline(50, color=PALETTE["neutral"], lw=0.5, ls=":")
    ax_b.set_xscale("log")
    ax_b.set_xlabel("Dose (uM)")
    ax_b.set_ylabel("Viability (%)")
    ax_b.set_title("In vitro potency", fontsize=8, loc="left", pad=3)
    label_x = b["dose_uM"].max() * 1.03
    label_y = {}
    last_points = []
    for color, compound in zip(dose_colors, compounds_b):
        sub = b[b["compound"] == compound]
        stats = sub.groupby("dose_uM")["viability_pct"].mean().reset_index()
        last_points.append((stats.sort_values("dose_uM")["viability_pct"].iloc[-1], compound, color))
    prev = -10
    for y_last, compound, color in sorted(last_points):
        y_text = max(y_last, prev + 5.0)
        label_y[compound] = y_text
        prev = y_text
    for y_last, compound, color in last_points:
        ax_b.text(label_x, label_y[compound], compound, color=color, fontsize=5.8, va="center", ha="left")
    ax_b.set_xlim(b["dose_uM"].min() * 0.8, b["dose_uM"].max() * 1.55)
    add_panel_label(ax_b, "B", x=-0.2)
    style_axis(ax_b)

    # C: ADMET small multiple violins in one compact axis
    metrics = list(c["metric"].drop_duplicates())
    metric_labels = ["CLint", "Vd", "F%", "t1/2"]
    c_compounds = ["X1", "X2", "X3"]
    xbase = np.arange(len(metrics))
    offsets = [-0.22, 0, 0.22]
    c_colors = [PALETTE["signal"], PALETTE["accent"], PALETTE["low"]]
    for offset, compound, color in zip(offsets, c_compounds, c_colors):
        values = [c[(c["compound"] == compound) & (c["metric"] == metric)]["value"].to_numpy()
                  for metric in metrics]
        parts = ax_c.violinplot(values, positions=xbase + offset, widths=0.18,
                                showmedians=True, showextrema=False)
        for body in parts["bodies"]:
            body.set_facecolor(color)
            body.set_edgecolor(PALETTE["neutral_dark"])
            body.set_linewidth(0.35)
            body.set_alpha(0.72)
        if "cmedians" in parts:
            parts["cmedians"].set_color(PALETTE["neutral_dark"])
            parts["cmedians"].set_linewidth(0.55)
    ax_c.set_xticks(xbase)
    ax_c.set_xticklabels(metric_labels, rotation=25, ha="right")
    ax_c.set_ylabel("Scaled assay value")
    ax_c.set_title("ADMET profile", fontsize=8, loc="left", pad=3)
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in c_colors]
    ax_c.legend(handles, c_compounds, loc="upper right", fontsize=5.8, handlelength=1)
    add_panel_label(ax_c, "C", x=-0.2)
    style_axis(ax_c)

    # D: target engagement
    for treatment, color in [("Vehicle", PALETTE["neutral"]), ("CompoundX", PALETTE["signal"])]:
        sub = d[d["treatment"] == treatment]
        stats = sub.groupby("time_h")["engagement_pct"].agg(["mean", sem]).reset_index()
        ax_d.errorbar(stats["time_h"], stats["mean"], yerr=stats["sem"], color=color,
                      lw=1.2, marker="o", ms=3.2, capsize=2.2,
                      elinewidth=0.6, capthick=0.6, label=treatment)
    ax_d.set_xlabel("Time after dose (h)")
    ax_d.set_ylabel("Target engagement (%)")
    ax_d.set_title("Pharmacodynamic target engagement", fontsize=8, loc="left", pad=3)
    ax_d.legend(loc="upper right", fontsize=7, handlelength=1.3)
    add_panel_label(ax_d, "D", x=-0.1)
    style_axis(ax_d)

    # E: full-width safety strip, kept wide because 15 bars would be cramped in a side column.
    organs = list(e["organ"].drop_duplicates())
    groups = ["Vehicle", "Low", "High"]
    e_colors = {"Vehicle": PALETTE["neutral_soft"], "Low": PALETTE["signal_soft"], "High": PALETTE["signal"]}
    x = np.arange(len(organs))
    bar_w = 0.23
    for i, group in enumerate(groups):
        vals, errs = [], []
        for organ in organs:
            y = e[(e["organ"] == organ) & (e["group"] == group)]["toxicity_score"]
            vals.append(y.mean())
            errs.append(y.std(ddof=1))
        xpos = x + (i - 1) * bar_w
        ax_e.bar(xpos, vals, width=bar_w, yerr=errs, color=e_colors[group],
                 edgecolor=PALETTE["neutral_dark"], linewidth=0.45, capsize=2.2,
                 error_kw={"elinewidth": 0.6, "capthick": 0.6}, label=group)
    ax_e.set_xticks(x)
    ax_e.set_xticklabels(organs)
    ax_e.set_ylabel("Toxicity score")
    ax_e.set_title("Tolerability across dose groups", fontsize=8, loc="left", pad=3)
    ax_e.legend(loc="upper left", bbox_to_anchor=(0.01, 0.98), fontsize=7, ncol=3, handlelength=1.1)
    ax_e.set_ylim(0, max(5.2, ax_e.get_ylim()[1]))
    for xi in x:
        add_sig_bar(ax_e, xi - bar_w, xi + bar_w, 4.55, text="*", h=0.14)
    add_panel_label(ax_e, "E", x=-0.035)
    style_axis(ax_e)

    caption = (
        "Source data: A cancer_type/compound/mouse/tumor_volume_reduction_pct; "
        "B compound/dose_uM/rep/viability_pct; C compound/metric/rep/value; "
        "D treatment/time_h/rep/engagement_pct; E organ/group/mouse/toxicity_score. "
        "Bars show mean +/- SD; time courses show mean +/- SEM; *P<0.05, **P<0.01."
    )
    fig.text(0.07, 0.035, caption, fontsize=6.2, color=PALETTE["neutral_dark"], ha="left", va="bottom")

    save_figure(fig, os.path.join(OUT_DIR, "candidate-nature-figure"))


if __name__ == "__main__":
    main()
