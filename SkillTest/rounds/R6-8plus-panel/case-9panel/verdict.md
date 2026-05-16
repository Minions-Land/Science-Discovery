# Verdict — R6.A 9-panel figure / case-9panel

**Round:** R6.A · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary)

## User visual review (verbatim)

> Baseline 和 Candidate 似乎长得一模一样，没有什么区别.
>
> 单看这个排版呢，左右都还行，但整体字还有点小. 最重要的问题是右上角有四张子图，
> 它们分别部署在右上角小板块的左上、右上、左下、右下当中. 这导致在右上角这一
> 块地方，图表是散开的，中间有很多留白，视觉上非常不好看.
>
> 1. 视觉效果与新意:
>    (a) 整体图表缺乏新意，设计非常朴素.
>    (b) 文字字号依然偏小，肉眼看得很费劲.
> 2. 布局与面积浪费:
>    (a) 有些图占用的空间很大，但其实根本不需要这么大.
>    (b) 比如左上角的柱状图，给了这么大的位置，结果柱子画得那么长，完全没有意义.
> 3. 差异体现:
>    (a) Bar / box 图最核心的作用是体现数据差异.
>    (b) 假设数值越高越好，那么最低的那根柱子可能只有一点点 — 多出一点点就能
>        把差异体现出来.

## Numeric score

| Dim | Pts | Baseline | Candidate | Δ |
|---|---|---|---|---|
| Information architecture | 4 | 3/4 (right-quadrant 2×2 wastes space) | 3/4 (same) | 0 |
| Visual hierarchy / hero | 3 | 2/3 (hero present but bars over-stretched) | 2/3 (same) | 0 |
| Palette discipline | 3 | 3/3 | 3/3 | 0 |
| Typography & export | 3 | 2/3 (147 `<text>` + Arial; size too small per user) | 2/3 (same) | 0 |
| Statistical annotation | 3 | 3/3 | 3/3 | 0 |
| Reproducibility | 3 | 3/3 | 3/3 | 0 |
| Review readiness | 3 | 1/3 (right-quadrant whitespace + small fonts) | 1/3 (same) | 0 |
| **Total** | **22** | **17/22** | **17/22** | **0** |

## Headline

**Skill is inert at 9 panels.** Baseline and candidate produced visually
identical artefacts (same grid, same figsize within 2%, same editable-
text rcParams). At 9-panel complexity, Codex naive baseline already
arrives at the figure-layout-defaults' "designate 4-cell hero +
contiguous remainder" pattern without skill guidance.

## What this round did expose (NEW failure mode, both runs share)

The user identified TWO problems shared by both runs that NO skill in
SkillTest currently addresses:

### NEW Rule 1: Right-quadrant 2×2 produces wasted whitespace

When B/C/D/E occupy `gs[0,2]`, `gs[0,3]`, `gs[1,2]`, `gs[1,3]` —
each panel is a single grid cell, and matplotlib spaces them with
default `wspace`/`hspace` proportional to the FULL grid (4 columns
total). The result is whitespace BETWEEN B-C horizontally and B-D
vertically, larger than necessary for 4 cells of related plots.

User's exact observation: "右上角这一块地方，图表是散开的，中间有很多留白."

**Proposed fix:** When 4 single-cell subordinate panels share a
2×2 region within a larger grid, use `subgridspec(2, 2, wspace=0.4,
hspace=0.4)` (or smaller) on that region rather than relying on
the parent grid's spacing. This packs the 2×2 sub-region without
forcing the spacing to match the larger grid.

### NEW Rule 2: Y-axis range should match data density, not nominal range

User's exact observation:
> "Bar chart 假设数值越高越好，那么最低的那根柱子可能只有一点点 — 多出一点点
> 就能把差异体现出来. 让最低柱可见即可，不要从 0 一直画到 100，把上面的空间
> 全留白."

The 9-panel hero (panel A) shows tumor volume reduction CompoundX
~65% vs Vehicle ~-3%. Plotted on the y-axis 0-100 default, the bars
fill ~65% of the panel height; the top 35% is empty. Better: y-axis
~-10 to 70, bars fill nearly the full height, contrast between
CompoundX and Vehicle is maximally salient.

Same principle applies to box / violin / dot plots: zoom y-axis to
data range +/- a few percent of headroom, not to the theoretical
0-100 (or 0-1) range.

**Proposed fix:** When the data spans <70% of the nominal axis range,
re-scale axis to `data_min - 0.1*(data_max-data_min)` to
`data_max + 0.1*(data_max-data_min)`. Document the rescaling in
caption.

NOTE: this rule has a counter-rule — if the y-axis is a probability
or fraction (0 to 1) and the data is naturally near the boundaries,
truncating to "data range only" can mislead the reader about scale.
The rule applies to bar / dot / violin plots where the visual
emphasis IS the difference, not the absolute level.

## Bucket

**Matches baseline** for the layout-defaults skill specifically (no
delta vs naive baseline at 9 panels).

But the round IS productive because it surfaces 2 NEW rules that
should be added to the skill before final port:
- subgridspec packing for nested 2×2 sub-regions
- y-axis range tuning to data density

## Cross-validation across all figure rounds (final)

| Panel count | Skill effect | Bucket |
|---|---|---|
| Single (R1.A/R1.B bar) | rcParams + palette portable, but mm-figsize HURTS | Overreaches partial |
| Single (R1.A/R1.B heatmap) | TwoSlopeNorm + palette HELP | Calibrates |
| 4 (R1.A) | Asymmetric grid HURTS | Overreaches |
| 4 (R1.B) | Asymmetric grid HURTS | Overreaches |
| 5 (R4.B) | Asymmetric grid HURTS × 2 | Overreaches |
| 6 (R5.C) | Skill inert (Codex finds right answer) | Matches baseline |
| 7 (R5.C) | Layout pattern HELPS substantially | Calibrates +10 |
| **9 (R6.A)** | **Skill inert; new rules surfaced** | **Matches baseline** |

The skill's value scales with COMPLEXITY OF DECISION, not with panel
count. At 4 and 5 panels existing third-party skills push the runner
to the wrong answer; the SkillTest-authored layout-defaults skill
catches them. At 6 and 9 panels, the runner finds the right answer
naturally; the skill is inert. At 7 panels (in between), the skill's
explicit guidance produces the clearest win.

## Porting recommendation

`figure-layout-defaults.md` (proposed-skills) needs 2 ADDITIONS before
final port:

1. **Subgridspec packing for nested 2×2 sub-regions.** When 4 single-
   cell panels would share a 2×2 sub-region of a larger grid, wrap
   them in their own subgridspec with tighter spacing.
2. **Y-axis range tuning to data density.** When data spans <70% of
   the default axis range, tune the limits to data_min/max with 10%
   headroom. Counter-rule for natural-bounded data (0-1 probability,
   etc.) where the bound IS the message.

Add these as ## Step 5 and ## Step 6 in the existing skill draft, after
the current 4 steps (grid → figsize → layout-budget → sanity-check).

## What R6.A closed

The figure-layout-defaults skill's coverage is now mapped:
- 4-panel: load-bearing (R1.A + R1.B failed without it)
- 5-panel: load-bearing (R4.B failed without it)
- 6-panel: inert (R5.C 6-panel, both runs identical)
- 7-panel: load-bearing (R5.C +10 win)
- 9-panel: inert FOR LAYOUT, but exposes 2 missing rules (right-
  quadrant subgridspec packing + axis range tuning)

The skill is mature for layout itself; the 2 new rules from R6.A
should be folded in before final port.
