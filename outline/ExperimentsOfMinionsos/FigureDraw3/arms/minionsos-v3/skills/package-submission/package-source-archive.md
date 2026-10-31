---
slug: package-source-archive
summary: Build a standalone-compilable tex.zip source archive that reproduces the submission PDF on any clean machine.
layer: logical
version: 1
status: active
provenance: human
---

# Package Source Archive

Build `tex.zip` — a source archive that compiles standalone on any clean machine.

## When to use

- Venue requires source upload alongside PDF.
- You want to verify the paper is self-contained.

## Skip when

- Venue accepts PDF-only (rare).
- Preprint-only upload (arXiv handles source differently).

## Procedure

1. **Assemble contents:** all `*.tex`, `*.bib`, style files (`.sty` / `.cls` per venue), `figures/*.pdf` (prefer vector), `figures/*.png` (raster-only). Exclude `build/` intermediates, `.aux` / `.log`, editor backups, hidden files.

2. **Verify standalone compilation.** Extract to a scratch directory on a clean path, run `latexmk -pdf main.tex`. Must produce the same PDF as the main build. No system-specific includes.

3. **Check file size.** Most venues cap at 50 MB; prefer < 10 MB. If over, check for uncompressed raster images.

## Output

`tex.zip` — self-contained, compiles to the same PDF, no external dependencies.
