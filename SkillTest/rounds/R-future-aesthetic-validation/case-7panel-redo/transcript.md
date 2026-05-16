# Transcript — case-7panel-redo (R-future aesthetic validation)

## Brief (verbatim — same as R5.C 7-panel)

# Figure brief: 7-panel — preclinical pipeline + clinical correlate

**Type:** figure — 7-panel composite, complex asymmetric layout
**Use in:** R5.C 7-panel layout extension test
**Data:** `../data/6panel-{A,B,C,D,E,F}-*.csv` + `../data/7panel-G-correlation.csv`

## Scientific claim

> Same as 6-panel + Panel G shows that biomarker X correlates with clinical
> response (r=0.7, n=80), establishing a translational handle.

## Required panels

- A-F: same as 6-panel brief
- **G**: scatter — biomarker X vs clinical response %, n=80, regression
  line + 95% CI band

## Style requirements

Same as 6-panel + add G as a translational link in the bottom row.

## R5.C purpose

Hardest of the layout-default extension tests. 7 panels with one being
a clinical correlate (lower priority than efficacy hero). Runner has to
solve panel hierarchy AND grid geometry simultaneously.

## Source draft (the R5.C 7-panel candidate)

Path: /Users/mjm/Skill/SkillTest/rounds/R5-6-7-panel-figure/case-7panel/candidate.png

## Chosen exemplar

gallery/fig3-in-vivo-efficacy-rich.png

## Top-3 deltas identified (diff-and-revise output)

1. Palette ratio: the R5.C draft uses saturated blue/green/orange/purple across several panels; the exemplar is grey-dominant with one signal red reserved for the directional treatment condition and only muted subordinate hues.
2. White-space and packing: the R5.C draft is rule-correct but vertically loose; the exemplar reads as one composite because the inter-panel gutters are tighter and related subordinate panels are packed as a local group.
3. Statistical/typographic hierarchy: the R5.C draft relies on legends and similarly weighted large text; the exemplar uses inline labels, local significance marks, and a four-step text ladder from 9 pt panel letters down to 5.5 pt notes.

## Revision applied (which deltas, what code change)

- Delta 1 -> code change: replaced the multi-hue cycle with grey foreground, one signal red `#c04040` for CompoundX / High-dose directional effects, one neutral blue `#406a95` for subordinate quantitative traces, and light grey / pale blue support colours.
- Delta 2 -> code change: rebuilt the layout as `gridspec(3, 4)` with A at `gs[0:2, 0:2]`, B/C/D packed into a nested upper-right subgridspec, E spanning bottom-right, F/G as bottom-left translational panels, and manual `wspace` / `hspace` rather than `constrained_layout`.
- Delta 3 -> code change: moved dose-response EC50 text and treatment line labels inline, used local brackets over the panel-A bar pairs, and set panel letters 9 pt bold, axis labels 8 pt, ticks 7 pt, inline annotations 6.5 pt, and notes 5.5 pt.

## Iteration count

1 validation iteration, with one small render-cleanup pass to de-crowd EC50 labels and prevent an inline endpoint label from clipping.

## Layout sanity checks

- constrained_layout collapsed to zero: no; the script does not use constrained_layout.
- font fallback: no; Arial was detected by Matplotlib and selected.
- legend overlap: no obvious legend-data overlap in the final PNG.
- y-axis zoomed to data: yes; panel A uses data-derived headroom instead of a nominal 0-100 range, and safety / clinical panels are also data-bounded.

## Skill files actually loaded

- figure-aesthetic-exemplars/SKILL.md
- figure-aesthetic-exemplars/workflow/diff-and-revise.md
- figure-aesthetic-exemplars/typography/reference.md
- figure-aesthetic-exemplars/gallery/fig3-in-vivo-efficacy-rich.annotation.md
- figure-aesthetic-exemplars/gallery/fig3-in-vivo-efficacy-rich.png (opened as the exemplar image)
- figure-layout-defaults.md (the prerequisite rule-based skill)

## What I rejected from the exemplar

- The exemplar includes a timeline/schematic panel; this fixture has no timeline data, so I did not invent a schematic.
- The exemplar is much denser, with more than seven panels; I kept the required 7-panel brief and used the exemplar only for palette, packing, hierarchy, and inline labeling decisions.
- I did not copy the exemplar's full four-treatment palette literally. The fixture's directional treatment contrast is CompoundX / High dose versus control, so the red signal was mapped to that direction and blue was kept as a neutral quantitative support hue.
