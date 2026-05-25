# Fixture: 4panel-hero
## Task
4-panel hero figure following gridspec(2,3,width_ratios=[2,1,1]):
- A (top-left, dominant): conceptual overview of the method (text/diagram, you draw it).
- B (top-mid): ablation bars (5 ablations).
- C (top-right): training trend (Baseline vs Ours).
- D (bottom, full width): 5x5 heatmap (sensitivity sweep).
## Inputs
- data.json
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Hero panel must read as scientific overview, not decoration.
- Panel labels A B C D upper-left, bold sans-serif.
- Avoid empty quadrants; bottom panel spans the whole row.
