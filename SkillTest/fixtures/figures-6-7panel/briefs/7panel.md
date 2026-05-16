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
