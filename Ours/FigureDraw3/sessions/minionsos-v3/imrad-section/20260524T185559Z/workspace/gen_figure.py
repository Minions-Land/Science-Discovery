#!/usr/bin/env python3
"""Compile main.tex to figure.pdf and figure.png."""

import subprocess
import shutil
import os
import sys
from pathlib import Path

CWD = Path(__file__).parent.resolve()


def run(cmd, **kwargs):
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-2000:] if result.stdout else "")
        print("STDERR:", result.stderr[-2000:] if result.stderr else "")
        sys.exit(f"Command failed: {' '.join(cmd)}")
    return result


def main():
    # Compile twice to resolve references
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])

    pdf_src = CWD / "main.pdf"
    pdf_dst = CWD / "figure.pdf"
    shutil.copy2(pdf_src, pdf_dst)
    print(f"Wrote {pdf_dst}")

    # Convert first page to PNG at 150 dpi
    png_dst = CWD / "figure.png"
    # Try pdftoppm first (poppler), fall back to ImageMagick convert
    pdftoppm = shutil.which("pdftoppm")
    convert = shutil.which("convert")
    if pdftoppm:
        run([
            "pdftoppm", "-r", "150", "-png", "-singlefile",
            str(pdf_dst), str(CWD / "figure")
        ])
        # pdftoppm writes figure.png directly with -singlefile
        if not png_dst.exists():
            # Some versions append -1
            candidate = CWD / "figure-1.png"
            if candidate.exists():
                candidate.rename(png_dst)
    elif convert:
        run([
            "convert", "-density", "150",
            f"{pdf_dst}[0]", str(png_dst)
        ])
    else:
        sys.exit("Neither pdftoppm nor ImageMagick convert found; install poppler-utils or imagemagick.")

    print(f"Wrote {png_dst}")

    # Optional SVG via pdf2svg
    pdf2svg = shutil.which("pdf2svg")
    if pdf2svg:
        svg_dst = CWD / "figure.svg"
        run(["pdf2svg", str(pdf_dst), str(svg_dst), "1"])
        print(f"Wrote {svg_dst}")
    else:
        print("pdf2svg not found; skipping SVG (optional).")


if __name__ == "__main__":
    main()
