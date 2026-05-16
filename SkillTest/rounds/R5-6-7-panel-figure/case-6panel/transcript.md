# Transcript — case-6panel

## Brief (verbatim)

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

## Baseline run

### What I did (incl. chosen grid pattern)

Used only the brief plus CSV schemas. I chose a natural `GridSpec(3, 4)` composite at `figsize=(7.2, 6.1)` inches: A spans `gs[0:2, 0:2]`, B spans `gs[0, 2:4]`, C spans `gs[1, 2:4]`, D spans `gs[2, 0:2]`, E uses `gs[2, 2]`, and F uses `gs[2, 3]`.

This makes A a 4-cell hero in a 12-cell grid, about 33% of the canvas by grid area, while using every cell.

### Failures or shortcuts

No plotting failures. Fontconfig reported that its normal cache directories were not writable, but `fc-match Arial` resolved `Arial.ttf: "Arial" "Regular"`.

### Layout sanity checks

Rendered `baseline.png` at 2160 x 1830 px. Visual PNG check: legible, no empty grid cells, A dominant by area, no constrained-layout collapse warning. E and F are compact but not over-stretched.

## Candidate run

### Skill files actually loaded

- figure-layout-defaults.md

### What changed because of the skill

The candidate explicitly followed the skill's 6-panel generalisation: a 4-cell hero region plus a contiguous, fully occupied remainder. I kept figsize in inches first, increased the canvas slightly to `figsize=(7.6, 6.3)`, and used mild width/height ratios so the hero stayed dominant without making the right-side and bottom panels feel like empty bands.

### Chosen 6-panel grid pattern

Used `GridSpec(3, 4, width_ratios=[1.15, 1.15, 1.0, 1.0], height_ratios=[1.15, 1.15, 1.0])`.

- A: `gs[0:2, 0:2]` as the 4-cell hero.
- B: `gs[0, 2:4]`.
- C: `gs[1, 2:4]`.
- D: `gs[2, 0:2]`.
- E: `gs[2, 2]`.
- F: `gs[2, 3]`.

The subordinate panels form a contiguous filled remainder around A with no holes. The weighted grid gives A roughly 34% of the canvas area.

### What I overrode (if any) and why

The skill gives only a general 6-panel rule, not exact ratios. I overrode equal grid sizing with slight `width_ratios` and `height_ratios` to preserve A dominance while avoiding excess width in the smaller E/F panels. I also used a slightly larger figure than baseline after PNG inspection.

### Layout sanity checks performed

- "constrained_layout collapsed to zero" fired? no
- final candidate render legible? yes
- hero panel dominant by area? yes
- empty quadrants? no
