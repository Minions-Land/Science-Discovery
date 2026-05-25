#!/usr/bin/env python3
"""
Compile the LaTeX paper and produce figure.pdf / figure.png.

Requires: pdflatex, bibtex, pdftoppm (poppler-utils)
Run from the workspace directory containing main.tex and fig01-04.pdf.
"""

import subprocess
import shutil
from pathlib import Path


def run(cmd, **kwargs):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True, **kwargs)
    if result.returncode != 0:
        print(result.stdout[-2000:])
        print(result.stderr[-2000:])
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def main():
    run("pdflatex -interaction=nonstopmode main.tex")
    run("bibtex main")
    run("pdflatex -interaction=nonstopmode main.tex")
    run("pdflatex -interaction=nonstopmode main.tex")

    # Copy main.pdf -> figure.pdf (the paper IS the figure deliverable)
    shutil.copy("main.pdf", "figure.pdf")

    # Rasterize page 1 -> figure.png
    run("pdftoppm -r 150 -png -f 1 -l 1 main.pdf figure_page")
    shutil.copy("figure_page-1.png", "figure.png")

    # Save compile.log summary
    log = Path("main.log").read_text()
    summary_lines = [l for l in log.splitlines()
                     if any(kw in l for kw in ("Warning", "Error", "Output written"))]
    Path("compile.log").write_text("\n".join(summary_lines))

    print("Done. Outputs: main.pdf, figure.pdf, figure.png, compile.log")


if __name__ == "__main__":
    main()
