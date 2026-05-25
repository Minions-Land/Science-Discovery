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

def fmt_cell(mean, std):
    # Build LaTeX: $72.4_{\pm 1.41}$ — avoid backslash in f-string by using concat
    return "$" + f"{mean:.1f}" + r"_{\pm " + f"{std:.2f}" + "}$"

def fmt_cell_bold(mean, std):
    inner = fmt_cell(mean, std)
    return r"\textbf{" + inner + "}"

def is_best(method, metric, data):
    """True if this method has the highest mean OR overlaps within 1 std of the highest mean."""
    values = data["values"]
    best_mean = max(values[m][metric]["mean"] for m in data["methods"])
    mean = values[method][metric]["mean"]
    std  = values[method][metric]["std"]
    # Bold if: this method IS the best OR its [mean+std] >= best_mean
    return mean + std >= best_mean

def build_cell(method, metric, data):
    v = data["values"][method][metric]
    mean, std = v["mean"], v["std"]
    cell = fmt_cell(mean, std)
    if is_best(method, metric, data):
        return r"\textbf{" + cell + "}"
    return cell

def make_table_tex(data):
    methods = data["methods"]
    metrics = data["metrics"]
    groups  = data["groups"]

    # Group-spanning header
    baselines = groups[0]["members"]   # ["Baseline","Method-A","Method-B"]
    ours      = groups[1]["members"]   # ["OursModel"]

    n_base = len(baselines)
    n_ours = len(ours)
    n_total = len(methods)
    n_cols = 1 + n_total  # Method col + metric cols ... wait, columns are Method + one per metric

    # Actually: rows=methods, cols=metrics
    # Table: Method | MMLU | HumanEval | GSM8K | MATH | GPQA
    # Rows grouped: baselines block then ours block

    col_spec = "l" + "c" * len(metrics)

    lines = []
    lines.append(r"\begin{tabular}{" + col_spec + "}")
    lines.append(r"\toprule")

    # Header row
    metric_headers = " & ".join(r"\textbf{" + m + "}" for m in metrics)
    lines.append(r"\textbf{Method} & " + metric_headers + r" \\")
    lines.append(r"\midrule")

    # Group partial-rule spans and group labels
    # We'll emit a \multicolumn cmidrule label row per group
    for grp_idx, grp in enumerate(groups):
        members = grp["members"]
        label   = grp["label"].capitalize()

        # Group label row (spanning all columns)
        lines.append(
            r"\multicolumn{" + str(1 + len(metrics)) + r"}{l}{\textit{" + label + r"}} \\"
        )

        for method in members:
            cells = [build_cell(method, metric, data) for metric in metrics]
            # Distinguish "OursModel" with a nicer display name
            display = method if method != "OursModel" else r"\textbf{Ours}"
            lines.append(display + " & " + " & ".join(cells) + r" \\")

        if grp_idx < len(groups) - 1:
            lines.append(r"\midrule")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)

def make_standalone_tex(table_body):
    return r"""\documentclass{article}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{array}
\pagestyle{empty}
\begin{document}
\centering
""" + table_body + r"""
\end{document}
"""

def main():
    data = load_data()

    table_body = make_table_tex(data)

    # Write table.tex (standalone compilable)
    standalone = make_standalone_tex(table_body)
    table_tex_path = CWD / "table.tex"
    table_tex_path.write_text(standalone)
    print(f"Wrote {table_tex_path}")

    # Compile with pdflatex
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(table_tex_path)],
        capture_output=True, text=True, cwd=str(CWD)
    )
    if result.returncode != 0:
        print("pdflatex stdout:", result.stdout[-3000:])
        print("pdflatex stderr:", result.stderr[-1000:])
        sys.exit(1)

    # pdflatex outputs table.pdf; crop with pdfcrop if available, then copy to figure.pdf
    src_pdf = CWD / "table.pdf"
    dst_pdf = CWD / "figure.pdf"
    if not src_pdf.exists():
        print("ERROR: table.pdf not produced")
        sys.exit(1)

    crop_result = subprocess.run(
        ["pdfcrop", str(src_pdf), str(dst_pdf)],
        capture_output=True, text=True
    )
    if crop_result.returncode != 0:
        import shutil
        shutil.copy(src_pdf, dst_pdf)
    print(f"Wrote {dst_pdf}")

    # Rasterize to figure.png at 300 dpi
    result2 = subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", str(dst_pdf),
         str(CWD / "figure")],
        capture_output=True, text=True
    )
    if result2.returncode != 0:
        # Try ImageMagick convert as fallback
        result2b = subprocess.run(
            ["magick", "-density", "300", str(dst_pdf), str(CWD / "figure.png")],
            capture_output=True, text=True
        )
        if result2b.returncode != 0:
            result2c = subprocess.run(
                ["convert", "-density", "300", str(dst_pdf), str(CWD / "figure.png")],
                capture_output=True, text=True
            )
            if result2c.returncode != 0:
                print("WARNING: could not rasterize PDF to PNG automatically")
                print(result2.stderr)
    print(f"Wrote {CWD / 'figure.png'}")

    # Write caption.tex
    n_seeds = data.get("n_seeds", 5)
    caption = (
        r"\caption{Comparison of four methods on five LLM benchmarks (all metrics in \%). "
        r"Results are averaged over " + str(n_seeds) + r" random seeds. "
        r"\textbf{Bold} entries indicate the best result per metric; "
        r"multiple entries are bolded when their means overlap within one standard deviation. "
        r"$\pm$ values denote standard deviation.}"
    )
    caption_path = CWD / "caption.tex"
    caption_path.write_text(caption + "\n")
    print(f"Wrote {caption_path}")

if __name__ == "__main__":
    main()
