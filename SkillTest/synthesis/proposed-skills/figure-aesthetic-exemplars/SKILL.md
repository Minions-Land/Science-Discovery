---
slug: figure-aesthetic-exemplars
summary: Reference-driven figure design — diff your figure against the closest exemplar in the gallery, identify 3 biggest deltas, revise. Different paradigm from rule-based figure-layout-defaults / academic-plotting.
layer: logical
tools:
version: 1
status: draft-from-SkillTest-R-future
supersedes:
references: figure-layout-defaults, academic-plotting
provenance: SkillTest-R6.A-aesthetic-ceiling-finding
---

# Skill — Figure Aesthetic Exemplars (DRAFT — SkillTest research zone)

> This is a draft from SkillTest, not a live MinionsOS skill. Authored
> in response to R6.A user feedback: "用了 Skill 的配色可能稍微规范一点，
> 但是和美感、好看完全搭不上边."

## What this skill is

A REFERENCE LIBRARY plus a JUDGEMENT WORKFLOW, not a rule list. The
companion skills [[figure-layout-defaults]] and [[academic-plotting]]
make figures *correct* (no rasterised text, no clashing hues, no empty
quadrants). This skill makes figures *beautiful* — closer to what
appears in a recent Nature or Cell publication.

The premise: rules can constrain (don't do X) but cannot generate
(produce Y). Beauty in scientific figures comes from specific,
non-rule-encodable choices: a particular palette ratio, a particular
typographic rhythm, a particular allocation of white space. The only
way to learn these is to STUDY EXEMPLARS — figures that are
empirically beautiful — and DIFF YOUR FIGURE AGAINST THEM.

## When to invoke

- You have a draft figure that satisfies all rule-based skills
  (figure-layout-defaults, academic-plotting) but the user / co-author
  has flagged it as "looks fine but not beautiful," "缺乏新意," "和美感、
  好看完全搭不上边."
- You are preparing a Nature / Cell / Science cover-eligible figure
  where aesthetic quality matters beyond submittability.
- You have iteration budget: this skill expects 2-4 render-revise cycles,
  not single-pass rule application.

Do NOT invoke if:
- The figure is pre-submission and only needs to be SUBMITTABLE (use
  rule-based skills only).
- You have no iteration budget — exemplar diffing assumes you can
  re-render after revision.

## Procedure

### Step 1 — Render your figure with rule-based skills first

Apply [[figure-layout-defaults]] and [[academic-plotting]] FIRST.
Render the figure. Save the artefact at, say, `figures/draft1.png`.
Don't skip this — exemplar workflow assumes a baseline-correct figure
to refine.

### Step 2 — Pick the closest exemplar from the gallery

Open `gallery/index.md`. Find the exemplar that matches your figure's
ARCHETYPE most closely:

| Archetype | Exemplar |
|---|---|
| Multi-panel hero with dose-response + safety + biomarker | `fig3-in-vivo-efficacy-rich` |
| Heatmap-heavy single-cell / dimension reduction | `fig4-single-cell-systems-rich` |
| Single-panel grouped bar (ablation, comparison) | `bars_ablation_Cancer` |
| Multi-bar cross-category comparison | `correctness_by_category` |
| Multi-method sweep with parameter ranges | `results_sweep` |

If your figure type isn't in the gallery, pick the *closest* archetype
and note the gap. Future R rounds extend the gallery.

### Step 3 — Open the exemplar's annotation card

Each exemplar in `gallery/` has a sibling `<exemplar>.annotation.md`
file documenting:

- **Extracted palette**: actual hex values dominant in the rendered
  figure (not generic rules, but what THIS exemplar uses)
- **Palette ratio**: percentage of pixels in each colour family
  (background grey vs signal accent vs subordinate hue)
- **Typography**: font sizes per element class (axis label, panel
  letter, caption note, in-panel annotation)
- **White space allocation**: ratio of panel area to whitespace
- **Visual rhythm**: where the eye lands first, second, third
- **What makes this figure work**: 3-5 bullet points naming the
  specific design choices that differentiate it from a "correct but
  bland" figure

### Step 4 — Diff your figure against the exemplar

Open both side-by-side (Playwright HTML page or local image viewer).
Identify the 3 biggest visual deltas. Examples:

- Your palette has 4 saturated hues; exemplar has 1 signal + 2 neutrals
  + heavy background grey.
- Your panel labels are 7-pt bold; exemplar uses 9-pt bold with extra
  weight contrast.
- Your hero panel fills 30% of canvas; exemplar's hero fills 45%.
- Your bars use 0-100 axis with 35% empty top; exemplar zooms to data
  range with 10% headroom.

Rank the 3 deltas by aesthetic impact (typography is usually high
impact; precise hex value is usually low).

### Step 5 — Revise the script to address top-3 deltas

DON'T re-do the figure from scratch. Edit the existing script to
address only the 3 named deltas. Re-render to `draft2.png`.

### Step 6 — Re-diff and decide

Compare draft2 vs the exemplar again. If the gap has closed
substantially, stop. If 1-2 of the 3 deltas remain, do one more
iteration. **Cap at 4 iterations** — beyond that, you're polishing
what should have been redesigned.

## What this skill does NOT do

- It does NOT rewrite [[figure-layout-defaults]] or [[academic-plotting]].
  Use those first; this skill is the polish step.
- It does NOT generate exemplars. The gallery is curated from real
  published figures.
- It does NOT replace human aesthetic judgment for a venue cover. For
  Nature cover-grade figures, a human designer still adds ~20% beyond
  what this workflow produces.
- It does NOT tell you a specific colour to use. It tells you ratios
  and exemplar precedents; the runner picks specific hex values
  matching the manuscript palette family.

## Pitfalls

- **Picking the wrong exemplar.** If your figure is a single-panel
  bar chart and you diff against `fig3-in-vivo-efficacy-rich` (a
  4-panel hero composite), the deltas will be misleading. Match
  archetype first.
- **Copying the exemplar's palette pixel-perfect.** The point is to
  learn the RATIO and the FAMILY, not to literally copy hex values
  from a different paper's figure. Translate the lesson to your
  manuscript's palette.
- **Endless iteration.** 4-iteration cap is a hard limit. If you can't
  close the gap in 4 cycles, the figure needs structural redesign,
  not aesthetic polish.
- **Ignoring the rule-based baseline.** This skill ASSUMES rules are
  already applied. If you skip [[figure-layout-defaults]] first, the
  exemplar diff becomes "your figure is wrong AND ugly" — fix wrong
  first.

## Output habit

When delivering a polished figure, document:

```
# aesthetic exemplar workflow
exemplar_used: gallery/fig3-in-vivo-efficacy-rich.png
top-3 deltas addressed:
  1. palette: removed 2 redundant hues, kept 1 signal + 2 neutrals
  2. typography: panel letters 8pt -> 9pt bold, axis labels 6.5 -> 7pt
  3. hero panel area: 30% -> 42% via gridspec width_ratios
iterations: 2
remaining gaps (acknowledged): exemplar uses subtle background tint
  in hero panel; we did not replicate (manuscript palette has no
  near-white tint family available)
```

## Provenance

Distilled from SkillTest R6.A user feedback. The R1-R6 figure rounds
established that rule-based skills (figure-layout-defaults,
academic-plotting) plateau at "correct / submittable" but do not reach
"beautiful." The aesthetic-exemplar paradigm — REFERENCE LIBRARY +
DIFF WORKFLOW — is the SkillTest hypothesis for closing that gap.

R-future validation: re-run R5.C 7-panel or R6.A 9-panel through this
workflow + user visual review. If the user grades the result
materially better than rule-only candidate, this paradigm is
load-bearing. If not, the gap requires a vision-capable iterative
loop or a human designer.
