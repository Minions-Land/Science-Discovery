from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures-6-7panel" / "data"
OUT = Path(__file__).resolve().parent


def panel_label(ax, label):
    ax.text(-0.16, 1.08, label, transform=ax.transAxes, fontweight="bold",
            fontsize=10, va="top", ha="left")


def mean_sd(df, group_cols, value_col):
    return df.groupby(group_cols)[value_col].agg(["mean", "std"]).reset_index()


def plot_a(ax):
    df = pd.read_csv(DATA / "6panel-A-efficacy.csv")
    s = mean_sd(df, ["cancer_type", "compound"], "tumor_volume_pct")
    types = list(s["cancer_type"].drop_duplicates())
    compounds = ["Vehicle", "CompoundX"]
    x = np.arange(len(types))
    width = 0.36
    for i, compound in enumerate(compounds):
        sub = s[s["compound"] == compound].set_index("cancer_type").loc[types]
        ax.bar(x + (i - 0.5) * width, sub["mean"], width, yerr=sub["std"],
               capsize=3, label=compound)
    ax.set_xticks(x)
    ax.set_xticklabels(types, rotation=25, ha="right")
    ax.set_ylabel("Tumour volume (%)")
    ax.set_title("A. Antitumour efficacy")
    ax.legend(frameon=False, fontsize=8)
    ymax = s["mean"].max() + s["std"].max() + 12
    ax.set_ylim(0, ymax)
    for xi in x:
        ax.text(xi, ymax - 6, "**", ha="center", va="bottom", fontsize=11)
    panel_label(ax, "A")


def plot_b(ax):
    df = pd.read_csv(DATA / "6panel-B-doseresponse.csv")
    for compound, sub in df.groupby("compound"):
        stat = sub.groupby("dose_uM")["viability_pct"].agg(["mean", "std"]).reset_index()
        ax.errorbar(stat["dose_uM"], stat["mean"], yerr=stat["std"], marker="o",
                    linewidth=1.5, capsize=2, label=compound)
    ax.set_xscale("log")
    ax.set_xlabel("Dose (uM)")
    ax.set_ylabel("Viability (%)")
    ax.set_title("B. In vitro potency")
    ax.legend(frameon=False, fontsize=7)
    panel_label(ax, "B")


def plot_c(ax):
    df = pd.read_csv(DATA / "6panel-C-admet.csv")
    metrics = list(df["metric"].drop_duplicates())
    positions = np.arange(1, len(metrics) + 1)
    data = [df[df["metric"] == m]["value"].to_numpy() for m in metrics]
    parts = ax.violinplot(data, positions=positions, widths=0.75, showmeans=True)
    for body in parts["bodies"]:
        body.set_alpha(0.45)
    ax.set_xticks(positions)
    ax.set_xticklabels(metrics)
    ax.set_ylabel("Value")
    ax.set_title("C. ADMET profile")
    panel_label(ax, "C")


def plot_d(ax):
    df = pd.read_csv(DATA / "6panel-D-engagement.csv")
    for treatment, sub in df.groupby("treatment"):
        stat = sub.groupby("time_h")["engagement_pct"].agg(["mean", "sem"]).reset_index()
        ax.errorbar(stat["time_h"], stat["mean"], yerr=stat["sem"], marker="o",
                    linewidth=1.5, capsize=2, label=treatment)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Engagement (%)")
    ax.set_title("D. Engagement")
    ax.legend(frameon=False, fontsize=7)
    panel_label(ax, "D")


def plot_e(ax):
    df = pd.read_csv(DATA / "6panel-E-safety.csv")
    stat = mean_sd(df, ["organ", "group"], "toxicity_score")
    organs = list(stat["organ"].drop_duplicates())
    groups = list(stat["group"].drop_duplicates())
    x = np.arange(len(organs))
    width = 0.24
    for i, group in enumerate(groups):
        sub = stat[stat["group"] == group].set_index("organ").loc[organs]
        ax.bar(x + (i - 1) * width, sub["mean"], width, yerr=sub["std"],
               capsize=2, label=group)
    ax.set_xticks(x)
    ax.set_xticklabels(organs, rotation=25, ha="right")
    ax.set_ylabel("Toxicity")
    ax.set_title("E. Safety")
    ax.legend(frameon=False, fontsize=6, ncol=1)
    panel_label(ax, "E")


def plot_f(ax):
    df = pd.read_csv(DATA / "6panel-F-survival.csv")
    for group, sub in df.groupby("group"):
        times = np.sort(sub["time_days"].to_numpy())
        surv = 1 - np.arange(1, len(times) + 1) / len(times)
        ax.step(np.r_[0, times], np.r_[1, surv], where="post", label=group)
    ax.set_xlabel("Days")
    ax.set_ylabel("Survival")
    ax.set_title("F. Survival")
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, fontsize=7)
    panel_label(ax, "F")


def plot_g(ax):
    df = pd.read_csv(DATA / "7panel-G-correlation.csv")
    x = df["biomarker_X"].to_numpy()
    y = df["clinical_response_pct"].to_numpy()
    ax.scatter(x, y, s=16, alpha=0.65)
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 120)
    yy = slope * xx + intercept
    resid = y - (slope * x + intercept)
    se = np.sqrt(np.sum(resid ** 2) / (len(x) - 2))
    ci = 1.96 * se * np.sqrt(1 / len(x) + (xx - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2))
    ax.plot(xx, yy)
    ax.fill_between(xx, yy - ci, yy + ci, alpha=0.2)
    r = np.corrcoef(x, y)[0, 1]
    ax.text(0.04, 0.92, f"r={r:.2f}, n={len(x)}", transform=ax.transAxes, fontsize=8)
    ax.set_xlabel("Biomarker X")
    ax.set_ylabel("Clinical response (%)")
    ax.set_title("G. Correlation")
    panel_label(ax, "G")


def main():
    fig = plt.figure(figsize=(9.2, 6.8), constrained_layout=True)
    gs = fig.add_gridspec(3, 4, height_ratios=[1.15, 1.15, 1.0])
    axes = {
        "A": fig.add_subplot(gs[0:2, 0:2]),
        "B": fig.add_subplot(gs[0, 2:4]),
        "C": fig.add_subplot(gs[1, 2:4]),
        "D": fig.add_subplot(gs[2, 0]),
        "E": fig.add_subplot(gs[2, 1]),
        "F": fig.add_subplot(gs[2, 2]),
        "G": fig.add_subplot(gs[2, 3]),
    }
    plot_a(axes["A"])
    plot_b(axes["B"])
    plot_c(axes["C"])
    plot_d(axes["D"])
    plot_e(axes["E"])
    plot_f(axes["F"])
    plot_g(axes["G"])
    for ext in ("svg", "pdf", "png"):
        fig.savefig(OUT / f"baseline.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    main()
