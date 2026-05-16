# Annotation — results_sweep

**Source:** figures4papers `figure_RNAGenScape/figures/results_sweep.png`.
Real research figure from RNA generation method comparison.

**Archetype:** Multi-method parameter sweep with confidence interval
bands. Use for hyperparameter / method comparison sweeps with continuous
x-axis.

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#c0c0c0` | 15.5 | neutral grey gridlines |
| `#6a6a6a` | 15.4 | text and dark axis |
| `#eaeaea` | 15.4 | background |
| `#959595` | 13.0 | mid-grey baselines |
| `#404040` | 12.2 | nearest-black for emphasis |
| `#ea95ea` | **7.5** | **signal magenta — proposed method** |
| `#eac0ea` | 4.6 | signal magenta soft (CI band fill) |
| `#406a95` | 4.6 | accent dark blue (one comparison method) |
| `#c0c0ea` | 2.9 | accent blue soft (CI band) |
| `#6a95c0` | 1.7 | accent blue mid |

**Critical observation:** **71% of foreground is grey/dark.** Only 7.5%
is the signal magenta (the proposed method). The figure visually
SCREAMS "this is the new method" because magenta is the loudest hue
in a sea of grey curves. Other comparison methods are coloured but
DESATURATED (`#406a95` dark blue, `#c0c0ea` light blue) so they
read as "context" rather than "competitor."

## Typography

- Method name labels: positioned AT the curve endpoints (right side
  of the plot), not in a legend block. Reader's eye lands at the
  rightmost data point and immediately knows which curve is which.
- X-axis label: 8pt
- Y-axis label: 8pt
- Tick labels: 7pt
- The label-at-curve-end pattern is the critical typographic move.

## White space

- Plot area uses ~80% of canvas; remaining 20% is axis labels and
  curve labels
- CI band fill alpha: ~0.18 — very faint, but visible on close inspection
- Line width for "main" methods: 1.6pt; for "comparison" methods:
  1.2pt. Subtle weight contrast.

## Visual rhythm

1. Eye lands on the magenta curve (highest saturation, only fully
   saturated hue in the plot)
2. Eye traces magenta curve LEFT-TO-RIGHT
3. Other curves register as "those didn't do as well" in peripheral
   vision
4. Curve-end labels confirm which method is which without forcing
   eye travel to a legend

## What makes this figure work

1. **Magenta-on-grey signal hierarchy.** 71% grey + 12% magenta
   instructs the reader exactly where to look. The proposed method
   wins the eye before any data is read.
2. **Labels at curve endpoints.** Eliminates the eye-travel cost of
   legend lookup. Reader knows curve identity without breaking gaze
   from the data.
3. **CI band alpha very faint (~0.18).** Uncertainty is visible on
   close reading but doesn't compete with the line itself for visual
   primacy.
4. **Line weight contrast (1.6 vs 1.2).** Subtle but real — the proposed
   method's line is heavier than baselines'. Combined with hue
   saturation, this is a 2-axis hierarchy.
5. **Magenta as the signal, not red.** Magenta on grey reads
   distinctively — no other paper in the same field used magenta as
   the signal hue, so the figure has visual identity. Red would have
   been generic.

## Typical amateur deltas

- All methods plotted at equal line weight + saturation — no hierarchy
- Legend block in the upper-right, dragging eye away from the data
- CI band alpha at 0.4+ — uncertainty competes with the line
- All curves use the matplotlib default Tab10 cycle (blue / orange /
  green / red...) — generic, no visual identity
- Signal method coloured the same as a baseline method by accident
