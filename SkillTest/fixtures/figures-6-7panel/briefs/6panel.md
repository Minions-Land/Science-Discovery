# Figure brief: 6-panel — preclinical pipeline with safety + survival

**Type:** figure — 6-panel composite, asymmetric layout
**Use in:** R5.C 6-panel layout extension test
**Data:** `../data/6panel-{A,B,C,D,E,F}-*.csv`

## Scientific claim

> Compound X has antitumor efficacy (A, hero) backed by in vitro potency (B),
> tolerable ADMET (C), in vivo target engagement (D), acceptable
> multi-organ safety (E), and a survival benefit in tumour-bearing mice (F).

## Required panels

- **A** (hero, ~30-40% canvas): grouped bar — tumour volume reduction
  CompoundX vs Vehicle across 4 cancer types, mean ± SD, ** p<0.01
- **B**: dose-response curves, 3 compounds (X1-X3)
- **C**: violin plots of 3 ADMET metrics (CL_int, Vd, F%), 3 compounds
- **D**: time course of target engagement, mean ± SEM, 6 timepoints
- **E**: safety bar — toxicity score by organ × group (4 organs × 3 groups)
- **F**: Kaplan-Meier survival curves (CompoundX vs Vehicle, n=20 each)

## Style requirements

- Two-column width (~180 mm), one page tall
- Hero A genuinely dominant by area
- Each panel answers one unique scientific question — no two panels redundant
- Unified palette family across panels
- Editable text; sans-serif Arial 7-pt body, 8-pt panel labels
- No empty quadrants; no over-stretched panels

## R5.C purpose

Test whether the figure-layout-defaults skill's "designate 4-cell hero +
contiguous remainder, no empty cells" generalisation holds at 6 panels,
or whether the runner needs a more specific 6-panel default.
