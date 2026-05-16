from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures-6-7panel" / "data"
OUT = Path(__file__).resolve().parent

PALETTE = {
    "Vehicle": "#6b7280",
    "CompoundX": "#2563eb",
    "X1": "#2563eb",
    "X2": "#16a34a",
    "X3": "#dc2626",
    "Low dose": "#93c5fd",
    "High dose": "#1d4ed8",
}


def setup_style():
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans"],
            "font.size": 7,
            "axes.titlesize": 7,
            "axes.labelsize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 6,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )


def panel_label(ax, label):
    ax.text(
        -0.14,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=8,
        fontweight="bold",
        va="top",
        ha="left",
    )


def plot_a(ax):
    df = pd.read_csv(DATA / "6panel-A-efficacy.csv")
    summary = (
        df.groupby(["cancer_type", "compound"])["tumor_volume_pct"]
        .agg(["mean", "std"])
        .reset_index()
    )
    cancers = list(summary["cancer_type"].unique())
    x = np.arange(len(cancers))
    width = 0.36
    for i, compound in enumerate(["Vehicle", "CompoundX"]):
        vals = summary[summary["compound"] == compound].set_index("cancer_type").loc[cancers]
        offset = (i - 0.5) * width
        ax.bar(
            x + offset,
            vals["mean"],
            width,
            yerr=vals["std"],
            capsize=2,
            label=compound,
            color=PALETTE[compound],
            edgecolor="white",
            linewidth=0.4,
        )
    for xpos in x:
        ax.text(xpos, 108, "**", ha="center", va="bottom", fontsize=8)
    ax.set_title("A. Tumour volume reduction")
    ax.set_ylabel("Tumour volume (% vehicle baseline)")
    ax.set_xticks(x)
    ax.set_xticklabels(cancers, rotation=18, ha="right")
    ax.set_ylim(0, 120)
    ax.legend(frameon=False, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)


def plot_b(ax):
    df = pd.read_csv(DATA / "6panel-B-doseresponse.csv")
    for compound, color in [("X1", PALETTE["X1"]), ("X2", PALETTE["X2"]), ("X3", PALETTE["X3"])]:
        sub = df[df["compound"] == compound]
        stats = sub.groupby("dose_uM")["viability_pct"].agg(["mean", "sem"]).reset_index()
        ax.errorbar(
            stats["dose_uM"],
            stats["mean"],
            yerr=stats["sem"],
            marker="o",
            markersize=3,
            linewidth=1.1,
            capsize=2,
            label=compound,
            color=color,
        )
    ax.set_xscale("log")
    ax.set_title("Dose-response")
    ax.set_xlabel("Dose (uM)")
    ax.set_ylabel("Viability (%)")
    ax.set_ylim(0, 110)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)


def plot_c(ax):
    df = pd.read_csv(DATA / "6panel-C-admet.csv")
    metrics = list(df["metric"].unique())
    compounds = ["X1", "X2", "X3"]
    positions = []
    values = []
    colors = []
    labels = []
    pos = 1
    for metric in metrics:
        for compound in compounds:
            values.append(df[(df["metric"] == metric) & (df["compound"] == compound)]["value"])
            positions.append(pos)
            colors.append(PALETTE[compound])
            labels.append(compound)
            pos += 1
        pos += 0.7
    parts = ax.violinplot(values, positions=positions, widths=0.55, showmeans=True, showextrema=False)
    for body, color in zip(parts["bodies"], colors):
        body.set_facecolor(color)
        body.set_edgecolor("none")
        body.set_alpha(0.55)
    parts["cmeans"].set_color("#111827")
    centers = [np.mean(positions[i * 3 : i * 3 + 3]) for i in range(len(metrics))]
    ax.set_xticks(centers)
    ax.set_xticklabels(metrics)
    ax.set_title("ADMET distribution")
    ax.set_ylabel("Scaled metric value")
    handles = [plt.Line2D([0], [0], color=PALETTE[c], lw=4, alpha=0.55) for c in compounds]
    ax.legend(handles, compounds, frameon=False, ncol=3, loc="upper right", handlelength=1)
    ax.spines[["top", "right"]].set_visible(False)


def plot_d(ax):
    df = pd.read_csv(DATA / "6panel-D-engagement.csv")
    for treatment in ["Vehicle", "CompoundX"]:
        sub = df[df["treatment"] == treatment]
        stats = sub.groupby("time_h")["engagement_pct"].agg(["mean", "sem"]).reset_index()
        ax.errorbar(
            stats["time_h"],
            stats["mean"],
            yerr=stats["sem"],
            marker="o",
            markersize=3,
            linewidth=1.1,
            capsize=2,
            label=treatment,
            color=PALETTE[treatment],
        )
    ax.set_title("Target engagement")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Engagement (%)")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)


def plot_e(ax):
    df = pd.read_csv(DATA / "6panel-E-safety.csv")
    stats = df.groupby(["organ", "group"])["toxicity_score"].mean().reset_index()
    organs = list(stats["organ"].unique())
    groups = list(stats["group"].unique())
    x = np.arange(len(organs))
    width = 0.24
    for i, group in enumerate(groups):
        vals = stats[stats["group"] == group].set_index("organ").loc[organs]
        ax.bar(x + (i - 1) * width, vals["toxicity_score"], width, label=group, color=PALETTE.get(group, "#16a34a"))
    ax.set_title("Multi-organ safety")
    ax.set_ylabel("Toxicity score")
    ax.set_xticks(x)
    ax.set_xticklabels(organs, rotation=20, ha="right")
    ax.legend(frameon=False, fontsize=5)
    ax.spines[["top", "right"]].set_visible(False)


def km_curve(times, events):
    order = np.argsort(times)
    times = np.asarray(times)[order]
    events = np.asarray(events)[order]
    at_risk = len(times)
    survival = 1.0
    xs = [0.0]
    ys = [1.0]
    for t, e in zip(times, events):
        xs.extend([t, t])
        ys.extend([survival, survival * (1 - e / at_risk)])
        survival = ys[-1]
        at_risk -= 1
    return xs, ys


def plot_f(ax):
    df = pd.read_csv(DATA / "6panel-F-survival.csv")
    for group in ["Vehicle", "CompoundX"]:
        sub = df[df["group"] == group]
        xs, ys = km_curve(sub["time_days"], sub["event"])
        ax.step(xs, np.asarray(ys) * 100, where="post", label=group, color=PALETTE[group], linewidth=1.4)
    ax.set_title("Survival benefit")
    ax.set_xlabel("Days")
    ax.set_ylabel("Survival (%)")
    ax.set_ylim(0, 105)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)


def main():
    setup_style()
    fig = plt.figure(figsize=(7.2, 6.1), constrained_layout=True)
    gs = fig.add_gridspec(3, 4)
    axes = {
        "A": fig.add_subplot(gs[0:2, 0:2]),
        "B": fig.add_subplot(gs[0, 2:4]),
        "C": fig.add_subplot(gs[1, 2:4]),
        "D": fig.add_subplot(gs[2, 0:2]),
        "E": fig.add_subplot(gs[2, 2]),
        "F": fig.add_subplot(gs[2, 3]),
    }
    plot_a(axes["A"])
    plot_b(axes["B"])
    plot_c(axes["C"])
    plot_d(axes["D"])
    plot_e(axes["E"])
    plot_f(axes["F"])
    for label, ax in axes.items():
        if label != "A":
            panel_label(ax, label)
    fig.savefig(OUT / "baseline.svg")
    fig.savefig(OUT / "baseline.pdf")
    fig.savefig(OUT / "baseline.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
