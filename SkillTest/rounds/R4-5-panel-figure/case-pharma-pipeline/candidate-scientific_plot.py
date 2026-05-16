from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures" / "figures-5panel" / "data"
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


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 7
    axes_linewidth: float = 0.75
    use_tex: bool = False
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")


def apply_publication_style(style: FigureStyle | None = None) -> None:
    style = style or FigureStyle()
    plt.rcParams.update(
        {
            "font.family": list(style.font_family),
            "font.size": style.font_size,
            "axes.linewidth": style.axes_linewidth,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.labelsize": style.font_size,
            "axes.titlesize": style.font_size,
            "xtick.labelsize": style.font_size - 1,
            "ytick.labelsize": style.font_size - 1,
            "legend.fontsize": style.font_size - 1,
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "text.usetex": style.use_tex,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def finalize_figure(fig: plt.Figure, out_base: Path, formats: list[str]) -> None:
    for fmt in formats:
        fig.savefig(
            out_base.with_suffix(f".{fmt}"),
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.05,
        )


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=8,
        fontweight="bold",
        va="bottom",
        ha="left",
    )


def add_sig(ax: plt.Axes, x0: float, x1: float, y: float, text: str = "**") -> None:
    h = 0.025 * max(1.0, ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.plot([x0, x0, x1, x1], [y, y + h, y + h, y], color="black", lw=0.7)
    ax.text((x0 + x1) / 2, y + h * 1.2, text, ha="center", va="bottom", fontsize=7)


def summarize(df: pd.DataFrame, groups: list[str], value: str, err: str) -> pd.DataFrame:
    agg = df.groupby(groups, observed=True)[value].agg(["mean", err, "count"]).reset_index()
    if err == "sem":
        agg = agg.rename(columns={"sem": "err"})
    else:
        agg = agg.rename(columns={"std": "err"})
    return agg


def ic50_from_curve(curve: pd.DataFrame) -> float:
    ordered = curve.sort_values("dose_uM")
    x = ordered["dose_uM"].to_numpy(float)
    y = ordered["viability_pct"].to_numpy(float)
    if y.min() > 50 or y.max() < 50:
        return float("nan")
    order = np.argsort(y)
    return float(np.interp(50, y[order], x[order]))


def plot_panel_a(ax: plt.Axes, df: pd.DataFrame) -> None:
    order = ["Melanoma", "NSCLC", "CRC", "Glioma"]
    compounds = ["Vehicle", "CompoundX"]
    stats = summarize(df, ["cancer_type", "compound"], "tumor_volume_reduction_pct", "std")
    stats["cancer_type"] = pd.Categorical(stats["cancer_type"], order, ordered=True)
    stats["compound"] = pd.Categorical(stats["compound"], compounds, ordered=True)
    stats = stats.sort_values(["cancer_type", "compound"])

    x = np.arange(len(order))
    width = 0.34
    offsets = [-width / 2, width / 2]
    colors = [PALETTE["neutral"], PALETTE["blue_main"]]
    hatches = ["", "///"]

    for i, compound in enumerate(compounds):
        sub = stats[stats["compound"] == compound]
        ax.bar(
            x + offsets[i],
            sub["mean"],
            width,
            yerr=sub["err"],
            capsize=2.5,
            label=compound,
            color=colors[i],
            edgecolor="black",
            linewidth=0.65,
            hatch=hatches[i],
        )
    ax.set_ylabel("Tumour volume reduction (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_ylim(-6, 84)
    ax.axhline(0, color=PALETTE["mid"], lw=0.6)
    ax.legend(loc="upper left", ncol=2, handlelength=1.4, columnspacing=0.9)
    for i, cancer in enumerate(order):
        sub = stats[stats["cancer_type"] == cancer]
        ymax = float((sub["mean"] + sub["err"].fillna(0)).max())
        add_sig(ax, x[i] + offsets[0], x[i] + offsets[1], ymax + 4)
    ax.set_title("A  Cross-model antitumour efficacy", loc="left", fontweight="bold", fontsize=8)


def plot_panel_b(ax: plt.Axes, df: pd.DataFrame) -> None:
    colors = [
        PALETTE["blue_main"],
        PALETTE["blue_secondary"],
        PALETTE["green_3"],
        PALETTE["teal"],
        PALETTE["violet"],
        PALETTE["red_strong"],
    ]
    means = df.groupby(["compound", "dose_uM"], observed=True)["viability_pct"].mean().reset_index()
    for color, compound in zip(colors, sorted(means["compound"].unique())):
        curve = means[means["compound"] == compound].sort_values("dose_uM")
        ax.plot(
            curve["dose_uM"],
            curve["viability_pct"],
            marker="o",
            ms=2.4,
            lw=1.15,
            color=color,
            label=compound,
        )
        ic50 = ic50_from_curve(curve)
        if np.isfinite(ic50):
            ax.plot(ic50, 50, marker="|", ms=8, mew=1.0, color=color)
        ax.text(
            float(curve["dose_uM"].iloc[-1]) * 1.05,
            float(curve["viability_pct"].iloc[-1]),
            compound,
            color=color,
            fontsize=5.5,
            va="center",
        )
    ax.axhline(50, color=PALETTE["mid"], lw=0.55, ls=":")
    ax.set_xscale("log")
    ax.set_xlabel("Dose (uM)")
    ax.set_ylabel("Viability (%)")
    ax.set_ylim(0, 106)
    ax.set_xlim(df["dose_uM"].min() * 0.8, df["dose_uM"].max() * 1.55)
    ax.set_title("B  In vitro potency", loc="left", fontweight="bold", fontsize=8)


def plot_panel_c(fig: plt.Figure, spec: GridSpec, df: pd.DataFrame) -> None:
    metric_order = ["CL_int_mL_min_kg", "Vd_L_kg", "F_pct", "t_half_h"]
    metric_labels = {
        "CL_int_mL_min_kg": "CLint",
        "Vd_L_kg": "Vd",
        "F_pct": "F%",
        "t_half_h": "t1/2",
    }
    colors = [PALETTE["blue_main"], PALETTE["green_3"], PALETTE["violet"]]
    sub = spec.subgridspec(2, 2, wspace=0.42, hspace=0.62)
    for i, metric in enumerate(metric_order):
        ax = fig.add_subplot(sub[i // 2, i % 2])
        vals = [
            df[(df["metric"] == metric) & (df["compound"] == compound)]["value"].to_numpy(float)
            for compound in ["X1", "X2", "X3"]
        ]
        parts = ax.violinplot(vals, positions=[1, 2, 3], widths=0.75, showextrema=False)
        for body, color in zip(parts["bodies"], colors):
            body.set_facecolor(color)
            body.set_edgecolor("black")
            body.set_alpha(0.72)
            body.set_linewidth(0.45)
        medians = [np.median(v) for v in vals]
        ax.scatter([1, 2, 3], medians, color="white", edgecolor="black", s=9, zorder=3, lw=0.45)
        ax.set_xticks([1, 2, 3])
        ax.set_xticklabels(["X1", "X2", "X3"], fontsize=5.5)
        ax.set_title(metric_labels[metric], fontsize=6.2, pad=1.5)
        ax.tick_params(axis="y", labelsize=5.5, length=2)
        ax.tick_params(axis="x", length=0)
        if i == 0:
            ax.text(
                -0.42,
                1.38,
                "C  ADMET distribution",
                transform=ax.transAxes,
                fontsize=8,
                fontweight="bold",
                va="bottom",
                ha="left",
            )


def plot_panel_d(ax: plt.Axes, df: pd.DataFrame) -> None:
    stats = summarize(df, ["treatment", "time_h"], "engagement_pct", "sem")
    styles = {
        "Vehicle": (PALETTE["neutral"], "o"),
        "CompoundX": (PALETTE["blue_main"], "s"),
    }
    for treatment in ["Vehicle", "CompoundX"]:
        sub = stats[stats["treatment"] == treatment].sort_values("time_h")
        color, marker = styles[treatment]
        ax.plot(sub["time_h"], sub["mean"], color=color, marker=marker, ms=3.0, lw=1.35, label=treatment)
        ax.fill_between(
            sub["time_h"].to_numpy(float),
            (sub["mean"] - sub["err"]).to_numpy(float),
            (sub["mean"] + sub["err"]).to_numpy(float),
            color=color,
            alpha=0.18,
            linewidth=0,
        )
    ax.set_xlabel("Time after dose (h)")
    ax.set_ylabel("Target engagement (%)")
    ax.set_ylim(-3, 104)
    ax.legend(loc="lower right", ncol=2)
    ax.set_title("D  Pharmacodynamic engagement", loc="left", fontweight="bold", fontsize=8)


def plot_panel_e(ax: plt.Axes, df: pd.DataFrame) -> None:
    organs = ["Heart", "Liver", "Kidney", "Lung", "Brain"]
    groups = ["Vehicle", "Low", "High"]
    colors = [PALETTE["neutral"], PALETTE["green_3"], PALETTE["blue_main"]]
    hatches = ["", "..", "///"]
    stats = summarize(df, ["organ", "group"], "toxicity_score", "std")
    stats["organ"] = pd.Categorical(stats["organ"], organs, ordered=True)
    stats["group"] = pd.Categorical(stats["group"], groups, ordered=True)
    stats = stats.sort_values(["organ", "group"])
    x = np.arange(len(organs))
    width = 0.22
    offsets = [-width, 0, width]
    for i, group in enumerate(groups):
        sub = stats[stats["group"] == group]
        ax.bar(
            x + offsets[i],
            sub["mean"],
            width,
            yerr=sub["err"],
            capsize=2.0,
            color=colors[i],
            edgecolor="black",
            linewidth=0.55,
            hatch=hatches[i],
            label=group,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(organs)
    ax.set_ylabel("Toxicity score")
    ax.set_ylim(0, 4.2)
    ax.legend(loc="upper left", ncol=3, columnspacing=1.1, handlelength=1.3)
    for i, organ in enumerate(organs):
        sub = stats[stats["organ"] == organ]
        ymax = float((sub["mean"] + sub["err"].fillna(0)).max())
        add_sig(ax, x[i] + offsets[0], x[i] + offsets[2], ymax + 0.12, "*")
    ax.set_title("E  Tolerability across organs", loc="left", fontweight="bold", fontsize=8)


def main() -> None:
    apply_publication_style(FigureStyle())
    a = pd.read_csv(DATA / "panel-A-efficacy.csv")
    b = pd.read_csv(DATA / "panel-B-doseresponse.csv")
    c = pd.read_csv(DATA / "panel-C-admet.csv")
    d = pd.read_csv(DATA / "panel-D-engagement.csv")
    e = pd.read_csv(DATA / "panel-E-safety.csv")

    fig = plt.figure(figsize=(8.8, 7.2))
    gs = GridSpec(
        3,
        4,
        figure=fig,
        width_ratios=[1.4, 1.4, 1.1, 1.1],
        height_ratios=[1.3, 1.1, 0.9],
        wspace=0.56,
        hspace=0.68,
    )

    ax_a = fig.add_subplot(gs[0:2, 0:2])
    ax_b = fig.add_subplot(gs[0, 2])
    ax_d = fig.add_subplot(gs[1, 2:4])
    ax_e = fig.add_subplot(gs[2, 0:4])

    plot_panel_a(ax_a, a)
    plot_panel_b(ax_b, b)
    plot_panel_c(fig, gs[0, 3], c)
    plot_panel_d(ax_d, d)
    plot_panel_e(ax_e, e)

    fig.text(
        0.015,
        0.012,
        "Source data: panel-A-efficacy.csv columns cancer_type/compound/mouse/tumor_volume_reduction_pct; "
        "panel-B-doseresponse.csv compound/dose_uM/rep/viability_pct; panel-C-admet.csv compound/metric/rep/value; "
        "panel-D-engagement.csv treatment/time_h/rep/engagement_pct; panel-E-safety.csv organ/group/mouse/toxicity_score. "
        "Bars show mean +/- SD except D, which shows mean +/- SEM; * p<0.05, ** p<0.01.",
        ha="left",
        va="bottom",
        fontsize=5.2,
        color=PALETTE["dark"],
    )
    fig.subplots_adjust(left=0.07, right=0.985, top=0.955, bottom=0.105)
    finalize_figure(fig, OUT / "candidate-scientific", ["svg", "pdf", "png"])
    plt.close(fig)


if __name__ == "__main__":
    main()
