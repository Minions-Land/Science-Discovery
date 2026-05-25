#!/usr/bin/env python3
"""
gen_figure.py — compile equations.tex → figure.pdf and figure.png
"""
import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent.resolve()
TEX = CWD / "equations.tex"
PDF_OUT = CWD / "figure.pdf"
PNG_OUT = CWD / "figure.png"
SVG_OUT = CWD / "figure.svg"


def run(cmd, **kwargs):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, **kwargs)
    return result


def compile_pdf():
    for _ in range(2):  # two passes for cross-references
        run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)],
            cwd=CWD,
        )
    produced = CWD / "equations.pdf"
    if not produced.exists():
        raise FileNotFoundError("pdflatex did not produce equations.pdf")
    shutil.copy(produced, PDF_OUT)
    print(f"PDF written to {PDF_OUT}")


def pdf_to_png():
    # Try pdftoppm (poppler) first, then ImageMagick convert
    try:
        run([
            "pdftoppm",
            "-r", "200",
            "-png",
            "-singlefile",
            str(PDF_OUT),
            str(CWD / "figure"),
        ])
        # pdftoppm writes figure.png directly when -singlefile is set
        if not PNG_OUT.exists():
            raise FileNotFoundError("pdftoppm did not write figure.png")
        print(f"PNG written to {PNG_OUT}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        run([
            "convert",
            "-density", "200",
            "-background", "white",
            "-alpha", "remove",
            str(PDF_OUT),
            str(PNG_OUT),
        ])
        print(f"PNG written to {PNG_OUT} (via ImageMagick)")


def pdf_to_svg():
    try:
        run(["pdf2svg", str(PDF_OUT), str(SVG_OUT)])
        print(f"SVG written to {SVG_OUT}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pdf2svg not available; skipping SVG output")


if __name__ == "__main__":
    compile_pdf()
    pdf_to_png()
    pdf_to_svg()
    print("Done.")
