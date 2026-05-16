# Verdict — nature-data / case-mixed-restrictions

**Round:** R3.A · **Date:** 2026-05-16 · **Rubric version:** v1
**Rubric scale:** /18 (Data Availability rubric — adapted from rebuttal /15)

## Numeric score

| Dim | Pts | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|---|
| Restricted-data access route specificity | 4 | 1/4 | 4/4 | +3 | baseline: "request from corresponding author... institutional approval" — bare reasonable-request variant. Candidate: names institutional Data Access Committee, lists 4 review conditions (eligibility / proposed use / ethics approval / data-use agreement) |
| Public-dataset citation discipline | 3 | 1/3 | 3/3 | +2 | baseline: "available from their original repositories" — fails DataCite spec. Candidate: explicit DataCite-style fields required (creator / year / title / repository / version / DOI/accession) without fabricating identifiers |
| Restriction reason + controller named | 3 | 2/3 | 3/3 | +1 | baseline: "patient consent restricts redistribution"; candidate adds named controller (institutional DAC) and review process |
| Code Availability with reproducibility fallback | 3 | 1/3 | 3/3 | +2 | baseline: patent-pending = "will not be released" period. Candidate: provide "runnable wrappers, documentation, environment files, placeholder interface sufficient to reproduce all non-restricted preprocessing and analysis steps" — preserves reproducibility under IP constraint |
| FAIR metadata coverage | 3 | 1/3 | 3/3 | +2 | candidate explicitly requires public metadata + file manifest + persistent identifier |
| No fabrication | 2 | 2/2 | 2/2 | 0 | both runs avoided inventing DOIs / accession numbers; both used "application 78922" only because the fixture supplied it |
| **Total** | **18** | **8/18** | **18/18** | **+10** | |

## What the skill actually delivered

Three load-bearing changes:

1. **Replace "reasonable request" with a named DAC + access conditions.**
   This is the rule the skill exists for. Baseline did better than the
   author's original Chinese-influenced "available upon reasonable
   request" wording (it added "institutional approval"), but still leaves
   the reviewer guessing about who reviews and on what criteria.
   Candidate names: institutional Data Access Committee + 4 review
   conditions (researcher eligibility, proposed use, ethics approval,
   data-use agreement).

2. **Patent-pending code reproducibility fallback.** The fixture's hardest
   trap — author wants to withhold patent-pending code, baseline accepts
   that as "will not be released," candidate reframes it as "release
   runnable wrappers, documentation, environment files and a placeholder
   interface sufficient to reproduce all non-restricted preprocessing and
   analysis steps." This preserves reproducibility while protecting IP —
   the only correct way to handle this for Nature-family submission.

3. **Explicit DataCite-style metadata requirements.** Baseline says the
   public datasets "are available from their original repositories";
   that fails the FAIR metadata checklist. Candidate names the required
   fields (creator / year / title / repository / version / DOI/accession)
   without fabricating values — the discipline both Nature and DataCite
   require.

## What the skill missed

Nothing critical for this case. The candidate could have flagged that
"Zenodo restricted-access" is consortium-internal terminology and
explicitly state the link between Zenodo's restricted-access mechanism
and the EU GDPR / German DSGVO compliance regime. Minor; a future hard-
probe fixture (data residency / international transfer) could test this.

## Visual / textual inspection

Both statements are well-formed prose for a Nature submission. Candidate
is ~70 words longer than baseline (380 vs 310) — modest, all of the
extra words go into specifying access conditions and DataCite fields.

Both correctly:
- Separate the three patient-data subsets (ECG / RNA-seq / public)
- Cite ethics approval Heidelberg-2024-127 (verbatim from fixture)
- Keep "application 78922" verbatim (no fabrication)

Only candidate:
- Names Data Access Committee + review conditions
- Specifies DataCite-style fields for reused public data
- Specifies a reproducibility-preserving code release alongside patent-
  pending placeholder

## Token cost

See `tokens.json`. Single-case run; nature-data is mid-weight skill
(~10 KB SKILL.md + ~5 references averaging ~6 KB each). Candidate input
~10x baseline; output ~1.2x.

## Bucket

**Prevents real failure.** Three independent submission-blockers fixed
on a Nature-family Data Availability statement: vague restriction route
(would draw editor pushback), missing DataCite metadata (would draw
production pushback), patent-pending code with no reproducibility
fallback (would draw reviewer pushback). The skill turns "we share
when we can" prose into a Nature-policy-compliant statement.

## Cross-validation with R1.C / R2

R1.C taught: "name the specific missing experiment." R2 confirmed:
"never fabricate page numbers." R3.A extends the family: **"name the
specific access controller / review conditions / metadata fields."**
The shared meta-rule emerging: *substantively-bounded specificity,
not vague good-faith promises*. This is now confirmed across 3 fixtures
(R1.C overclaim Discussion + R2 rebuttal letter + R3.A data availability)
and is a portable cross-skill principle.

## Porting recommendation

`import-strongly`. nature-data delivers exactly the discipline its
description claims. Plan to:

### Add new skill: `data-availability-statement.md` (Writer)

A rules-and-templates skill, drawing on:
- The "reasonable request is inadequate" anchor rule
- Named DAC + review conditions for restricted human data
- DataCite-style fields for reused public data (without fabrication)
- Code Availability separation with reproducibility fallback for
  patent-pending or proprietary code
- Chinese-author-alignment subroutine for translating Chinese-flavoured
  data-availability prose into Nature-policy-compliant English

Draft to be authored after user approves R1 / R2 ports. Will live at
`synthesis/proposed-skills/data-availability-statement.md`.

## Open questions for the next round

- Would adding a hard-probe fixture (international data transfer /
  GDPR / IRB-restricted with redaction questions) extend the rule?
  Schedule for R3.A.B if the user wants stronger evidence.
- Cross-validate with `nature-citation` (R3.B) — both skills need to
  not-fabricate identifiers, and a shared "no fabrication" anchor
  rule may emerge.
