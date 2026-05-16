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
