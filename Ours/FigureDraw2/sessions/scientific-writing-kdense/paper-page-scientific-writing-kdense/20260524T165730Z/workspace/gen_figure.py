#!/usr/bin/env python3
"""
Reproducible build script for the RetroDiff paper section.

Inputs  (must exist in cwd):
  fig01.pdf, fig02.pdf, fig03.pdf, fig04.pdf
  captions.json, claim.json
  main.tex, references.bib

Outputs (written to cwd):
  main.pdf, compile.log
  figure.pdf  (copy of main.pdf)
  figure.png  (page-1 raster at 150 dpi)
"""

import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent


def run(cmd, **kwargs):
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}", file=sys.stderr)
        print(result.stdout[-2000:], file=sys.stderr)
        print(result.stderr[-2000:], file=sys.stderr)
        sys.exit(result.returncode)
    return result


def main():
    latex = ["pdflatex", "-interaction=nonstopmode", "main.tex"]

    run(latex)
    run(["bibtex", "main"])
    run(latex)
    run(latex)

    log = (CWD / "main.log").read_text(errors="replace")
    (CWD / "compile.log").write_text(log)

    shutil.copy(CWD / "main.pdf", CWD / "figure.pdf")

    run(["pdftoppm", "-r", "150", "-png", "-singlefile",
         str(CWD / "figure.pdf"), str(CWD / "figure")])

    print("Build complete: main.pdf, figure.pdf, figure.png")


if __name__ == "__main__":
    main()
