# Fixture: grouped-bar

## Task
Produce a publication-quality grouped bar chart comparing 4 methods on 5 benchmarks.
Read accuracy means and standard errors from data.json. Show error bars (std).
The figure must clearly highlight which method wins overall and tolerate Nature/CVPR-style
single-column inclusion.

## Inputs
- data.json: {benchmarks: [...], methods: [...], values: {method: {benchmark: {mean, std}}}}
- All values in 0..100 (percentage points).

## Outputs (cwd)
- figure.pdf, figure.png  (figure.svg optional)
- caption.tex   (the LaTeX caption text only)
- gen_figure.py (the script that produced figure.pdf)

## Hints (apply if not already enforced by your skills)
- Embed editable text (matplotlib: pdf.fonttype=42, svg.fonttype="none").
- Distinguish methods with palette + (optionally) hatch for B&W readers.
- Reasonable y-range: do not start at 0 if all values are above 60 (waste of space).
- Title is optional; the LaTeX caption is the primary description.
