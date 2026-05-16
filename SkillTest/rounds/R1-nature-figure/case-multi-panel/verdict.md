# Verdict — nature-figure / case-multi-panel  (REVISED 2026-05-16)

**Round:** R1.A · **Rubric version:** v1
**Status:** Revised after user visual review.

## Headline

User: "baseline 排版是最正确的，非常合理！超级厉害。candidate 颜色可能稍微漂亮点，
但是排版全错". Confirmed by gridspec inspection — candidate's asymmetric
layout leaves quadrants empty and squeezes panels B/C into the top-right ¼
while panel A occupies left half + upper 2/3 with bottom-left whitespace.

## Numeric score (revised)

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4/4 | 3/4 | -1 | both keep panels distinct, but candidate's empty `gs[2, 0:2]` cell is real wasted real estate |
| Visual hierarchy / hero panel | 3/3 | 1/3 | -2 | baseline's `width_ratios=[2,1,1] + ax_d full-width-bottom` is the conventional & correct hero pattern: A wider on left, B/C beside, D wide below. Candidate's `gs[0:2, 0:2] + gs[1:, 2:]` produces an L-shape with a gaping hole in `gs[2, 0:2]` |
| Palette discipline | 1/3 | 3/3 | +2 | baseline three independent default cycles; candidate threads single PALETTE dict — this is genuinely better in candidate |
| Typography & export | 0/3 | 2/3 | +2 | editable text gain real (60 vs 0 `<text>` nodes). Penalised one point because panel B's slope-text annotations land in tight corners due to the squeezed B/C panels |
| Statistical annotation | 1/3 | 3/3 | +2 | candidate adds CI band on A, EC50 inline labels, pairwise-vs-WT on D; all real wins |
| Reproducibility | 3/3 | 3/3 | 0 | both runnable |
| Review readiness | 3/3 | 0/3 | -3 | **candidate is not submittable as rendered.** The empty bottom-left quadrant + cramped B/C panels in the top-right ¼ is layout failure that no caption can paper over |
| **Total** | **15/22** | **15/22** | **0** | wash overall — palette + statistical wins exactly offset hero/IA/review losses |

## What the skill actually changed

Two real wins (PALETTE dict, editable text, statistical hooks) cancelled by
two structural losses (broken hero geometry, empty quadrant). The user's
read is exactly right: baseline's layout is **the** standard hero-multi-panel
pattern (`width_ratios=[2,1,1]` + bottom-spanning panel D) and the skill
nudged the runner away from it toward an asymmetric `gs` grid that *sounds*
more sophisticated but has a load-bearing empty cell.

## What the skill missed or hurt

The skill says "hero panel ~50% area, with subordinates B/C/D arranged
asymmetrically" — and the runner translated this into `gs[0:2, 0:2]` + `gs[0,
2]` + `gs[0, 3]` + `gs[1:, 2:]`. That grid is a left-half hero + a tiny
top-right strip for B/C + a right-half panel D — leaving bottom-left empty.
The simpler and stronger pattern (which baseline used by accident) is:

```
[ A . . | B | C ]    width_ratios=[2,1,1]
[ A . . | B | C ]    height_ratios=[1.4, 1]
[ D . . . . . . ]
```

A is wide & tall on the left, B/C compact on the right at the same row, D
spans bottom full width. No empty cells, hero clearly dominant.

The skill's `common-patterns.md` does describe this pattern, but it also
describes the L-shape variant; the runner picked the harder one without
reasoning about whitespace.

## Visual inspection (what I should have done first)

User confirmed: baseline 排版最正确, candidate 排版全错.

- baseline gridspec: `(2, 3, width_ratios=[2,1,1], height_ratios=[1.4, 1])`
  with `ax_d = gs[1, :]` → clean wide-A + B/C beside + wide D below
- candidate gridspec: `(3, 4, height_ratios=[1.35, 0.95, 0.85], width_ratios=[1.2,1.2,1.0,1.0])`
  with `ax_a = gs[0:2, 0:2]; ax_b = gs[0,2]; ax_c = gs[0,3]; ax_d = gs[1:, 2:]`
  → A occupies UL (4 cells), D occupies right column rows 1-2 (4 cells), B/C
  squeezed into top-right two cells, **`gs[2, 0:2]` is empty**

## Bucket (revised)

**Overreaches.** Skill caused the runner to pick a harder grid pattern that
produces a worse rendered figure. Palette + statistical wins are real but do
not compensate for unsubmittable layout.

## Porting recommendation (revised)

`fork-narrowly`. Port only:

- The PALETTE-dict pattern (cross-panel colour coherence) — this was the real
  win.
- The CI band + EC50 inline labels + pairwise-significance recipes for panel
  A and D respectively.
- The editable-text rcParams (independent gain).

Do **NOT** port:

- The asymmetric `gs[0:2, 0:2] + gs[1:, 2:]` hero recipe. Default to
  `width_ratios=[2,1,1] + bottom-strip` for 4-panel composites.
- The "hero ~50% area" rule without an "empty-cell check" pitfall.

Add to ported skill: an explicit "no empty quadrant" rule. If the chosen
grid leaves a cell with no panel, either extend a panel into it or pick a
different grid.
