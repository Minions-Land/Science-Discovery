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
