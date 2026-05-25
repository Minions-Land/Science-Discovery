# Annotation — correctness_by_category

**Source:** figures4papers `figure_brainteaser/figures/correctness_by_category.png`.
Real research figure from a benchmark categorical comparison study.

**Archetype:** Multi-bar cross-category comparison with hue-grouped
variables. Use when your fixture has several categories AND each
category has 2-3 sub-comparisons.

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#c0c0c0` | 14.6 | neutral grey background |
| `#406ac0` | 14.4 | signal blue (Method A) |
| `#eaeaea` | 14.2 | panel background tint |
| `#959595` | 13.9 | mid-grey (Baseline / Vehicle / Control variable) |
| `#eac0c0` | 10.9 | accent red soft (Method B) |
| `#ea9595` | 10.6 | accent red mid |
| `#c0eac0` | 5.7 | accent green soft (third variable) |
| `#95c095` | 5.6 | accent green mid |
| `#95ea95` | 2.0 | accent green deeper |

**Critical observation:** The figure uses a **3-hue + grey baseline**
pattern (blue + red + green + grey). Each non-grey hue is allotted
~10-15% of pixels; grey gets ~30%+. This is a 3-way categorical
comparison; the rule "single hue + alpha grade" doesn't apply because
the categories ARE the message. But the figure still subordinates colour
to grey in absolute pixel ratio.

## Typography

- Category labels (x-axis groups): 7pt, horizontal where space allows,
  rotated 30° where labels overlap
- Sub-category labels (within group): 6.5pt
- Bar value labels: 6pt at bar top
- Legend: 7pt, positioned in the bottom-right empty area, no frame

## White space

- Inter-group gap (between categories): ~50% of single-bar width
- Intra-group gap (between sub-bars in a category): ~20% of single-bar width
- The 2.5x ratio (50% inter / 20% intra) is the visual signal that says
  "these 3 bars belong together; this group is separate from the next group"

## Visual rhythm

1. Eye scans LEFT-TO-RIGHT through category groups
2. Within each group, the eye notices that ONE colour family dominates
   (which one wins varies by category — the differential pattern IS the
   scientific story)
3. Legend at bottom-right anchors the colour-to-method mapping

## What makes this figure work

1. **Inter-group gap 2.5x intra-group gap.** This pattern says "this is
   a 2-level grouping" without labelling it as such. Eye learns the
   hierarchy from spacing alone.
2. **Soft red + soft green (not saturated red + green).** Reds and
   greens are at ~50-60% saturation, not full. Reduces the harsh
   colourblind risk of saturated red/green pairs while still letting
   the categories distinguish.
3. **Grey baseline as 30%+ of pixels.** Even in a 3-hue figure, the
   majority of foreground is neutral. This is the same lesson as
   fig3-in-vivo: subordinate colour to grey.
4. **Legend in bottom-right empty area, no frame.** Frameless legend in
   "found space" instead of "claimed space." Doesn't compete with bars
   for visual attention.
5. **Sub-category labels under bars, not in tooltip / legend.** Reader
   doesn't have to cross-reference; the colour-to-method mapping is
   visible at every bar.

## Typical amateur deltas

- Saturated red + saturated green pair (colourblind hostile)
- Equal inter-group / intra-group gap — categorical hierarchy invisible
- Legend in framed box dominating the upper-right corner
- Method labels only in legend, not at bars
- All bars same colour family with hatch differentiation (R1.A failure
  mode at high panel count)
