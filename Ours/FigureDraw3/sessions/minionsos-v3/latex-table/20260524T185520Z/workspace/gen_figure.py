#!/usr/bin/env python3
"""Generate a booktabs comparison table from data.json, compile to PDF, rasterize to PNG."""

import json
import subprocess
import sys
from pathlib import Path

CWD = Path(__file__).parent

# ── Load data ──────────────────────────────────────────────────────────────────
with open(CWD / "data.json") as f:
    data = json.load(f)

methods  = data["methods"]
metrics  = data["metrics"]
values   = data["values"]
n_seeds  = data["n_seeds"]
groups   = data["groups"]

# ── Determine bold cells (best per column; also bold if within 1 std of best) ──
def is_bold(metric, method):
    best_mean = max(values[m][metric]["mean"] for m in methods)
    best_std  = next(values[m][metric]["std"] for m in methods
                     if values[m][metric]["mean"] == best_mean)
    v = values[method][metric]
    return v["mean"] == best_mean or (best_mean - v["mean"]) <= best_std

# ── Format a cell value ────────────────────────────────────────────────────────
def fmt_cell(metric, method):
    v    = values[method][metric]
    mean = v["mean"]
    std  = v["std"]
    # subscript ± style
    inner = rf"{mean:.1f}_{{\pm {std:.2f}}}"
    cell  = f"${inner}$"
    if is_bold(metric, method):
        cell = rf"\mathbf{{{mean:.1f}}}_{{\pm {std:.2f}}}"
        cell = f"${cell}$"
    return cell

# ── Build LaTeX ────────────────────────────────────────────────────────────────
n_metrics = len(metrics)
col_spec  = "l" + "c" * n_metrics   # method name + one col per metric

header_cols = " & ".join(rf"\textbf{{{m}}}" for m in metrics)

rows = []
for group in groups:
    label   = group["label"].capitalize()
    members = group["members"]
    # group header row
    rows.append(
        rf"    \multicolumn{{{n_metrics + 1}}}{{l}}{{\textit{{{label}}}}} \\"
    )
    for method in members:
        cells = [fmt_cell(metric, method) for metric in metrics]
        display = method.replace("OursModel", r"\textbf{OursModel}")
        row = "    " + display + " & " + " & ".join(cells) + r" \\"
        rows.append(row)
    rows.append(r"    \midrule")

# Remove trailing \midrule
if rows and rows[-1].strip() == r"\midrule":
    rows.pop()

rows_tex = "\n".join(rows)

table_body = rf"""
\begin{{tabular}}{{{col_spec}}}
\toprule
\textbf{{Method}} & {header_cols} \\
\midrule
{rows_tex}
\bottomrule
\end{{tabular}}
"""

standalone_tex = rf"""\documentclass{{article}}
\usepackage[margin=0.5in, paperwidth=6.5in, paperheight=3in]{{geometry}}
\usepackage{{booktabs}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\pagestyle{{empty}}
\begin{{document}}
\centering
{table_body}
\end{{document}}
"""

# ── Write table.tex ────────────────────────────────────────────────────────────
table_tex_path = CWD / "table.tex"
table_tex_path.write_text(standalone_tex)
print(f"Wrote {table_tex_path}")

# ── Compile with pdflatex ──────────────────────────────────────────────────────
result = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(table_tex_path)],
    capture_output=True, text=True, cwd=CWD
)
if result.returncode != 0:
    print("pdflatex stdout:", result.stdout[-2000:])
    print("pdflatex stderr:", result.stderr[-1000:])
    sys.exit(1)

# pdflatex names output after the input file: table.pdf → rename to figure.pdf
src_pdf = CWD / "table.pdf"
dst_pdf = CWD / "figure.pdf"
src_pdf.rename(dst_pdf)
print(f"Wrote {dst_pdf}")

# ── Rasterize to PNG (300 dpi) ─────────────────────────────────────────────────
png_path = CWD / "figure.png"
# Try pdftoppm first (poppler), fall back to ImageMagick convert
try:
    r = subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", str(dst_pdf),
         str(CWD / "figure")],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    print(f"Wrote {png_path}")
except (FileNotFoundError, RuntimeError):
    r = subprocess.run(
        ["convert", "-density", "300", str(dst_pdf), str(png_path)],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print("convert stderr:", r.stderr)
        sys.exit(1)
    print(f"Wrote {png_path}")

# ── Write caption.tex ──────────────────────────────────────────────────────────
caption = (
    r"\caption{Comparison of baselines and our model across five LLM benchmarks "
    r"(all metrics in \%). "
    r"Results are mean\,$\pm$\,std over " + str(n_seeds) + r" seeds. "
    r"\textbf{Bold} marks the best result per column; "
    r"ties within one standard deviation of the best are also bolded.}"
)
(CWD / "caption.tex").write_text(caption + "\n")
print(f"Wrote {CWD / 'caption.tex'}")

print("Done.")
