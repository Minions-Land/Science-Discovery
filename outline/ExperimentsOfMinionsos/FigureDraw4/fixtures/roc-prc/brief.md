# Fixture: roc-prc
## Task
Two-panel ROC + Precision-Recall for 4 binary classifiers. Compute curves from data.json scores.
## Inputs
- data.json: {methods, scores[method] = {positive: [...], negative: [...]}}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Annotate AUROC and AP per method in the legend.
- Diagonal reference line on ROC, prevalence baseline on PRC.
