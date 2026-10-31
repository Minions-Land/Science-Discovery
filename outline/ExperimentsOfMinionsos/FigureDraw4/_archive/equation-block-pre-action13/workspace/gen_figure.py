#!/usr/bin/env python3
"""Generate figure.pdf and figure.png from equations.tex via pdflatex."""
import subprocess
import shutil
import os
import sys

CWD = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(CWD, "equations.tex")


def run(cmd, **kw):
    result = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-2000:])
        print("STDERR:", result.stderr[-2000:])
        sys.exit(result.returncode)
    return result


# 1. Compile twice to resolve cross-references
for _ in range(2):
    run(["pdflatex", "-interaction=nonstopmode", "-output-directory", CWD, TEX])

# 2. Copy / rename to figure.pdf
src_pdf = os.path.join(CWD, "equations.pdf")
dst_pdf = os.path.join(CWD, "figure.pdf")
shutil.copy2(src_pdf, dst_pdf)

# 3. Rasterise to figure.png at 200 dpi via pdftoppm
ppm_prefix = os.path.join(CWD, "_fig_raster")
run(["pdftoppm", "-r", "200", "-png", "-singlefile", dst_pdf, ppm_prefix])
raster = ppm_prefix + ".png"
shutil.move(raster, os.path.join(CWD, "figure.png"))

# 4. Optional SVG via pdf2svg
svg_path = os.path.join(CWD, "figure.svg")
try:
    r = subprocess.run(
        ["pdf2svg", dst_pdf, svg_path],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print("pdf2svg failed — skipping figure.svg")
except FileNotFoundError:
    print("pdf2svg not available — skipping figure.svg")

print("Done: figure.pdf, figure.png written to", CWD)
