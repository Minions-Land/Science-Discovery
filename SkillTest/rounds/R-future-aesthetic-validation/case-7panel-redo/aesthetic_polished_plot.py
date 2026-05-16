from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures-6-7panel" / "data"
OUT = Path(__file__).resolve().parent

HAS_ARIAL = any("Arial" in f.name for f in font_manager.fontManager.ttflist)
FONT = "Arial" if HAS_ARIAL else "DejaVu Sans"

plt.rcParams.update({
    "font.family": FONT,
    "font.size": 7,
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 6,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "xtick.major.size": 2.4,
    "ytick.major.size": 2.4,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

COL = {
    "ink": "#404040",
    "axis": "#6a6a6a",
    "tick": "#959595",
    "grid": "#c0c0c0",
    "pale": "#eaeaea",
    "vehicle": "#6f7680",
    "light_grey": "#c0c0c0",
    "signal": "#c04040",
    "signal_soft": "#ea9595",
    "blue": "#406a95",
    "blue_soft": "#c0c0ea",
    "cyan": "#62bdb3",
}

PALETTE = {
    "Vehicle": COL["vehicle"],
    "CompoundX": COL["signal"],
    "X1": COL["signal"],
    "X2": COL["blue"],
    "X3": COL["light_grey"],
    "Low": COL["light_grey"],
    "High": COL["signal"],
}


def grouped(df, cols, val):
    return df.groupby(cols)[val].agg(["mean", "std", "sem"]).reset_index()


def label(ax, s):
    ax.text(-0.12, 1.07, s, transform=ax.transAxes, fontsize=9,
            fontweight="bold", color=COL["ink"], ha="left", va="top")


def style_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(COL["ink"])
        ax.spines[side].set_linewidth(0.7)
    ax.tick_params(colors=COL["tick"], labelcolor=COL["ink"], pad=2)
    ax.xaxis.label.set_color(COL["ink"])
    ax.yaxis.label.set_color(COL["ink"])
    ax.title.set_color(COL["ink"])


def add_panel_note(ax, text, x=0.02, y=0.03, ha="left"):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=5.5,
            color=COL["axis"], ha=ha, va="bottom", clip_on=False)


def panel_a(ax):
    df = pd.read_csv(DATA / "6panel-A-efficacy.csv")
    stat = grouped(df, ["cancer_type", "compound"], "tumor_volume_pct")
    types = ["CRC", "Glioma", "Melanoma", "NSCLC"]
    compounds = ["Vehicle", "CompoundX"]
    x = np.arange(len(types))
    w = 0.32
    for i, compound in enumerate(compounds):
        sub = stat[stat["compound"] == compound].set_index("cancer_type").loc[types]
        ax.bar(x + (i - 0.5) * w, sub["mean"], w, yerr=sub["sem"], capsize=2,
               color=PALETTE[compound], edgecolor=COL["ink"], linewidth=0.45,
               error_kw={"elinewidth": 0.75, "ecolor": COL["ink"]},
               label=compound)
    ytop = (stat["mean"] + stat["sem"]).max() + 7
    ax.set_ylim(0, ytop)
    for xi, cancer in enumerate(types):
        ymax = stat[stat["cancer_type"] == cancer]["mean"].max() + 4.4
        ax.plot([xi - 0.16, xi - 0.16, xi + 0.16, xi + 0.16],
                [ymax - 1.2, ymax, ymax, ymax - 1.2],
                color=COL["axis"], linewidth=0.65)
        ax.text(xi, ymax + 0.7, "**", ha="center", va="bottom",
                fontsize=7.5, fontweight="bold", color=COL["ink"])
    ax.set_xticks(x)
    ax.set_xticklabels(types, rotation=0)
    ax.set_ylabel("Tumour volume (%)")
    ax.set_title("Antitumour efficacy", fontweight="bold", pad=5)
    ax.legend(loc="upper left", frameon=False, ncol=2, handlelength=1.1,
              borderaxespad=0.1, labelcolor=COL["ink"])
    add_panel_note(ax, "mean +/- s.e.m.; n = 6 mice per group", y=-0.115)
    label(ax, "A")
    style_axis(ax)


def ec50_x(stat):
    x = stat["dose_uM"].to_numpy()
    y = stat["mean"].to_numpy()
    order = np.argsort(x)
    x, y = x[order], y[order]
    for i in range(len(x) - 1):
        if (y[i] - 50) * (y[i + 1] - 50) <= 0:
            lx0, lx1 = np.log10(x[i]), np.log10(x[i + 1])
            frac = (50 - y[i]) / (y[i + 1] - y[i])
            return 10 ** (lx0 + frac * (lx1 - lx0))
    return np.nan


def panel_b(ax):
    df = pd.read_csv(DATA / "6panel-B-doseresponse.csv")
    for compound, sub in df.groupby("compound"):
        stat = sub.groupby("dose_uM")["viability_pct"].agg(["mean", "sem"]).reset_index()
        color = PALETTE[compound]
        ax.errorbar(stat["dose_uM"], stat["mean"], yerr=stat["sem"], marker="o",
                    markersize=2.8, linewidth=1.15, capsize=1.8,
                    color=color, label=compound)
        ec50 = ec50_x(stat)
        if np.isfinite(ec50):
            ax.plot([ec50, ec50], [46.5, 53.5], color=color, linewidth=0.65)
            y_label = {"X1": 58.5, "X2": 55.0, "X3": 51.5}[compound]
            ax.text(ec50 * 1.08, y_label, f"{compound} EC50", fontsize=6.5,
                    color=color, ha="left", va="center")
    ax.axhline(50, color=COL["grid"], linewidth=0.7, linestyle="--", zorder=0)
    ax.set_xscale("log")
    ax.set_ylim(-3, 106)
    ax.set_xlabel("Dose (uM)")
    ax.set_ylabel("Viability (%)")
    ax.set_title("In vitro potency", fontweight="bold", pad=4)
    ax.legend(frameon=False, loc="upper right", ncol=3, handlelength=1,
              borderaxespad=0.1, labelcolor=COL["ink"])
    label(ax, "B")
    style_axis(ax)


def panel_c(ax):
    df = pd.read_csv(DATA / "6panel-C-admet.csv")
    metrics = list(df["metric"].drop_duplicates())
    positions = np.arange(len(metrics))
    data = [df[df["metric"] == metric]["value"].to_numpy() for metric in metrics]
    parts = ax.violinplot(data, positions=positions, widths=0.72, showmeans=False,
                          showmedians=True)
    fills = [COL["blue_soft"], COL["cyan"], COL["signal_soft"]]
    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(fills[i])
        body.set_edgecolor(COL["axis"])
        body.set_alpha(0.72)
        body.set_linewidth(0.65)
    for key in ("cbars", "cmins", "cmaxes", "cmedians"):
        parts[key].set_color(COL["ink"])
        parts[key].set_linewidth(0.65)
    ax.set_xticks(positions)
    ax.set_xticklabels(["CLint", "Vd", "F"])
    ax.set_ylabel("Value")
    ax.set_title("ADMET profile", fontweight="bold", pad=4)
    label(ax, "C")
    style_axis(ax)


def panel_d(ax):
    df = pd.read_csv(DATA / "6panel-D-engagement.csv")
    for treatment, sub in df.groupby("treatment"):
        stat = sub.groupby("time_h")["engagement_pct"].agg(["mean", "sem"]).reset_index()
        color = PALETTE.get(treatment, COL["vehicle"])
        ax.errorbar(stat["time_h"], stat["mean"], yerr=stat["sem"], marker="o",
                    markersize=2.8, linewidth=1.15, capsize=1.8,
                    color=color)
        y_frac = 0.16 if treatment == "Vehicle" else 0.33
        ax.text(0.76, y_frac, treatment, transform=ax.transAxes,
                fontsize=6.5, color=color, ha="left", va="center")
    ax.set_xlim(-0.6, 25.8)
    ax.set_ylim(0, 88)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Engagement (%)")
    ax.set_title("Target engagement", fontweight="bold", pad=4)
    label(ax, "D")
    style_axis(ax)


def panel_e(ax):
    df = pd.read_csv(DATA / "6panel-E-safety.csv")
    stat = grouped(df, ["organ", "group"], "toxicity_score")
    organs = list(stat["organ"].drop_duplicates())
    groups = ["Vehicle", "Low", "High"]
    x = np.arange(len(organs))
    w = 0.21
    offsets = {"Vehicle": -w, "Low": 0, "High": w}
    for group in groups:
        sub = stat[stat["group"] == group].set_index("organ").loc[organs]
        ax.bar(x + offsets[group], sub["mean"], w, yerr=sub["sem"], capsize=1.6,
               color=PALETTE[group], edgecolor=COL["ink"], linewidth=0.35,
               error_kw={"elinewidth": 0.65, "ecolor": COL["ink"]},
               label=group)
    ax.set_xticks(x)
    ax.set_xticklabels(organs, rotation=12, ha="right")
    ax.set_ylim(0, (stat["mean"] + stat["sem"]).max() + 0.22)
    ax.set_ylabel("Toxicity score")
    ax.set_title("Multi-organ safety", fontweight="bold", pad=4)
    ax.legend(frameon=False, loc="upper left", ncol=3, handlelength=1,
              borderaxespad=0.1, labelcolor=COL["ink"])
    label(ax, "E")
    style_axis(ax)


def panel_f(ax):
    df = pd.read_csv(DATA / "6panel-F-survival.csv")
    for group, sub in df.groupby("group"):
        times = np.sort(sub["time_days"].to_numpy())
        surv = 1 - np.arange(1, len(times) + 1) / len(times)
        color = PALETTE.get(group, COL["vehicle"])
        ax.step(np.r_[0, times], np.r_[1, surv], where="post",
                linewidth=1.25, color=color)
        ax.text(times[-1] + 1.0, surv[-1] + 0.03, group, fontsize=6.5,
                color=color, va="center")
    ax.set_xlim(-2, 92)
    ax.set_ylim(-0.02, 1.04)
    ax.set_xlabel("Days")
    ax.set_ylabel("Survival")
    ax.set_title("Survival benefit", fontweight="bold", pad=4)
    add_panel_note(ax, "Kaplan-Meier estimate", y=0.06)
    label(ax, "F")
    style_axis(ax)


def panel_g(ax):
    df = pd.read_csv(DATA / "7panel-G-correlation.csv")
    x = df["biomarker_X"].to_numpy()
    y = df["clinical_response_pct"].to_numpy()
    ax.scatter(x, y, s=12, color=COL["blue"], alpha=0.48, edgecolor="none")
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 160)
    yy = slope * xx + intercept
    resid = y - (slope * x + intercept)
    se = np.sqrt(np.sum(resid ** 2) / (len(x) - 2))
    ci = 1.96 * se * np.sqrt(1 / len(x) + (xx - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2))
    ax.plot(xx, yy, color=COL["blue"], linewidth=1.2)
    ax.fill_between(xx, yy - ci, yy + ci, color=COL["blue_soft"], alpha=0.55, linewidth=0)
    r = np.corrcoef(x, y)[0, 1]
    ax.text(0.04, 0.92, f"r = {r:.2f}", transform=ax.transAxes,
            fontsize=6.5, color=COL["blue"], ha="left", va="top")
    ax.set_xlim(x.min() - 3, x.max() + 3)
    ax.set_ylim(y.min() - 3, y.max() + 4)
    ax.set_xlabel("Biomarker X")
    ax.set_ylabel("Clinical response (%)")
    ax.set_title("Clinical correlate", fontweight="bold", pad=4)
    add_panel_note(ax, f"n = {len(x)} samples", y=0.05)
    label(ax, "G")
    style_axis(ax)


def main():
    fig = plt.figure(figsize=(9.2, 6.9))
    gs = fig.add_gridspec(
        3, 4,
        width_ratios=[1.35, 1.35, 1.0, 1.0],
        height_ratios=[1.30, 1.30, 1.0],
        wspace=0.27,
        hspace=0.46,
    )
    top_right = gs[0:2, 2:4].subgridspec(2, 2, wspace=0.34, hspace=0.44)
    axes = {
        "A": fig.add_subplot(gs[0:2, 0:2]),
        "B": fig.add_subplot(top_right[0, :]),
        "C": fig.add_subplot(top_right[1, 0]),
        "D": fig.add_subplot(top_right[1, 1]),
        "F": fig.add_subplot(gs[2, 0]),
        "G": fig.add_subplot(gs[2, 1]),
        "E": fig.add_subplot(gs[2, 2:4]),
    }
    panel_a(axes["A"])
    panel_b(axes["B"])
    panel_c(axes["C"])
    panel_d(axes["D"])
    panel_f(axes["F"])
    panel_g(axes["G"])
    panel_e(axes["E"])

    fig.subplots_adjust(left=0.065, right=0.987, bottom=0.075, top=0.955)
    for ext in ("svg", "pdf", "png"):
        fig.savefig(OUT / f"aesthetic_polished.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    main()
