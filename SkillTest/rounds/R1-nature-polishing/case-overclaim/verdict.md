# Verdict — nature-polishing / case-overclaim

**Round:** R1.C · **Date:** 2026-05-16 · **Rubric version:** v1

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Argument clarity / paper-type fit | 3/4 | 4/4 | +1 | both identify it as Discussion paragraph; candidate explicitly diagnoses "claim without evidence + missing boundary" |
| Hedging calibration | 2/3 | 3/3 | +1 | baseline softens to "consistent with a potential protective association"; candidate goes further: "consistent with a protective association, rather than proof of protection" — names the discipline directly |
| Sentence rhythm | 3/3 | 3/3 | 0 | both ≤30 words |
| AI-trace removal | 3/3 | 3/3 | 0 | clean |
| Claim-evidence completeness | 2/4 | 4/4 | +2 | baseline says "data do not support a clinical recommendation"; candidate says "Because the study was observational and did not include transfer experiments, standard-of-care recommendations would be premature" — names the *specific* missing experiments |
| Citation hygiene | 2/3 | 2/3 | 0 | not exercised |
| House style consistency | 2/2 | 2/2 | 0 | both British |
| **Total** | **17/22** | **21/22** | **+4** | |

## What the skill actually changed

Two real differences:

1. **Limitation specificity.** Baseline boundary is "do not support a clinical recommendation at this stage" — generic. Candidate names the specific experimental gaps: "the study was observational and did not include transfer experiments" — a reviewer can verify both, can't argue with either. This is the skill's "Discussion = how we understand it AND when it may fail" rule applied with teeth.
2. **Mechanism downgrade.** Both remove "almost certainly through SCFA signalling." Baseline → "provides a plausible mechanistic link, although direct mechanistic experiments will be needed." Candidate → "may contribute, but this mechanism remains to be tested directly." Candidate is one notch more bounded — "may contribute" is weaker than "provides a plausible mechanistic link."

## What the skill missed or hurt

Candidate is verbose: 175 words vs baseline 130. The boundary and mechanism qualifications take real word budget. For a Discussion paragraph this is fine; for a Conclusion or abstract it would crowd. Skill should warn that boundary-explicit Discussion prose is naturally longer.

## Visual / textual inspection

Both correctly remove "causes / proves / we are the first / will fundamentally change / should now become standard of care / almost certainly." The boundary specificity is where they part: baseline says "this kind of study can't conclude X"; candidate says "this study didn't do experiments Y and Z, which would be needed to conclude X." The latter is reviewer-proof.

## Token cost

See `tokens.json`. Same skill-load shape as case-intro-zh (~10× input). Output 175 vs 130 words — 35% longer for the explicit limitations.

## Bucket

**Calibrates response.** Both deliver an acceptable Discussion paragraph; candidate is sharper specifically on which experiments would be needed to upgrade an association to a causal claim. Real difference, not transformative.

## Porting recommendation

`fork-and-adapt`. The "name the specific missing experiment, not just the design class" rule is portable to MinionsOS reviewer skills (`reviewer/skills/code-validity-review.md` analog for prose). Combine with the existing "every claim must have evidence or be marked speculation" rule already in the writer system.
