# Round Notes — R6.A 9-panel figure (8+ panel layout extension)

**Cases:** case-9panel
**Date:** 2026-05-16

## Headline

**Skill is inert at 9 panels** (Codex naive baseline finds the same
gridspec(4, 4) hero pattern). But the round surfaces TWO new failure modes
that NO skill in SkillTest currently addresses, plus user feedback that
exposes the ceiling of "rule-based palette discipline" itself.

## Three findings

### 1. Layout skill is INERT at 9 panels
Same as R5.C 6-panel — at this complexity Codex finds the right grid
without skill guidance. The skill's value is at intermediate complexity
(4, 5, 7 panels) where the runner would otherwise drift to a wrong custom
grid. At 6 and 9 panels the natural answer is the right answer.

### 2. NEW Rule: subgridspec packing for nested 2x2 sub-regions
User caught: "右上角这一块地方，图表是散开的，中间有很多留白." When
B/C/D/E share a 2x2 sub-region of a 4x4 grid, default wspace/hspace
produces visible whitespace between them. Fix: wrap in subgridspec
with tighter spacing. Added as Step 5 to figure-layout-defaults.md.

### 3. NEW Rule: y-axis range to data density
User caught: bar chart with values 65 and -3 on y-axis 0-100 leaves 35%
empty top. "柱子画得那么长，完全没有意义." Fix: tune ylim to data range
+/- 10% headroom when data spans <70% of nominal axis. Added as Step 6
to figure-layout-defaults.md.

### 4. CEILING discovered: rule-based palette is规范 but not 美

User: "用了 Skill 的配色可能稍微规范一点，但是和美感、好看完全搭不上边."

This is the key finding of R6 as a whole. All figure skills tested
(nature-figure, scientific-figure-making, figure-layout-defaults) operate
at the level of RULES: pick from this palette, use these fonts, this
spacing. Rules produce CORRECT figures (no rasterised text, no clashing
hues, no empty quadrants, no over-stretching). Rules do NOT produce
BEAUTIFUL figures.

Beauty / aesthetic appeal requires:
- Genuine visual design judgment (rules can constrain but not generate)
- Iterative refinement based on overall composition (skills give rules
  per-panel, not per-figure)
- A reference library of GOOD figures to learn from (visual examplars,
  not rule lists)
- Possibly a human designer or a specialised vision-capable model that
  can judge "does this look like a Nature cover?"

The current skill library covers the "make it submittable" axis well.
It does NOT cover the "make it beautiful" axis at all. That requires
a different kind of skill — one with worked examples, palette
*galleries* (not rules), typography case studies, and possibly a
reference-figure visual diff workflow.

## Bucket

**Matches baseline** (skill inert for layout at 9 panels). 2 new rules
added to figure-layout-defaults.md. Aesthetic ceiling identified as a
gap that no current skill closes.

## Recommendation

- Continue with the R5 port plan (figure-layout-defaults import-strongly).
- After landing, author a separate R-future skill `figure-aesthetic-examplars.md`
  that shifts from rules to worked-examples-as-reference. Mark this as
  "skill design open question" — it may be that LLM-driven design simply
  cannot match aesthetic-quality figures without a vision-capable design
  loop.

## Methodology learning

R6.A's user judgment exposed BOTH structural failures (subgridspec
packing, y-axis range) AND a meta-level failure (rules vs aesthetic).
The structural failures are addressable by adding rules. The meta-level
failure is NOT addressable by adding more rules — it needs a different
skill paradigm.

This validates the SkillTest methodology: visual judgment by user is
load-bearing, not a luxury. R1.A's wrong score (revised after user
review) and R6.A's aesthetic ceiling finding both came from user
visual judgment, not from any auto-audit metric.
