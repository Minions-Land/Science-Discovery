# Round Notes — R-future aesthetic-exemplars validation

**Cases:** case-7panel-redo (1 case)
**Date:** 2026-05-17
**Skill:** figure-aesthetic-exemplars (SkillTest-authored, R6.A response)
**Method:** diff R5.C 7-panel rule-only candidate against fig3-in-vivo-
efficacy-rich exemplar; revise top-3 deltas; user visual A/B.

## Headline

R-future aesthetic candidate **20/22** vs R5.C rule-only **21/22**.
The aesthetic workflow delivered palette+typography improvements ("色彩
最漂亮") but introduced 1 regression and inherited 1 rule-layer bug:

- ✓ Palette discipline transferred from exemplar to candidate
- ✓ 4-step typography ladder applied
- ✓ Tighter inter-panel gutter via subgridspec packing
- ✗ Trailing whitespace at bottom (constrained_layout choice)
- ✗ Bar y-axis bug: negative Vehicle data (-3%) clipped to zero floor
  by `set_ylim(0, ytop)`. Both R5.C AND R-future hit this — Step 6
  of figure-layout-defaults has a negative-value gap.

## Three findings

### 1. Aesthetic paradigm IS load-bearing for palette + typography
User explicitly graded R-future "色彩最漂亮" while R5.C is "颜色感觉差了
一点". The annotation card's specific recommendations (52% grey
foreground, single signal red, 4-step typography ladder) transferred
to the rendered figure. This is the first positive evidence that
exemplar diff workflow produces aesthetic gains rules alone don't.

### 2. Aesthetic skill INHERITS rule-layer bugs
R6.A added Step 6 (y-axis tune to data density) to figure-layout-defaults
explicitly to fix R6.A's "bar over-stretched" issue. The R-future
candidate REGRESSED on this dimension because it edited R5.C's
candidate_plot.py (which predates Step 6). Lesson: aesthetic-exemplar
workflow must audit existing script against CURRENT rules, not the
rules in effect when the script was authored.

### 3. Step 6 had an unexpected gap (negative values)
Step 6 said "if data spans <70% of nominal range, tune to data_min ±
headroom." Both candidates have data spanning ~70% (-3% to 65%) of
0-100, so the rule formally fires; but they implemented it as
`set_ylim(0, ytop)` (positive-floor only) instead of including
negative values. Patch needed.

## Patches applied to skill drafts (in this round)

1. **figure-layout-defaults Step 6 update**: cover negative-value case
   explicitly. To be patched in synthesis/proposed-skills/figure-layout-
   defaults.md.

2. **figure-aesthetic-exemplars workflow Step 5 update**: add
   "audit existing script against CURRENT skill rules, not original."
   To be patched in workflow/diff-and-revise.md.

## Cross-skill anchor confirmed (5th time)

The substantively-bounded specificity rule fired AGAIN here: the
exemplar annotation card's claim "52% of foreground pixels grey" is
the kind of bounded, verifiable, specific claim that's portable. The
user-grade "色彩最漂亮" came from a candidate that genuinely matched
the documented ratio, not from generic palette guidance.

## Recommendation

`conditional-import-strongly` for figure-aesthetic-exemplars after
2 patches:
1. figure-layout-defaults Step 6 negative-value patch
2. figure-aesthetic-exemplars workflow current-rules-audit patch

Both patches are local and small. With them, the aesthetic skill is
mature; without them, it can introduce regressions.

## What R-future leaves open

- Heatmap aesthetics: user noted "热力图古怪占位大信息量少." Heatmap-
  specific annotation card needed; existing fig4 card covers it
  partially.
- Vision-capable iteration loop: workflow assumes runner can self-
  judge visually. Future R-round could test "model + vision-judging"
  against "model + annotation-card-text-only."
- 8+ panel exemplar: gallery currently has only ≤7-panel composites.
  R6.A 9-panel showed even rule-correct 9-panel composites have
  whitespace + y-axis bugs; need a real-published 9-panel exemplar
  to diff against.
