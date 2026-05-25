#!/usr/bin/env python3
"""Compile equations.tex -> figure.pdf, then rasterise to figure.png."""
import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent
TEX = CWD / "equations.tex"
PDF_OUT = CWD / "figure.pdf"
PNG_OUT = CWD / "figure.png"


def run(cmd, **kwargs):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, **kwargs)
    return result


def compile_pdf():
    # Run pdflatex twice for cross-references
    for _ in range(2):
        run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)],
            cwd=CWD,
        )
    # pdflatex names output after the .tex stem
    generated = CWD / "equations.pdf"
    if generated.exists():
        shutil.move(str(generated), str(PDF_OUT))
    if not PDF_OUT.exists():
        sys.exit("pdflatex did not produce a PDF")


def rasterise_png():
    # Prefer pdftoppm (poppler), fall back to ImageMagick convert
    if shutil.which("pdftoppm"):
        run(
            [
                "pdftoppm",
                "-r", "200",
                "-png",
                "-singlefile",
                str(PDF_OUT),
                str(CWD / "figure"),
            ]
        )
        # pdftoppm appends nothing when -singlefile is used
        if not PNG_OUT.exists():
            # some versions append -1
            candidate = CWD / "figure-1.png"
            if candidate.exists():
                shutil.move(str(candidate), str(PNG_OUT))
    elif shutil.which("convert"):
        run(
            [
                "convert",
                "-density", "200",
                str(PDF_OUT),
                "-quality", "95",
                str(PNG_OUT),
            ]
        )
    else:
        sys.exit("Neither pdftoppm nor ImageMagick convert found; cannot rasterise PDF.")


if __name__ == "__main__":
    compile_pdf()
    rasterise_png()
    print(f"Done: {PDF_OUT}  {PNG_OUT}")
