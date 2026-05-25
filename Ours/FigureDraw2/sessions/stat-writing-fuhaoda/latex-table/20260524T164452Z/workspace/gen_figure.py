#!/usr/bin/env python3
"""Generate a booktabs comparison table from data.json and compile to PDF/PNG."""
import json
import os
import shutil
import subprocess
import glob

cwd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(cwd, "data.json")) as f:
    data = json.load(f)

methods = data["methods"]
metrics = data["metrics"]
values = data["values"]
n_seeds = data["n_seeds"]
groups = data["groups"]

# --- Determine bold cells ---
# Bold the best mean per metric; also bold any method within 1 std of the best.
bold = {m: {metric: False for metric in metrics} for m in methods}
for metric in metrics:
    best_mean = max(values[m][metric]["mean"] for m in methods)
    for m in methods:
        v = values[m][metric]
        if v["mean"] == best_mean:
            bold[m][metric] = True
        elif best_mean - v["mean"] <= v["std"]:
            bold[m][metric] = True


def fmt_cell(mean, std, is_bold):
    inner = f"${mean:.1f}_{{\\pm {std:.2f}}}$"
    return f"\\textbf{{{inner}}}" if is_bold else inner


n_cols = 1 + len(metrics)

# --- Build LaTeX source ---
col_spec = "l" + "c" * len(metrics)

tex = []
tex.append(r"\documentclass[10pt]{article}")
tex.append(r"\usepackage{booktabs}")
tex.append(r"\usepackage{amsmath}")
tex.append(r"\usepackage[a4paper, margin=2cm]{geometry}")
tex.append(r"\usepackage{array}")
tex.append(r"\begin{document}")
tex.append(r"\begin{table}[h]")
tex.append(r"\centering")
tex.append(f"\\begin{{tabular}}{{{col_spec}}}")
tex.append(r"\toprule")

# Column header
tex.append(" & ".join(["Method"] + metrics) + r" \\")
tex.append(r"\midrule")

# Rows grouped
first_group = True
for group in groups:
    if not first_group:
        tex.append(r"\midrule")
    first_group = False
    label = group["label"].capitalize()
    tex.append(
        f"\\multicolumn{{{n_cols}}}{{l}}{{\\textit{{{label}}}}} \\\\"
    )
    for m in group["members"]:
        cells = [m]
        for metric in metrics:
            v = values[m][metric]
            cells.append(fmt_cell(v["mean"], v["std"], bold[m][metric]))
        tex.append(" & ".join(cells) + r" \\")

tex.append(r"\bottomrule")
tex.append(r"\end{tabular}")

caption_body = (
    f"Comparison of methods on five benchmarks "
    f"(mean$\\pm$std over {n_seeds} seeds, all metrics in \\%). "
    f"\\textbf{{Bold}} marks the best result per column; "
    f"a runner-up is also bolded when its mean is within one standard deviation of the best."
)
tex.append(f"\\caption{{{caption_body}}}")
tex.append(r"\end{table}")
tex.append(r"\end{document}")

table_tex_path = os.path.join(cwd, "table.tex")
with open(table_tex_path, "w") as f:
    f.write("\n".join(tex) + "\n")

# --- Write caption.tex ---
caption_tex_path = os.path.join(cwd, "caption.tex")
with open(caption_tex_path, "w") as f:
    f.write(f"\\caption{{{caption_body}}}\n")

# --- Compile with pdflatex ---
for _ in range(2):  # two passes for stable output
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", cwd, table_tex_path],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
if result.returncode != 0:
    print("pdflatex stdout:", result.stdout[-4000:])
    print("pdflatex stderr:", result.stderr[-1000:])
    raise SystemExit("pdflatex failed")

# Copy table.pdf -> figure.pdf
shutil.copy(os.path.join(cwd, "table.pdf"), os.path.join(cwd, "figure.pdf"))

# --- Rasterise to PNG ---
figure_pdf = os.path.join(cwd, "figure.pdf")
figure_png = os.path.join(cwd, "figure.png")

converted = False

# Try ImageMagick convert
try:
    r = subprocess.run(
        ["convert", "-density", "300", figure_pdf, "-quality", "95", figure_png],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        converted = True
except FileNotFoundError:
    pass

# Try pdftoppm (poppler)
if not converted:
    stem = os.path.join(cwd, "figure")
    r = subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", figure_pdf, stem],
        capture_output=True, text=True,
    )
    if r.returncode == 0 and os.path.exists(figure_png):
        converted = True
    else:
        # pdftoppm may produce figure-1.png
        candidates = sorted(glob.glob(stem + "*.png"))
        if candidates:
            shutil.copy(candidates[0], figure_png)
            converted = True

# Try ghostscript
if not converted:
    try:
        r = subprocess.run(
            [
                "gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m",
                "-r300", f"-sOutputFile={figure_png}", figure_pdf,
            ],
            capture_output=True, text=True,
        )
        if r.returncode == 0:
            converted = True
    except FileNotFoundError:
        pass

if not converted:
    raise SystemExit("Could not convert PDF to PNG — install ImageMagick, poppler, or ghostscript")

print("Done: figure.pdf, figure.png, table.tex, caption.tex")
