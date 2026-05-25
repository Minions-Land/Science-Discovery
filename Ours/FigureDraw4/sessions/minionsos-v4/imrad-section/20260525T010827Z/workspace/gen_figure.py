#!/usr/bin/env python3
"""
gen_figure.py — compile main.tex to figure.pdf and figure.png.

Inputs:  main.tex (in cwd)
Outputs: figure.pdf, figure.png (in cwd)

Requirements: pdflatex, pdftocairo (poppler-utils)
"""
import subprocess
import sys
import pathlib
import shutil
import re

CWD = pathlib.Path(__file__).parent


def run(cmd, **kwargs):
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        sys.exit(result.returncode)
    return result


def check_pdflatex():
    if not shutil.which("pdflatex"):
        sys.exit("ERROR: pdflatex not found. Install TeX Live or MacTeX.")
    if not shutil.which("pdftocairo"):
        sys.exit("ERROR: pdftocairo not found. Install poppler-utils.")


def compile_latex():
    # Two passes: first for content, second for hyperref outlines.
    for _ in range(2):
        run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])


def check_fonts(pdf_path: pathlib.Path):
    result = subprocess.run(
        ["pdffonts", str(pdf_path)], capture_output=True, text=True, check=False
    )
    if "Type 3" in result.stdout:
        sys.stderr.write(
            f"FATAL: {pdf_path} contains Type-3 bitmap fonts.\n{result.stdout}\n"
        )
        sys.exit(2)
    # Fallback: raw byte check when pdffonts is unavailable.
    raw = pdf_path.read_bytes()
    if re.search(rb"/Subtype\s*/Type3\b", raw):
        sys.stderr.write(f"FATAL: /Type3 found in {pdf_path}.\n")
        sys.exit(2)
    print(f"[fonttype-check] OK — no Type-3 fonts in {pdf_path}")


def export_png(pdf_path: pathlib.Path, png_path: pathlib.Path):
    run(
        [
            "pdftocairo",
            "-png",
            "-r", "200",
            "-singlefile",
            str(pdf_path),
            str(png_path.with_suffix("")),
        ]
    )


def main():
    check_pdflatex()
    compile_latex()

    main_pdf = CWD / "main.pdf"
    figure_pdf = CWD / "figure.pdf"
    figure_png = CWD / "figure.png"

    shutil.copy2(main_pdf, figure_pdf)
    check_fonts(figure_pdf)
    export_png(figure_pdf, figure_png)

    print(f"[gen_figure] figure.pdf  {figure_pdf.stat().st_size // 1024} KB")
    print(f"[gen_figure] figure.png  {figure_png.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
