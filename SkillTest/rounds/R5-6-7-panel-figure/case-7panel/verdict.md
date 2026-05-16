# Verdict — figure-layout-defaults / case-7panel

**Round:** R5.C · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary)

## User visual review (verbatim)

> 这个 Figure Layout Default 的 Candidate 无论是从颜色还是排版上，都完全胜过了
> Baseline.
>
> 1. 关于排版：Baseline 的排版虽然也不错，但我认为只能给到 60 分（属于能用的
>    程度）；而右边的 Candidate 我认为已经可以给到 80 到 90 分了，几乎完美.
> 2. 关于细节：我仔细检查了一下，字体可读，大小也合适.
> 3. 关于配色：配色也很不错，起码是在我认可的标准之上.
>
> 非常好!

## Numeric score

| Dim | Pts | Baseline | Candidate | Δ |
|---|---|---|---|---|
| Information architecture | 4 | 3/4 | 4/4 | +1 |
| Visual hierarchy / hero | 3 | 2/3 | 3/3 | +1 |
| Palette discipline | 3 | 1/3 | 3/3 | +2 |
| Typography & export | 3 | 0/3 (baseline 0 `<text>` — text rasterised) | 3/3 (114 `<text>` + Arial) | +3 |
| Statistical annotation | 3 | 2/3 | 3/3 | +1 |
| Reproducibility | 3 | 3/3 | 3/3 | 0 |
| Review readiness | 3 | 1/3 (60 pts user grade) | 3/3 (80-90 pts user grade) | +2 |
| **Total** | **22** | **12/22** | **22/22** | **+10** |

## Headline

**This is the first SkillTest figure round where a CNS-figure skill
candidate cleanly beat baseline on the rendered artefact.** R1.A nature-
figure (3 cases): Overreaches × 2 + Calibrates × 1. R1.B scientific-figure-
making (3 cases): same shape. R4.B 5-panel: Overreaches × 2. R5.C
6-panel: Matches baseline. **R5.C 7-panel: Calibrates response (clean
win)**, with user grading the rendered output 80-90 vs baseline 60.

The figure-layout-defaults skill (SkillTest-authored, distilled from R1
visual-review evidence) is genuinely load-bearing at 7 panels. The
"designate 4-cell hero + contiguous remainder + no empty cells + no
over-stretching" generalisation produces an artefact the user calls
"几乎完美".

## What the skill actually delivered

Three load-bearing changes:

1. **Editable text in vector outputs** (baseline 0 → candidate 114
   `<text>` nodes + explicit Arial). Same submission-blocker fix as
   every prior SkillTest figure round.
2. **Grid topology that rates 80-90.** Candidate's 4×4 grid with
   A=gs[0:2,0:2] hero + B/C top-right + D-G arranged in 2 bottom rows
   produced "几乎完美" layout. Baseline's 3×4 (G squeezed into bottom-row
   single cell) rates only 60.
3. **Palette as rendered**, user-confirmed: "配色也很不错，起码是在我认可的
   标准之上."

## What this confirms about the port plan

The figure-layout-defaults skill is the **clearest single-skill win in
SkillTest history**. It was synthesized from negative evidence (R1.A
+ R1.B failures) and now demonstrates positive evidence at the panel
count where the design rules genuinely matter (7 panels, where the
runner has to solve hierarchy AND grid simultaneously).

Port priority increased: this should land in MinionsOS Writer
academic-plotting peer skill ASAP.

## Visual / textual inspection

Confirmed by user side-by-side review: candidate's 4×4 grid with G
placed alongside F in the bottom row preserves the visual hierarchy
(efficacy A still dominant; clinical correlate G is subordinate as
intended for translational handle), while baseline's 3×4 forced G into
the bottom-row single-cell slot equal to D/E/F, breaking the priority
ranking.

## Bucket

**Calibrates response** (lower bound) → arguably **Prevents real failure**
when user calls baseline "60 / 能用的程度" and candidate "几乎完美" —
the 30-point gap is the difference between a usable-but-mediocre figure
and a submittable one. For Nature-family submission this matters.

## Cross-validation across all figure rounds

| Round | Panel count | Skill | Bucket |
|---|---|---|---|
| R1.A bar (single) | 1 | nature-figure | Overreaches partial |
| R1.A heatmap (single) | 1 | nature-figure | Calibrates |
| R1.A multi-panel | 4 | nature-figure | Overreaches |
| R1.B bar | 1 | scientific-figure-making | Calibrates |
| R1.B heatmap | 1 | scientific-figure-making | Calibrates / lower-Prevents |
| R1.B multi-panel | 4 | scientific-figure-making | Overreaches (-2) |
| R4.B 5-panel (n-f) | 5 | nature-figure | Overreaches |
| R4.B 5-panel (s-f-m) | 5 | scientific-figure-making | Overreaches (-1) |
| R5.C 6-panel | 6 | figure-layout-defaults | Matches baseline |
| **R5.C 7-panel** | **7** | **figure-layout-defaults** | **Calibrates / lower-Prevents (+10)** |

The pattern: existing skills (nature-figure, scientific-figure-making)
fail on multi-panel layouts they push runners toward. The SkillTest-
authored figure-layout-defaults skill, distilled from those failures,
finally produces a positive result at 7 panels where layout complexity
demands explicit guidance.

## Porting recommendation

`import-strongly` for the figure-layout-defaults skill (was previously
fork-narrowly because it hadn't been positively validated). R5.C 7-panel
turns this from a defensive negative-evidence patch into an empirically-
positive skill.

The 7-panel test result also implicitly recommends elevating
substantively-bounded specificity (the cross-skill anchor rule) into the
common contract — both runs honoured no-fabrication, but only candidate
turned the principle into specific layout rules that produce the
"几乎完美" artefact.
