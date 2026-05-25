# Fixture: line-errband
## Task
3 methods x 50 training steps. Plot mean validation loss with 95% CI (mean +/- ci_half).
## Inputs
- data.json: {steps, methods, curves[method] = {mean, ci_half}}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Y-axis log scale optional but reasonable for loss.
- Highlight the gap to OursModel at the final step.
