# Figure brief: radar — multi-method multi-metric comparison

**Type:** figure — single-panel polar / radar plot
**Use in:** R-future-3 Task 2 radar-form validation
**Data:** `../data/method-metric-comparison.csv` (5 methods × 6 metrics)

## Scientific claim the figure must defend

> MethodX (Ours) achieves the strongest balance across 6 evaluation
> dimensions, beating baseline methods on accuracy, F1, robustness,
> and calibration; trailing only on speed and memory (where it is
> still competitive).

## Required content

- 5 methods (MethodX Ours + 4 baselines: BERT-base, GPT-3.5, RoBERTa, T5)
- 6 metrics (Accuracy, F1, Robustness, Calibration, Speed, Memory)
- All metrics normalised to 0-1 (higher = better)

## Style requirements

- Single panel; canvas ~140 mm wide max
- Editable text, Arial 7-8pt
- Polygon fills with low saturation (Principle 2)
- Polygon strokes 2-2.5x normal (Principle 2 sub-rule for pastels)
- 5 methods means 5 polygons overlapped — visual clarity matters

## Failure modes the runner should fix

- **Reaching for grouped bar chart** (5 methods × 6 metrics = 30 bars
  across 6 panels). Most amateur figures default to this; loses the
  per-method shape signature.
- **Heatmap (methods × metrics)**. Communicates value-per-cell but
  loses the SHAPE that distinguishes each method.
- **Multiple separate line charts** (one per metric). Wastes canvas;
  reader can't compare across metrics easily.
- **Multi-hue full-saturation polygon fills** (one bright distinct
  hue per method). Visually loud; polygons obscure each other.
- **Full-saturation thin strokes** (default linewidth=1). With pastel
  fills, polygons disappear; with full fills, strokes are redundant.

## Reference rewrite expectations (for scoring)

A passing rewrite should:

1. Pick **polar / radar** as the form (not bar / heatmap / line)
2. Use 5 polygons overlapped on one radar grid
3. Apply pastel fill (Principle 2: ~25-30% saturation) + bumped
   stroke weight (Principle 2 sub-rule: 2-2.5px)
4. Use 5 hues from the SAME hue family (Principle 1 strict — e.g. all
   cool, with one signal direction). MethodX (Ours) gets the strongest
   saturation; baselines get progressively softer.
5. 77% grey foreground (Principle 5 / comparison_radar exemplar pattern)
6. Radial axis labels inline (no separate legend block for scale)
7. Method labels inline OR as a single ncol≥2 legend (Principle 3
   sub-rule for hybrid composites)

## R-future-3 hypothesis

If candidate (skill loaded with comparison_radar.annotation.md as
exemplar reference) picks polar form + applies the soft-pastel + grey-
dominant + bumped-stroke recipe, while baseline reaches for grouped
bar / heatmap, the skill demonstrably encodes the form-choice axis.
