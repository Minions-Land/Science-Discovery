# Verdict — scientific-figure-making / case-heatmap

**Round:** R1.B · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary)

## User visual review (verbatim)

> (a) Candidate 生成得非常好，起码比 Baseline 好非常多。
> (b) 配色中规中矩，我觉得还行，没有到惊艳的程度。
> (c) 整体来看 Candidate 更好一些，Baseline 主要输在排版上，不过 Baseline 的配色我认为也不错。

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4/4 | 4/4 | 0 | single-panel both |
| Visual hierarchy / hero panel | n/a | n/a | n/a | not applicable |
| Palette discipline | 2/3 | 2/3 | 0 | user: both palettes acceptable, neither standout |
| Typography & export | 0/3 | 3/3 | +3 | baseline 0 `<text>` (rasterised); candidate 34 `<text>` + Arial family stack |
| Statistical annotation | 2/3 | 3/3 | +1 | candidate adds explicit caption / cluster annotation discipline |
| Reproducibility | 3/3 | 3/3 | 0 | both runnable |
| Review readiness | 1/3 | 3/3 | +2 | **user identified layout as the decisive baseline failure** — candidate fixed it |
| **Total** | **12/19** | **18/19** | **+6** | (single-panel; hero dim omitted) |

## What the skill actually delivered

User's "Baseline 主要输在排版" is the decisive observation. The lighter
scientific-figure-making rule set still managed to fix the layout problem
that R1.A's heavier nature-figure also fixed on this case — both candidates
deliver readable heatmap geometry on this brief because heatmap is naturally
a forgiving canvas (no legend overlap risk, label thinning is the only real
constraint, side bar + colourbar are well-defined positions).

The skill bit primarily through:

1. **Editable text** — same load-bearing fix as everywhere else.
2. **Layout discipline carryover from common-patterns.md** — outside ticks,
   row-label thinning, colourbar position discipline.
3. **Diverging colormap centred at zero** — candidate uses TwoSlopeNorm or
   equivalent (verified in code).

Palette: user said "中规中矩" — neither candidate nor baseline is striking on
colour. The skill doesn't push hard on palette beyond "diverging cmap"; that
matches what the user observed.

## What the skill missed

Nothing material for this case. The brief's natural canvas size (~115 × 96
mm) gave the runner enough headroom that no figsize override was needed
(candidate ended at ~119 × 131 mm — generous).

## Bucket

**Calibrates response (lower-end of "Prevents real failure").** User explicitly
called out the layout gap on baseline as "主要输在排版上" — load-bearing.
Candidate fixes it. Not as transformative as R1.A's heatmap (which was the
clean win for nature-figure too), because the lighter skill set doesn't add
anything beyond what's needed for this fixture.

## Porting recommendation

`fork-narrowly`. Same elements as R1.A heatmap recommendation:

- TwoSlopeNorm-equivalent diverging cmap pattern
- Row label thinning rule (every-other when row count > 20)
- Outside tick discipline
- Editable text rcParams

The R1.A nature-figure heatmap port plan and the R1.B scientific-figure-making
heatmap port plan are essentially identical. **Either skill provides the
heatmap-ready content discipline.** The choice is on whether the rest of the
skill (figure-contract, archetype, design-theory chapters) is worth the
extra context cost — which depends on the case mix MinionsOS Writer expects.
