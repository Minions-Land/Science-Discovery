#!/usr/bin/env python3
"""Generate figure.pdf and figure.png from equations.tex using pdflatex."""
import subprocess
import shutil
import sys
from pathlib import Path

CWD = Path(__file__).parent.resolve()
TEX = CWD / "equations.tex"


def run(cmd, **kw):
    result = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-2000:])
        sys.exit(result.returncode)
    return result


# --- compile PDF ---
run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)],
    cwd=CWD,
)
# second pass for cross-references
run(
    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(CWD), str(TEX)],
    cwd=CWD,
)

pdf_src = CWD / "equations.pdf"
pdf_dst = CWD / "figure.pdf"
shutil.copy(pdf_src, pdf_dst)
print(f"PDF written to {pdf_dst}")

# --- rasterise to PNG ---
# Try pdftoppm (poppler), then ImageMagick convert, then ghostscript
png_dst = CWD / "figure.png"

def try_pdftoppm():
    r = subprocess.run(
        ["pdftoppm", "-r", "200", "-png", "-singlefile", str(pdf_dst),
         str(CWD / "figure")],
        capture_output=True, text=True,
    )
    return r.returncode == 0

def try_imagemagick():
    r = subprocess.run(
        ["convert", "-density", "200", str(pdf_dst), str(png_dst)],
        capture_output=True, text=True,
    )
    return r.returncode == 0

def try_ghostscript():
    r = subprocess.run(
        ["gs", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m",
         "-r200", f"-sOutputFile={png_dst}", str(pdf_dst)],
        capture_output=True, text=True,
    )
    return r.returncode == 0

def try_matplotlib_pdf2image():
    try:
        from pdf2image import convert_from_path
        pages = convert_from_path(str(pdf_dst), dpi=200)
        pages[0].save(str(png_dst))
        return True
    except Exception:
        return False

for fn in (try_pdftoppm, try_imagemagick, try_ghostscript, try_matplotlib_pdf2image):
    if fn():
        print(f"PNG written to {png_dst}")
        break
else:
    print("WARNING: could not rasterise PDF to PNG — install poppler, ImageMagick, or ghostscript")
    sys.exit(1)


# --- SVG (optional, via pdf2svg) ---
svg_dst = CWD / "figure.svg"
if shutil.which("pdf2svg"):
    r = subprocess.run(
        ["pdf2svg", str(pdf_dst), str(svg_dst)],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        print(f"SVG written to {svg_dst}")
    else:
        print("pdf2svg failed — skipping SVG (optional)")
else:
    print("pdf2svg not available — skipping SVG (optional)")

print("Done.")
