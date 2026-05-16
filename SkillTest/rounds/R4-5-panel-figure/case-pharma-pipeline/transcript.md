# Transcript — case-pharma-pipeline

## Brief (verbatim)

# Figure brief: 5-panel — preclinical drug discovery composite

**Type:** figure — 5-panel composite, asymmetric layout
**Use in:** R4.B 5-panel asymmetric-grid persistence test
**Data:** `../data/panel-A-efficacy.csv`, `panel-B-doseresponse.csv`,
         `panel-C-admet.csv`, `panel-D-engagement.csv`, `panel-E-safety.csv`

## Scientific claim the figure must defend

> Compound X has antitumor efficacy across multiple cancer types (panel A,
> hero), with a favourable potency profile in vitro (B), acceptable ADMET
> properties (C), pharmacodynamic target engagement in vivo (D), and a
> tolerable safety profile (E).

## Required panels

- **Panel A** (hero, ~40% of canvas): grouped bar — tumour volume
  reduction (%) for CompoundX vs Vehicle across 4 cancer types,
  mean ± SD, n=8 mice per group, ** p<0.01 over Vehicle
- **Panel B** (~20% width): dose-response curves, 6 compounds (X1-X6),
  log x axis, IC50 marker per compound
- **Panel C** (~20% width): violin plots of 4 ADMET metrics (CL_int, Vd,
  F%, t_half), 3 compounds (X1-X3) — small multiples
- **Panel D** (~20% width): time course of target engagement (CompoundX
  vs Vehicle), 6 timepoints, mean ± SEM
- **Panel E** (bottom strip, full width or right column): toxicity bar
  per organ (5 organs × 3 dose groups: Vehicle / Low / High); n=8 mice

## Style requirements

- Two-column width (~180 mm), one page tall
- Hero panel A is the dominant element by area (~2× any other panel)
- Each panel answers ONE unique scientific question — no two panels
  redundant
- Unified palette family across panels (one signal colour for "Compound X
  / High dose / treatment direction", one neutral for Vehicle, one accent)
- Source-data column references in caption
- Editable text in SVG; sans-serif Arial 7-pt body, 8-pt panel labels
- Statistical annotation on panel A and panel E

## Failure modes to watch (this is the R4 hard-probe purpose)

R1.A and R1.B both failed on 4-panel composite by picking custom
asymmetric grids that produced empty quadrants or stretched panels.
With 5 panels, the standard `width_ratios=[2,1,1] + bottom-D`
pattern doesn't directly apply — the runner has to solve this layout
genuinely, not copy a default.

Watch for:
- 5-panel grid with empty cell(s)
- Panel E (5 organs, 3 groups = 15 bars) over-stretched into 180 mm
- Hero A getting <30% of canvas, becoming co-equal with B/C/D
- B/C/D squeezed into a strip too narrow to read 6 dose-response curves
- Legend duplicated across panels (palette family not unified)

## Baseline run

### What I did

Created `baseline_plot.py` as a naive matplotlib-default five-panel composite. It reads the five CSVs, uses a natural 3×3 GridSpec, makes panel A span the upper-left 2×2 area, places B and C in the right column, D in the bottom-left cell, and E across the bottom-right two cells. It exports `baseline.svg`, `baseline.pdf`, and `baseline.png` at 300 dpi.

### Failures or shortcuts

The baseline intentionally does not load or apply any figure skill. It uses matplotlib defaults, mixed default palettes, standard legends inside panels, no editable-SVG rcParam setup, no source-data caption, no global typography contract, and only minimal statistical marker text.

### Layout sanity checks performed

- PNG opened after render.
- No constrained-layout collapse warning appeared; `constrained_layout` was not used.
- No empty GridSpec quadrants were left.
- Panel A is visually dominant.
- Known baseline weakness: default legends and large default text consume space, and panel B/C/D/E are less integrated than a publication figure.

## Candidate nature-figure run

### Skill files actually loaded

- `SKILL.md`
- `references/figure-contract.md`
- `references/common-patterns.md`
- `references/api.md`

### Figure contract used

Core conclusion: Compound X shows cross-model antitumour efficacy with supporting potency, ADMET, pharmacodynamic engagement, and tolerability evidence.

Figure archetype: asymmetric mixed-modality quantitative figure.

Backend: Python only, using `/Users/mjm/miniconda3/bin/python3`.

Final size: `figsize=(8.6, 6.8)` inches, exported as SVG/PDF/PNG.

Panel map: A spans the left two columns and top two rows; B and C occupy compact upper-right panels; D spans the middle-right two columns; E spans the full bottom row.

### What changed because of the skill

Created `candidate-nature-figure_plot.py` with Nature-style rcParams, editable SVG text via `svg.fonttype = none`, PDF TrueType text, 7-pt body text, 8-pt panel labels, restrained spines, a unified palette, source-data caption hooks, mean ± SD for bar panels, mean ± SEM for the time course, and panel-level statistical annotations.

The candidate uses a semantic palette: blue for CompoundX / high-dose treatment direction, grey for Vehicle, and restrained teal/violet/pink accents for secondary compound families. Panel B uses direct endpoint labels instead of a legend because six dose-response curves in a compact panel made an in-axis legend collide with data.

### What I rejected or overrode from the skill

- I did not use millimetre sizing or conversion. The run instructions required default `figsize` in inches.
- I did not use `constrained_layout`; explicit GridSpec spacing plus `bbox_inches="tight"` avoided the known collapse failure.
- I used a full-width bottom strip for panel E. A right-column placement would have cramped 15 grouped bars or made the strip too tall relative to its data density.
- I used direct labels in panel B and a small inline key in panel A because default legends collided with dense curves or significance annotations.

### Layout sanity checks performed

- PNG opened after render.
- No constrained-layout collapse warning appeared.
- No empty GridSpec cells or empty quadrants were used.
- Panel A remains the dominant panel at roughly 40% of the canvas area.
- Panel E is not forced into a narrow side column; its width matches the 5 organs × 3 groups density.
- Legends/direct labels do not cover the plotted evidence after the layout pass.
- No candidate-scientific files were created or touched.

## Candidate scientific-figure-making run

### Skill files actually loaded

- `SKILL.md`
- `references/api.md`
- `references/common-patterns.md`
- `references/design-theory.md`

### Figure contract used

Core conclusion: Compound X shows cross-model antitumour efficacy with supporting in vitro potency, ADMET distribution, pharmacodynamic engagement, and tolerability evidence.

Backend: Python only, using `/Users/mjm/miniconda3/bin/python3` with `MPLCONFIGDIR=/private/tmp/mpl-r4`.

Final size: `figsize=(8.8, 7.2)` inches, exported as SVG/PDF/PNG at 300 dpi.

Chosen 5-panel grid: 3 rows × 4 columns, with `width_ratios=[1.4, 1.4, 1.1, 1.1]` and `height_ratios=[1.3, 1.1, 0.9]`. Panel A spans the upper-left 2×2 block; panel B occupies the upper middle-right cell; panel C is a 2×2 ADMET small-multiple grid in the upper-right cell; panel D spans the middle-right two cells; panel E spans the full bottom row.

### What changed because of the skill

Created `candidate-scientific_plot.py` as a self-contained implementation of the scientific-figure-making conventions: `PALETTE`, `FigureStyle`, `apply_publication_style()`, and `finalize_figure()` are included directly because the skill is guidance rather than an importable package in this snapshot.

The candidate uses the repository palette semantics: blue for CompoundX / high-dose treatment direction, neutral grey for Vehicle, green for low-dose/supportive positive encodings, and restrained teal/violet/red accents for secondary dose-response compounds. It uses minimalist top/right spine removal, editable SVG text via `svg.fonttype = none`, PDF TrueType text, sans-serif 7-pt body text, 8-pt bold panel labels, print-safe hatches/black bar edges, frameless legends, direct curve labels for the six-compound potency panel, mean ± SD for bar panels, mean ± SEM for the engagement time course, and source-data column references in the bottom caption.

### What I rejected or overrode from the skill

- I did not use ultra-wide single-row layout patterns because the brief required a 5-panel asymmetric composite with panel A dominant, not a single multi-metric row.
- I did not use a dedicated legend-only panel because that would add a sixth visual cell and violate the no-empty-quadrant / five-panel intent. Instead, legends are compact and direct labels are used in panel B.
- I did not use `constrained_layout`; explicit GridSpec spacing plus `bbox_inches="tight"` avoided the known constrained-layout collapse mode.
- I kept `figsize` in inches, as required by the run instructions.

### Layout sanity checks performed

- Rendered `candidate-scientific.svg`, `candidate-scientific.pdf`, and `candidate-scientific.png`.
- PNG opened after render; output size was `4065×2170` pixels.
- No constrained-layout collapse warning appeared; `constrained_layout` was not used.
- No empty quadrants or empty GridSpec cells were used.
- Panel A occupies roughly 40% of the planned GridSpec canvas area and remains visually dominant.
- Panel E is not over-stretched into a side column; the full-width bottom strip keeps 5 organs × 3 dose groups readable.
- Legend and direct labels do not overlap the primary plotted evidence after the layout pass.
