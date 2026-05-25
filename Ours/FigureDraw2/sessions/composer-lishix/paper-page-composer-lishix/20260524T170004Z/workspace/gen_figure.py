#!/usr/bin/env python3
"""
Reproducible build script for figure.pdf / figure.png.

Steps:
  1. Compile main.tex -> main.pdf  (pdflatex x3 + bibtex)
  2. Copy main.pdf -> figure.pdf
  3. Rasterise page 1 of figure.pdf -> figure.png  (pdftoppm @ 150 dpi)

Requirements: pdflatex, bibtex, pdftoppm (poppler-utils)
Run from the workspace directory that contains main.tex, references.bib,
and fig01-fig04.pdf.
"""

import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-2000:])
        print(result.stderr[-2000:])
        sys.exit(f"Command failed: {' '.join(cmd)}")


def main() -> None:
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"])
    run(["bibtex", "main"])
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"])
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"])

    shutil.copy(CWD / "main.pdf", CWD / "figure.pdf")

    run([
        "pdftoppm", "-r", "150", "-png",
        "-f", "1", "-l", "1",
        "figure.pdf", "figure_page",
    ])
    (CWD / "figure_page-1.png").rename(CWD / "figure.png")

    print("Done: figure.pdf and figure.png written.")


if __name__ == "__main__":
    main()
