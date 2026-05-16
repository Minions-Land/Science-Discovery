# R6 Synthesis (Hard-Probe Extension Round)

**Round:** R6 (R6.A 9-panel figure + R6.B real-network citation + R6.C subtler-slop)
**Date:** 2026-05-16
**Status:** Research-zone artefacts. R6 closes 3 deferred questions from
R3-synthesis.md and surfaces a NEW aesthetic-ceiling gap that no current
skill addresses.

## Summary

| Sub-round | Tested | Result |
|---|---|---|
| R6.A | figure-layout-defaults at 9 panels | Layout skill INERT; surfaced 2 new rules (subgridspec packing, y-axis range) + aesthetic-ceiling finding |
| R6.B | nature-citation with real Crossref | UPGRADED to "Prevents real failure" — Crossref query.title rank-1 is polluted for famous papers |
| R6.C | deslop family on buried-slop | 3rd consecutive confirmation of skip; final |

## Three load-bearing R6 findings

### 1. Crossref query API has rank-1 pollution (R6.B)

When Codex / Writer queries Crossref by title for famous papers, rank-1
can be a third-party record using the famous title. Without sanity
checks (year matches, container matches, first author matches), rank-1
trust produces hallucinated citations. R6.B caught this on Vaswani 2017
(returned 2025 Shenzhen Medical Academy record) and Devlin 2019 BERT
(returned 2014 Museum Education paper).

**Implication for port:** nature-citation's "verify before cite" rule
is upgraded from R3.B Calibrates to R6.B **Prevents real failure**.
The proposed `citation-audit.md.diff` update should add the
sanity-check rule as HARD.

### 2. figure-layout-defaults coverage is now mapped (R6.A)

| Panel count | Skill effect |
|---|---|
| 4 | load-bearing (Overreaches if absent) |
| 5 | load-bearing (Overreaches if absent) |
| 6 | inert (Codex finds right grid) |
| 7 | load-bearing (+10 user-confirmed win) |
| 9 | inert for layout; surfaces 2 new rules |

The skill's value scales with COMPLEXITY OF DECISION, not panel count
linearly. Add the 2 new rules from R6.A and the skill is mature.

### 3. Aesthetic ceiling: rules don't produce beauty (R6.A meta-finding)

User: "用了 Skill 的配色可能稍微规范一点，但是和美感、好看完全搭不上边."

All figure skills tested operate at the rule level: pick from palette,
use these fonts, this spacing. Rules produce CORRECT (submittable)
figures. They do NOT produce BEAUTIFUL figures. Beauty requires:
- Genuine visual design judgment (cannot be encoded as rules alone)
- Iterative refinement based on whole-figure composition
- A library of WORKED EXAMPLES to learn from (galleries, not rule lists)
- Possibly a vision-capable model that can judge "is this beautiful?"

This is a gap NO current skill in SkillTest addresses. Future work:

**Proposed new skill (NOT for current port): `figure-aesthetic-exemplars.md`**

A reference-driven skill rather than rule-driven:
- Curate 20-30 published Nature / Cell / Science figures with annotation:
  what makes this figure beautiful, what design choices it makes
- Document specific palettes (RGB / hex) used in venue's recent figures,
  not generic "colourblind-safe" rules
- Document typography case studies (caption density, panel-letter
  styling, scale-bar treatment)
- Document figure-level composition principles (visual rhythm across
  panels, where the eye lands first, white space allocation)
- Recommended workflow: "diff your figure against the closest exemplar
  in the gallery; identify the 3 biggest deltas; address those"

This is a different SKILL PARADIGM (examples + judgment) from the
current rules-based skills. Worth its own R-future round to develop.

## Cross-validation across deslop rounds (now closed)

| Round | Executor | Density | Δ |
|---|---|---|---|
| R3.C | Opus 4.7 | saturated | 0 |
| R4.C | Haiku 4.5 | saturated | 0 |
| R6.C | Haiku 4.5 | buried | 0 |

3 rounds × 4 skills × 2 executors × 2 densities = 24 cells, all "matches
baseline." The deslop family is empirically inert. **Question closed.**

## What R6 changes for the port plan

### Updates

1. **R6.A 2 new rules** added to `proposed-skills/figure-layout-defaults.md`:
   - Step 5: subgridspec packing for nested 2x2 sub-regions
   - Step 6: y-axis range tuning to data density

2. **R6.B finding** strengthens `proposed-updates/citation-audit.md.diff`:
   - Add HARD rule "never accept Crossref query.title rank-1 without
     sanity check (year, container, first author); fall back to direct
     DOI lookup if check fails"
   - Upgrade citation-audit / nature-citation port from fork-narrowly to
     **import-strongly** for the verify-before-cite rule specifically

3. **R6.C** confirms deslop skip (no change to port plan; just final).

### New (deferred to R-future, not for current port)

- `figure-aesthetic-exemplars.md` — separate skill paradigm (examples
  + judgment, not rules) to address the "rules-don't-produce-beauty"
  ceiling. Out of scope for current port; flagged for future work.

## What R6 leaves unresolved

- Beauty / aesthetic figure quality remains an open problem.
- Vision-capable iterative design loop (model + render + judge) is not
  yet in scope for any tested skill.
- Deeper venue-specific palette galleries (Nature vs Cell vs Science
  visual identity) are not in scope either.

These are R-future / R-experimental territory. The current port plan
covers "make submittable figures with rules"; the future plan should
cover "make beautiful figures with examples + judgment."

## Decision required from user (post-R6)

R6 confirms R5's recommendation: ready to land R1+R2+R3+R4+R5 ports,
plus R6's 2 new layout rules + R6.B citation upgrade. The aesthetic-
ceiling gap is documented but not blocked-on.

Land the port? Or run a R-future round on aesthetic exemplars first?
