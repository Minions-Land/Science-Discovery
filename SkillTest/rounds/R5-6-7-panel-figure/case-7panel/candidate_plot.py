from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures-6-7panel" / "data"
OUT = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 7,
    "axes.titlesize": 8,
    "axes.labelsize": 7,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})

PALETTE = {
    "Vehicle": "#6f7785",
    "CompoundX": "#0072B2",
    "X1": "#0072B2",
    "X2": "#009E73",
    "X3": "#D55E00",
    "Low dose": "#8da0cb",
    "High dose": "#fc8d62",
}


def label(ax, s):
    ax.text(-0.13, 1.06, s, transform=ax.transAxes, fontsize=8,
            fontweight="bold", ha="left", va="top")


def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=2.5, width=0.7)


def grouped(df, cols, val):
    return df.groupby(cols)[val].agg(["mean", "std", "sem"]).reset_index()


def panel_a(ax):
    df = pd.read_csv(DATA / "6panel-A-efficacy.csv")
    stat = grouped(df, ["cancer_type", "compound"], "tumor_volume_pct")
    types = list(stat["cancer_type"].drop_duplicates())
    compounds = ["Vehicle", "CompoundX"]
    x = np.arange(len(types))
    w = 0.34
    for i, compound in enumerate(compounds):
        sub = stat[stat["compound"] == compound].set_index("cancer_type").loc[types]
        ax.bar(x + (i - 0.5) * w, sub["mean"], w, yerr=sub["std"], capsize=2.5,
               color=PALETTE.get(compound), edgecolor="black", linewidth=0.4,
               label=compound)
    ax.set_xticks(x)
    ax.set_xticklabels(types, rotation=18, ha="right")
    ax.set_ylabel("Tumour volume (%)")
    ax.set_title("Antitumour efficacy")
    ymax = stat["mean"].max() + stat["std"].max() + 10
    ax.set_ylim(0, ymax)
    for xi in x:
        ax.text(xi, ymax - 5, "**", ha="center", fontsize=8)
    ax.legend(loc="upper left", frameon=False, ncol=2, handlelength=1.2)
    label(ax, "A")
    despine(ax)


def panel_b(ax):
    df = pd.read_csv(DATA / "6panel-B-doseresponse.csv")
    for compound, sub in df.groupby("compound"):
        stat = sub.groupby("dose_uM")["viability_pct"].agg(["mean", "sem"]).reset_index()
        ax.errorbar(stat["dose_uM"], stat["mean"], yerr=stat["sem"], marker="o",
                    markersize=3, linewidth=1.2, capsize=2,
                    color=PALETTE.get(compound), label=compound)
    ax.axhline(50, color="#9a9a9a", linewidth=0.7, linestyle="--")
    ax.set_xscale("log")
    ax.set_xlabel("Dose (uM)")
    ax.set_ylabel("Viability (%)")
    ax.set_title("In vitro potency")
    ax.legend(frameon=False, ncol=3, handlelength=1)
    label(ax, "B")
    despine(ax)


def panel_c(ax):
    df = pd.read_csv(DATA / "6panel-C-admet.csv")
    metrics = list(df["metric"].drop_duplicates())
    positions = np.arange(len(metrics))
    data = [df[df["metric"] == metric]["value"].to_numpy() for metric in metrics]
    parts = ax.violinplot(data, positions=positions, widths=0.7, showmeans=False,
                          showmedians=True)
    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(["#0072B2", "#009E73", "#D55E00"][i % 3])
        body.set_edgecolor("black")
        body.set_alpha(0.45)
        body.set_linewidth(0.5)
    for key in ("cbars", "cmins", "cmaxes", "cmedians"):
        parts[key].set_color("#333333")
        parts[key].set_linewidth(0.7)
    ax.set_xticks(positions)
    ax.set_xticklabels(metrics)
    ax.set_ylabel("Value")
    ax.set_title("ADMET profile")
    label(ax, "C")
    despine(ax)


def panel_d(ax):
    df = pd.read_csv(DATA / "6panel-D-engagement.csv")
    for treatment, sub in df.groupby("treatment"):
        stat = sub.groupby("time_h")["engagement_pct"].agg(["mean", "sem"]).reset_index()
        ax.errorbar(stat["time_h"], stat["mean"], yerr=stat["sem"], marker="o",
                    markersize=3, linewidth=1.2, capsize=2,
                    color=PALETTE.get(treatment, "#009E73"), label=treatment)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Engagement (%)")
    ax.set_title("Target engagement")
    ax.legend(frameon=False, loc="lower right")
    label(ax, "D")
    despine(ax)


def panel_e(ax):
    df = pd.read_csv(DATA / "6panel-E-safety.csv")
    stat = grouped(df, ["organ", "group"], "toxicity_score")
    organs = list(stat["organ"].drop_duplicates())
    groups = list(stat["group"].drop_duplicates())
    x = np.arange(len(organs))
    w = 0.22
    for i, group in enumerate(groups):
        sub = stat[stat["group"] == group].set_index("organ").loc[organs]
        ax.bar(x + (i - 1) * w, sub["mean"], w, yerr=sub["std"], capsize=1.8,
               color=PALETTE.get(group, "#b0b0b0"), edgecolor="black",
               linewidth=0.35, label=group)
    ax.set_xticks(x)
    ax.set_xticklabels(organs, rotation=15, ha="right")
    ax.set_ylabel("Toxicity score")
    ax.set_title("Multi-organ safety")
    ax.legend(frameon=False, ncol=3, handlelength=1)
    label(ax, "E")
    despine(ax)


def panel_f(ax):
    df = pd.read_csv(DATA / "6panel-F-survival.csv")
    for group, sub in df.groupby("group"):
        times = np.sort(sub["time_days"].to_numpy())
        surv = 1 - np.arange(1, len(times) + 1) / len(times)
        ax.step(np.r_[0, times], np.r_[1, surv], where="post",
                linewidth=1.35, color=PALETTE.get(group), label=group)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Days")
    ax.set_ylabel("Survival")
    ax.set_title("Survival benefit")
    ax.legend(frameon=False, loc="lower left")
    label(ax, "F")
    despine(ax)


def panel_g(ax):
    df = pd.read_csv(DATA / "7panel-G-correlation.csv")
    x = df["biomarker_X"].to_numpy()
    y = df["clinical_response_pct"].to_numpy()
    ax.scatter(x, y, s=13, color="#7E57C2", alpha=0.65, edgecolor="none")
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 160)
    yy = slope * xx + intercept
    resid = y - (slope * x + intercept)
    se = np.sqrt(np.sum(resid ** 2) / (len(x) - 2))
    ci = 1.96 * se * np.sqrt(1 / len(x) + (xx - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2))
    ax.plot(xx, yy, color="#4A148C", linewidth=1.2)
    ax.fill_between(xx, yy - ci, yy + ci, color="#7E57C2", alpha=0.16, linewidth=0)
    r = np.corrcoef(x, y)[0, 1]
    ax.text(0.05, 0.9, f"r={r:.2f}, n={len(x)}", transform=ax.transAxes)
    ax.set_xlabel("Biomarker X")
    ax.set_ylabel("Clinical response (%)")
    ax.set_title("Clinical correlate")
    label(ax, "G")
    despine(ax)


def main():
    # Skill-applied layout: 4-cell A hero, contiguous two-cell remainder, no empty cells.
    fig = plt.figure(figsize=(7.9, 7.0), constrained_layout=True)
    gs = fig.add_gridspec(
        4, 4,
        width_ratios=[1.25, 1.25, 1.0, 1.0],
        height_ratios=[1.25, 1.25, 1.0, 1.0],
    )
    axes = {
        "A": fig.add_subplot(gs[0:2, 0:2]),
        "B": fig.add_subplot(gs[0, 2:4]),
        "C": fig.add_subplot(gs[1, 2:4]),
        "D": fig.add_subplot(gs[2, 0:2]),
        "E": fig.add_subplot(gs[2, 2:4]),
        "F": fig.add_subplot(gs[3, 0:2]),
        "G": fig.add_subplot(gs[3, 2:4]),
    }
    panel_a(axes["A"])
    panel_b(axes["B"])
    panel_c(axes["C"])
    panel_d(axes["D"])
    panel_e(axes["E"])
    panel_f(axes["F"])
    panel_g(axes["G"])
    for ext in ("svg", "pdf", "png"):
        fig.savefig(OUT / f"candidate.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    main()
