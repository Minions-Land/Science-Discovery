#!/usr/bin/env python3
"""Render equations.tex -> figure.pdf and figure.png via pdflatex + pdftoppm."""
import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent.resolve()
TEX = CWD / "equations.tex"
PDF_OUT = CWD / "figure.pdf"
PNG_OUT = CWD / "figure.png"


def run(cmd, **kwargs):
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-2000:])
        print("STDERR:", result.stderr[-2000:])
        sys.exit(f"Command failed: {' '.join(str(c) for c in cmd)}")
    return result


def main():
    # Compile twice for cross-references
    for _ in range(2):
        run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)],
            cwd=CWD,
        )

    compiled_pdf = CWD / "equations.pdf"
    if not compiled_pdf.exists():
        sys.exit("pdflatex did not produce equations.pdf")
    shutil.copy(compiled_pdf, PDF_OUT)
    print(f"PDF written to {PDF_OUT}")

    # Convert first page to PNG at 150 dpi
    run(
        ["pdftoppm", "-r", "150", "-png", "-singlefile", str(PDF_OUT), str(CWD / "figure")],
    )
    # pdftoppm appends nothing when -singlefile is used; output is figure.png
    if not PNG_OUT.exists():
        # Some versions append -1
        alt = CWD / "figure-1.png"
        if alt.exists():
            alt.rename(PNG_OUT)
        else:
            sys.exit("pdftoppm did not produce figure.png")
    print(f"PNG written to {PNG_OUT}")


if __name__ == "__main__":
    main()
