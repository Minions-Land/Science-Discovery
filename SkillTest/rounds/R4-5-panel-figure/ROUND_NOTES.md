# Round Notes — R4.B 5-panel figure (asymmetric-grid persistence test)

**Cases:** case-pharma-pipeline (1 fixture × 3 outputs)
**Date:** 2026-05-16
**Methodology:** Codex generated 3 plotting scripts; user did the visual review.

## Headline

User: baseline 无敌好看且非常准确; nature-figure 超级垃圾; scientific-
figure-making 配色最好看但排版要向 Baseline 学习.

The 4-panel multi-panel failure mode from R1.A and R1.B is **structural
to both skills, not a 4-panel-specific quirk**. The same custom-asymmetric-
grid trap fires at 5 panels too. **3 independent cases × 2 skills = 6
data points all in the "asymmetric grid loses to standard matplotlib-
default" direction.**

## Numeric scores

| Run | Score / 22 |
|---|---|
| baseline | 16 |
| candidate-nature-figure | 14 |
| candidate-scientific-figure-making | 15 |

(Wins palette and typography for the candidates; loses hero + review
readiness — net negative trade.)

## Cross-validation with R1.A + R1.B

| Round | Panel count | nature-figure | scientific-figure-making |
|---|---|---|---|
| R1.A multi-panel | 4 | Overreaches partial | n/a (different round) |
| R1.B multi-panel | 4 | n/a | Overreaches (-2 to baseline) |
| R4.B pharma-pipeline | 5 | Overreaches | Overreaches (palette win, layout loss) |

The asymmetric-grid failure is now confirmed at both 4 and 5 panels,
across both skills. **The "default 4-panel pattern is `[2,1,1] + bottom
D`" rule from R1 synthesis must be extended.**

## What this round added to the port plan

Update `synthesis/proposed-skills/figure-layout-defaults.md` with a
**5-panel default**:

```
# 5-panel hero default (user-confirmed in R4.B)
gridspec(3, 3) with:
  ax_a = gs[0:2, 0:2]    # hero (4 cells, dominant by area)
  ax_b = gs[0, 2]        # subordinate top-right
  ax_c = gs[1, 2]        # subordinate mid-right
  ax_d = gs[2, 0]        # bottom-left single cell
  ax_e = gs[2, 1:3]      # bottom-spanning 2 cells
```

The skill should add this as a NAMED default, not an option among many.

Generalised principle (untested beyond 5 panels):
> Designate a 4-cell hero region. Arrange subordinates around it as a
> contiguous remainder — no empty cells, no over-stretching. Default
> patterns: 4-panel = [2,1,1]+bottom-D; 5-panel = the 3×3 above.

## What the candidate skills did right

- **scientific-figure-making palette: 2-for-2 wins.** R1.B case-multi-panel
  ("配色已经过关了") + R4.B case-pharma-pipeline ("配色目前来看最好看").
  The PALETTE-dict + reserve-green/red rule produces consistently good
  cross-panel colour. Promote this rule in port plan over nature-figure's
  variant if user must pick one.
- **Editable text in vector outputs:** baseline 0 `<text>` nodes vs
  candidates 93 / 108. Same R1+R3 result; submission-blocker fix is
  consistent.

## Token economics

Codex ran in 2 parts (Part 1: baseline + nature-figure; Part 2:
scientific-figure-making) due to single-run timeout. Each part ~60s.

## Recommendation

`fork-narrowly` for both skills (consistent with R1.A + R1.B verdicts).
The port plan elements are unchanged; the figure-layout-defaults skill
gains a 5-panel section.

## What R4 has now confirmed end-to-end

- **R4.A** nature-response: AUTHOR_INPUT_NEEDED works. R2 port plan
  gains top-of-letter flag + PI question list rules.
- **R4.B** 5-panel figure: asymmetric-grid failure is structural. R1
  port plan extended with 5-panel default.
- **R4.C** Haiku-class deslop: skip prediction holds at 2 executor classes.

R4 closes. R5 candidates remain in R3-synthesis.md open questions.
