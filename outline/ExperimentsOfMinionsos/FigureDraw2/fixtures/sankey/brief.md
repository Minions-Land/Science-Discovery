# Fixture: sankey
## Task
Sankey diagram of dataset preparation flow.
## Inputs
- data.json: {nodes, links[{source,target,value}]}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- matplotlib has plt.sankey but plotly+kaleido or a manual rectangle/path approach often looks cleaner.
- Color each source's outflow consistently.
