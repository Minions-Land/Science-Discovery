# Fixture: dual-axis-time
## Task
Dual-axis time-series: training loss (left axis, log y) + cosine LR schedule (right axis).
## Inputs
- data.json: {steps, loss, lr}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Color-couple axis ticks/labels to their line.
- Avoid using both axes for a "more is better" sense without telling the reader.
