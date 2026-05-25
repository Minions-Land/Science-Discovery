#!/usr/bin/env python3
"""Compile equations.tex -> figure.pdf, figure.png, figure.svg."""
import subprocess
import shutil
import os
from pathlib import Path

CWD = Path(__file__).parent.resolve()
TEX = CWD / "equations.tex"


def run(cmd, **kw):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)
    return result


def main():
    # Run pdflatex twice (for cross-references)
    for _ in range(2):
        run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)])

    # Rename output to figure.pdf
    src_pdf = CWD / "equations.pdf"
    dst_pdf = CWD / "figure.pdf"
    shutil.copy(src_pdf, dst_pdf)
    print(f"Written: {dst_pdf}")

    # Convert to PNG (300 dpi) using pdftoppm or ImageMagick
    dst_png = CWD / "figure.png"
    if shutil.which("pdftoppm"):
        run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(dst_pdf), str(CWD / "figure")])
        # pdftoppm appends nothing when -singlefile is used
        if not dst_png.exists():
            # some versions append -1
            candidate = CWD / "figure-1.png"
            if candidate.exists():
                shutil.move(str(candidate), str(dst_png))
        print(f"Written: {dst_png}")
    elif shutil.which("convert"):
        run(["convert", "-density", "300", str(dst_pdf), "-quality", "95", str(dst_png)])
        print(f"Written: {dst_png}")
    else:
        raise RuntimeError("Neither pdftoppm nor ImageMagick convert found.")

    # Optional SVG via pdf2svg
    dst_svg = CWD / "figure.svg"
    if shutil.which("pdf2svg"):
        run(["pdf2svg", str(dst_pdf), str(dst_svg)])
        print(f"Written: {dst_svg}")

    # Clean up auxiliary files
    for ext in (".aux", ".log", ".out"):
        f = CWD / ("equations" + ext)
        if f.exists():
            f.unlink()


if __name__ == "__main__":
    main()
