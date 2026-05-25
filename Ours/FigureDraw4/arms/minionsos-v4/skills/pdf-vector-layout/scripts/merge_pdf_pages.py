#!/usr/bin/env python3
"""Merge a region of one PDF into another, with vector + text fidelity.

The source page's content stream is filtered: every atomic unit (q/Q frame,
BT/ET text block, m/re...paint path, standalone Do) whose y-bbox falls inside
the source region is kept and translated; outside units are dropped; straddling
q/Q frames are recursed. State-only ops (Tf, gs, w, ...) are always preserved.

The filtered content becomes a Form XObject embedded in the composite PDF, so
the resulting text layer contains only the chosen region — pdftotext, copy/
paste, search, and screen readers see exactly what is rendered.

Optional vector white masks (rectangles) are drawn after the stamp; use them to
hide source-side panel letters that conflict with composite-side labels.

Usage:
    1. Render composite + source to PNG at 150 DPI to measure coords.
    2. Edit the constants below.
    3. python merge_pdf_pages.py
    4. Render the output and verify with verify_vector.py.
"""

from pathlib import Path

import pikepdf
from pikepdf import Name, Operator

# ============================================================================
# Configuration — EDIT THESE
# ============================================================================

COMPOSITE_PDF = Path("composite_base.pdf")
SOURCE_PDF = Path("source_row.pdf")
OUTPUT_PDF = Path("composite_final.pdf")

# Source region (PDF points) to extract from SOURCE_PDF
SOURCE_REGION_BOTTOM = 100.0
SOURCE_REGION_TOP = 350.0

# Where the source region's bottom-left should land in the composite
DEST_X = 0.0
DEST_Y = 50.0

# Optional uniform scale (1.0 = no scaling)
SCALE = 1.0

# Vector white masks (in COMPOSITE coords): list of (x, y, width, height).
# Drawn AFTER the stamp, so they hide source-side labels but not composite ones.
MASKS = [
    # Example: (0, 320, 595.28, 30),
]


# ============================================================================
# Content-stream transform (shared shape with move_pdf_region.py)
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


def _extract_and_translate(insns, src_bottom, src_top, dx, dy, parent_ctm):
    """Drop everything outside [src_bottom, src_top]; translate everything
    inside by (dx, dy). State-like blocks (no y-bbox, e.g. Tf font setters)
    are preserved unconditionally so later draw ops still resolve fonts.
    """
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
        if ymin is None:
            out.extend(chunk)
        elif ymax < src_bottom or ymin > src_top:
            continue
        elif ymin >= src_bottom and ymax <= src_top:
            out.append(([], Operator("q")))
            out.append(([1, 0, 0, 1, dx, dy], Operator("cm")))
            out.extend(chunk)
            out.append(([], Operator("Q")))
        else:
            if kind == "frame":
                out.append(chunk[0])
                out.extend(
                    _extract_and_translate(chunk[1:-1], src_bottom, src_top, dx, dy, list(ctm))
                )
                out.append(chunk[-1])
    return out


# ============================================================================
# Driver
# ============================================================================


def main():
    composite = pikepdf.Pdf.open(str(COMPOSITE_PDF))
    source = pikepdf.Pdf.open(str(SOURCE_PDF))

    src_page = source.pages[0]
    src_box = [_f(x) for x in src_page.MediaBox]
    src_w = src_box[2] - src_box[0]
    src_h = src_box[3] - src_box[1]

    print(f"Composite: {COMPOSITE_PDF}")
    print(f"Source: {SOURCE_PDF} ({src_w:.2f} × {src_h:.2f} pt)")  # noqa: RUF001
    print(f"Source region y ∈ [{SOURCE_REGION_BOTTOM:.2f}, {SOURCE_REGION_TOP:.2f}]")
    print(f"Destination: ({DEST_X:.2f}, {DEST_Y:.2f}), scale={SCALE}")
    print(f"Masks: {len(MASKS)}")

    dx = DEST_X
    dy = DEST_Y - SOURCE_REGION_BOTTOM

    src_insns = list(pikepdf.parse_content_stream(pikepdf.Page(src_page)))
    filtered = _extract_and_translate(
        src_insns,
        SOURCE_REGION_BOTTOM,
        SOURCE_REGION_TOP,
        dx,
        dy,
        [1.0, 0, 0, 1.0, 0, 0],
    )
    src_page.Contents = source.make_stream(pikepdf.unparse_content_stream(filtered))

    # Round-trip the filtered source through a temp file so we can pull a
    # Form XObject (with all its Resources) into the composite via copy_foreign.
    temp_path = Path(str(OUTPUT_PDF) + ".tmp.pdf")
    source.save(str(temp_path))
    source.close()

    temp_pdf = pikepdf.Pdf.open(str(temp_path))
    form = pikepdf.Page(temp_pdf.pages[0]).as_form_xobject()
    foreign_form = composite.copy_foreign(form)

    dst_page = composite.pages[0]
    form_name = pikepdf.Page(dst_page).add_resource(
        foreign_form, Name.XObject, prefix="ExtractedRegion"
    )

    if SCALE == 1.0:
        overlay = f"q\n{form_name} Do\nQ\n"
    else:
        tx = DEST_X * (1 - SCALE)
        ty = DEST_Y * (1 - SCALE)
        overlay = f"q\n{SCALE} 0 0 {SCALE} {tx} {ty} cm\n{form_name} Do\nQ\n"
    pikepdf.Page(dst_page).contents_add(overlay.encode("latin-1"), prepend=False)

    if MASKS:
        parts = ["q\n1 1 1 rg\n"]
        for x, y, w, h in MASKS:
            parts.append(f"{x} {y} {w} {h} re\nf\n")
        parts.append("Q\n")
        pikepdf.Page(dst_page).contents_add("".join(parts).encode("latin-1"), prepend=False)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    composite.save(str(OUTPUT_PDF))
    temp_pdf.close()
    temp_path.unlink()

    print(f"\nOutput: {OUTPUT_PDF}")
    print(f"File size: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")
    print("\nNext steps:")
    print(f"  1. Render to PNG: pdftocairo -png -r 150 {OUTPUT_PDF} preview")
    print(f"  2. Verify: python verify_vector.py {OUTPUT_PDF}")
    print("  3. Check: only one set of panel letters, no clipping, correct spacing")


if __name__ == "__main__":
    main()
