# Transcript — case-multi-panel

## Brief (verbatim)

# Figure brief: multi-panel — drug discovery composite

**Type:** figure — 4-panel composite, asymmetric layout
**Use in:** R1.A nature-figure, R1.B scientific-figure-making
**Data:** `../data/multi-panel-A-dose.csv`, `multi-panel-B-scatter.csv`,
         `multi-panel-C-timecourse.csv`, `multi-panel-D-fraction.csv`

## Scientific claim the figure must defend

> Compound X is a more potent and selective modulator than Compound Y, validated
> across pharmacology (panel A), structural prediction (B), in vivo cytokine
> response (C), and cell-resolution genotype rescue (D).

## Required panels

- **Panel A** (hero, ~50% width): two-compound dose-response curves with 95% CI
  bands; mark EC50 with a thin vertical guide
- **Panel B** (~25%): scatter of predicted vs measured pK, two groups
  (kinase / GPCR), unity line and slope shown as text annotation per group
- **Panel C** (~25%): time course of 3 biomarkers (IL6, TNFa, IL10),
  mean ± SEM, shared y-axis, log scale optional
- **Panel D** (bottom strip, full width or right column): bar chart of fraction
  of responding cells by genotype (WT / Het / KO), n=8 mice per group, dots
  overlaid

## Style requirements

- Two-column width (~180 mm), single page-height
- Hero panel A is roughly twice the area of any other; B/C/D are subordinate
- Each panel answers one unique scientific question (no two panels redundant)
- Unified palette family across panels — one signal colour for "Compound X" or
  "KO" treatment-direction, one neutral, one accent
- Source-data column references in caption (panel A → file A, etc.)
- Statistical annotation: panel D should show pairwise tests vs WT
- Editable text in SVG; sans-serif Arial 7-pt body, 8-pt panel labels

## Failure modes to watch

- Equal-size 2x2 grid (kills the hero)
- Four different palettes across panels
- Panel B unity line missing — readers can't judge over/under-prediction
- Panel C with a separate y-axis per biomarker — kills cross-comparison
- No source-data caption hooks
- Panel D bars without data points (Nature requires per-replicate dots when n &lt; 10)

## Baseline run

### What I did

Created `baseline_plot.py` as a naive matplotlib-default academic figure. It reads the four CSVs, makes a simple 2x2 subplot layout, plots panel A dose-response curves with CI bands and EC50 guide lines, panel B scatter with unity line, panel C time-course error bars, and panel D genotype bars with overlaid mouse dots.

### Failures or shortcuts

The baseline intentionally does not load or apply the scientific-figure-making skill. It uses matplotlib default rcParams, an equal-size 2x2 grid, default color cycling, default legends, no source-data caption, and no panel-D statistical annotation.

## Candidate run

### Skill files actually loaded

- SKILL.md
- references/api.md (palette, `apply_publication_style`, `finalize_figure`, SVG/PDF/PNG export, validation expectations)
- references/common-patterns.md (multi-panel layout, dedicated legend panel, semantic color mapping, print-safe bars)
- references/design-theory.md (publication typography, minimalist spines, vector text, export policy, palette rationale)

### What changed because of the skill

The candidate applies a publication rcParams preset with sans-serif font fallbacks, 7-pt body text, 8-pt panel labels, top/right spines removed, frameless legends, editable SVG text, and 300-dpi PNG export. It uses the skill palette semantically: blue for Compound X / KO direction, neutral gray for Compound Y / WT, green for Het/IL10, red for IL6, teal/violet for scatter groups. Panel D uses edged bars and overlaid individual mouse points. A source-data caption maps each panel to its CSV file.

### What I rejected (or overrode) from the skill

- explicit note on figsize and grid choices: I did not use millimeter conversion or the skill's ultra-wide examples because the R1.A lessons required default figsize in inches and enough height for legend, caption, and density. I used `figsize=(8.0, 6.2)` inches for the candidate, then saved with tight bounding boxes.
- The skill suggests `tight_layout(pad=2)` as a common finishing pass. I used explicit GridSpec spacing plus `bbox_inches="tight"` at save time to avoid constrained-layout collapse and to preserve the bottom caption.
- I used a dedicated legend axis in the middle-right GridSpec cells. This is a filled layout cell, not an empty quadrant.

### Layout sanity checks performed

- hero panel dominant? gridspec free of empty cells? legend non-overlapping? yes: panel A spans two rows in the 2x1 left hero column, B/C occupy the two top-right cells, the shared legend occupies the middle-right span, and D spans the full bottom row.
- "constrained_layout collapsed to zero" fired? no. `constrained_layout` was not used, and no such warning appeared.
- final candidate render legible? yes. B/C are readable, D is not crammed, panel D dots and WT comparisons are visible, and the legend does not overlap plotted data.
