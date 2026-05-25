#!/usr/bin/env python3
"""
gen_figure.py — compile equations.tex → figure.pdf and figure.png
"""
import subprocess
import shutil
import os
import sys

CWD = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(CWD, "equations.tex")
PDF_SRC = os.path.join(CWD, "equations.pdf")
PDF_DST = os.path.join(CWD, "figure.pdf")
PNG_DST = os.path.join(CWD, "figure.png")
SVG_DST = os.path.join(CWD, "figure.svg")


def run(cmd, **kw):
    result = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-3000:])
        print("STDERR:", result.stderr[-3000:])
        sys.exit(result.returncode)
    return result


def main():
    # --- compile LaTeX (twice for cross-refs) ---
    for _ in range(2):
        run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", CWD, TEX],
            cwd=CWD,
        )

    shutil.copy2(PDF_SRC, PDF_DST)
    print(f"PDF written to {PDF_DST}")

    # --- rasterise with pdftoppm (poppler) or ImageMagick convert ---
    if shutil.which("pdftoppm"):
        run(
            ["pdftoppm", "-r", "300", "-png", "-singlefile",
             PDF_DST, os.path.join(CWD, "figure")],
            cwd=CWD,
        )
        # pdftoppm appends nothing when -singlefile; check both
        if not os.path.exists(PNG_DST):
            candidate = os.path.join(CWD, "figure-1.png")
            if os.path.exists(candidate):
                shutil.move(candidate, PNG_DST)
    elif shutil.which("convert"):
        run(
            ["convert", "-density", "300", PDF_DST, "-quality", "95", PNG_DST],
            cwd=CWD,
        )
    else:
        sys.exit("Neither pdftoppm nor convert (ImageMagick) found — install poppler or ImageMagick.")

    print(f"PNG written to {PNG_DST}")

    # --- optional SVG via pdf2svg ---
    if shutil.which("pdf2svg"):
        run(["pdf2svg", PDF_DST, SVG_DST], cwd=CWD)
        print(f"SVG written to {SVG_DST}")
    else:
        print("pdf2svg not found — skipping SVG (optional).")


if __name__ == "__main__":
    main()
