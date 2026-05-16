# Figure brief: 9-panel — full preclinical-to-clinical pipeline

**Type:** figure — 9-panel composite, complex layout
**Use in:** R6.A 8+ panel layout extension test
**Data:** `../data/9p-{A..I}-*.csv`

## Scientific claim

> Compound X has an antitumor effect across cancer types (A, hero), backed by
> in vitro potency (B), favourable ADMET (C), in vivo target engagement (D),
> tolerable safety (E), survival benefit (F), a translational biomarker
> correlation (G), longitudinal biomarker dynamics distinguishing responders
> (H), and consistent benefit across pre-specified patient subsets (I).

## Required panels

- **A** (hero, ~25-30% canvas): grouped bar — tumour volume reduction
  CompoundX vs Vehicle across 4 cancer types
- **B**: dose-response for 3 compounds (X1-X3)
- **C**: violin plots of 3 ADMET metrics × 3 compounds
- **D**: timecourse of target engagement (CompoundX vs Vehicle), 6 timepoints
- **E**: safety bar, 4 organs × 3 dose groups
- **F**: Kaplan-Meier survival curves
- **G**: scatter of biomarker X vs clinical response, n=80
- **H**: longitudinal biomarker trajectory (Responder vs Non-responder),
  5 timepoints, n=20 each
- **I**: forest plot — response rate by patient subset, with 95% CI

## Style requirements

- Two-column width (~180 mm), one full page tall
- Hero A clearly the dominant panel (but proportionally less so than 4-panel
  case — there's more competing for canvas)
- Each panel answers one unique scientific question
- Unified palette family across all 9 panels
- Editable text; sans-serif Arial; 7-pt body, 8-pt panel labels
- No empty quadrants; no over-stretched panels

## R6.A purpose

Test whether figure-layout-defaults' "designate 4-cell hero region +
contiguous remainder, no empty cells" generalisation extends to 9 panels,
or whether at this complexity the runner needs a more specific 9-panel
default (e.g. 4-row × 3-col grid, hero spans 2x2 in upper-left).

This is the hardest layout test SkillTest has run.
