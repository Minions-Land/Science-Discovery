# Synthesis — What to Import

**Round:** R1 (R1.A + R1.B + R1.C)
**Date:** 2026-05-16
**Status:** Recommendation only. Nothing in this document is applied to
`/Users/mjm/MinionsOS/minions/roles/` until the user explicitly approves.
Drafts of the proposed new / forked skills live in `proposed-skills/` and
`proposed-updates/` next to this file.

## Summary

Three skills tested this round; one recommended as `import-strongly`, two as
`fork-narrowly` (content-discipline rules only, layout patterns rejected).

| Skill | Round | Bucket distribution | Recommendation |
|---|---|---|---|
| nature-polishing | R1.C | 3 Calibrates + 1 Prevents | **import-strongly** |
| nature-figure | R1.A (revised) | 1 Calibrates + 1 Overreaches partial + 1 Overreaches | fork-narrowly |
| scientific-figure-making | R1.B | 2 Calibrates + 1 Overreaches | fork-narrowly |

## What to import (full or strong fork)

### From nature-polishing → MinionsOS Writer skills

These are the highest-confidence ports from R1.

#### 1. New skill: `cn-en-academic-polish.md`

Reason: case-intro-zh +5 (Prevents real failure). The "reconstruct logic
before translating clauses" + hourglass restructure rule transformed a
Chinese-translation-flavoured paragraph into a Nature-style introduction.
This addresses a real Writer use case (Chinese-author labs targeting CNS).

Draft: `proposed-skills/cn-en-academic-polish.md`

#### 2. Update `minions/roles/writer/skills/abstract-writing.md`

Add as hard rules:
- Explicit "Here, we show" main-result anchor (or equivalent direct verb in
  the venue's house style).
- Bounded-implication closer: implications must name the species / scope /
  system actually tested. No "for neurological disease" when the data are
  mouse preclinical.

Draft delta: `proposed-updates/abstract-writing.md.diff`

#### 3. Update `minions/roles/writer/skills/apply-revisions.md`

Add as hard rules:
- Paper-type diagnosis as first move: identify research / methods / hypothesis
  / algorithmic before any sentence-level edit.
- Results vs Discussion verb taxonomy: list the past-tense observation verbs
  (was detected, increased, showed, enabled, achieved) vs interpretive verbs
  (may reflect, suggests, could indicate, is likely due to, may facilitate)
  as a hard register rule.

Draft delta: `proposed-updates/apply-revisions.md.diff`

#### 4. Update `minions/roles/reviewer/skills/aspect-note.md` (or peer)

Add as a quality-of-criticism rule:
- "Name the specific missing experiment, not just the experimental design
  class." From case-overclaim: "did not include transfer experiments" beats
  "observational design cannot establish causation."

Draft delta: `proposed-updates/aspect-note.md.diff`

### From nature-figure + scientific-figure-making → MinionsOS Writer skills

These two skills produced the same set of portable wins and the same set of
rejections. Treating them together is more efficient than picking one as
canonical.

#### 5. Update `minions/roles/writer/skills/academic-plotting.md`

Add as hard rules:
- rcParams block: Arial / Helvetica / DejaVu Sans / Liberation Sans fallback
  chain, `svg.fonttype="none"`, `pdf.fonttype=42`, top/right spines off,
  axis linewidth 0.8, `legend.frameon=False`.
- PALETTE-dict pattern: define a single dict at the top of any multi-panel
  plot script and thread it through every panel. Rule: "reserve green/red
  for directional signals; use neutrals (grey, single-blue family, faint
  pink) for categorical labels."
- Default figsize in inches, not millimetres. Compress to mm only at
  submission packaging stage, after layout is visually confirmed.
- TwoSlopeNorm(vcenter=0) for any diverging colormap.
- Outside-tick discipline: `direction="out", length=2.2-2.5, width=0.6-0.7`.
- Editable text in vector outputs is a hard submission requirement (verified
  in R1: baseline SVGs had 0 `<text>` nodes; rasterised text is not editable
  by copy-editors and breaks Nature-family submission).

Draft delta: `proposed-updates/academic-plotting.md.diff`

#### 6. New skill / new section: 4-panel hero default

Reason: case-multi-panel for both nature-figure and scientific-figure-making
**lost** to baseline because both skills nudged the runner toward custom
asymmetric grids that produced empty quadrants or stretched bars. Baseline
naturally used `width_ratios=[2,1,1] + gs[1, :]` for D — and the user called
that layout "非常漂亮、精致" both times.

Add as a hard rule:
- "Default 4-panel hero pattern is `gridspec(2, 3, width_ratios=[2,1,1],
  height_ratios=[1.4, 1])` with `ax_d = gs[1, :]`. Try this first; only
  design a custom asymmetric grid if it demonstrably fails for the brief."
- "No empty quadrants in gridspec." If the chosen grid leaves a cell with
  no panel, either extend a panel into it or pick a smaller grid.
- "No over-stretched panels." A panel containing 3 categorical bars should
  not span 180 mm of width. Match panel width to data density.
- "Tight figsize requires layout-budget triage": choose at most one of
  {above-axes legend, below-axes caption, in-axes significance brackets}
  per figure.

Draft: `proposed-skills/figure-layout-defaults.md`

## Provenance

Each ported rule lists the round + case that justified it:

- `cn-en-academic-polish`: R1.C case-intro-zh
- `abstract-writing` deltas: R1.C case-abstract
- `apply-revisions` deltas: R1.C case-results, case-overclaim
- `aspect-note` deltas: R1.C case-overclaim
- `academic-plotting` deltas (rcParams, PALETTE, TwoSlopeNorm, outside ticks):
  R1.A case-bar / case-heatmap / case-multi-panel + R1.B case-bar / case-heatmap
- `figure-layout-defaults`: R1.A case-bar (mm-figsize cramming) +
  R1.A case-multi-panel (empty quadrant) +
  R1.B case-multi-panel (cramped B/C + over-stretched D)

## Validation note

R1.A's initial scoring was wrong because I evaluated figures by code-layer
inspection (rcParams set, palette dict present, gridspec asymmetric) without
opening the rendered output. The user's visual review caught what the
structural rubric missed: layout failures hidden inside content-discipline
wins. R1.B used user visual review as the load-bearing input from the start.
**For any future figure round: visual inspection is mandatory before
scoring.**
