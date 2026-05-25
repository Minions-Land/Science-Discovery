#!/usr/bin/env python3
"""
gen_figure.py — reproducible build script for the RetroDiff paper section.

Inputs (must exist in cwd):
  fig01.pdf, fig02.pdf, fig03.pdf, fig04.pdf
  references.bib
  main.tex

Outputs:
  main.pdf       — full 3-page compiled paper
  figure.pdf     — copy of main.pdf (satisfies /goal figure requirement)
  figure.png     — PNG render of page 1 at 150 DPI
  compile.log    — final pdflatex pass log
"""

import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent


def run(cmd, **kwargs):
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print(result.stdout[-2000:])
        print(result.stderr[-2000:])
        sys.exit(f"Command failed: {' '.join(cmd)}")
    return result


def build():
    # Full pdflatex + bibtex + pdflatex x2 cycle
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"])
    run(["bibtex", "main"])
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"])
    result = run(["pdflatex", "-interaction=nonstopmode", "main.tex"])

    # Save compile log
    (CWD / "compile.log").write_text(result.stdout)

    # Copy to figure.pdf
    shutil.copy(CWD / "main.pdf", CWD / "figure.pdf")

    # Render page 1 to PNG at 150 DPI
    run(["pdftoppm", "-r", "150", "-png", "-f", "1", "-l", "1",
         "figure.pdf", str(CWD / "figure_page")])
    page_file = CWD / "figure_page-1.png"
    if page_file.exists():
        page_file.rename(CWD / "figure.png")

    print("Build complete:")
    for f in ["main.pdf", "figure.pdf", "figure.png", "compile.log"]:
        p = CWD / f
        print(f"  {f}: {p.stat().st_size // 1024} KB" if p.exists() else f"  {f}: MISSING")


if __name__ == "__main__":
    build()
