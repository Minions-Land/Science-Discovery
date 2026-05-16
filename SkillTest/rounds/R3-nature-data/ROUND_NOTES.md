# Round Notes — R3.A nature-data

**Cases:** case-mixed-restrictions (1 case)
**Date:** 2026-05-16
**Candidate skill:** `/Users/mjm/Skill/nature-skills-main/skills/nature-data/`

## Headline

Candidate **18/18** vs baseline **8/18** (+10). Bucket: Prevents real
failure. Strongest single-case Δ in SkillTest so far.

The skill exists to turn "we share when we can" prose into Nature-policy-
compliant Data Availability + Code Availability statements. R3.A confirms:
it does.

## Three load-bearing changes (in order of importance)

1. **Replace "reasonable request" with named DAC + 4 review conditions.**
   This is what Nature explicitly flags as inadequate; this is what the
   skill explicitly fixes.
2. **Patent-pending code reproducibility fallback.** "Release runnable
   wrappers, documentation, environment files and placeholder interface
   sufficient to reproduce all non-restricted steps" — preserves repro
   under IP constraint.
3. **DataCite-style metadata fields without fabrication.** Names creator
   / year / title / repository / version / DOI/accession as REQUIRED
   without inventing any. Baseline failed this entirely.

## Cross-confirmed meta-rule

R1.C: "name the specific missing experiment, not the design class."
R2:  "never invent page numbers / line numbers; use [X] placeholders."
R3.A: "name the specific access controller / review conditions /
       metadata fields; placeholder for unknown identifiers."

A shared anchor rule across all three rounds: **substantively-bounded
specificity, not vague good-faith promises.**

This is no longer a single-skill rule — it's a portable cross-skill
principle that should land at the Writer / Reviewer SYSTEM.md level
or as a top-level skill.

## Token economics

- baseline input ~700 tokens
- candidate input ~7600 tokens (10.8x)
- output ~750 vs ~470 tokens (1.6x)

Light premium relative to nature-figure / nature-response. The skill
focuses tightly on data-availability discipline and doesn't need a
huge reference library.

## Recommendation

`import-strongly`. Plan to author:

- `synthesis/proposed-skills/data-availability-statement.md` — new skill
  for Writer covering: reasonable-request replacement; named DAC +
  review conditions; DataCite-style metadata; code reproducibility
  fallback; Chinese-author-alignment.

Plus, add the cross-skill anchor rule to MinionsOS Writer + Reviewer
common contract (or the existing `evidence-first EACN communication`
section): **substantively-bounded specificity, not vague good-faith
promises.** Three independent fixtures now demand it.

## What to test next in R3 (the queue)

- R3.B nature-citation — Nature/Science/Cell citation retrieval. Will
  test whether the no-fabrication anchor rule extends to citations
  (it should), and whether the skill can scope-filter properly.
- R3.C deslop family — three small skills (skill-deslop, avoid-ai-writing,
  humanizer-academic, stop-slop) tested as a comparison set. R1.C already
  showed AI-trace blacklists are insurance, not transformative; R3.C
  should sharpen what dimensions of "AI-slop" actually move under skill
  guidance.
