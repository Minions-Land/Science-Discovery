# Verdict — nature-figure / case-heatmap  (REVISED 2026-05-16)

**Round:** R1.A · **Rubric version:** v1
**Status:** Revised after user visual review.

## Headline

User: "candidate 这次排版会更好一点，但是颜色两者没啥质的差别". The heatmap is
the one case where the skill's mm-figsize discipline didn't blow up — 96 mm
height is genuinely enough room for 30 rows + cluster bar + colourbar.

## Numeric score (revised)

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4/4 | 4/4 | 0 | both single-panel by brief |
| Visual hierarchy / hero panel | n/a | n/a | n/a | not applicable |
| Palette discipline | 2/3 | 2/3 | 0 | as user observed: "颜色两者没啥质的差别" — both use `RdBu_r` for the body; candidate's neutral-grey cluster bar is mildly better but not "质的差别" |
| Typography & export | 0/3 | 3/3 | +3 | candidate editable text (28 `<text>` nodes vs 0); this case has enough canvas to actually use it readably |
| Statistical annotation | 2/3 | 3/3 | +1 | candidate adds explicit `TwoSlopeNorm(vcenter=0)` and out-of-axes caption documenting structure |
| Reproducibility | 3/3 | 3/3 | 0 | both runnable |
| Review readiness | 2/3 | 3/3 | +1 | candidate's layout discipline (every-other row label at fontsize 6, outside ticks) is genuinely cleaner |
| **Total** | **13/19** | **18/19** | **+5** | (single-panel; hero dim omitted) |

## What the skill actually changed

**This is the one case the skill helped without overshoot.** Editable text +
`TwoSlopeNorm(vcenter=0)` + every-other-row label discipline are all real
wins, and the 96 mm canvas is large enough that candidate's mm-precision
figsize doesn't crush legibility. Palette difference between baseline and
candidate is small (cluster bar hue swap; same RdBu_r body).

## What the skill missed or hurt

Nothing critical for this case. The skill's recommendation here matched the
brief's natural canvas size (~115 mm × 96 mm) so figsize discipline didn't
clash with text density.

## Visual inspection (what I should have done first)

User confirmed: candidate "排版会更好一点，颜色两者没啥质的差别". Geometry
backs this up — candidate at 333 × 280 pt (~118 × 99 mm) sits comfortably,
and the brief explicitly asked for ~115 mm wide.

## Bucket (revised)

**Calibrates response.** Both produce roughly the right artefact; candidate
is better defended (`TwoSlopeNorm`, fontsize discipline, label thinning,
explicit caption). Not "prevents real failure" — baseline is also usable.

## Porting recommendation (revised)

`fork-narrowly`. Port the heatmap-specific recipes:

- `TwoSlopeNorm(vcenter=0)` for any diverging colormap. Baseline relied on
  data symmetry — fragile.
- "Every-other row label at small fontsize when row count > 20" — the
  density rule.
- Outside-tick discipline (`direction="out", length=2.2, width=0.6`).

Don't port:

- The "neutral-grey + single-blue + faint-pink" cluster palette as a fixed
  recipe — it works for this case, but the rule "reserve green/red for
  directional signals" is the actual transferable insight; the specific
  colours are not load-bearing.

This case validates that **when canvas size is right for the brief, the
skill's content discipline is pure win**. The bar/multi-panel failures came
from cramming, not from the rcParams or palette discipline.
