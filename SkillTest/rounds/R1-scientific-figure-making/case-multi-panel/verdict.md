# Verdict — scientific-figure-making / case-multi-panel

**Round:** R1.B · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary) — this case had the largest visual divergence

## User visual review (verbatim)

> (a) Baseline 的排版没有任何问题，非常漂亮、精致。
> (b) 配色方面依然是 Candidate 胜出，目前 Candidate 在 Case 3 的配色已经过关了。
> (c) 但 Candidate 的排版明显不行，甚至是有误的：
>     - 图 B 和图 C 在右上角非常小。
>     - 图 D 占据了一个非常宽的位置。
>     - 奇怪的是它其实只有三个柱状图，但每个柱子都被拉得非常长。
>     - 图 B、C 分布在上下，中间是图 D，而 Legend 也特别小。
>     - 整个图留白非常多。

> 总结来说，Candidate 在 Case 3 的排版完全没有 Baseline 好。

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4/4 | 3/4 | -1 | both keep panels distinct, but candidate's whitespace + cramped B/C means readers can't extract panel-level info efficiently |
| Visual hierarchy / hero panel | 3/3 | 1/3 | -2 | user: "图B、C 在右上角非常小... 图D 占据了一个非常宽的位置". Hero geometry is genuinely broken — A is dominant in width but B/C are squeezed and D is over-stretched |
| Palette discipline | 1/3 | 3/3 | +2 | user: "配色已经过关了" — clear win |
| Typography & export | 0/3 | 2/3 | +2 | candidate 62 `<text>` nodes, Arial. -1 for "Legend 也特别小" — readable text is undermined by sub-spec legend size |
| Statistical annotation | 2/3 | 2/3 | 0 | both annotate panel D; neither stands out |
| Reproducibility | 3/3 | 3/3 | 0 | both runnable |
| Review readiness | 3/3 | 0/3 | -3 | user: "Candidate 在 Case 3 的排版完全没有 Baseline 好" — not submittable as rendered |
| **Total** | **16/22** | **14/22** | **-2** | candidate **lost** to baseline |

## What the skill actually delivered

One genuine win: **palette discipline** ("配色已经过关了"). Candidate uses a
unified palette across panels (CompoundX = signal blue, biomarker family
threaded through C, genotypes in D) — user accepted this.

That win is overwhelmed by two layout failures:

1. **B / C panels stacked vertically and squeezed.** The user identified the
   exact fault: B and C end up in a cramped right-side column with C below B,
   leaving panel D as the wide horizontal bar in the middle, and lots of
   whitespace around it. This is the SAME failure mode as R1.A nature-figure
   on multi-panel, just with a different grid choice — both lighter and
   heavier skills pushed the runner toward an asymmetric grid that doesn't
   work for this brief.
2. **Panel D over-stretched.** User: "其实只有三个柱状图，但每个柱子都被
   拉得非常长 ... 图 D 占据了一个非常宽的位置 ... 整个图留白非常多."
   Three categorical bars in a wide panel = mostly whitespace. The simpler
   width-3 row with bars right-sized would be cleaner.

The user's preferred layout (baseline) used the standard 4-panel hero pattern
that R1.A's ROUND_NOTES already flagged: `width_ratios=[2,1,1] +
bottom-spanning panel D`. Both nature-figure and scientific-figure-making
nudged the runner *away* from this standard pattern toward asymmetric
gridspecs.

## What the skill missed

Same as R1.A but in different shape:

- **Asymmetric gridspec without "no whitespace" rule.** When the user calls
  out "整个图留白非常多" it means the rule "no empty quadrants" needs an
  expanded form: "no panel should be over-stretched into whitespace either."
- **No bar-aspect-ratio rule** for panel D. Three categorical bars don't need
  180 mm of width.
- **No "compare to standard hero pattern first" check.** The skill doesn't
  tell the runner: "before designing a custom asymmetric grid, check if
  `width_ratios=[2,1,1] + bottom row` would work — usually it does."

## Visual / structural inspection

Candidate canvas: 516 x 413 pt ≈ 182 x 146 mm. The size is ample (no
cramming this time). The problem is geometry — too much horizontal real
estate allocated to D, and B/C compressed into a vertical strip.

Baseline geometry (per R1.A inspection): `width_ratios=[2, 1, 1]` with D
spanning bottom — exactly what the user called "非常漂亮、精致".

## Bucket

**Overreaches.** Skill caused the runner to pick a grid that produces a
worse rendered figure than the matplotlib-default sensible 4-panel pattern.
Palette win is real but does not compensate for unsubmittable layout.

This mirrors R1.A multi-panel verdict almost exactly: different skill, same
failure mode. The conclusion sharpens: **for 4-panel composites, both nature-
figure and scientific-figure-making nudge runners toward asymmetric grids
that are harder than the standard pattern.** Neither skill teaches "default
hero pattern is `[2,1,1] + bottom row`" as a first-line recommendation.

## Porting recommendation

Do **NOT** port the multi-panel patterns from this skill. Take only:

- Palette discipline (PALETTE-dict-equivalent, threaded across panels)
- Editable text rcParams

Add as a NEW rule (not in either nature-figure or scientific-figure-making):

> **Default 4-panel hero pattern is `width_ratios=[2,1,1] + bottom-spanning
> panel D`.** Use `gridspec(2, 3, width_ratios=[2,1,1], height_ratios=[1.4, 1])`
> with `ax_d = gs[1, :]`. Do not design a custom asymmetric grid until you have
> tried this default and it has demonstrably failed for the specific brief.

> **No over-stretched panels.** A panel containing 3 categorical bars should
> not span 180 mm of width. Match panel width to data density.
