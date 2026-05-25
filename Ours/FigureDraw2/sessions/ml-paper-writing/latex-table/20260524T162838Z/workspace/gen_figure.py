#!/usr/bin/env python3
"""Generate a booktabs comparison table from data.json."""
import json
import subprocess
import shutil
import sys
from pathlib import Path

cwd = Path(__file__).parent

with open(cwd / "data.json") as f:
    data = json.load(f)

methods = data["methods"]
metrics = data["metrics"]
values = data["values"]
n_seeds = data["n_seeds"]
groups = data["groups"]

# Determine bold winners per metric:
# Bold if a method has the highest mean, or overlaps within 1 std of the highest.
def get_bold_set(metric):
    best_mean = max(values[m][metric]["mean"] for m in methods)
    bold = set()
    for m in methods:
        v = values[m][metric]
        if v["mean"] == best_mean:
            bold.add(m)
    # Also bold any method whose mean + std >= best_mean - std_of_best
    best_method = max(methods, key=lambda m: values[m][metric]["mean"])
    best_std = values[best_method][metric]["std"]
    for m in methods:
        v = values[m][metric]
        if v["mean"] + v["std"] >= best_mean - best_std:
            bold.add(m)
    return bold

bold_map = {metric: get_bold_set(metric) for metric in metrics}

def fmt_cell(method, metric):
    v = values[method][metric]
    mean, std = v["mean"], v["std"]
    cell = f"${mean:.1f}{{\\pm {std:.2f}}}$"
    if method in bold_map[metric]:
        cell = f"\\textbf{{{mean:.1f}}}${{\\pm {std:.2f}}}$"
    return cell

# Build group spans
baseline_members = [g["members"] for g in groups if g["label"] == "baselines"][0]
ours_members = [g["members"] for g in groups if g["label"] == "ours"][0]
n_baseline = len(baseline_members)
n_ours = len(ours_members)

# LaTeX source
lines = []
lines.append(r"\documentclass[10pt]{article}")
lines.append(r"\usepackage[margin=0.5in,paperwidth=7in,paperheight=3in]{geometry}")
lines.append(r"\usepackage{booktabs}")
lines.append(r"\usepackage{amsmath}")
lines.append(r"\usepackage{amssymb}")
lines.append(r"\usepackage{xcolor}")
lines.append(r"\usepackage{colortbl}")
lines.append(r"\definecolor{oursbg}{RGB}{240,248,255}")
lines.append(r"\pagestyle{empty}")
lines.append(r"\begin{document}")
lines.append(r"\centering")
lines.append(r"\begin{tabular}{l" + "c" * len(metrics) + "}")
lines.append(r"\toprule")

# Column group header
lines.append(
    r"\multicolumn{1}{c}{} & "
    + r"\multicolumn{" + str(len(metrics)) + r"}{c}{\textbf{Benchmark (\%)}} \\"
)
lines.append(r"\cmidrule(lr){2-" + str(len(metrics) + 1) + "}")

# Metric header row
header_cols = ["\\textbf{Method}"] + [f"\\textbf{{{m}}}" for m in metrics]
lines.append(" & ".join(header_cols) + r" \\")
lines.append(r"\midrule")

# Group: Baselines
lines.append(
    r"\multicolumn{" + str(len(metrics) + 1) + r"}{l}{\textit{Baselines}} \\"
)
for method in baseline_members:
    row = [method] + [fmt_cell(method, metric) for metric in metrics]
    lines.append(" & ".join(row) + r" \\")

lines.append(r"\midrule")

# Group: Ours
lines.append(
    r"\multicolumn{" + str(len(metrics) + 1) + r"}{l}{\textit{Ours}} \\"
)
for method in ours_members:
    row = [r"\rowcolor{oursbg}" + method] + [fmt_cell(method, metric) for metric in metrics]
    lines.append(" & ".join(row) + r" \\")

lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")
lines.append(r"\end{document}")

tex_source = "\n".join(lines) + "\n"

# Write table.tex (standalone, compiles with pdflatex)
table_tex = cwd / "table.tex"
table_tex.write_text(tex_source)
print("Wrote table.tex")

# Compile with pdflatex
result = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(cwd), str(table_tex)],
    capture_output=True, text=True, cwd=str(cwd)
)
if result.returncode != 0:
    print("pdflatex stdout:", result.stdout[-2000:])
    print("pdflatex stderr:", result.stderr[-2000:])
    sys.exit(1)

# Rename output to figure.pdf
generated_pdf = cwd / "table.pdf"
figure_pdf = cwd / "figure.pdf"
if generated_pdf.exists():
    shutil.copy(generated_pdf, figure_pdf)
    print("Wrote figure.pdf")
else:
    print("ERROR: table.pdf not found after pdflatex")
    sys.exit(1)

# Convert to PNG with pdftoppm or convert (ImageMagick)
png_path = cwd / "figure.png"
ret = subprocess.run(
    ["pdftoppm", "-r", "300", "-png", "-singlefile", str(figure_pdf), str(cwd / "figure")],
    capture_output=True
)
if ret.returncode != 0:
    # fallback: ImageMagick
    ret2 = subprocess.run(
        ["convert", "-density", "300", str(figure_pdf), str(png_path)],
        capture_output=True
    )
    if ret2.returncode != 0:
        print("WARNING: could not rasterize PDF to PNG")
    else:
        print("Wrote figure.png (via ImageMagick)")
else:
    print("Wrote figure.png (via pdftoppm)")

# Also attempt SVG via pdf2svg (optional)
if shutil.which("pdf2svg"):
    svg_path = cwd / "figure.svg"
    ret_svg = subprocess.run(
        ["pdf2svg", str(figure_pdf), str(svg_path)],
        capture_output=True
    )
    if ret_svg.returncode == 0:
        print("Wrote figure.svg")
else:
    print("(pdf2svg not available, skipping figure.svg)")

print("Done.")
