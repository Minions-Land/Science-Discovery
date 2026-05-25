#!/usr/bin/env python3
import json
import subprocess
import shutil
from pathlib import Path

CWD = Path(__file__).parent

with open(CWD / "data.json") as f:
    data = json.load(f)

methods = data["methods"]
metrics = data["metrics"]
values = data["values"]
n_seeds = data["n_seeds"]
groups = data["groups"]

# Determine best per metric (bold if within 1 std of the best mean)
def get_bold(metric):
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

bold_map = {metric: get_bold(metric) for metric in metrics}

def fmt(method, metric):
    v = values[method][metric]
    mean, std = v["mean"], v["std"]
    cell = f"${mean:.1f}{{{{\\pm {std:.2f}}}}}$"
    if method in bold_map[metric]:
        cell = f"\\textbf{{{mean:.1f}}}$_{{\\pm {std:.2f}}}$"
    return cell

# Build group spans
baseline_methods = groups[0]["members"]
ours_methods     = groups[1]["members"]
n_metrics = len(metrics)

header_cols = " & ".join([f"\\textbf{{{m}}}" for m in metrics])

lines = []
lines.append(r"\documentclass[10pt]{article}")
lines.append(r"\usepackage{booktabs}")
lines.append(r"\usepackage{amsmath}")
lines.append(r"\usepackage[margin=1in]{geometry}")
lines.append(r"\usepackage{array}")
lines.append(r"\usepackage{xcolor}")
lines.append(r"\begin{document}")
lines.append(r"\thispagestyle{empty}")
lines.append(r"\begin{table}[ht]")
lines.append(r"\centering")
lines.append(r"\small")

col_spec = "l" + "r" * n_metrics
lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
lines.append(r"\toprule")

# Header row
lines.append(f"\\textbf{{Method}} & {header_cols} \\\\")
lines.append(r"\midrule")

# Baselines group
lines.append(f"\\multicolumn{{{n_metrics + 1}}}{{l}}{{\\textit{{Baselines}}}} \\\\[2pt]")
for method in baseline_methods:
    cells = " & ".join([fmt(method, metric) for metric in metrics])
    lines.append(f"\\quad {method} & {cells} \\\\")

lines.append(r"\midrule")

# Ours group
lines.append(f"\\multicolumn{{{n_metrics + 1}}}{{l}}{{\\textit{{Ours}}}} \\\\[2pt]")
for method in ours_methods:
    cells = " & ".join([fmt(method, metric) for metric in metrics])
    lines.append(f"\\quad {method} & {cells} \\\\")

lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")

caption_text = (
    f"Comparison of methods on five benchmarks (mean $\\pm$ std over {n_seeds} seeds, all scores in \\%). "
    r"\textbf{Bold} indicates the best result per column; "
    r"a runner-up within one standard deviation of the best is also bolded."
)
lines.append(f"\\caption{{{caption_text}}}")
lines.append(r"\label{tab:main}")
lines.append(r"\end{table}")
lines.append(r"\end{document}")

tex_source = "\n".join(lines)

table_tex_path = CWD / "table.tex"
table_tex_path.write_text(tex_source)

# Compile with pdflatex
result = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(table_tex_path)],
    capture_output=True, text=True, cwd=str(CWD)
)
if result.returncode != 0:
    print("pdflatex stdout:", result.stdout[-3000:])
    print("pdflatex stderr:", result.stderr[-1000:])
    raise RuntimeError("pdflatex failed")

# Rename output to figure.pdf
pdf_out = CWD / "table.pdf"
figure_pdf = CWD / "figure.pdf"
if pdf_out.exists():
    shutil.move(str(pdf_out), str(figure_pdf))

# Rasterize to figure.png using pdftoppm or convert
png_out = CWD / "figure.png"
try:
    subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", str(figure_pdf), str(CWD / "figure")],
        check=True, capture_output=True
    )
    # pdftoppm appends -1 or nothing depending on version
    candidate = CWD / "figure-1.png"
    if candidate.exists():
        shutil.move(str(candidate), str(png_out))
except (subprocess.CalledProcessError, FileNotFoundError):
    subprocess.run(
        ["convert", "-density", "300", str(figure_pdf), str(png_out)],
        check=True
    )

# Write caption.tex (caption text only, no \begin{figure})
caption_tex = (
    f"\\caption{{Comparison of methods on five benchmarks "
    f"(mean $\\pm$ std over {n_seeds} seeds, all scores in \\%). "
    r"\textbf{Bold} indicates the best result per column; "
    r"a runner-up within one standard deviation of the best is also bolded.}}"
)
(CWD / "caption.tex").write_text(caption_tex + "\n")

print("Done: figure.pdf, figure.png, table.tex, caption.tex written.")
