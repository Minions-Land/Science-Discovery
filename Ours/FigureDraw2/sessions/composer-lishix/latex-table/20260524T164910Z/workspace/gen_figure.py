#!/usr/bin/env python3
import json, subprocess, shutil, sys
from pathlib import Path

cwd = Path(__file__).parent
data = json.loads((cwd / "data.json").read_text())

methods  = data["methods"]
metrics  = data["metrics"]
values   = data["values"]
n_seeds  = data["n_seeds"]
groups   = data["groups"]

# Determine best per metric (bold if within 1 std of the max mean)
def is_bold(method, metric):
    best_mean = max(values[m][metric]["mean"] for m in methods)
    v = values[method][metric]
    return v["mean"] + v["std"] >= best_mean

def fmt(method, metric):
    v = values[method][metric]
    mean_s = "{:.1f}".format(v["mean"])
    std_s  = "{:.2f}".format(v["std"])
    cell = "$" + mean_s + "_{\\pm " + std_s + "}$"
    if is_bold(method, metric):
        cell = r"\textbf{" + cell + "}"
    return cell

# Build group spans
baseline_methods = groups[0]["members"]
ours_methods     = groups[1]["members"]
n_baseline = len(baseline_methods)
n_ours     = len(ours_methods)
n_metrics  = len(metrics)

lines = []
lines.append(r"\documentclass[10pt]{article}")
lines.append(r"\usepackage{booktabs,xcolor,geometry,amsmath}")
lines.append(r"\geometry{paperwidth=18cm,paperheight=8cm,margin=0.6cm}")
lines.append(r"\renewcommand{\arraystretch}{1.25}")
lines.append(r"\begin{document}")
lines.append(r"\pagestyle{empty}")
lines.append(r"\begin{table}[!ht]")
lines.append(r"\centering")
lines.append(r"\small")

col_spec = "l" + "c" * n_metrics
lines.append(r"\begin{tabular}{" + col_spec + "}")
lines.append(r"\toprule")

# Header row
metric_headers = " & ".join(r"\textbf{" + m + "}" for m in metrics)
lines.append(r"\textbf{Method} & " + metric_headers + r" \\")
lines.append(r"\midrule")

# Group: Baselines
lines.append(r"\multicolumn{" + str(n_metrics + 1) + r"}{l}{\textit{Baselines}} \\")
for method in baseline_methods:
    cells = " & ".join(fmt(method, metric) for metric in metrics)
    lines.append(f"{method} & {cells} \\\\")

lines.append(r"\midrule")

# Group: Ours
lines.append(r"\multicolumn{" + str(n_metrics + 1) + r"}{l}{\textit{Ours}} \\")
for method in ours_methods:
    cells = " & ".join(fmt(method, metric) for metric in metrics)
    lines.append(f"{method} & {cells} \\\\")

lines.append(r"\bottomrule")
lines.append(r"\end{tabular}")

caption = (
    r"\caption{Comparison of methods on five ML benchmarks (all metrics in \%). "
    r"Results are mean\,$\pm$\,std over " + str(n_seeds) + r" seeds. "
    r"\textbf{Bold} indicates the best result per column; "
    r"multiple entries are bolded when their means overlap within one standard deviation.}"
)
lines.append(caption)
lines.append(r"\end{table}")
lines.append(r"\end{document}")

tex_source = "\n".join(lines) + "\n"

table_tex = cwd / "table.tex"
table_tex.write_text(tex_source)
print("Wrote table.tex")

# Compile with pdflatex
result = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(cwd), str(table_tex)],
    capture_output=True, text=True, cwd=str(cwd)
)
if result.returncode != 0:
    print("pdflatex stdout:", result.stdout[-3000:])
    print("pdflatex stderr:", result.stderr[-1000:])
    sys.exit(1)
print("Compiled table.pdf")

# Rename to figure.pdf
pdf_out = cwd / "table.pdf"
figure_pdf = cwd / "figure.pdf"
shutil.copy(pdf_out, figure_pdf)
print("Copied to figure.pdf")

# Rasterize to figure.png
png_result = subprocess.run(
    ["pdftoppm", "-r", "300", "-png", "-singlefile", str(figure_pdf), str(cwd / "figure")],
    capture_output=True, text=True
)
if png_result.returncode != 0:
    # fallback: try convert (ImageMagick)
    png_result2 = subprocess.run(
        ["convert", "-density", "300", str(figure_pdf), str(cwd / "figure.png")],
        capture_output=True, text=True
    )
    if png_result2.returncode != 0:
        print("Warning: could not rasterize PDF to PNG")
        print(png_result2.stderr)
    else:
        print("Rasterized to figure.png via ImageMagick")
else:
    print("Rasterized to figure.png via pdftoppm")

# Write caption.tex
caption_tex = cwd / "caption.tex"
caption_tex.write_text(
    r"\caption{Comparison of methods on five ML benchmarks (all metrics in \%). "
    r"Results are mean\,$\pm$\,std over " + str(n_seeds) + r" seeds. "
    r"\textbf{Bold} indicates the best result per column; "
    r"multiple entries are bolded when their means overlap within one standard deviation.}"
    + "\n"
)
print("Wrote caption.tex")
print("Done.")
