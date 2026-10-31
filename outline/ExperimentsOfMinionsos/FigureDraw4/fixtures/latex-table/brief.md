# Fixture: latex-table

## Task
Produce a publication-quality booktabs comparison table comparing 4 methods on 5 metrics, render it as a standalone PDF (figure.pdf) AND save the underlying LaTeX source as table.tex. Then also produce figure.png by rasterizing the PDF.

## Inputs
- data.json: {methods, metrics, values[method][metric] = {mean, std}, units[metric]}
- All values are realistic ML benchmark numbers.

## Outputs (cwd)
- figure.pdf, figure.png  (the rendered table as a single-page PDF + raster preview)
- table.tex   (the standalone .tex source - must compile with pdflatex)
- caption.tex (the LaTeX caption text only)
- gen_figure.py  (the script that produced figure.pdf - should call pdflatex on table.tex)

## Hints
- Use booktabs (\toprule, \midrule, \bottomrule). NO vertical lines.
- Bold the best per column. If a method has highest mean and overlaps with another within 1 std, bold both.
- mean +/- std formatting: "$72.4_{\pm 1.2}$" subscript style is preferred for camera-ready compactness.
- Add a column-spanning grouping if methods naturally fall into baseline / ours.
- Caption should explain bold convention and seed count.
