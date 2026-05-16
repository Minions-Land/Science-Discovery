# Verdict — nature-figure / case-bar  (REVISED 2026-05-16)

**Round:** R1.A · **Rubric version:** v1
**Status:** Revised after user visual review flagged candidate as unusable.

## Headline

User visual review: "candidate 完全就挤在了一起，丝毫都没有排版" — confirmed
by SVG geometry. Baseline is "非常的朴素，颜色也很磨人，但是起码显示是正常的".

## Numeric score (revised)

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4/4 | 4/4 | 0 | single-panel both |
| Visual hierarchy / hero panel | n/a | n/a | n/a | not applicable |
| Palette discipline | 1/3 | 2/3 | +1 | candidate's single-blue + hatch is greyscale-safe but at 7-pt + 178-pt-tall canvas the hatches read as noise; baseline's 4-saturated cycle is "magpie" but legible |
| Typography & export | 0/3 | 2/3 | +2 | candidate emits editable `<text>` (18 nodes vs baseline 0) — real submission gain — BUT 7-pt body text on a 63 mm-tall canvas is below readable density; the editable-text win is "would-help-if-figure-fit" |
| Statistical annotation | 2/3 | 2/3 | 0 | both add `*`/`**`. Candidate's caption pushed below-axes overlaps in the rendered figure |
| Reproducibility | 3/3 | 3/3 | 0 | both runnable end-to-end |
| Review readiness | 2/3 | 0/3 | -2 | **candidate figure is not submittable as rendered.** Legend + caption + significance markers are all crammed into 63 mm of vertical space; baseline at 102 mm is loose but readable |
| **Total** | **12/19** | **13/19** | **+1** | (single-panel; hero dim omitted) |

## What the skill actually changed

The skill emitted **content-correct** discipline (editable text, palette
families, mm-precision sizing) but the runner applied it without slack:
`figsize=(85/25.4, 58/25.4)` is 85 mm × 58 mm, and on top of that the
candidate placed legend above-axes, caption below-axes, and 4-series hatched
bars with `*`/`**` brackets between them. The matplotlib
`constrained_layout collapsed to zero` warning that fired during rendering
was the real signal — I previously marked it cosmetic, which was wrong.
`bbox_inches="tight"` recovered file output but the actual rendered figure
is unreadably cramped.

## What the skill missed or hurt

**Layout overshoot is the failure mode.** The skill's "single column ~85 mm"
rule is correct for the *width*, but the runner blindly carried the same mm
discipline into height and let everything else (legend, caption, signif
brackets, sig-marker line) compete for a 58 mm vertical budget at 7-pt text.
Baseline at default `(6, 4)` inches = 152 × 102 mm is too big for single-column
but **renders legibly**.

The skill is missing a "if you carve the figsize tight, you must compromise on
either legend placement OR caption position OR series hatching density" rule.
Without that rule, the runner applies all three and produces an unsalvageable
artefact.

## Visual inspection (what I should have done first)

User confirmed: candidate is "挤在一起，丝毫没有排版，根本用不了"。
Baseline is "朴素，颜色磨人，但显示正常". SVG dimensions back this up:

- baseline: `432 × 288 pt` ≈ 152 × 102 mm at default 8–10 pt font → readable
- candidate: `361 × 178 pt` ≈ 127 × 63 mm at 7 pt body → text density too high

## Bucket (revised)

**Overreaches (partial).** The skill prevents one real failure (rasterised
text) but causes a different one (unreadable layout). Net delivery is
**negative**: a non-editable but readable figure beats an editable but
unreadable one for any practical use.

## Porting recommendation (revised)

`fork-narrowly`. Port only:

- `rcParams` block: `font.family`, `font.sans-serif`, `svg.fonttype="none"`,
  `pdf.fonttype=42`, spine policy, `legend.frameon=False`. These are pure
  wins, no layout cost.
- The PALETTE-as-dict pattern for cross-panel coherence.

Do **NOT** port:

- `figsize=(width_mm/25.4, height_mm/25.4)` mm-exact patterns. The Writer
  role's MinionsOS skill should keep figsize in inches and let users compress
  to mm only at submission time, after layout is confirmed.
- `constrained_layout=True` paired with above-axes legend + below-axes caption
  in the same figure. That combination is what blew up here.
- Hatch + alpha-graded single-hue family for 4+ series at 7-pt body —
  collapses below readability density. Reserve hatches for ≤3 series, or
  bigger figures.
