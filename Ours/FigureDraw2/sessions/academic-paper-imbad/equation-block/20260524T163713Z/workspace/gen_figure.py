#!/usr/bin/env python3
"""Compile equations.tex -> figure.pdf, figure.png, figure.svg."""
import subprocess
import shutil
import os
from pathlib import Path

CWD = Path(__file__).parent
TEX = CWD / "equations.tex"
PDF_OUT = CWD / "figure.pdf"
PNG_OUT = CWD / "figure.png"
SVG_OUT = CWD / "figure.svg"

def run(cmd, **kw):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)
    return result

# --- compile LaTeX ---
run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)])
# second pass for cross-references
run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)])

compiled_pdf = CWD / "equations.pdf"
shutil.copy(compiled_pdf, PDF_OUT)
print(f"PDF: {PDF_OUT}")

# --- rasterise to PNG (300 dpi) ---
# prefer pdftoppm (poppler), fall back to ImageMagick convert
if shutil.which("pdftoppm"):
    run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(PDF_OUT), str(CWD / "figure")])
    # pdftoppm appends nothing when -singlefile; output is figure.png
    if not PNG_OUT.exists():
        # some versions append -1
        candidate = CWD / "figure-1.png"
        if candidate.exists():
            shutil.move(str(candidate), str(PNG_OUT))
    print(f"PNG: {PNG_OUT}")
elif shutil.which("convert"):
    run(["convert", "-density", "300", str(PDF_OUT), "-quality", "95", str(PNG_OUT)])
    print(f"PNG: {PNG_OUT}")
else:
    print("WARNING: neither pdftoppm nor convert found; PNG not generated")

# --- SVG via pdf2svg (optional) ---
if shutil.which("pdf2svg"):
    run(["pdf2svg", str(PDF_OUT), str(SVG_OUT)])
    print(f"SVG: {SVG_OUT}")
else:
    print("INFO: pdf2svg not found; SVG skipped")

# --- clean up LaTeX aux files ---
for ext in (".aux", ".log", ".out"):
    p = CWD / ("equations" + ext)
    if p.exists():
        p.unlink()

print("Done.")
