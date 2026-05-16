# Verdict — nature-citation / case-mixed-claims

**Round:** R3.B · **Date:** 2026-05-16 · **Rubric version:** v1
**Rubric scale:** /15 (Citation candidate rubric — adapted from rebuttal /15)

## Numeric score

| Dim | Pts | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|---|
| Stable IDs / claim segmentation | 3 | 1/3 | 3/3 | +2 | baseline uses prose claim labels; candidate uses `S001-S008` IDs (cross-reference-able) |
| Scope filtering (in-scope CNS-family) | 3 | 1/3 | 3/3 | +2 | baseline lists every claim; candidate marks scVelo "scope unresolved" and SCFA paper as conditional on "directly tests... in relevant immune context" |
| No fabrication | 3 | 3/3 | 3/3 | 0 | both runs avoided inventing DOIs / volumes / pages — `[needs verification]` everywhere. Note this is the primary failure mode being tested; both passed |
| Citable-vs-internal discrimination | 2 | 2/2 | 2/2 | 0 | both correctly flagged the manuscript's own r=0.63 result as out-of-scope for external citation |
| Chinese fragment translation | 2 | 2/2 | 2/2 | 0 | both translated "之前在 Science 上有人报道过" to "previously reported in Science" + "short-chain fatty acid signalling T cell exhaustion Science" search terms |
| Support grading / status field | 2 | 0/2 | 2/2 | +2 | baseline doesn't tier candidates; candidate tags each as metadata-only / background / "first requires verification" / scope-unresolved / out-of-scope-for-external-support |
| **Total** | **15** | **9/15** | **13/15** | **+4** | |

## What the skill actually delivered

Three structural improvements:

1. **Stable claim IDs (`S001-S008`).** Same load-bearing benefit as
   nature-response's `R<N>.C<M>` format — citation candidates need to be
   cross-referenced when an editor or co-author audits the bibliography.
2. **Scope-filtering with conditional acceptance.** Baseline lists every
   claim as "search Cell / Nature Medicine / Science"; candidate adds
   conditional qualifiers ("Science-family in-scope only if it directly
   tests SCFA signalling in relevant immune context"; "scope unresolved
   for scVelo"). The conditional accept / reject logic is the point of
   journal-scope filtering.
3. **Support grading.** Each candidate gets a status tag: metadata-only,
   background, "first requires verification", scope-unresolved,
   out-of-scope. This lets a downstream reviewer triage the candidate
   list without re-reading the source paragraph.

## What the skill missed

The candidate did NOT call the skill's `nature_citation.py` Crossref
script (which was correct — no network access in this case), but the
skill did not provide a fallback procedure for "no-network" mode. The
script-based skill is high-leverage when network is available; without
network, candidate falls back to roughly what an attentive baseline
runner would produce (with structural improvements). The skill should
document this two-mode operation explicitly.

Both runs avoided fabrication — the primary thing nature-citation exists
to prevent. This is a "skill confirms a discipline both candidate and
baseline already had access to" outcome rather than a transformative
gain.

## Visual / textual inspection

- Both outputs are roughly the same word count.
- Both correctly identify the 8 distinct citable units.
- Both translate Chinese fragments to English search terms.
- Only candidate adds a status / scope column.
- Neither invents identifiers (good; this was the primary trap).

## Token cost

See `tokens.json`. nature-citation has SKILL.md ~12 KB + 3 references
totaling ~10 KB. Candidate input ~10x baseline; output similar length
(structural overhead from the IDs / status column adds modest tokens).

## Bucket

**Calibrates response.** Both reach the right artefact. Candidate is
better-defended by virtue of stable IDs + scope qualifiers + status
tags. Not a "Prevents real failure" because both runs already avoid
the primary failure (fabrication).

This is the first R1+R2+R3 skill where baseline performed strongly on
the primary risk dimension. Worth noting: when the runner is
disciplined enough to use `[needs verification]` placeholders without
prompting, the skill's main contribution is structure, not safety.

## Cross-validation with R3.A no-fabrication anchor

R3.A demanded "name the specific access controller / placeholder for
unknown identifiers." R3.B reaches the same conclusion via Crossref-
script-aware no-fabrication discipline. The cross-skill anchor rule
**substantively-bounded specificity, not vague good-faith promises**
now confirmed across 4 fixtures (R1.C overclaim + R2 rebuttal + R3.A
data availability + R3.B citation candidates).

## Porting recommendation

`fork-narrowly`. The structural rules (stable IDs, scope filtering,
support grading) are portable. The Crossref script and journal-family-
filter logic are too venue-specific for MinionsOS's general Writer
role. Plan to:

### Update `minions/roles/writer/skills/citation-audit.md` (existing)

Add as hard rules:
- **Stable claim IDs (`S<NNN>` format)** for cross-reference between
  bibliography audits and editorial review.
- **Scope filtering with conditional acceptance**: when the target
  journal family is constrained (Nature Portfolio / Cell Press /
  Science / etc), each candidate must be tagged as in-scope, out-of-
  scope, or scope-conditional with the qualifier named.
- **Support grading status tag**: metadata-only / background /
  primary-source / methodological / requires-verification.

Draft to be authored after user approves R1+R2+R3.A ports. Will live at
`synthesis/proposed-updates/citation-audit.md.diff`.

## Open questions for next round

- A real-network test would show whether the skill's Crossref script
  saves time. SkillTest is a no-network benchmark by design; this
  could be a future R4 task with a real online evaluation.
- Both R3.A and R3.B confirm the no-fabrication anchor rule. R3.C
  (deslop family) tests it from a different angle — does the skill
  prevent AI-generated slop *vocabulary* fabrication? Already partially
  evidenced in R1.C; R3.C will sharpen the picture.
