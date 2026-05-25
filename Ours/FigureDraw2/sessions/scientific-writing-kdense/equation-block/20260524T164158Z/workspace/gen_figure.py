#!/usr/bin/env python3
"""Generate figure.pdf and figure.png from equations.tex using pdflatex."""

import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent
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
    # Compile LaTeX -> PDF
    for _ in range(2):  # two passes for cross-references
        run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)],
            cwd=CWD,
        )

    compiled_pdf = CWD / "equations.pdf"
    if not compiled_pdf.exists():
        sys.exit("pdflatex did not produce equations.pdf")
    shutil.copy(compiled_pdf, PDF_OUT)
    print(f"PDF written: {PDF_OUT}")

    # Crop to content (remove blank lower half of page)
    crop_pdf = CWD / "figure_crop.pdf"
    result = subprocess.run(
        ["pdfcrop", str(PDF_OUT), str(crop_pdf)],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and crop_pdf.exists():
        shutil.move(str(crop_pdf), str(PDF_OUT))
        print("PDF cropped with pdfcrop")
    else:
        print("pdfcrop not available or failed — using full page PDF")

    # Rasterise PDF -> PNG at 150 dpi
    # Try pdftoppm first, then ImageMagick convert
    ppm_result = subprocess.run(
        ["pdftoppm", "-r", "150", "-png", "-singlefile", str(PDF_OUT),
         str(CWD / "figure")],
        capture_output=True, text=True,
    )
    if ppm_result.returncode == 0:
        # pdftoppm outputs figure.png (or figure-1.png on some versions)
        candidate = CWD / "figure.png"
        candidate2 = CWD / "figure-1.png"
        if not candidate.exists() and candidate2.exists():
            shutil.move(str(candidate2), str(candidate))
        print(f"PNG written: {PNG_OUT}")
    else:
        # Fallback: ImageMagick
        run(
            ["convert", "-density", "150", str(PDF_OUT), str(PNG_OUT)],
        )
        print(f"PNG written via ImageMagick: {PNG_OUT}")


if __name__ == "__main__":
    main()
