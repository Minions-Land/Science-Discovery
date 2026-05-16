# R3 Synthesis

**Round:** R3 (R3.A nature-data + R3.B nature-citation + R3.C deslop-comparison)
**Date:** 2026-05-16
**Status:** Research-zone artefacts. **Nothing in `proposed-skills/` or
`proposed-updates/` is applied to `/Users/mjm/MinionsOS/minions/roles/` until
the user explicitly approves.**

## Summary

| Skill | Round | Bucket | Recommendation |
|---|---|---|---|
| nature-data | R3.A | Prevents real failure (18/18 vs 8/18) | **import-strongly** |
| nature-citation | R3.B | Calibrates response (13/15 vs 9/15) | fork-narrowly |
| skill-deslop | R3.C | Matches baseline | skip |
| avoid-ai-writing | R3.C | Matches baseline | skip |
| humanizer-academic | R3.C | Matches baseline | skip |
| stop-slop | R3.C | Calibrates response (active-subject rule only) | fork-narrowly (very narrow) |

R3 produced 1 strong port, 2 narrow ports, and 3 explicit skips. Highest-
confidence cross-round finding: the **substantively-bounded specificity**
anchor rule is now confirmed across 4 fixtures (R1.C overclaim + R2 rebuttal
+ R3.A data availability + R3.B citation candidates).

## Key cross-round findings

### 1. Substantively-bounded specificity (cross-confirmed across 4 fixtures)

> Replace vague good-faith promises with substantively-bounded specificity.

- R1.C overclaim: "did not include transfer experiments" beats
  "observational design cannot establish causation"
- R2 rebuttal: `[X]` placeholder beats inventing `page 12, lines 310-324`
- R3.A data availability: named DAC + 4 review conditions beats
  "available upon reasonable request"
- R3.B citation: `[needs verification]` placeholder beats fabricating DOIs

This is the highest-confidence portable principle from R1+R2+R3.
Should land at MinionsOS Writer + Reviewer common contract level (or
as a top-level common skill), not inside any single skill file.

Draft the elevation as: `proposed-skills/substantively-bounded-specificity.md`
or as an addition to `minions/roles/SYSTEM.md`'s "evidence-first EACN
communication" section. (To be authored after user approves the rule
elevation.)

### 2. Big blacklists don't bite Opus-class models

R3.C's controlled comparison (4 deslop skills × 1 saturated-slop fixture
+ baseline) showed all 5 outputs scored 0 on slop-term and em-dash
removal. Opus 4.7 (May 2026) internalises every entry in the union of
these 4 skills' blacklists.

Implication for MinionsOS: skip the deslop family for Writer. The
existing AI-trace blacklist proposed in R1.C `apply-revisions.md.diff`
is sufficient (and that one was R1.C-confirmed, not 2026-confirmed —
arguably even it is already redundant for Opus-class).

### 3. nature-data is the highest-leverage R3 import

The "available upon reasonable request" failure mode is universal in
Chinese-author labs preparing CNS submissions. nature-data's named-DAC
+ DataCite-metadata + code-reproducibility-fallback discipline produces
a Nature-policy-compliant statement from rough Chinese-influenced
English. R3.A's 18/18 vs 8/18 is the largest single-case Δ in
SkillTest so far.

Plan to author `synthesis/proposed-skills/data-availability-statement.md`
once the user approves R1+R2 ports.

## Files in R3

| Path | Purpose |
|---|---|
| `rounds/R3-nature-data/` | 1 case (mixed-restrictions) |
| `rounds/R3-nature-citation/` | 1 case (mixed-claims) |
| `rounds/R3-deslop-comparison/` | 1 case (saturated-slop) × 4 candidates |
| `synthesis/R3-synthesis.md` | this file |
| `promoted/submission-mechanics/` | nature-data added to promoted library |

## What to test next

R4 candidates (from R1+R2 round notes):

- **Hard-probe rebuttal** (R2.B): minor revision / appeal-like / transfer-
  after-review fixtures to test the full `nature-response` action-label FSM.
- **Multi-panel figure with non-4-panel layout** (R1.x extension): does
  the asymmetric-grid failure mode that hit R1.A and R1.B persist on
  5-panel or 6-panel briefs? Or is the matplotlib-default `[2,1,1]+bottom`
  rule specifically a 4-panel artefact?
- **Haiku-class deslop** (R3.x extension): re-run R3.C on Haiku as
  executor (per skill-evaluator-by-metaharness protocol) to see if
  smaller models genuinely benefit from blacklists where Opus does not.
- **Real-network citation** (R3.B extension): an online evaluation of
  nature-citation's Crossref script to test the high-leverage feature
  SkillTest's no-network design didn't exercise.
- **End-to-end paper writing** (new): combine multiple ported skills
  (nature-polishing + nature-figure rcParams + nature-data + nature-
  response) on a single fixture to test cross-skill orchestration.

## Decision required from user

R3 results don't change the R1+R2 port plan; R3 adds:
1. nature-data → port (new skill `data-availability-statement.md`)
2. nature-citation → fork-narrowly (update existing `citation-audit.md`
   with stable IDs + scope filtering + support grading)
3. deslop family → skip (baseline already handles it)
4. **Cross-skill anchor rule** (substantively-bounded specificity) →
   elevate to common contract or top-level skill

Drafts for #1 and #2 will be authored after user approves the R1+R2
port plan, to keep R3 synthesis decoupled.
