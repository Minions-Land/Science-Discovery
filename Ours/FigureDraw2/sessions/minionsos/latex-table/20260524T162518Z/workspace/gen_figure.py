#!/usr/bin/env python3
"""Generate a booktabs comparison table from data.json, compile to PDF, and rasterize to PNG."""

import json
import subprocess
import shutil
import os
from pathlib import Path

cwd = Path(__file__).parent

with open(cwd / "data.json") as f:
    data = json.load(f)

methods = data["methods"]
metrics = data["metrics"]
values = data["values"]
groups = data["groups"]
n_seeds = data["n_seeds"]

# Determine best (highest mean) per metric; bold if within 1 std of best
def get_bold_set(metric):
    means = {m: values[m][metric]["mean"] for m in methods}
    stds  = {m: values[m][metric]["std"]  for m in methods}
    best_mean = max(means.values())
    bold = set()
    for m in methods:
        if means[m] == best_mean:
            bold.add(m)
        elif best_mean - means[m] <= stds[m]:
            bold.add(m)
    return bold

bold_sets = {metric: get_bold_set(metric) for metric in metrics}

def fmt_cell(method, metric):
    v = values[method][metric]
    mean, std = v["mean"], v["std"]
    cell = f"${mean:.1f}{{\\scriptstyle \\pm{std:.2f}}}$"
    if method in bold_sets[metric]:
        cell = f"\\textbf{{{cell}}}"
    return cell

# Build group structure: baselines (3 methods) + ours (1 method)
baseline_methods = groups[0]["members"]   # Baseline, Method-A, Method-B
ours_methods     = groups[1]["members"]   # OursModel

n_metrics = len(metrics)
col_spec = "l" + "r" * n_metrics  # method name + one column per metric

# Header row
header_cols = " & ".join([f"\\textbf{{{m}}}" for m in metrics])

lines = []
lines.append(r"\begin{tabular}{" + col_spec + r"}")
lines.append(r"\toprule")

# Metric header with spanning label
lines.append(
    r"\multicolumn{1}{c}{} & "
    + r"\multicolumn{" + str(n_metrics) + r"}{c}{\textbf{Benchmark (\%)}}\\"
)
lines.append(r"\cmidrule(lr){2-" + str(n_metrics + 1) + r"}")
lines.append(r"\textbf{Method} & " + header_cols + r"\\")
lines.append(r"\midrule")

# Baselines group header
lines.append(
    r"\multicolumn{" + str(n_metrics + 1) + r"}{l}{\textit{Baselines}}\\"
)
for method in baseline_methods:
    row = method + " & " + " & ".join(fmt_cell(method, m) for m in metrics) + r"\\"
    lines.append(row)

lines.append(r"\midrule")

# Ours group header
lines.append(
    r"\multicolumn{" + str(n_metrics + 1) + r"}{l}{\textit{Ours}}\\"
)
for method in ours_methods:
    row = method + " & " + " & ".join(fmt_cell(method, m) for m in metrics) + r"\\"
    lines.append(row)

lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")

table_body = "\n".join(lines)

standalone_tex = r"""\documentclass{article}
\usepackage[margin=1cm]{geometry}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{lmodern}
\pagestyle{empty}
\begin{document}
\begin{center}
""" + table_body + r"""
\end{center}
\end{document}
"""

table_tex_path = cwd / "table.tex"
with open(table_tex_path, "w") as f:
    f.write(standalone_tex)

print("Wrote table.tex")

# Compile with pdflatex
result = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(cwd), str(table_tex_path)],
    capture_output=True, text=True, cwd=str(cwd)
)
if result.returncode != 0:
    print("pdflatex stdout:", result.stdout[-3000:])
    print("pdflatex stderr:", result.stderr[-1000:])
    raise RuntimeError("pdflatex failed")

print("Compiled table.tex -> table.pdf")

# pdflatex outputs as table.pdf; rename/copy to figure.pdf
pdf_src = cwd / "table.pdf"
pdf_dst = cwd / "figure.pdf"
shutil.copy(pdf_src, pdf_dst)
print("Copied to figure.pdf")

# Rasterize to PNG using pdftoppm or convert (ImageMagick)
png_dst = cwd / "figure.png"
if shutil.which("pdftoppm"):
    result2 = subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", str(pdf_dst), str(cwd / "figure")],
        capture_output=True, text=True
    )
    if result2.returncode != 0:
        raise RuntimeError("pdftoppm failed: " + result2.stderr)
    print("Rasterized to figure.png via pdftoppm")
elif shutil.which("convert"):
    result2 = subprocess.run(
        ["convert", "-density", "300", str(pdf_dst), str(png_dst)],
        capture_output=True, text=True
    )
    if result2.returncode != 0:
        raise RuntimeError("convert failed: " + result2.stderr)
    print("Rasterized to figure.png via ImageMagick convert")
else:
    raise RuntimeError("Neither pdftoppm nor convert found; cannot rasterize PDF to PNG")

print("Done.")
