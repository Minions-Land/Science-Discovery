#!/usr/bin/env python3
"""Generate figure.pdf and figure.png from equations.tex using pdflatex + pdftoppm."""
import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent
TEX = "equations.tex"
BASE = "equations"


def run(cmd, **kw):
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, **kw)
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-2000:])
        print("STDERR:", result.stderr[-2000:])
        sys.exit(result.returncode)
    return result


# Compile twice so \eqref labels resolve
for _ in range(2):
    run(["pdflatex", "-interaction=nonstopmode", TEX])

# Rename to figure.pdf
pdf_src = CWD / f"{BASE}.pdf"
pdf_dst = CWD / "figure.pdf"
shutil.copy(pdf_src, pdf_dst)
print(f"Written: {pdf_dst}")

# Raster to PNG at 150 dpi via pdftoppm (poppler)
png_prefix = CWD / "figure"
result = subprocess.run(
    ["pdftoppm", "-r", "150", "-png", "-singlefile", str(pdf_dst), str(png_prefix)],
    capture_output=True, text=True,
)
if result.returncode != 0:
    # Fallback: try ImageMagick convert
    print("pdftoppm failed, trying ImageMagick convert...")
    run(["convert", "-density", "150", str(pdf_dst), str(CWD / "figure.png")])
else:
    # pdftoppm -singlefile writes <prefix>.png
    produced = CWD / "figure.png"
    if not produced.exists():
        # some versions append -1
        alt = CWD / "figure-1.png"
        if alt.exists():
            shutil.move(str(alt), str(produced))
    print(f"Written: {produced}")

print("Done.")
