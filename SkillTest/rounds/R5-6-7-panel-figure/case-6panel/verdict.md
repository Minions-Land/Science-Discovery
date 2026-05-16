# Verdict — figure-layout-defaults / case-6panel

**Round:** R5.C · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary)

## User visual review (verbatim)

> Case 1 baseline 和 candidate 画出来都是一样的.

## Numeric score

| Dim | Pts | Baseline | Candidate | Δ |
|---|---|---|---|---|
| Information architecture | 4 | 4/4 | 4/4 | 0 |
| Visual hierarchy / hero | 3 | 3/3 | 3/3 | 0 |
| Palette discipline | 3 | 3/3 | 3/3 | 0 |
| Typography & export | 3 | 3/3 | 3/3 | 0 (both 100+ `<text>` nodes — Codex applied rcParams in both runs because the brief explicitly required editable text) |
| Statistical annotation | 3 | 3/3 | 3/3 | 0 |
| Reproducibility | 3 | 3/3 | 3/3 | 0 |
| Review readiness | 3 | 3/3 | 3/3 | 0 |
| **Total** | **22** | **22/22** | **22/22** | **0** |

## What this case tells us

The skill's value at 6 panels is **zero or near-zero** because Codex's
naive default grid for 6-panel composites (3×4, A=gs[0:2,0:2], B=gs[0,2:4],
C=gs[1,2:4], D=gs[2,0:2], E=gs[2,2], F=gs[2,3]) is **already** what the
skill's "designate 4-cell hero + contiguous remainder, no empty cells"
rule recommends. User confirmed the two outputs are visually identical.

This is informative: the skill's failure mode of "pushing runner toward
worse asymmetric grid" did NOT fire at 6 panels. The 4-cell-hero
generalisation is genuinely the natural answer. The skill saves work
mostly when the runner would otherwise pick a grid that omits cells or
over-stretches panels — which Codex already avoided here without the skill.

## Bucket

**Matches baseline.** Codex naive baseline already used the layout the
skill recommends; the skill added marginal `width_ratios` / `height_ratios`
fine-tuning that didn't change the visual output. No skill effect at this
panel count for this fixture.

## Why this matters for the port plan

The figure-layout-defaults skill's value scales with panel count complexity:

- **4-panel (R1.A + R1.B)**: skill HURTS by pushing runner to L-shape grid;
  the rule "default `[2,1,1] + bottom-D`" prevents the harm. Real win.
- **5-panel (R4.B)**: skill HURTS unless the 5-panel `gs[0:2,0:2] + ...`
  default is named explicitly. Real win once the explicit rule is added.
- **6-panel (R5.C this case)**: skill is **inert** — the natural grid IS
  the right grid. No measurable win.
- **7-panel (R5.C next case)**: TBD — separate verdict.

This is a healthy finding: the skill is load-bearing for 4-panel and
5-panel composites (the cases where the runner would otherwise drift to
custom grids), and inert for 6-panel where the matplotlib default
naturally aligns with the skill's "no empty cells" rule.

## Porting recommendation (no change)

The figure-layout-defaults port plan from R1+R4 stands. The 6-panel test
confirms the skill's generalisation IS the right answer at 6 panels;
the skill just isn't load-bearing because the runner finds the same
answer naturally.
