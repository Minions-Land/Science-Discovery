# Verdict — nature-polishing / case-abstract

**Round:** R1.C · **Date:** 2026-05-16 · **Rubric version:** v1

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Argument clarity / paper-type fit | 3/4 | 4/4 | +1 | candidate explicitly diagnoses "Methods-leaning research abstract; missing abstract ladder plus method detail crowding the result" |
| Hedging calibration | 2/3 | 3/3 | +1 | baseline closes "support further evaluation in neurological disease models" — implies neurological disease use; candidate closes "define a platform for further preclinical evaluation" — bounded to preclinical, no implied disease class |
| Sentence rhythm | 3/3 | 3/3 | 0 | both ≤30 words |
| AI-trace removal | 3/3 | 3/3 | 0 | both remove "we think", "could enable many neurological applications", "significant advance" |
| Claim-evidence completeness | 3/4 | 4/4 | +1 | candidate has explicit "Here, we show" sentence as the main-result anchor (skill's hard rule); baseline has equivalent direct verb ("The formulation delivered ... producing editing in 38%") but no "Here, we show" formula |
| Citation hygiene | 2/3 | 2/3 | 0 | not exercised |
| House style consistency | 2/2 | 2/2 | 0 | both British |
| **Total** | **18/22** | **21/22** | **+3** | |

## What the skill actually changed

Three differences:

1. **Explicit "Here, we show" anchor.** Skill names this as the main-result formula. Baseline has a direct verb but the formula isn't there. For Nature-family abstract triage, "Here, we" is essentially a venue convention.
2. **Bounded implication.** Baseline closes "support further evaluation in neurological disease models" — slipping in "disease" without disease evidence. Candidate closes "define a platform for further preclinical evaluation" — clearly bounded to mouse preclinical, no implied disease scope.
3. **Six-rung ladder explicit.** Both remove the formulation parameters (microfluidic 3:1, PDI 0.12). Candidate's revision notes name the rungs ("context, blocker, approach, key result, bounded implication") — meta-evidence that the structure was driven by the skill, not by intuition.

## What the skill missed or hurt

Candidate is 196 words vs baseline 146 — the longest of the four cases. Some of this is the diagnosis footer; the rest is the explicit "Here, we show" + bounded-implication construction. For a strict 200-word abstract this is right at the limit; the skill should warn about this.

## Visual / textual inspection

Both correctly trim formulation methods, both strengthen the closing. Differences:

- Opening: candidate says "could clarify disease mechanisms and support targeted therapeutic strategies" — broader scientific motivation. Baseline says "could support studies and treatments for neurological disease" — narrower.
- Anchor: candidate "Here, we show that a lipid nanoparticle ..." — formula. Baseline "We developed a lipid nanoparticle formulation ..." — narrative.
- Closing: candidate "define a platform for further preclinical evaluation" — bounded. Baseline "support further evaluation in neurological disease models" — implies disease utility.

## Token cost

See `tokens.json`. Same shape as the other cases. Output ~35% longer.

## Bucket

**Calibrates response.** Both deliver a venue-quality abstract; candidate hits the formal anchor + bounded implication the venue actually expects.

## Porting recommendation

`fork-and-adapt`. The "Here, we show" anchor + bounded-implication closer should port into MinionsOS Writer's existing `abstract-writing.md`. The six-rung ladder is already there; the formal anchor isn't.
