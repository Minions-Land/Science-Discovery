# Typography Reference

Distilled from the 5 starter exemplars (`fig3`, `fig4`,
`bars_ablation_Cancer`, `correctness_by_category`, `results_sweep`).

## Element hierarchy ladder

| Element | Typical size | Weight | Colour |
|---|---|---|---|
| Panel letter (a, b, c, d) | 9pt | bold | dark grey `#404040` |
| Hero / large panel title | 8pt | bold | dark grey `#404040` |
| Y-axis label, X-axis label | 8pt | regular | dark grey `#404040` |
| Bar value labels (above bars) | 7pt | regular | dark grey `#6a6a6a` |
| Tick labels | 7pt | regular | mid grey `#959595` |
| In-panel annotation (EC50, slope, n=) | 6.5pt | regular | mid grey or matched-to-curve |
| Caption note (n =, p =, scale bar) | 5.5-6pt | regular | mid grey |
| Significance markers (`*`, `**`) | 7-8pt | bold | dark grey `#404040` |

The ladder has 4-5 distinct steps in size + weight + colour. Amateur
figures often have only 2-3 steps (everything is 8pt, all dark).

## Specific patterns by figure type

### Bar chart
- Bar value labels ABOVE the bar, not floating in legend
- X-axis labels at fixed angle (0° if room, 30° if overlap, never 45° in
  Nature-family figures because it looks dated)
- Significance markers `*` (p<0.05) `**` (p<0.01) `***` (p<0.001)
  centred between paired bars at fixed offset above the higher bar

### Heatmap
- Row labels at 5.5pt (small, you have many rows)
- Column labels at 6pt
- Cluster labels at 7pt with WHITE HALO when crossing dark cluster regions
- Colourbar tick labels at 5.5pt
- Colourbar title (z-score, log2FC, etc) at 7pt

### Line / curve
- Method names AT THE CURVE ENDPOINT (right side of plot), not in
  legend block — eliminates eye-travel cost
- Label colour matches curve colour
- 6.5-7pt for endpoint labels
- Avoid "solid + dashed + dotted" line styles for differentiation;
  use hue + weight instead

### Multi-panel composite
- Panel letters (a, b, c, d) at 9pt bold, positioned at upper-left of
  each panel with consistent x/y offset (e.g. transAxes (-0.14, 1.08))
- Maintain CONSISTENT offset across all panels — the eye reads panel
  letter position as visual anchor

## Font family

All 5 exemplars use **Arial** (or its Helvetica / Liberation Sans
fallback). Sans-serif default; serif fonts in scientific figures are
2010-vintage and look dated in 2024+.

For mathematical notation:
- Variable names italic via `<em>x</em>` or matplotlib `$x$`
- Constants and unit labels regular weight

## Weight contrast as the typographic signal

The ladder is what differentiates EXEMPLAR figures from amateur ones:
exemplar figures have 4+ distinct text weights/sizes; amateurs have 2.

The cheapest typography upgrade: take an existing figure and downsize
caption notes (n=, p=) by 1-1.5pt. This pushes them down the ladder
and the panel reads cleaner.
