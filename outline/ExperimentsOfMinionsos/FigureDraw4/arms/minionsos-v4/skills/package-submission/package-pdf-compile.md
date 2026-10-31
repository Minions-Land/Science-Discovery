---
slug: package-pdf-compile
summary: Clean PDF compile from scratch — delete build artifacts, run paper-compile, verify the PDF is reproducible from source.
layer: logical
version: 1
status: active
references: paper-compile, pdf-vector-layout
provenance: human
---

# Package PDF Compile

Re-compile the paper from a clean state to produce a submission-ready PDF.

## When to use

- Any submission that includes a paper PDF.
- After final edits, before packaging other deliverables.

## Procedure

1. Delete `build/` and all intermediate files (`.aux`, `.log`, `.bbl`, `.blg`).
2. Run `paper-compile` from scratch (invoke that skill or run `latexmk -pdf main.tex`).
3. Verify the output PDF:
   - All fonts embedded (`pdffonts main.pdf | grep -v yes` is empty).
   - No missing references or citations (`grep -i "undefined\|multiply" build/*.log`).
   - Page count within venue limit.
4. Never ship a PDF whose source cannot rebuild it.

## Output

`main.pdf` — clean, reproducible, fonts embedded, no warnings.
