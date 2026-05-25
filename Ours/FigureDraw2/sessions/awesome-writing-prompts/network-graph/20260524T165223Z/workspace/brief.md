# Fixture: network-graph
## Task
Small network with ~30 nodes colored by community. Force-directed or circular layout.
## Inputs
- data.json: {nodes[{id, community}], edges[{source,target}], communities}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- networkx + matplotlib is fine.
- Avoid hairball: tune edge alpha and node size.
