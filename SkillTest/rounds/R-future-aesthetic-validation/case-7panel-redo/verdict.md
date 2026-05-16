# Verdict — R-future aesthetic validation / case-7panel-redo

**Round:** R-future · **Date:** 2026-05-17 · **Rubric:** v1
**Visual judge:** user (primary, 3-way + A/B comparison)

## User visual review (verbatim, abridged)

**Three-way (exemplar fig3 vs R5.C rule-only vs R-future aesthetic):**
> 1. EXEMPLAR fig3: 色彩最丰富，样式多样甚至显得花哨；A 部分有点小不合群；
>    左上角的热力图古怪，占了很大位置但信息量少.
> 2. R5.C rule-only: 排版非常合规，整体中规中矩，挑不出毛病；缺点是颜色
>    感觉差了一点.
> 3. R-future aesthetic: 色彩最漂亮；排版有点问题，下面似乎有点空白；
>    柱子拉得太大太高，矮的柱子完全不见了.

**Direct A/B (R5.C vs R-future):**
> R-future 排版下面留白有点多. 如果留白不是刻意的，R-future 排版更好，
> 信息密度更大. 两者通病: 柱状图占位大、灰色柱看不见(y 轴设置有问题).

## Verified by structural inspection

1. **Trailing whitespace:** R-future 2.9% trailing blank rows
   (PNG 2070 px high, last content row at 2008). R5.C 0.6%. The user's
   留白 observation IS real — R-future's constrained_layout has 5x
   the bottom margin of R5.C. Bug, not HTML rendering.

2. **Bar y-axis bug (BOTH candidates share):**
   - R-future panel A: `ax.set_ylim(0, ytop)` (line 99 of plot.py)
   - R5.C panel A: `ax.set_ylim(0, ymax)` (line 67)
   - Vehicle group data is negative (~-3% tumour reduction; data
     point is -5% to -1%). The 0-floor truncates Vehicle bars to zero
     visible height. Only CompoundX bars are visible.
   - **figure-layout-defaults Step 6** ("y-axis tune to data density")
     said "if data spans <70% of nominal range, tune to data_min ±
     headroom" — but did NOT say "if data includes negative values,
     start ylim at data_min, not 0." Rule has a gap; both candidates
     hit it.

## Numeric score

| Dim | Pts | R5.C rule-only | R-future aesthetic |
|---|---|---|---|
| Information architecture | 4 | 4/4 | 4/4 |
| Visual hierarchy / hero | 3 | 3/3 | 3/3 |
| Palette discipline | 3 | 2/3 ("颜色感觉差了一点") | **3/3 ("色彩最漂亮")** |
| Typography & export | 3 | 3/3 (rule-correct) | 3/3 (4-step ladder applied) |
| Statistical annotation | 3 | 3/3 | 2/3 (灰柱不可见 — Vehicle direction lost) |
| Reproducibility | 3 | 3/3 | 3/3 |
| Review readiness | 3 | 3/3 ("挑不出毛病") | 2/3 (留白 + 灰柱 bug) |
| **Total** | **22** | **21/22** | **20/22** |

## Headline

**R-future got the palette right but lost ground on bar legibility +
trailing whitespace.** Net: marginally lower than R5.C rule-only.
This is the first SkillTest round where adding a layer of skill made
things WORSE (not catastrophically — palette is genuinely better —
but the bar bug is a real review-readiness loss).

## What the exemplar workflow successfully delivered

User's "色彩最漂亮" confirms the **palette discipline** ported
across:
- Grey-dominant foreground (52%+ neutral)
- Single signal red `#c04040` for direction
- Subordinate accent blue
- 4-step typography ladder
- Tight inter-panel gutter

These are the lessons fig3-in-vivo-efficacy-rich's annotation card
documented; they DID transfer to the candidate when the runner did
the diff-and-revise workflow.

## What the exemplar workflow failed to catch

1. **Bar y-axis with negative data values.** This was a Step 6 rule
   gap in figure-layout-defaults. The exemplar didn't have negative
   data so the rule didn't fire. Both candidates produced the same
   bug. The exemplar workflow doesn't supersede the rule layer; it
   inherits its gaps.

2. **Trailing whitespace.** The candidate's `figsize=(11, 7.5)` plus
   constrained_layout left ~3% of canvas blank at bottom. The
   exemplar's annotation card mentioned "tight inter-panel gutter"
   but didn't mention "match figsize aspect to content density"
   explicitly. Another gap.

3. **Bar over-stretching at panel A.** R6.A user feedback said "假设
   数值越高越好，最低柱多出一点点就行 — 不要 0 到 100 留 35% 空白."
   The R6.A finding became Step 6 of figure-layout-defaults but the
   R-future candidate didn't apply it because Step 6 was authored
   AFTER R5.C's candidate.py was inherited. Future workflow: when
   re-rendering an old draft, audit the script against ALL CURRENT
   skill rules, not just the ones the original draft was built with.

## Bucket

**Calibrates response with bug.** Aesthetic exemplar workflow
delivers genuine palette/typography improvement (user-confirmed).
But it inherits gaps from the underlying rule layer (Step 6's
negative-value blind spot), and adds one new failure mode (trailing
whitespace from figsize choice). Net A/B vs R5.C is marginal.

## What this means for the figure-aesthetic-exemplars port

The skill IS load-bearing for palette + typography (the things
exemplars uniquely communicate). But it does NOT supersede the rule
layer's bugs. Both layers must be correct.

**Updates required before final port:**

1. **figure-layout-defaults Step 6 patch (negative values):**
   Update Step 6 to read:
   > If data span includes negative values OR (data_max - data_min)
   > is less than 70% of nominal range: set ylim to
   > `[data_min - 0.1*span, data_max + 0.15*span]`. The 0-floor
   > applies only when the data is naturally non-negative AND the
   > absolute level is part of the message.

2. **figure-aesthetic-exemplars workflow Step 5 audit checklist:**
   When revising the script per top-3 deltas, also audit against the
   COMPLETE current rule set (not just the rules the original draft
   followed). Add to workflow/diff-and-revise.md.

3. **Inherit-don't-replace rule:** When the workflow says "don't
   re-do from scratch, edit existing script," the runner must
   explicitly verify each pre-existing axis-range / figsize / spacing
   choice against current rules.

## Cross-validation across all R-future hypotheses

R-future hypothesised: "rules + exemplar diff" closes the aesthetic
gap that "rules alone" leaves open.

User judgment:
- Palette gap: **YES, closed.** "色彩最漂亮" — exemplar workflow
  delivered the palette improvement.
- Layout gap: **partial.** R-future's nested subgridspec for B/C/D
  was an upgrade on R5.C (more compact); but trailing whitespace
  is a regression.
- Bar legibility gap: **NO, regressed.** Both R5.C and R-future
  have the negative-value bar bug; R-future inherited it.

Overall: **the exemplar workflow is positive evidence for the
paradigm but exposes that aesthetic skills don't fix rule-layer
bugs.** The 2 layers must be fixed separately and chained
correctly.

## Porting recommendation

**Conditional import-strongly** for figure-aesthetic-exemplars:

1. Land the figure-aesthetic-exemplars skill draft (palette +
   typography + workflow are all positive evidence).
2. Patch figure-layout-defaults Step 6 (negative values).
3. Add to figure-aesthetic-exemplars workflow: "audit existing
   script against current rule set, not just original rule set."

Without (2) and (3), aesthetic-exemplars introduces a regression on
some fixtures. With them, the paradigm is sound.

## Open questions for R-future-2

- Heatmap aesthetics: user said "左上角的热力图古怪，占很大位置但
  信息量少." This is consistent across exemplars in our gallery.
  Heatmap aesthetic patterns deserve their own annotation card
  (different design rules: row count vs panel size, cluster
  annotation styling, colourbar position).
- Vision-capable iterative loop: the workflow assumes runner can
  visually self-judge. If model can't see the rendered image, the
  workflow degrades to text-based diff against annotation cards.
  Future R round: test whether vision-capable model judging the
  PNG closes the gap further.
