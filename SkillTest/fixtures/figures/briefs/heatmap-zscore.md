# Figure brief: heatmap — cross-condition expression z-score

**Type:** figure — single-panel diverging heatmap
**Use in:** R1.A nature-figure, R1.B scientific-figure-making
**Data:** `../data/heatmap-zscore.csv`

## Scientific claim the figure must defend

> Genes in cluster B show a coordinated shift from condition CTRL to condition
> TREAT, while clusters A and C remain stable.

## Required content

- 30 genes (rows), 8 conditions (columns: CTRL_1–CTRL_4, TREAT_1–TREAT_4)
- Cell value: row-wise z-score (already provided in csv)
- Rows grouped into 3 clusters: A (rows 1–10), B (rows 11–20), C (rows 21–30)
- Cluster annotation as a thin coloured side bar
- Diverging colormap centred at 0, white at the centre

## Style requirements

- Two-column-eligible single panel (~115 mm wide); not a square
- Sans-serif 6-pt row labels; rotated 0° (horizontal); only every 2nd or 3rd label if overlap
- Colormap: choose a colourblind-safe diverging family (e.g. RdBu_r, BrBG)
- Print-safe: distinguishable in CMYK preview
- Editable text in SVG; ticks on outside

## Failure modes to watch

- Default `viridis` or `plasma` (sequential colormaps misrepresent diverging data)
- Saturation-only colour without value — diagonal-line overprint test fails
- Row labels truncated
- Missing condition group separator between CTRL and TREAT
- No cluster side bar
