# Verdict — R4.B 5-panel figure / case-pharma-pipeline

**Round:** R4.B · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary)

## User visual review (verbatim)

> 1. Baseline: 排版非常好看，无敌好看且非常准确，已经不能再准确了。
> 2. Nature Figure: 排版超级垃圾，虽然配色比左边的 Baseline 好一点点，但也强不到哪去。
> 3. Scientific Figure Making: 配色是目前来看最好看的，但是排版真的要向 Baseline 学习，
>    Baseline 的排版太好看了。

## Numeric score

| Dim | Pts | Baseline | nature-figure | scientific-figure-making |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4 | 4/4 | 3/4 | 3/4 |
| Visual hierarchy / hero panel | 3 | 3/3 | 1/3 | 1/3 |
| Palette discipline | 3 | 1/3 | 2/3 | 3/3 |
| Typography & export | 3 | 0/3 (rasterised text) | 3/3 | 3/3 |
| Statistical annotation | 3 | 2/3 | 2/3 | 2/3 |
| Reproducibility | 3 | 3/3 | 3/3 | 3/3 |
| Review readiness | 3 | 3/3 | 0/3 | 0/3 |
| **Total** | **22** | **16/22** | **14/22** | **15/22** |

## What the user observation tells us

This is the same failure pattern as R1.A and R1.B 4-panel composites,
now confirmed at 5 panels:

- **baseline geometry is the standard answer.** 3×3 grid with
  `ax_a=gs[0:2,0:2]` (4 cells, hero), small B/C right column rows 0-1,
  D single-cell bottom-left, E spanning bottom-middle/right. User: "无敌
  好看且非常准确."
- **Both candidate grids broke this.** nature-figure used 3×4 with E
  spanning full bottom; scientific-figure-making used same 3×4 plus
  sub-gridspec for panel C ADMET small multiples. User: both排版垃圾.

The two skills' content discipline (rcParams, palette, editable text)
is real — scientific-figure-making's palette was praised as "最好看".
But that wins back palette/typography points (1+3 dim) at the cost of
the layout points (hero + review readiness, ~6 dim). Net trade is bad.

## Three rounds, identical failure mode

R1.A nature-figure (4-panel): Overreaches — empty `gs[2, 0:2]` quadrant.
R1.B scientific-figure-making (4-panel): Overreaches — cramped B/C, over-
stretched D.
R4.B nature-figure (5-panel): user 排版超级垃圾.
R4.B scientific-figure-making (5-panel): user 排版要向 Baseline 学习.

**Both skills nudge the runner to a custom asymmetric grid that loses
to whatever matplotlib-default grid the baseline runner picks.** This is
no longer a 4-panel artefact; it's a fundamental skill-side gap.

## What the skills did right

- **scientific-figure-making palette wins twice in a row.** R1.B
  case-multi-panel: user said palette 已经过关. R4.B: user said palette
  最好看. Cross-confirmed: the skill's PALETTE-dict pattern + reserve-
  green/red rule produces visually coherent multi-panel colour, even
  when the layout fails.
- **Editable text in vector outputs.** Both candidates 93 / 108
  `<text>` nodes; baseline 0. Same R1+R3 conclusion: rasterised baseline
  text is a Nature-family submission blocker; the skill rcParams fix it.
- **No fabrication.** Both candidates honoured data correctly.

## Buckets

- **nature-figure:** Overreaches (-2 to baseline, third consecutive
  multi-panel overreach)
- **scientific-figure-making:** Overreaches (-1 to baseline, palette win
  partially compensates but layout still loses)

Both skills now have **3 independent multi-panel cases of overreach**
(R1.A multi-panel, R1.B multi-panel, R4.B 5-panel respectively for
each — though only one each was tested at 5-panel, the pattern across
4-panel and 5-panel is the same).

## Cross-validation summary (R1.A + R1.B + R4.B)

| Skill | 4-panel result | 5-panel result | Same failure mode? |
|---|---|---|---|
| nature-figure | Overreaches partial (R1.A multi-panel) | Overreaches (R4.B) | YES — asymmetric grid losing to standard pattern |
| scientific-figure-making | Overreaches (R1.B multi-panel, -2 to baseline) | Overreaches (R4.B, -1 to baseline) | YES — same |

**Conclusion:** the multi-panel layout failure is structural in both
skills, not a 4-panel-specific quirk. The matplotlib-default geometry
both baselines naturally pick (`width_ratios=[2,1,1] + bottom-spanning`
for 4-panel; user-confirmed; `3×3 with hero=gs[0:2,0:2]` for 5-panel,
also user-confirmed) wins consistently against the skills' asymmetric
custom grids.

## Sharpened port plan

Update `proposed-skills/figure-layout-defaults.md` (R1 synthesis) with
**explicit 5-panel default**:

```
# 5-panel hero default
gridspec(3, 3) with:
  ax_a = gs[0:2, 0:2]    # hero (4 cells)
  ax_b = gs[0, 2]
  ax_c = gs[1, 2]
  ax_d = gs[2, 0]
  ax_e = gs[2, 1:3]
```

This is the layout the user called "无敌好看 且非常准确." Make this the
named default for any 5-panel composite, not just an option.

For 6-panel and beyond: the rule generalises to "designate a 4-cell
hero region; arrange subordinates around it as a single contiguous
remainder, no empty cells, no over-stretching." But that's untested
beyond 5; future R rounds can extend.

## Porting recommendation

Same as R1.A + R1.B verdict: `fork-narrowly`. Keep both skills' content
discipline (rcParams, PALETTE, TwoSlopeNorm, outside ticks). Reject the
multi-panel layout patterns. Rely on `figure-layout-defaults.md`
(SkillTest-authored) for the actual layout defaults — now extended with
the 5-panel pattern from this round.

The key insight from R4.B is that this is **not specific to 4-panel** —
the figure-layout-defaults skill is genuinely load-bearing across panel
counts.

## Open questions

- Test 6-panel and 7-panel briefs in R5 — do baseline runners still
  pick the right grid? Or is there a panel count where asymmetric
  custom grids actually win?
- The palette wins in R4.B were strong enough that scientific-figure-
  making's palette discipline should arguably be promoted over nature-
  figure's PALETTE-dict for the port. Worth documenting in the port
  plan.
