# Fixture: volcano
## Task
Volcano plot for ~3000 genes. Highlight up/down/non-sig with thresholds in data.json.
## Inputs
- data.json: {log2fc, neg_log10_p, thresholds}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- 3 colors: down (left), non-sig (center), up (right).
- Optional: annotate top-5 by neg_log10_p magnitude.
