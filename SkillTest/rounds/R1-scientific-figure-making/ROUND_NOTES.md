# Round Notes — R1.B scientific-figure-making

**Cases:** case-bar, case-heatmap, case-multi-panel
**Date:** 2026-05-16
**Candidate skill:** `/Users/mjm/Skill/figures4papers-main/scientific-figure-making/`
**Methodology:** Stage 1 only. Codex generated artefacts; user did the visual
review (R1.A's lesson — code-layer evidence is necessary but not sufficient
for figure rounds).

## Aggregate scores (user-judged)

| Case | Baseline | Candidate | Δ | Bucket |
|---|---|---|---|---|
| case-bar (single-panel; hero N/A) | 12 / 19 | 17 / 19 | +5 | Calibrates response |
| case-heatmap (single-panel; hero N/A) | 12 / 19 | 18 / 19 | +6 | Calibrates / lower-end "Prevents real failure" |
| case-multi-panel | 16 / 22 | 14 / 22 | -2 | **Overreaches** (candidate < baseline) |
| **Mean (normalised /22)** | **70%** | **76%** | **+6 pp** |

## R1.B vs R1.A side-by-side

| Case | R1.A nature-figure Δ | R1.B scientific-figure-making Δ | Comment |
|---|---|---|---|
| case-bar | +1 (Overreaches partial) | +5 (Calibrates) | scientific-figure-making's lighter rule set avoided R1.A's mm-precision cramming. User: candidate "颜色非常好" but "赢的不太多" — narrow win |
| case-heatmap | +5 (Calibrates) | +6 (Calibrates / Prevents) | Both skills succeed on heatmap. User: candidate "非常好，比 Baseline 好非常多". Heatmap is forgiving canvas |
| case-multi-panel | 0 (Overreaches) | -2 (Overreaches, worse) | **Both skills fail multi-panel, in different ways.** R1.A: empty quadrants. R1.B: cramped B/C + over-stretched D. User: baseline "非常漂亮、精致"; candidate "排版完全没有 Baseline 好" |

## Key finding

**Both nature-figure and scientific-figure-making teach content discipline
(palette, editable text, font, ticks) but neither teaches the **standard
4-panel hero pattern**.** When the runner needs to lay out a 4-panel composite,
both skills push toward custom asymmetric gridspecs. The user calls out the
SAME failure mode in both rounds: B/C cramped, D over-stretched or in the
wrong row. The matplotlib-default `width_ratios=[2,1,1] + bottom-spanning
panel D` (which both R1.A baseline and R1.B baseline used naturally) is what
both candidates should have started from but didn't.

## Where the candidate consistently helped

- **Editable text in vector outputs.** Same load-bearing fix as R1.A. SVGs go
  from 0 `<text>` (rasterised paths) to 18-62 `<text>` nodes with explicit
  Arial fallback chain.
- **Palette discipline.** User approved palette on all three cases:
  case-bar "颜色非常好"; case-heatmap "中规中矩还行"; case-multi-panel
  "配色已经过关了". This is the single most consistent win across the round.
- **Layout slack on tight figsize.** Codex (warned by R1.A lessons applied to
  the prompt) chose inches over mm for case-bar (5.2x3.0in) and case-heatmap
  (5.4x5.9in), avoiding the cramming failure mode. The skill itself doesn't
  *cause* this discipline; it just doesn't push hard against it.

## Where the candidate didn't help

- **Multi-panel layout.** Same shape of failure as R1.A: asymmetric
  gridspec, cramped subordinate panels, mis-allocated whitespace. The
  skill's lighter rule set didn't save it; the runner still picked a
  custom grid over the standard pattern.
- **Visual "design concept" beyond palette.** User on case-bar: "整体没有
  给我一种很惊艳的感觉，仅仅是配色和选用的花纹不一样，没有体现出额外的设计概念."
  This is the difference between a content-discipline skill and a
  design-philosophy skill — scientific-figure-making is the former.

## Token economics

- case-bar: candidate input ~14x baseline, output ~2.3x.
- case-heatmap: candidate input ~14x baseline, output ~4.0x (heatmap baseline
  was very terse).
- case-multi-panel: candidate input ~10x baseline, output ~1.6x.

Compared to R1.A's nature-figure (~25x input across cases),
scientific-figure-making is ~14x — the skill is genuinely lighter (~24 KB of
references vs nature-figure's ~36 KB). Output overhead similar.

## Recommendation

`fork-narrowly`. The portable elements overlap with R1.A:

- rcParams block (Arial fallback chain, `svg.fonttype="none"`,
  `pdf.fonttype=42`, spine policy)
- PALETTE-dict pattern for cross-panel colour coherence
- Outside-tick discipline

Plus a unique R1.B contribution from this skill's *omission*:

- The skill avoids R1.A's mm-precision figsize trap by simply not pushing
  it. This is a feature: **for the MinionsOS Writer port, the skill should
  default to inches, not mm.** Mm-strict only at submission packaging.

Do **NOT** port:

- The multi-panel hero patterns from either nature-figure or scientific-
  figure-making. Both produced worse rendered figures than baseline.
- Add a NEW rule (not in either skill): "Default 4-panel hero is
  `width_ratios=[2,1,1] + bottom-spanning D`. Try this first; only design a
  custom grid if it demonstrably fails for the specific brief."

## Methodology validation

R1.A lesson held this round: I did NOT score figures by code-layer evidence
this time. The user's visual review was the load-bearing input, and it
caught failures (multi-panel cramped B/C, over-stretched D, small legend)
that I could not have detected from script inspection alone. Codex's
self-report claimed "panel A dominant, B/C readable, D bottom-spanning, no
empty cells, legend non-overlapping" — every one of those points was
contested by the user looking at the actual PNG. **Self-report from the
artefact-producing agent is not evidence; the rendered figure is.**

## Open questions for R1 synthesis

- Both nature-figure and scientific-figure-making are content-discipline skills.
  MinionsOS Writer needs **one** ported figure skill with content discipline
  rules + a sane multi-panel default + figsize-in-inches.
- Neither skill teaches "design concept" beyond palette. If the user wants
  Nature-cover-grade figures, that requires a separate skill (or human
  designer); the procedural skill cannot deliver it. Document this boundary
  in the R1 synthesis.
- For cn-en polishing wins (R1.C), no figure-skill peer exists — that port
  is independent.
