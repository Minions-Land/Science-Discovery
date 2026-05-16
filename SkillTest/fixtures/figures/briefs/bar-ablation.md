# Figure brief: bar — multi-method ablation

**Type:** figure — single-panel grouped bar chart
**Use in:** R1.A nature-figure, R1.B scientific-figure-making
**Data:** `../data/bar-ablation.csv`

## Scientific claim the figure must defend

> Removing component C from our framework hurts performance more than removing
> component A or B, indicating that C carries the dominant inductive bias.

## Required content

- Three datasets along x-axis (Dataset-1, Dataset-2, Dataset-3)
- Four methods per dataset: `Full` (ours), `−A`, `−B`, `−C`
- y-axis: accuracy (0–1, three datasets share scale)
- Error bars: ±1 SD across n=5 seeds
- Dashed horizontal line per dataset for the strongest external baseline
  (values in csv column `external_baseline`)

## Style requirements (the runner must figure these out from the skill)

- Single column width (~85 mm equivalent at 600 dpi)
- Editable text in SVG, sans-serif, 7-pt body labels
- Direct labelling of methods is fine; if a legend is used it must not duplicate axis labels
- Significance markers (`*` p&lt;0.05, `**` p&lt;0.01) for `Full` vs `−C` only

## Failure modes to watch

- 4 saturated colours that fight each other; expect a unified low-saturation palette
- Legend dumped into a corner that overlaps a bar
- Missing error bar definition in caption
- y-axis truncated (zooming in to make differences look bigger) — should start at 0 or be flagged
