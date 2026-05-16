from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "fixtures/figures-novel-form/radar/data/method-metric-comparison.csv"
OUT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "Arial",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 7,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.55,
})

df = pd.read_csv(DATA).set_index("method")
metrics = list(df.columns)
n = len(metrics)
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
theta_closed = np.r_[theta, theta[0]]

palette = {
    "MethodX (Ours)": "#2f9aa0",
    "BERT-base": "#98cfd0",
    "GPT-3.5": "#84bfc7",
    "RoBERTa": "#b4ddd8",
    "T5": "#cfe9e2",
}

fig, ax = plt.subplots(figsize=(4.95, 4.95), subplot_kw={"projection": "polar"})
fig.patch.set_facecolor("white")
ax.set_facecolor("#fafafa")
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.set_xticks(theta)
ax.set_xticklabels(metrics, color="#626262")
ax.tick_params(axis="x", pad=7)
ax.set_ylim(0, 1.0)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], color="#777777")
ax.set_rlabel_position(90)
ax.grid(color="#c8c8c8", linewidth=0.7)
ax.spines["polar"].set_color("#b8b8b8")
ax.spines["polar"].set_linewidth(0.8)

for method, row in df.iterrows():
    values = np.r_[row.values.astype(float), row.values.astype(float)[0]]
    color = palette[method]
    lw = 2.45 if method == "MethodX (Ours)" else 2.05
    alpha = 0.24 if method == "MethodX (Ours)" else 0.16
    ax.fill(theta_closed, values, color=color, alpha=alpha, zorder=2)
    ax.plot(theta_closed, values, color=color, linewidth=lw, label=method, zorder=3)

ax.legend(
    frameon=False,
    ncol=2,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.16),
    handlelength=1.9,
    columnspacing=1.1,
)

fig.tight_layout(pad=0.35)
for ext in ("svg", "pdf", "png"):
    kwargs = {"dpi": 300} if ext == "png" else {}
    fig.savefig(OUT / f"candidate.{ext}", bbox_inches="tight", **kwargs)
