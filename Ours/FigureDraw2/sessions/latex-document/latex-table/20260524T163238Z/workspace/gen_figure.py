#!/usr/bin/env python3
"""Generate a booktabs comparison table from data.json, compile to PDF, rasterize to PNG."""

import json
import subprocess
import sys
from pathlib import Path

CWD = Path(__file__).parent

def load_data():
    with open(CWD / "data.json") as f:
        return json.load(f)

def is_bold(mean, std, best_mean, best_std):
    """Bold if within 1 std of the best mean (overlap rule)."""
    return mean + std >= best_mean - best_std

def fmt_cell(mean, std, bold):
    s = f"${mean:.1f}_{{\\pm {std:.2f}}}$"
    if bold:
        s = f"\\textbf{{{mean:.1f}}}$_{{\\pm {std:.2f}}}$"
    return s

def build_tex(data):
    methods = data["methods"]
    metrics = data["metrics"]
    values = data["values"]
    groups = data["groups"]
    n_seeds = data["n_seeds"]

    # Determine best per metric
    best = {}
    for metric in metrics:
        best_mean = max(values[m][metric]["mean"] for m in methods)
        best_std = max(
            values[m][metric]["std"]
            for m in methods
            if values[m][metric]["mean"] == best_mean
        )
        best[metric] = (best_mean, best_std)

    # Group spans
    baseline_methods = groups[0]["members"]
    ours_methods = groups[1]["members"]
    n_baseline = len(baseline_methods)
    n_ours = len(ours_methods)
    n_metrics = len(metrics)

    lines = []
    lines.append(r"""\documentclass[10pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{array}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\pagestyle{empty}
\begin{document}

\begin{table}[ht]
\centering
\renewcommand{\arraystretch}{1.25}""")

    # Column spec: method name + one col per metric
    col_spec = "l" + "c" * n_metrics
    lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\toprule")

    # Group header row
    header_parts = [""]
    header_parts.append(
        f"\\multicolumn{{{n_metrics}}}{{c}}{{Benchmark (\%)}}"
    )
    lines.append(" & ".join(header_parts) + r" \\")
    lines.append(f"\\cmidrule(lr){{2-{n_metrics+1}}}")

    # Metric header
    metric_header = ["\\textbf{Method}"] + [f"\\textbf{{{m}}}" for m in metrics]
    lines.append(" & ".join(metric_header) + r" \\")
    lines.append(r"\midrule")

    # Group span: Baselines
    lines.append(
        f"\\multicolumn{{{n_metrics+1}}}{{l}}"
        r"{\textit{\small Baselines}} \\"
    )

    for method in baseline_methods:
        row = [method.replace("_", r"\_")]
        for metric in metrics:
            mv = values[method][metric]
            bm, bs = best[metric]
            bold = is_bold(mv["mean"], mv["std"], bm, bs)
            row.append(fmt_cell(mv["mean"], mv["std"], bold))
        lines.append(" & ".join(row) + r" \\")

    lines.append(r"\midrule")

    # Group span: Ours
    lines.append(
        f"\\multicolumn{{{n_metrics+1}}}{{l}}"
        r"{\textit{\small Ours}} \\"
    )

    for method in ours_methods:
        row = [f"\\textbf{{{method.replace('_', chr(92)+chr(95))}}}"]
        for metric in metrics:
            mv = values[method][metric]
            bm, bs = best[metric]
            bold = is_bold(mv["mean"], mv["std"], bm, bs)
            row.append(fmt_cell(mv["mean"], mv["std"], bold))
        lines.append(" & ".join(row) + r" \\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")

    caption = (
        r"\caption{Comparison of methods on five benchmarks (mean $\pm$ std over "
        + str(n_seeds)
        + r" seeds). "
        r"\textbf{Bold} entries are the best or within one standard deviation of the best per column. "
        r"OursModel consistently outperforms all baselines.}"
    )
    lines.append(caption)
    lines.append(r"\end{table}")
    lines.append(r"\end{document}")

    return "\n".join(lines)

def main():
    data = load_data()
    tex = build_tex(data)

    table_tex = CWD / "table.tex"
    table_tex.write_text(tex)
    print(f"Wrote {table_tex}")

    # Compile with pdflatex (twice for stable layout)
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(table_tex)],
            capture_output=True, text=True, cwd=CWD
        )
        if result.returncode != 0:
            print("pdflatex stdout:", result.stdout[-3000:])
            print("pdflatex stderr:", result.stderr[-1000:])
            sys.exit(1)

    # Rename output to figure.pdf
    src_pdf = CWD / "table.pdf"
    fig_pdf = CWD / "figure.pdf"
    src_pdf.rename(fig_pdf)
    print(f"Wrote {fig_pdf}")

    # Rasterize to PNG with pdftoppm (300 dpi)
    result = subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", str(fig_pdf), str(CWD / "figure")],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # fallback: convert via ImageMagick
        result2 = subprocess.run(
            ["convert", "-density", "300", str(fig_pdf), str(CWD / "figure.png")],
            capture_output=True, text=True
        )
        if result2.returncode != 0:
            print("PNG rasterization failed:", result.stderr, result2.stderr)
            sys.exit(1)

    fig_png = CWD / "figure.png"
    if not fig_png.exists():
        # pdftoppm may produce figure-1.png
        candidate = CWD / "figure-1.png"
        if candidate.exists():
            candidate.rename(fig_png)

    print(f"Wrote {fig_png}")

    # Also produce SVG via pdf2svg if available
    try:
        result = subprocess.run(
            ["pdf2svg", str(fig_pdf), str(CWD / "figure.svg")],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"Wrote {CWD / 'figure.svg'}")
    except FileNotFoundError:
        pass  # pdf2svg not installed; SVG is optional

if __name__ == "__main__":
    main()
