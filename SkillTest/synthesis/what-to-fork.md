# Synthesis — What to Fork (modify before importing)

**Round:** R1 (R1.A + R1.B + R1.C)
**Date:** 2026-05-16
**Status:** SkillTest research zone — none of this is applied to MinionsOS
yet. See `what-to-import.md` for the parallel "high-confidence" list.

## Summary

Three patterns from R1 candidates need to be modified before they are useful.
"Fork-narrowly" in a verdict means: take the underlying intent, but rewrite
the rule to fix what the original got wrong.

## Forks

### 1. Multi-panel hero geometry (from nature-figure + scientific-figure-making)

**Original (rejected):** Both skills push toward custom asymmetric gridspecs
("hero ~50% area + subordinates arranged for visual interest"). On
case-multi-panel, both skills' candidates produced layouts the user
explicitly rejected:

- nature-figure: `gs[0:2, 0:2] + gs[1:, 2:]` → empty `gs[2, 0:2]` quadrant
- scientific-figure-making: B/C cramped right column, D over-stretched bottom-
  middle, lots of whitespace

**Fork (proposed):** Make `width_ratios=[2,1,1] + gs[1, :]` the default 4-panel
hero pattern. Custom grids only when this demonstrably fails for the specific
brief. Add explicit rules: "no empty quadrants" and "no over-stretched panels."

Lives in: `proposed-skills/figure-layout-defaults.md`

### 2. mm-precision figsize (from nature-figure)

**Original (rejected):** nature-figure prescribes `figsize=(width_mm/25.4,
height_mm/25.4)` for journal-strict submission dimensions. On case-bar this
produced 85x58 mm canvas with `constrained_layout collapsed to zero` warning
and unreadable cramming.

**Fork (proposed):** Default figsize in inches with sensible defaults
(`(6, 4)` for single panel, `(11, 6)` for 4-panel with hero). Compress to
exact mm only at submission packaging stage, AFTER layout is visually
confirmed. The skill should treat the warning `constrained_layout collapsed
to zero` as a hard fail (re-render at larger figsize) rather than a cosmetic
warning.

Lives in: `proposed-updates/academic-plotting.md.diff` (rcParams block) +
`proposed-skills/figure-layout-defaults.md` (figsize policy)

### 3. PALETTE rule (from nature-figure + scientific-figure-making)

**Original (acceptable but underspecified):** Both skills mention "unified
palette across panels" but neither names a default palette family.

**Fork (proposed):** Concretise as a 7-key dict:

```python
PALETTE = {
    "signal": "#0F4D92",       # the intervention / treatment / KO direction
    "signal_soft": "#B4C0E4",  # subordinate signal
    "neutral": "#767676",      # control / WT / non-direction
    "neutral_light": "#D8D8D8",
    "accent": "#E4CCD8",       # secondary discriminator (kinase vs GPCR, etc)
    "accent_dark": "#9A4D8E",
    "black": "#272727",
}
```

With the rule: "reserve green/red for directional signals (gain/loss). Use
neutrals + signal-blue + accent-pink for non-directional categorical labels.
The cluster sidebar in case-heatmap baseline used green/red wrongly — green/red
should signify direction, not category."

Lives in: `proposed-updates/academic-plotting.md.diff`

### 4. Diagnosis footer (from nature-polishing)

**Original (acceptable but verbose):** nature-polishing's candidate outputs
emit a "Diagnosed paper type / failure mode" footer. Useful as evidence the
skill loaded; less useful as production manuscript prose.

**Fork (proposed):** Make the diagnosis a *required first move* (rule-level)
but a *suppressed output* (production prose doesn't include it; the diagnosis
is a Reviewer-facing note in the manuscript metadata or skill-internal
scratch). The skill should let the runner toggle the footer based on
audience: include it in revision-coach mode, suppress it in production.

Lives in: `proposed-updates/apply-revisions.md.diff`

## Why fork instead of import or skip

These four are cases where the underlying rule is genuinely useful but the
specific implementation is wrong:

- Multi-panel hero geometry: the *intent* (one panel dominates) is right;
  the *recipe* (custom asymmetric gridspec) is wrong.
- mm-precision figsize: the *intent* (submission-ready dimensions) is right;
  the *default* (mm-strict) blocks the runner from giving the figure
  layout-slack budget.
- PALETTE rule: the *intent* (unified palette across panels) is right; the
  rule was missing a concrete default.
- Diagnosis footer: the *first-move discipline* is right; the *output
  inclusion* is wrong.

Skipping any of these would lose useful intent. Importing as-is would
preserve the failure modes documented in R1 verdicts.
