#!/usr/bin/env python3
"""Compile equations.tex -> figure.pdf, then rasterise to figure.png."""
import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent.resolve()
TEX = CWD / "equations.tex"
PDF_SRC = CWD / "equations.pdf"
PDF_DST = CWD / "figure.pdf"
PNG_DST = CWD / "figure.png"
SVG_DST = CWD / "figure.svg"


def run(cmd, **kw):
    result = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-2000:])
        print("STDERR:", result.stderr[-2000:])
        sys.exit(result.returncode)
    return result


# --- compile (twice for cross-refs) ---
for _ in range(2):
    run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)], cwd=CWD)

shutil.copy2(PDF_SRC, PDF_DST)
print(f"PDF: {PDF_DST}")

# --- rasterise to PNG (prefer pdftoppm, fall back to ImageMagick convert) ---
if shutil.which("pdftoppm"):
    run(["pdftoppm", "-r", "200", "-png", "-singlefile", str(PDF_DST), str(CWD / "figure")])
    # pdftoppm writes figure.png directly when -singlefile is used
    if not PNG_DST.exists():
        # some versions append -1
        candidate = CWD / "figure-1.png"
        if candidate.exists():
            shutil.move(str(candidate), str(PNG_DST))
    print(f"PNG: {PNG_DST}")
elif shutil.which("convert"):
    run(["convert", "-density", "200", str(PDF_DST), str(PNG_DST)])
    print(f"PNG: {PNG_DST}")
else:
    print("WARNING: neither pdftoppm nor convert found; PNG not produced.")
    sys.exit(1)

# --- optional SVG via pdf2svg ---
if shutil.which("pdf2svg"):
    run(["pdf2svg", str(PDF_DST), str(SVG_DST)])
    print(f"SVG: {SVG_DST}")

print("Done.")
