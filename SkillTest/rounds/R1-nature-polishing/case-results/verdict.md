# Verdict — nature-polishing / case-results

**Round:** R1.C · **Date:** 2026-05-16 · **Rubric version:** v1

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Argument clarity / paper-type fit | 3/4 | 4/4 | +1 | candidate explicitly diagnoses "Research paper, Results paragraph; failure mode was Results / Discussion mixing" — meta-discipline that baseline didn't articulate |
| Hedging calibration | 2/3 | 3/3 | +1 | baseline kept "supporting a requirement for"; candidate uses "linking the co-activator to the measured expression change" — measurement language, not interpretation |
| Sentence rhythm | 3/3 | 3/3 | 0 | both ≤30 words throughout |
| AI-trace removal | 3/3 | 3/3 | 0 | neither emits AI-typical vocabulary or em-dashes |
| Claim-evidence completeness | 3/4 | 3/4 | 0 | both keep n=4, 4%, 1.8-fold, p-values |
| Citation hygiene | 2/3 | 2/3 | 0 | not exercised in this fixture |
| House style consistency | 2/2 | 2/2 | 0 | both British (`generalisation` etc.) |
| **Total** | **18/22** | **20/22** | **+2** | |

## What the skill actually changed

Two real differences, both small:

1. **One additional verb downgrade.** Baseline ends "supporting a requirement for this factor" — "supporting" + "requirement" is mild interpretation. Candidate ends "linking the co-activator to the measured expression change" — pure observation, no claim about necessity. This is the "Results = what we observed; Discussion = how we understand it" rule applied at sentence level.
2. **Explicit failure-mode diagnosis.** Candidate added a "Diagnosed paper type / failure mode" footer block. This isn't fluff — it's the skill's first move ("identify the paper type before editing") emitted as evidence.

## What the skill missed or hurt

Nothing. This is the case the user picked as "easy to converge" — both runs reach roughly the same place because the Results-discipline rules are well-known. The skill just sharpened the edge by one notch.

## Visual / textual inspection

- Both keep the same numerical evidence (3.2-fold, n=4, p=0.011, 4%, 1.8-fold, p=0.003).
- Candidate output is 159 words vs baseline 129 — extra 30 words mostly in revision notes + diagnosis footer, polished prose itself is similar length.
- No em-dashes, no AI-trace vocabulary in either.

## Token cost

See `tokens.json`. Candidate input ~10× baseline because the SKILL.md is ~10 KB. Output similar length. **For results-class polishing the skill premium is paid for the meta-discipline (paper-type ID, hourglass check) more than for the wording — only worth it if those checks save downstream rounds.**

## Bucket

**Calibrates response.** Both reach the right artefact. Candidate is better defended (paper-type diagnosis, observational verb downgrade) but baseline is also publishable.

## Porting recommendation

`fork-narrowly`. The Results-vs-Discussion verb taxonomy (was detected / increased / showed / enabled / achieved vs may reflect / suggests / could indicate / is likely due to / may facilitate) is the portable insight. The "diagnose paper type before editing" rule should also port — it's cheap and biases the output toward the right discipline.
