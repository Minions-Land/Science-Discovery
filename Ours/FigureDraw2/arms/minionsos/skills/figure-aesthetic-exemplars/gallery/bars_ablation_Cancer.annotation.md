# Annotation — bars_ablation_Cancer

**Source:** figures4papers `figure_ImmunoStruct/figures/bars_ablation_Cancer.png`.
Real research figure from a peer-reviewed bioinformatics ablation study.

**Archetype:** Single-panel grouped bar chart with statistical significance.
Use for R1.A case-bar / model ablation comparison fixtures.

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#406ac0` | 22.3 | signal blue (full / Ours method) |
| `#6a95c0` | 21.5 | mid blue (one ablation removed) |
| `#c0c0ea` | 15.4 | light blue (more ablations) |
| `#c0c0c0` | 10.1 | neutral grey |
| `#eaeaea` | 9.5 | background |
| `#959595` | 9.4 | mid grey for axis |
| `#6a6a6a` | 2.7 | text dark |
| `#95c0ea` | 2.1 | additional blue tint |
| `#c0eaea` | 1.8 | accent cyan |

**Critical observation:** This is a **single-hue family alpha-graded
palette** — almost everything is on the blue axis (`#406ac0` →
`#6a95c0` → `#c0c0ea` → `#95c0ea`). Greyscale-safe by construction:
the bars degrade to monotonic shades of grey, preserving order. About
60% of pixels are blue-family; ~30% are grey-family. NO secondary hue
is introduced (no red, green, accent pink). This is the "single-blue
alpha-grade" pattern that the R1.A case-bar candidate ATTEMPTED but
combined with hatches; this exemplar shows the cleaner version
WITHOUT hatches because the alpha gradient alone is sufficient.

## Typography

- Bar value labels (above bars): 7pt, dark grey, positioned at bar top
- Method name labels (x-axis): 7pt, mid-grey, horizontal
- Significance markers (`*`, `**`): centred between paired bars at
  fixed offset above the higher bar of the pair
- Y-axis label: 8pt, slightly bigger than tick labels for hierarchy

## White space

- Y-axis range: starts at the data minimum (not 0), ~5% headroom above
  tallest bar. **Differences between bars are visually amplified by the
  zoomed axis.** This is what the R6.A user feedback called out:
  "assuming higher is better, the shortest bar should be barely visible;
  even a small extra height makes the difference legible."
- Bar width: ~70% of available cell width; gap between groups ~30%
- Top margin (above bars): ~5% canvas
- Bottom margin (below x-axis): ~10% canvas (room for x-axis labels)

## Visual rhythm

1. Eye lands on the tallest bar (Full / Ours method) because of
   saturation contrast
2. Reader's eye then scans LEFT-TO-RIGHT through ablation variants
3. Pattern of progressively-fading blue + progressively-shorter bars
   communicates "ablation hurts performance" without any caption text
4. Significance markers anchor the comparison pairs

## What makes this figure work

1. **Single-hue alpha gradient instead of multi-hue palette.** This is
   the R1.A case-bar lesson; the exemplar shows the clean execution.
   Removing hue contrast forces the reader to focus on bar HEIGHT,
   which is the actual data.
2. **Y-axis zoomed to data range.** The differences between Full and
   ablation variants are made visually salient by NOT showing the
   0-100 range. The R6.A feedback rule applied correctly.
3. **No hatches.** The R1.A case-bar candidate added hatches to make
   bars greyscale-distinguishable; this exemplar trusts the alpha
   gradient alone. Cleaner.
4. **Bar value labels positioned at top, not floating.** Each bar's
   numeric value is ATTACHED to the bar. Reader doesn't have to look
   up at the y-axis.
5. **Spinetop and right disabled.** Standard rule, but visible here:
   the figure feels less "boxed in," more open.

## Typical amateur deltas

- Multi-hue palette (red / blue / green / orange) for ablation
  variants — kills greyscale reading
- Y-axis 0-100 with bars filling 60% — wastes top 40%
- Bar values in a separate legend instead of attached to bars
- Hatches on top of fully-coloured bars — visual noise
- Inter-bar gap too small or too large — bars feel crowded or
  disconnected
