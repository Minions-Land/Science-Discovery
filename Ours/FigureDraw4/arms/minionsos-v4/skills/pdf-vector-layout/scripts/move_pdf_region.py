#!/usr/bin/env python3
"""Move a region of a PDF page to a new location, preserving vectors AND text.

The transform edits the page's content stream directly: every "atomic unit"
(q/Q frame, BT/ET text block, m/re...paint path, or standalone Do) is
classified by its page-coords y-bbox into one of three buckets — entirely
in the moving region, entirely outside, or straddling the boundary. In-region
units get wrapped with `q 1 0 0 1 0 SHIFT_Y cm ... Q`; outside units pass
through unchanged; straddling q/Q frames are recursed into.

Why this matters: the obvious shortcut is to clone the source page with a
narrow cropbox/mediabox and stamp it three times (above region, shifted
region, below region). The render looks right, but pypdf-style cropbox
metadata does NOT clip the content stream — pdftotext, copy/paste, search,
and screen readers see THREE copies of the full page. The content-stream
edit below makes the text layer match the visual layer.

Usage:
    1. Render the source PDF to PNG at 150 DPI to measure coords.
    2. Edit the constants below.
    3. python move_pdf_region.py
    4. Render the output and verify with verify_vector.py.
"""

from pathlib import Path

import pikepdf
from pikepdf import Operator

# ============================================================================
# Configuration — EDIT THESE
# ============================================================================

INPUT_PDF = Path("source.pdf")
OUTPUT_PDF = Path("output_shifted.pdf")

# Region to move (in PDF points, origin at bottom-left, y-axis points up)
REGION_BOTTOM = 100.0
REGION_TOP = 300.0
SHIFT_Y = -50.0  # negative = down, positive = up


def y_px_to_pt(y_px, img_height_px, pdf_height_pt):
    """Convert pixel y (top-down) to PDF points (bottom-up)."""
    return pdf_height_pt * (1 - y_px / img_height_px)


# ============================================================================
# Content-stream transform
# ============================================================================

PATH_BUILD = {"m", "l", "c", "v", "y", "h", "re"}
PATH_PAINT = {"S", "s", "f", "F", "f*", "B", "B*", "b", "b*", "n"}


def _f(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def _matmul(M, N):
    a1, b1, c1, d1, e1, f1 = M
    a2, b2, c2, d2, e2, f2 = N
    return [
        a1 * a2 + b1 * c2,
        a1 * b2 + b1 * d2,
        c1 * a2 + d1 * c2,
        c1 * b2 + d1 * d2,
        e1 * a2 + f1 * c2 + e2,
        e1 * b2 + f1 * d2 + f2,
    ]


def _xform(x, y, M):
    a, b, c, d, e, f = M
    return x * a + y * c + e, x * b + y * d + f


def _y_bbox(insns, parent_ctm):
    """Page-coords y-range covered by drawing ops in `insns`, given parent CTM."""
    ctm = list(parent_ctm)
    stack = []
    text_tm = None
    ymin = ymax = None

    def hit(yp):
        nonlocal ymin, ymax
        if ymin is None or yp < ymin:
            ymin = yp
        if ymax is None or yp > ymax:
            ymax = yp

    for operands, op in insns:
        s = str(op)
        if s == "q":
            stack.append(list(ctm))
        elif s == "Q":
            if stack:
                ctm = stack.pop()
        elif s == "cm":
            ctm = _matmul([_f(x) for x in operands], ctm)
        elif s == "BT":
            text_tm = [1.0, 0, 0, 1.0, 0, 0]
        elif s == "ET":
            text_tm = None
        elif s == "Tm" and text_tm is not None:
            text_tm = [_f(x) for x in operands]
            _, py = _xform(text_tm[4], text_tm[5], ctm)
            hit(py)
        elif s in ("Td", "TD") and text_tm is not None:
            tx, ty = _f(operands[0]), _f(operands[1])
            text_tm = _matmul([1, 0, 0, 1, tx, ty], text_tm)
            _, py = _xform(text_tm[4], text_tm[5], ctm)
            hit(py)
        elif s in ("Tj", "TJ", "'", '"') and text_tm is not None:
            _, py = _xform(text_tm[4], text_tm[5], ctm)
            hit(py)
        elif s in ("m", "l"):
            x, y = _f(operands[0]), _f(operands[1])
            _, py = _xform(x, y, ctm)
            hit(py)
        elif s == "re":
            x, y, w, h = (_f(operands[k]) for k in range(4))
            _, py1 = _xform(x, y, ctm)
            _, py2 = _xform(x + w, y + h, ctm)
            hit(py1)
            hit(py2)
        elif s in ("c", "v", "y"):
            for k in range(0, len(operands), 2):
                x, y = _f(operands[k]), _f(operands[k + 1])
                _, py = _xform(x, y, ctm)
                hit(py)
        elif s == "Do":
            _, py = _xform(0, 0, ctm)
            hit(py)
    return ymin, ymax


def _segment(insns):
    """Yield atomic units as (kind, start, end_exclusive)."""
    n = len(insns)
    i = 0
    while i < n:
        s = str(insns[i][1])
        if s == "q":
            depth, j = 1, i + 1
            while j < n and depth > 0:
                ss = str(insns[j][1])
                if ss == "q":
                    depth += 1
                elif ss == "Q":
                    depth -= 1
                j += 1
            yield ("frame", i, j)
            i = j
        elif s == "BT":
            j = i + 1
            while j < n and str(insns[j][1]) != "ET":
                j += 1
            j = min(j + 1, n)
            yield ("text", i, j)
            i = j
        elif s in PATH_BUILD:
            j = i + 1
            while j < n and str(insns[j][1]) not in PATH_PAINT:
                j += 1
            j = min(j + 1, n)
            yield ("path", i, j)
            i = j
        elif s == "Do":
            yield ("do", i, i + 1)
            i += 1
        else:
            yield ("state", i, i + 1)
            i += 1


def _transform(insns, region_bottom, region_top, shift_y, parent_ctm):
    out = []
    ctm = list(parent_ctm)
    for kind, a, b in _segment(insns):
        chunk = insns[a:b]
        if kind == "state":
            operands, op = chunk[0]
            if str(op) == "cm":
                ctm = _matmul([_f(x) for x in operands], ctm)
            out.extend(chunk)
            continue
        ymin, ymax = _y_bbox(chunk, list(ctm))
        if ymin is None or ymax < region_bottom or ymin > region_top:
            out.extend(chunk)
        elif ymin >= region_bottom and ymax <= region_top:
            out.append(([], Operator("q")))
            out.append(([1, 0, 0, 1, 0, shift_y], Operator("cm")))
            out.extend(chunk)
            out.append(([], Operator("Q")))
        else:
            if kind == "frame":
                out.append(chunk[0])
                out.extend(_transform(chunk[1:-1], region_bottom, region_top, shift_y, list(ctm)))
                out.append(chunk[-1])
            else:
                out.extend(chunk)
    return out


def move_region(pdf, page, region_bottom, region_top, shift_y):
    insns = list(pikepdf.parse_content_stream(pikepdf.Page(page)))
    new_insns = _transform(insns, region_bottom, region_top, shift_y, [1.0, 0, 0, 1.0, 0, 0])
    page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(new_insns))


def main():
    pdf = pikepdf.Pdf.open(str(INPUT_PDF))
    page = pdf.pages[0]
    box = [float(x) for x in page.MediaBox]
    W, H = box[2] - box[0], box[3] - box[1]

    print(f"Source: {INPUT_PDF}")
    print(f"Page size: {W:.2f} × {H:.2f} pt")  # noqa: RUF001
    print(f"Moving region: y ∈ [{REGION_BOTTOM:.2f}, {REGION_TOP:.2f}]")
    print(f"Shift: {SHIFT_Y:+.2f} pt")

    move_region(pdf, page, REGION_BOTTOM, REGION_TOP, SHIFT_Y)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(str(OUTPUT_PDF))

    print(f"Output: {OUTPUT_PDF}")
    print(f"File size: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")
    print("\nNext steps:")
    print(f"  1. Render to PNG: pdftocairo -png -r 150 {OUTPUT_PDF} preview")
    print(f"  2. Verify text: pdftotext {OUTPUT_PDF} -")
    print(f"  3. Check that the region moved by {SHIFT_Y:+.2f} pt")


if __name__ == "__main__":
    main()
