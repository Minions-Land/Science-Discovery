"""
gen_figure.py — Produce figure.pdf, figure.png from data.json via pdflatex on table.tex.
Data source: data.json (cwd)
"""
import json
import pathlib
import subprocess
import sys
import re
import shutil

CWD = pathlib.Path(__file__).parent
DATA = json.loads((CWD / "data.json").read_text())

methods = DATA["methods"]
metrics = DATA["metrics"]
values = DATA["values"]
n_seeds = DATA.get("n_seeds", 5)
groups = DATA.get("groups", [])

# Determine group spans for \multicolumn header
# groups: [{"label": "baselines", "members": [...]}, {"label": "ours", "members": [...]}]
group_spans = []
for g in groups:
    group_spans.append((g["label"], len(g["members"])))

# Determine best per metric (column = metric, row = method)
# Bold rule: bold the best mean; also bold any method within 1 std of the best
def get_bold_set(metric):
    best_mean = max(values[m][metric]["mean"] for m in methods)
    bold = set()
    for m in methods:
        v = values[m][metric]
        if v["mean"] == best_mean:
            bold.add(m)
        # within-1-sigma overlap: method mean + std >= best_mean - best_std
        best_std = values[[mm for mm in methods if values[mm][metric]["mean"] == best_mean][0]][metric]["std"]
        if v["mean"] + v["std"] >= best_mean - best_std:
            bold.add(m)
    return bold

bold_sets = {metric: get_bold_set(metric) for metric in metrics}

def fmt_cell(method, metric):
    v = values[method][metric]
    mean = v["mean"]
    std = v["std"]
    # subscript style: $72.4_{\pm 1.2}$
    cell = f"${mean:.1f}_{{\\pm {std:.2f}}}$"
    if method in bold_sets[metric]:
        cell = f"\\textbf{{{cell}}}"
    return cell

# Build LaTeX
n_methods = len(methods)
# Column spec: l + one c per method
col_spec = "l " + " ".join(["c"] * n_methods)

# Group header row
group_header_parts = [""]  # empty for metric column
col_idx = 2  # 1-indexed, metric col is 1
cmidrule_parts = []
for label, span in group_spans:
    cap_label = label.capitalize()
    group_header_parts.append(f"\\multicolumn{{{span}}}{{c}}{{{cap_label}}}")
    cmidrule_parts.append(f"\\cmidrule(lr){{{col_idx}-{col_idx + span - 1}}}")
    col_idx += span

group_header_row = " & ".join(group_header_parts) + " \\\\"
cmidrule_row = " ".join(cmidrule_parts)

# Method name header row
method_header_parts = ["Metric"] + [f"\\textbf{{{m}}}" for m in methods]
method_header_row = " & ".join(method_header_parts) + " \\\\"

# Data rows
data_rows = []
for metric in metrics:
    cells = [f"{metric}$\\uparrow$"]
    for method in methods:
        cells.append(fmt_cell(method, metric))
    data_rows.append(" & ".join(cells) + " \\\\")

data_rows_str = "\n".join(data_rows)

latex_source = r"""\documentclass[10pt]{article}
\usepackage[margin=0.5in, paperwidth=7in, paperheight=3.5in]{geometry}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{amsmath}
\usepackage{lmodern}
\usepackage[T1]{fontenc}
\renewcommand{\familydefault}{\sfdefault}
\pagestyle{empty}

\begin{document}
\centering
\begin{tabular}{""" + col_spec + r"""}
\toprule
""" + group_header_row + "\n" + cmidrule_row + "\n" + method_header_row + r"""
\midrule
""" + data_rows_str + r"""
\bottomrule
\end{tabular}
\end{document}
"""

table_tex_path = CWD / "table.tex"
table_tex_path.write_text(latex_source)
print(f"[gen_figure] Wrote {table_tex_path}")

# Compile with pdflatex
result = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(table_tex_path)],
    capture_output=True, text=True, cwd=str(CWD)
)
if result.returncode != 0:
    sys.stderr.write(result.stdout[-3000:])
    sys.stderr.write(result.stderr[-1000:])
    sys.exit(1)

# pdflatex outputs table.pdf; rename to figure.pdf
table_pdf = CWD / "table.pdf"
figure_pdf = CWD / "figure.pdf"
if table_pdf.exists():
    shutil.move(str(table_pdf), str(figure_pdf))
    print(f"[gen_figure] Renamed table.pdf -> figure.pdf")
else:
    sys.stderr.write("ERROR: table.pdf not produced by pdflatex\n")
    sys.exit(1)

# Rasterize to figure.png using pdftoppm or convert
figure_png = CWD / "figure.png"
# Try pdftoppm first
pdftoppm = shutil.which("pdftoppm")
convert = shutil.which("convert")
if pdftoppm:
    r = subprocess.run(
        [pdftoppm, "-r", "300", "-png", "-singlefile", str(figure_pdf), str(CWD / "figure")],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    print(f"[gen_figure] Rasterized to {figure_png}")
elif convert:
    r = subprocess.run(
        [convert, "-density", "300", str(figure_pdf), str(figure_png)],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    print(f"[gen_figure] Rasterized to {figure_png}")
else:
    # Fallback: use Python pdf2image if available
    try:
        from pdf2image import convert_from_path
        pages = convert_from_path(str(figure_pdf), dpi=300)
        pages[0].save(str(figure_png), "PNG")
        print(f"[gen_figure] Rasterized to {figure_png} via pdf2image")
    except ImportError:
        sys.stderr.write("WARNING: No rasterizer found (pdftoppm, convert, pdf2image). figure.png not produced.\n")

# Font check
raw = figure_pdf.read_bytes()
if re.search(rb"/Subtype\s*/Type3\b", raw):
    sys.stderr.write("FATAL: /Type3 found in figure.pdf — bitmap fonts detected.\n")
    sys.exit(2)
print("[fonttype-check] OK — no Type 3 fonts in figure.pdf")

# Clean up aux files
for ext in [".aux", ".log"]:
    p = CWD / f"table{ext}"
    if p.exists():
        p.unlink()

print("[gen_figure] Done.")
