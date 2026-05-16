# R-future Synthesis (Aesthetic Exemplar Paradigm Validation)

**Round:** R-future (1 sub-round: case-7panel-redo)
**Date:** 2026-05-17
**Status:** Research-zone artefacts. SKILL-paradigm validation round.

## Summary

The R-future round tested whether the figure-aesthetic-exemplars skill
(SkillTest-authored from R6.A user feedback) closes the "rules-correct
but bland" gap that R6.A identified.

## Headline

The aesthetic exemplar paradigm IS load-bearing for palette + typography,
but inherits rule-layer bugs and exposes a workflow gap. With 2 small
patches, the paradigm is sound; without them, it can introduce
regressions.

User-confirmed: "右边那张图(R-future aesthetic) 色彩最漂亮" vs R5.C
rule-only "颜色感觉差了一点". Palette discipline transferred from
exemplar fig3-in-vivo-efficacy-rich's annotation card to the rendered
candidate.

But user also caught: "右边图柱子拉得太大太高，矮的柱子完全不见了."
Both R5.C and R-future have a Vehicle-bar-clipped-to-zero bug from
`set_ylim(0, ytop)` with negative-value data — Step 6 of
figure-layout-defaults didn't cover negative-value case.

## Three load-bearing findings

### 1. Exemplars deliver palette + typography in a way rules cannot

The fig3 exemplar's annotation card documented:
- 52% grey foreground (vs amateur 30%+ saturated)
- Single signal red `#c04040` for direction only (~6% of pixels)
- 4-step typography ladder (panel letters 9pt -> caption notes 5.5pt)
- Tight inter-panel gutter (~6% canvas)

When the runner diffed R5.C against this and revised, the rendered
candidate took on these properties — and the user saw the difference.

This is positive evidence that REFERENCE-DRIVEN SKILL paradigm
(annotation cards) communicates aesthetic information that
RULE-DRIVEN SKILL paradigm (rcParams + PALETTE dict) cannot.

### 2. Aesthetic skill is a polish step, not a replacement

The R-future candidate inherited R5.C's `set_ylim(0, ytop)` bug,
because Step 6 of figure-layout-defaults was authored AFTER R5.C's
plot.py was written. The exemplar workflow said "edit existing
script, don't re-do from scratch" — but didn't say "audit existing
script against CURRENT rules, not original rules."

Patched: workflow Step 5 now includes a current-rules audit
checklist before applying the diff-and-revise edit.

### 3. Step 6 has a negative-value gap (now patched)

Step 6 originally said "if data spans <70% of nominal range, re-scale
to data_min ± headroom." Vehicle = -3%, CompoundX = 65%, span = 68
units = 68% of 0-100 — formally just inside the rule trigger. But
even if the rule had fired, the candidate's `set_ylim(0, ytop)`
literal interpretation clipped the negative side.

Patched: Step 6 now explicitly says "never use `set_ylim(0, ytop)`
when data includes negative values."

## Patches applied (in synthesis/proposed-skills)

| File | Change | Reason |
|---|---|---|
| `figure-layout-defaults.md` Step 6 | Add negative-value clause + explicit "never 0-floor with negative data" warning | Caught by R-future user review |
| `figure-aesthetic-exemplars/workflow/diff-and-revise.md` Step 5 | Add current-rules audit checklist before editing existing script | Caught by R-future inheritance pattern |

## Numeric audit

| Run | User score (visual) | Numeric rubric (/22) | Bucket |
|---|---|---|---|
| R5.C 7-panel candidate (rule-only) | 80-90 / 100 (R5.C verdict, "几乎完美") | 21/22 | Calibrates +10 |
| **R-future 7-panel aesthetic-polished** | "色彩最漂亮" but bar bug + 留白 | **20/22** | Calibrates with bug |

The single-point delta on the rubric reflects: palette gain +1 - bar legibility -1 - whitespace bug 0 (already counted in review-readiness).

## Bucket per skill

| Skill | Bucket | Recommendation |
|---|---|---|
| figure-aesthetic-exemplars | Calibrates response (palette+typography) when chained correctly | **conditional-import-strongly** after 2 patches |
| figure-layout-defaults | Was Calibrates +10; with Step 6 negative-value patch, holds | import-strongly |

## Cross-skill anchor confirmed (now 6 fixtures)

> **Substantively-bounded specificity, not vague good-faith promises.**

R-future adds a 6th fixture: the exemplar annotation card's claim
"52% of foreground pixels grey" is the kind of bounded, verifiable
specific claim that ports across runs. Generic palette guidance
("use colourblind-safe palette") would not have transferred.

## Cross-validation

| Test | Result |
|---|---|
| Does exemplar workflow deliver palette gains rules can't? | **YES** (user-confirmed "色彩最漂亮") |
| Does exemplar workflow inherit rule-layer bugs? | **YES** (Step 6 negative-value bug caught here) |
| Is the aesthetic paradigm worth porting? | **YES with 2 patches** |
| Does it close the R6.A "rules vs beauty" ceiling? | **PARTIALLY** — palette + typography close. Layout aesthetic still has gaps (heatmap proportions, hero panel sizing at high panel counts) |

## What R-future leaves open

1. **Heatmap aesthetic patterns.** User: "热力图古怪占很大位置但信息量少."
   Existing exemplar fig4 covers single-cell heatmap; needs a separate
   annotation card for "small heatmap as a panel" (when heatmap is one
   of many panels, not the hero).

2. **Vision-capable iterative loop.** Workflow assumes runner self-judges
   visually. If model can't see PNG, workflow degrades. R-future-2
   candidate: model + vision-judge + diff-and-revise.

3. **8+ panel exemplar.** Gallery is biased toward ≤7 panel. Real
   published 8/9-panel composites would let us diff against rather
   than reason about the layout.

## Decision required from user (post R-future)

R-future closes the aesthetic-exemplar paradigm validation. With the
2 patches applied, the figure-aesthetic-exemplars skill is mature for
port.

The full R1-R6 + R-future port plan now stands:

| Item | Status |
|---|---|
| 5 promoted-category READMEs (academic-writing, academic-figures, review-quality, submission-mechanics) | mature |
| 8 proposed-skills/proposed-updates drafts | mature |
| figure-aesthetic-exemplars (NEW from R-future) | conditional-import after 2 patches APPLIED |
| substantively-bounded specificity → common contract | confirmed across 6 fixtures |
| deslop family skip | confirmed across 24 cells |

Decision options:
1. Land R1-R6 + R-future ports together
2. Run R-future-2 (heatmap aesthetic + vision-capable iteration) before landing
3. Pause and revisit
