#!/usr/bin/env python3
"""
Verify that a generated PDF passes the vector-integrity checks.

Run this after every composition step. It catches:
    - Silent script failures (file missing or 0 bytes)
    - Accidental rasterization (file too large, no selectable text)
    - Wrong number of panel labels (e.g. duplicates from source PDFs)
    - Renders that look right but extract no text

Usage:
    python verify_vector.py path/to/output.pdf [--expected-labels f g h i j]
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def find_poppler_tool(name):
    """Find a Poppler tool (pdftotext, pdftocairo, pdftoppm) on the PATH or common locations."""
    found = shutil.which(name)
    if found:
        return found
    # Common Windows locations
    for candidate in [
        rf"F:\texlive\2025\bin\windows\{name}.exe",
        rf"C:\Program Files\poppler\bin\{name}.exe",
    ]:
        if Path(candidate).exists():
            return candidate
    return None


def check_file_size(pdf_path, fail_kb=1, warn_kb=10, max_mb=10):
    """Check that the file size is plausible for a vector PDF.

    Hard fail only when the file is missing, empty, or implausibly tiny
    (< fail_kb). A clean single-page vector PDF can be ~3–8 KB, so we soft-warn
    in [fail_kb, warn_kb) instead of failing — the SKILL.md "50 KB – 2 MB"
    range is a heuristic for figure-grade composites, not a hard floor.
    """  # noqa: RUF002
    if not pdf_path.exists():
        return False, f"File does not exist: {pdf_path}"
    size_bytes = pdf_path.stat().st_size
    if size_bytes == 0:
        return False, "File is 0 bytes — script failed silently"
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    if size_kb < fail_kb:
        return False, f"File implausibly small ({size_kb:.1f} KB) — likely truncated"
    if size_mb > max_mb:
        return False, f"File too large ({size_mb:.1f} MB) — possibly rasterized"
    if size_kb < warn_kb:
        return True, f"File size OK ({size_kb:.1f} KB; small but valid for a sparse vector page)"
    return True, f"File size OK: {size_kb:.1f} KB"


def check_text_extractable(pdf_path):
    """Check that text can be extracted via pdftotext."""
    pdftotext = find_poppler_tool("pdftotext")
    if not pdftotext:
        return None, "pdftotext not found, skipping text extraction check"
    try:
        result = subprocess.run(
            [pdftotext, str(pdf_path), "-"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        text = result.stdout.strip()
        if not text:
            return False, "No text extracted — PDF may be entirely raster"
        return True, f"Text extractable ({len(text)} chars)"
    except subprocess.TimeoutExpired:
        return False, "pdftotext timed out"
    except Exception as e:
        return False, f"pdftotext error: {e}"


def _count_label(text, label):
    """Count standalone occurrences of a panel label.

    Naive `text.count(label)` over `pdftotext` output sweeps in every `e` inside
    words like "test"/"figure". For the single-letter panel labels this skill
    targets, that path always trips the "duplicate" heuristic. Word-boundary
    regex matches only isolated runs, which is what panel labels actually are
    in a PDF text stream.
    """
    return len(re.findall(r"\b" + re.escape(label) + r"\b", text))


def check_label_count(pdf_path, expected_labels, max_per_label=5):
    """Check that each expected label appears as a standalone token."""
    if not expected_labels:
        return None, "No labels to check"
    pdftotext = find_poppler_tool("pdftotext")
    if not pdftotext:
        return None, "pdftotext not found, skipping label check"
    try:
        result = subprocess.run(
            [pdftotext, str(pdf_path), "-"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        text = result.stdout
        issues = []
        for label in expected_labels:
            count = _count_label(text, label)
            if count == 0:
                issues.append(f"label '{label}' not found")
            elif count > max_per_label:
                issues.append(f"label '{label}' appears {count}× (possible duplicate)")  # noqa: RUF001
        if issues:
            return False, "; ".join(issues)
        return True, f"Labels OK: {', '.join(expected_labels)}"
    except Exception as e:
        return False, f"label check error: {e}"


def render_preview(pdf_path, dpi=150):
    """Render the first page to PNG for visual inspection."""
    pdftocairo = find_poppler_tool("pdftocairo")
    if not pdftocairo:
        return None, "pdftocairo not found, skipping preview render"
    preview_dir = pdf_path.parent / "tmp"
    preview_dir.mkdir(exist_ok=True)
    preview_base = preview_dir / f"{pdf_path.stem}_preview"
    try:
        subprocess.run(
            [
                pdftocairo,
                "-png",
                "-f",
                "1",
                "-l",
                "1",
                "-r",
                str(dpi),
                str(pdf_path),
                str(preview_base),
            ],
            capture_output=True,
            timeout=60,
        )
        preview_png = preview_dir / f"{pdf_path.stem}_preview-1.png"
        if preview_png.exists():
            return True, f"Preview rendered: {preview_png}"
        return False, "Preview file not created"
    except Exception as e:
        return False, f"render error: {e}"


def check_text_duplication(pdf_path, source_pdf):
    """Compare token counts between output and source PDF.

    Catches the failure mode where a "clipped" PDF rendered correctly but the
    text layer was actually triplicated — pdftotext / search / copy-paste /
    accessibility readers see N copies of the page even though the pixels are
    correct. Any token appearing MORE in the output than in the source is the
    smoking-gun signature of cropbox-only "clipping".
    """
    if source_pdf is None:
        return None, "No --source given, skipping duplication check"
    pdftotext = find_poppler_tool("pdftotext")
    if not pdftotext:
        return None, "pdftotext not found, skipping duplication check"
    try:
        src_text = subprocess.run(
            [pdftotext, str(source_pdf), "-"],
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout
        out_text = subprocess.run(
            [pdftotext, str(pdf_path), "-"],
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout
        from collections import Counter

        src_tokens = Counter(re.findall(r"\S+", src_text))
        out_tokens = Counter(re.findall(r"\S+", out_text))
        duplicated = {
            tok: out_tokens[tok] - src_tokens[tok]
            for tok in out_tokens
            if out_tokens[tok] > src_tokens[tok]
        }
        if duplicated:
            top = sorted(duplicated.items(), key=lambda kv: -kv[1])[:3]
            sample = "; ".join(f"{tok!r} +{n}" for tok, n in top)
            return False, (
                f"{len(duplicated)} token(s) appear more often in output than in source"
                f" — likely cropbox-only clipping or stamp duplication. e.g. {sample}"
            )
        return True, "No tokens duplicated vs source"
    except Exception as e:
        return False, f"duplication check error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Verify a generated PDF.")
    parser.add_argument("pdf_path", type=Path, help="Path to the PDF to verify")
    parser.add_argument(
        "--expected-labels",
        nargs="*",
        default=[],
        help="Panel labels expected to appear (e.g. f g h i j)",
    )
    parser.add_argument(
        "--source", type=Path, default=None, help="Source PDF; enables text-duplication detection"
    )
    parser.add_argument("--no-render", action="store_true", help="Skip the preview render step")
    args = parser.parse_args()

    pdf_path = args.pdf_path

    print(f"Verifying: {pdf_path}\n")

    checks = []

    ok, msg = check_file_size(pdf_path)
    checks.append((ok, "File size", msg))

    ok, msg = check_text_extractable(pdf_path)
    checks.append((ok, "Text extractable", msg))

    ok, msg = check_label_count(pdf_path, args.expected_labels)
    checks.append((ok, "Panel labels", msg))

    ok, msg = check_text_duplication(pdf_path, args.source)
    checks.append((ok, "Text-layer duplication", msg))

    if not args.no_render:
        ok, msg = render_preview(pdf_path)
        checks.append((ok, "Preview render", msg))

    # Print results
    print("=" * 60)
    all_passed = True
    for ok, name, msg in checks:
        if ok is True:
            print(f"  [PASS] {name}: {msg}")
        elif ok is False:
            print(f"  [FAIL] {name}: {msg}")
            all_passed = False
        else:
            print(f"  [SKIP] {name}: {msg}")
    print("=" * 60)

    if all_passed:
        print("\nAll checks passed. Visually inspect the preview before delivering.")
        sys.exit(0)
    else:
        print("\nOne or more checks failed. Fix before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
