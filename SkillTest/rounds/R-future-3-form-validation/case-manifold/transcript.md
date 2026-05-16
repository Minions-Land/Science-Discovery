# R-future-3 Task 1 transcript: manifold form-choice validation

## Brief

Source brief: `/Users/mjm/Skill/SkillTest/fixtures/figures-novel-form/manifold/briefs/manifold.md`

The figure must defend the claim that cells differentiate from progenitor
through an intermediate trajectory toward terminal fates A and B, with a
midway bifurcation and gene_marker_pct behavior that varies over pseudotime.
The required content is a 2D natural geometric structure with four clusters,
pseudotime, and marker percentage. The figure should communicate trajectory
and bifurcation visually, not just cluster identity.

## Baseline run notes

Skill files loaded: none. The run read only the brief.

Chosen form: conventional 2D embedding scatter colored by cluster.

Why: The brief asks for a Nature Methods style cell trajectory figure, and a
polished embedding scatter is the natural baseline choice for single-cell
coordinates. The implementation uses the provided x/y coordinates directly,
adds cluster colors and a compact legend, and preserves equal aspect ratio.

## Candidate run notes

Skill files loaded:

- `/Users/mjm/Skill/SkillTest/synthesis/proposed-skills/figure-aesthetic-exemplars/SKILL.md`
- `/Users/mjm/Skill/SkillTest/synthesis/proposed-skills/figure-aesthetic-exemplars/aesthetic-principles.md`
- `/Users/mjm/Skill/SkillTest/synthesis/proposed-skills/figure-aesthetic-exemplars/gallery/diffusion_swiss_roll.annotation.md`

Chosen form: manifold trajectory map with pseudotime-colored cells, smoothed
trajectory branches, inline terminal labels, and an explicit bifurcation point.

Why: Principle 5 says that when geometry is the message, the geometric manifold
form should be primary. The diffusion_swiss_roll annotation drove three concrete
decisions: keep the geometric structure as the visual subject, use a single
cyan-teal hue family with saturation gradient for flow, and reduce chart chrome
so the manifold occupies the display area. The annotation's warning against
default multi-hue colormaps also drove the custom cyan trajectory colormap.
