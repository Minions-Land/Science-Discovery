# Transcript — case-7panel

## Brief (verbatim)

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

## Baseline run

### What I did (incl. chosen 7-panel grid)

Used matplotlib defaults plus the 7-panel brief and the A-F details from the 6-panel brief. I chose a natural `GridSpec(3, 4)` at `figsize=(9.2, 6.8)` inches: A spans `gs[0:2, 0:2]`, B spans `gs[0, 2:4]`, C spans `gs[1, 2:4]`, and D/E/F/G fill the bottom row as four compact single cells.

This gives A a 4-cell hero region in a 12-cell grid, approximately 35% of the weighted grid area, with no unused cells.

### Layout sanity checks

Rendered `baseline.png` at 2757 x 2040 px. No `constrained_layout collapsed to zero` warning occurred. Visual PNG check: all seven panels are legible, A is dominant, no grid cells are empty, and the four bottom panels are compact rather than horizontally over-stretched. I increased the baseline canvas from the first render and shortened the bottom-row titles because matplotlib default title sizing crowded the bottom row.

## Candidate run

### Skill files actually loaded

- `/Users/mjm/Skill/SkillTest/synthesis/proposed-skills/figure-layout-defaults.md`

### What changed because of the skill

The candidate explicitly applied the 7-panel generalisation: designate a 4-cell hero region and arrange all subordinate panels as a contiguous remainder. I chose figsize in inches first, kept all cells occupied, and used modest width/height ratios to keep A near 30% of the canvas without stretching subordinate panels into long bands.

### Chosen 7-panel grid

Used `GridSpec(4, 4, width_ratios=[1.25, 1.25, 1.0, 1.0], height_ratios=[1.25, 1.25, 1.0, 1.0])` at `figsize=(7.9, 7.0)` inches.

- A: `gs[0:2, 0:2]` as the 4-cell hero.
- B: `gs[0, 2:4]`.
- C: `gs[1, 2:4]`.
- D: `gs[2, 0:2]`.
- E: `gs[2, 2:4]`.
- F: `gs[3, 0:2]`.
- G: `gs[3, 2:4]`.

The subordinate panels form one contiguous filled remainder around A; no cells are empty.

### Layout sanity checks (warnings? legible? hero dominant? empty cells?)

Rendered `candidate.png` at 2370 x 2100 px. No `constrained_layout collapsed to zero` warning occurred. Visual PNG check: all labels are legible, A remains the largest panel at about 31% of weighted grid area, the six subordinate panels form a contiguous occupied remainder, no cells are empty, and no panel is stretched into a low-density strip.
