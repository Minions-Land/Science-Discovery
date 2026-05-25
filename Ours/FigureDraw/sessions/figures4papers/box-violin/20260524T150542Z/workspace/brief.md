# Fixture: box-violin
## Task
4 conditions x 100 samples. Violin + box overlay, show medians and individual points (jittered, alpha<=0.4).
## Inputs
- data.json: {conditions, samples[condition] = [N values]}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Significance brackets (Mann-Whitney U) optional.
- Order conditions Control -> low -> high -> Combo.
