# Fixture: architecture
## Task
Boxes-and-arrows architecture diagram for the system in data.json. No data points, just the pipeline.
## Inputs
- data.json: {system_name, stages, groups}
## Outputs
- figure.pdf, figure.png; caption.tex; gen_figure.py
## Hints
- Use a tool that produces vector output (matplotlib patches, graphviz->pdf, drawio->pdf, or a manual SVG renderer).
- Show direction of data flow with solid arrows; control/feedback dashed.
- Group "Retrieval" and "Generation" with rounded rectangles.
