# Annotation — fig3-in-vivo-efficacy-rich

**Source:** nature-skills `nature-figure` repository, gallery directory.
Curated as exemplar of multi-panel hero composite for in-vivo efficacy +
safety + biomarker + cytometry papers (Nature Machine Intelligence vintage).

**Archetype:** 4-panel hero composite. Use for R5.C 7-panel / R6.A 9-panel
preclinical pipeline fixtures.

## Extracted palette (real pixel counts from the rendered PNG)

| Hex | % of foreground pixels | Role |
|---|---|---|
| `#eaeaea` | 24.4 | background tint / panel cards |
| `#959595` | 12.0 | mid-grey for axis ticks, gridlines, neutral data |
| `#c0c0c0` | 12.0 | light grey for separator panels |
| `#c04040` | **5.7** | **signal red — only used for the directional "treatment" group** |
| `#6a6a6a` | 5.0 | dark grey for axis labels and panel letters |
| `#ea9595` | 4.2 | signal-red soft (95% CI band fill, secondary occurrences) |
| `#c0c0ea` | 4.0 | accent blue (control group, ~12% saturation) |
| `#404040` | 3.9 | near-black for emphasised text |
| `#eac0c0` | 3.1 | signal-red faintest (background condition fills) |
| `#c0eaea` | 2.9 | accent cyan (subordinate categorical) |

**Critical observation:** **52% of foreground is grey** (#eaeaea / #959595 /
#c0c0c0 / #6a6a6a / #404040). The red signal `#c04040` accounts for only
~6%. This is the inverse of what most amateur figures do — amateurs use
saturated colour for >30% of pixels and grey for <20%. The exemplar
SUBORDINATES colour to neutrals; that's what makes one signal red feel
high-impact instead of noisy.

## Typography (visual reading, not exact extraction)

- Panel letters: bold ~9pt, slight darker than other text (#404040 vs
  #6a6a6a for body)
- Axis labels: ~7pt body, mid-grey
- In-panel annotations (significance markers, EC50 labels): ~6.5pt,
  positioned tight against the marker they label, not floating
- Caption notes (n =, p =, scale bar): smallest text, ~5.5pt, sub-axis
  position

Weight contrast across element types is the typographic signal:
panel letters > axis labels > caption notes is a 3-step hierarchy in
both size AND weight. This is a hierarchy LADDER not a flat list.

## White-space allocation (visual estimate)

- Per-panel internal margin (axes to panel edge): ~10% of panel size
- Inter-panel gutter: ~6% of canvas (tighter than matplotlib default
  wspace/hspace)
- Hero panel area: ~42-45% of canvas (less than the 50% nominal "hero
  rule"; the gain is from making subordinate panels more substantive,
  not from making hero bigger)

## Visual rhythm (where the eye lands)

1. Panel A hero — dose-response curve with shaded CI band, grabs eye
   first because of the wide canvas allocation + the only fully-
   saturated curve in the figure.
2. Panel D bottom-spanning — secondary anchor because of width.
3. Panels B, C — read as a pair (top-right column) because they share
   the same x-axis style and chart convention.

The reading order is HIERARCHICAL not narrative. The figure does NOT
expect the reader to read A → B → C → D in sequence; it expects the
reader to fix on A first, then sample B/C/D.

## What makes this figure work (5 design decisions)

1. **Grey-dominant palette.** 52% of foreground pixels are grey; the
   single signal red `#c04040` is reserved for one direction (treatment).
   This contrasts with amateur figures that fill 30-40% of pixels with
   saturated colour.
2. **CI band over individual points.** Panel A uses fill_between for the
   95% CI rather than per-replicate dots. The fill_between alpha is ~0.16
   — barely-there, but enough to read as "uncertainty extent." Avoids
   the visual noise of 5+ overlapping dot scatter.
3. **Inline statistical labels.** EC50 markers are placed AT the curve
   crossing, not in a separate legend block. Reader doesn't have to
   look up significance — it's positioned where the eye is already
   landing.
4. **Tight inter-panel gutter.** ~6% canvas allocated to inter-panel
   space (vs ~10-12% in matplotlib default). The figure reads as ONE
   composite, not 4 independent plots.
5. **Subordinate panels matched by chart convention.** B and C share
   x-axis style + position so they read as a pair. Reduces the visual
   work the reader has to do to switch contexts between panels.

## What you'd diff against (typical amateur figure deltas)

If your figure looks "rule-correct but bland" against this exemplar,
the most-likely deltas are:

- **Palette saturation too high.** Replace ~30% of saturated-colour
  pixels with grey neutrals.
- **Inter-panel gutter too wide.** Tighten wspace/hspace to ~0.06 of
  canvas, not the matplotlib default 0.2.
- **Statistical text floating in a legend.** Move significance markers
  to inline positions next to the data they label.
- **Hero panel proportionally too small or too large.** Aim for ~42-45%
  of canvas, not 30% (too small) or 60% (subordinates suffer).
- **Equal panel weight across all panels.** B/C/D should subordinate
  visually to A, not match A's weight.
