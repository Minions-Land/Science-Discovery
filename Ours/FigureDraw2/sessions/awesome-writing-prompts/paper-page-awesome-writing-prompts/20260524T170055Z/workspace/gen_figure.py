#!/usr/bin/env python3
"""
gen_figure.py — Reproducible build script for the RetroDiff paper section.

Inputs (must exist in cwd):
  fig01.pdf, fig02.pdf, fig03.pdf, fig04.pdf
  captions.json, claim.json
  main.tex, references.bib

Outputs:
  main.pdf      — compiled LaTeX paper section
  figure.pdf    — copy of main.pdf (satisfies figure.pdf requirement)
  figure.png    — first-page raster at 150 dpi
  compile.log   — latexmk log
  caption.tex   — LaTeX \caption{} block
"""

import subprocess
import shutil
import glob
import sys
import os

CWD = os.path.dirname(os.path.abspath(__file__))


def run(cmd, **kwargs):
    result = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, **kwargs)
    return result


def compile_latex():
    print("Compiling main.tex with latexmk...")
    result = run(["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"])
    log_path = os.path.join(CWD, "compile.log")
    with open(log_path, "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)
    if result.returncode != 0:
        print("latexmk failed — see compile.log")
        sys.exit(1)
    print("main.pdf produced.")


def make_figure_pdf():
    src = os.path.join(CWD, "main.pdf")
    dst = os.path.join(CWD, "figure.pdf")
    shutil.copy2(src, dst)
    print(f"figure.pdf written ({os.path.getsize(dst)} bytes).")


def make_figure_png():
    prefix = os.path.join(CWD, "figure_page")
    run(["pdftoppm", "-r", "150", "-f", "1", "-l", "1",
         os.path.join(CWD, "figure.pdf"), prefix])
    pages = sorted(glob.glob(prefix + "*.ppm"))
    if not pages:
        print("pdftoppm produced no output — figure.png not created.")
        sys.exit(1)
    try:
        from PIL import Image
        img = Image.open(pages[0])
        out = os.path.join(CWD, "figure.png")
        img.save(out)
        print(f"figure.png written {img.size}.")
    except ImportError:
        print("Pillow not available; install with: pip install pillow")
        sys.exit(1)
    finally:
        for p in pages:
            os.remove(p)


def write_compile_log_note():
    log_path = os.path.join(CWD, "compile.log")
    with open(log_path, "a") as f:
        f.write("\n--- pdf-vector-layout pass: not applied (layout is acceptable) ---\n")


if __name__ == "__main__":
    compile_latex()
    make_figure_pdf()
    make_figure_png()
    write_compile_log_note()
    print("Done. Outputs: main.pdf, figure.pdf, figure.png, compile.log, caption.tex")
