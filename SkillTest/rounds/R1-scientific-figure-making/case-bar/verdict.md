# Verdict — scientific-figure-making / case-bar

**Round:** R1.B · **Date:** 2026-05-16 · **Rubric version:** v1
**Visual judge:** user (primary) — code/structural inspection secondary

## User visual review (verbatim)

> (a) 我们的 Candidate 颜色非常好，相比之下 Baseline 的颜色不太行。
> (b) 但从显示效果来看，Candidate 赢的不太多。整体没有给我一种很惊艳的感觉，
> 仅仅是配色和选用的花纹不一样，没有体现出额外的设计概念。

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Information architecture / non-redundant panels | 4/4 | 4/4 | 0 | single-panel both |
| Visual hierarchy / hero panel | n/a | n/a | n/a | not applicable |
| Palette discipline | 1/3 | 3/3 | +2 | user: candidate "颜色非常好"; baseline "不太行" |
| Typography & export | 0/3 | 3/3 | +3 | baseline svg 0 `<text>` / rasterised paths; candidate 18 `<text>` + Arial family fallback |
| Statistical annotation | 2/3 | 2/3 | 0 | both have `*`/`**` markers; neither stands out |
| Reproducibility | 3/3 | 3/3 | 0 | both runnable end-to-end |
| Review readiness | 2/3 | 2/3 | 0 | user: "Candidate 赢的不太多" — palette + hatching差异之外没有额外设计 |
| **Total** | **12/19** | **17/19** | **+5** | (single-panel; hero dim omitted) |

## What the skill actually delivered

Two real but narrow wins:

1. **Editable text in vector outputs** — the same load-bearing fix as R1.A's
   nature-figure on case-bar (0 `<text>` baseline → 18 `<text>` + explicit Arial
   font family stack candidate).
2. **Palette + hatch discipline** — user explicitly approved.

Crucially, this is also where the candidate's contribution **stops**: the user
felt the gain was confined to "配色和选用的花纹不一样，没有体现出额外的设计概念."
Compare R1.A nature-figure on the same case, which crammed legend + caption +
density into 63 mm height and produced an unreadable figure — scientific-figure-
making's lighter rule set means it overrides figsize less aggressively and
doesn't try to enforce mm-precision packing. Candidate canvas here was
~114 x 75 mm (vs nature-figure's 127 x 63 mm) — 12 mm of extra height that
prevented the cramming failure.

## What the skill missed

- **No archetype reasoning.** R1.A's nature-figure pushed the runner to think
  "what is this figure trying to argue?" before laying it out. scientific-
  figure-making doesn't, so the candidate is essentially "matplotlib defaults
  + good palette + editable text." That's why the user didn't feel "惊艳."
- **No hero-panel concept** — moot here (single panel) but will matter on
  multi-panel.

## Bucket

**Calibrates response.** Both reach a usable artefact. Candidate is strictly
better-defended (editable text, unified palette) but the gap is incremental,
not transformative.

## Porting recommendation

`fork-narrowly`. Take:
- The rcParams discipline (Arial fallback chain + `svg.fonttype="none"` + `pdf.fonttype=42`)
- The palette + hatch pattern for greyscale-safe categorical data

Skip:
- The "design philosophy" sections of the skill — they don't bite at this case size.

Open question: does the same skill produce the same incremental-only result on
case-multi-panel where the hero-panel concept actually matters? See case-multi-
panel verdict.
