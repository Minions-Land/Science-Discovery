# Fixture: heatmap
## Task
10x10 confusion matrix. Annotate diagonal with values, off-diagonal cells with a sequential cmap.
## Inputs
- data.json: {x_labels, y_labels, matrix} where matrix[i][j] = predictions of true class i as class j.
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Use a perceptually uniform colormap (viridis / inferno / Blues).
- Label rows and columns. Diagonal text should be readable on dark cells.
