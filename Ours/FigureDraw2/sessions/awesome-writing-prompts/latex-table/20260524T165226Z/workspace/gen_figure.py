#!/usr/bin/env python3
import json, os, shutil, subprocess

CWD = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(CWD, "data.json")) as f:
    data = json.load(f)

methods = data["methods"]
metrics = data["metrics"]
values  = data["values"]
groups  = data["groups"]
n_seeds = data["n_seeds"]

# ── bold logic ────────────────────────────────────────────────────────────────
def best_for(metric):
    return max(methods, key=lambda m: values[m][metric]["mean"])

def should_bold(method, metric):
    bm        = best_for(metric)
    best_mean = values[bm][metric]["mean"]
    best_std  = values[bm][metric]["std"]
    m_mean    = values[method][metric]["mean"]
    m_std     = values[method][metric]["std"]
    if method == bm:
        return True
    return (best_mean - m_mean) <= max(best_std, m_std)

def fmt_cell(method, metric):
    mean = values[method][metric]["mean"]
    std  = values[method][metric]["std"]
    cell = f"${mean:.1f}_{{\\pm {std:.2f}}}$"
    if should_bold(method, metric):
        cell = f"\\textbf{{{cell}}}"
    return cell

# ── build LaTeX ───────────────────────────────────────────────────────────────
ncols = 1 + len(metrics)
col_spec = "@{}l" + "r" * len(metrics) + "@{}"

def method_display(method, group_label):
    if group_label == "ours":
        return f"\\textbf{{{method}}}"
    return method

rows = []
rows += [
    r"\documentclass{article}",
    r"\usepackage[margin=0.5in,paperwidth=7in,paperheight=3in]{geometry}",
    r"\usepackage{booktabs}",
    r"\usepackage{amsmath}",
    r"\usepackage{array}",
    r"\usepackage[T1]{fontenc}",
    r"\pagestyle{empty}",
    r"\begin{document}",
    r"\centering",
    f"\\begin{{tabular}}{{{col_spec}}}",
    r"\toprule",
]

# header
hdr = " & ".join(
    f"\\textbf{{{m}}} (\\%)" for m in metrics
)
rows.append(f"\\textbf{{Method}} & {hdr} \\\\")
rows.append(r"\midrule")

for g_idx, group in enumerate(groups):
    label = group["label"].capitalize()
    rows.append(f"\\multicolumn{{{ncols}}}{{l}}{{\\textit{{{label}}}}} \\\\[1pt]")
    for method in group["members"]:
        cells   = " & ".join(fmt_cell(method, metric) for metric in metrics)
        display = method_display(method, group["label"])
        rows.append(f"\\quad {display} & {cells} \\\\")
    if g_idx < len(groups) - 1:
        rows.append(r"\midrule")

rows += [
    r"\bottomrule",
    r"\end{tabular}",
    r"\end{document}",
]

tex_src = "\n".join(rows)

# ── write table.tex ───────────────────────────────────────────────────────────
table_tex = os.path.join(CWD, "table.tex")
with open(table_tex, "w") as f:
    f.write(tex_src)

# ── compile ───────────────────────────────────────────────────────────────────
res = subprocess.run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", CWD, table_tex],
    capture_output=True, text=True, cwd=CWD,
)
if res.returncode != 0:
    print(res.stdout[-3000:])
    raise RuntimeError("pdflatex failed")

shutil.copy(os.path.join(CWD, "table.pdf"), os.path.join(CWD, "figure.pdf"))

# ── rasterise → PNG ───────────────────────────────────────────────────────────
figure_pdf = os.path.join(CWD, "figure.pdf")
figure_png = os.path.join(CWD, "figure.png")
figure_base = os.path.join(CWD, "figure")

r = subprocess.run(
    ["pdftoppm", "-r", "300", "-png", "-singlefile", figure_pdf, figure_base],
    capture_output=True,
)
if r.returncode != 0:
    subprocess.run(
        ["convert", "-density", "300", figure_pdf, figure_png], check=True
    )

# ── optional SVG ─────────────────────────────────────────────────────────────
figure_svg = os.path.join(CWD, "figure.svg")
for cmd in [
    ["pdf2svg", figure_pdf, figure_svg],
    ["inkscape", "--export-plain-svg", figure_svg, figure_pdf],
]:
    try:
        r2 = subprocess.run(cmd, capture_output=True)
        if r2.returncode == 0:
            break
    except FileNotFoundError:
        continue

print("Done — figure.pdf, figure.png written.")
