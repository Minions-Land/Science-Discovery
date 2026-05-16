# Round Notes — R4.A nature-response hard probe

**Cases:** case-author-input-needed (1 case)
**Date:** 2026-05-16
**Candidate skill:** nature-response (R2 candidate; same skill, hard-probe fixture)

## Headline

Candidate **15/15** vs baseline **9/15** (+6). Bucket: Calibrates response
(lower-end of "Prevents real failure"). The hard probe successfully
exercised the AUTHOR_INPUT_NEEDED branch of the nature-response action
FSM. Two skill-specific wins:

1. **Top-of-letter editor flag** — candidate names unresolved comments
   in the opening paragraph of the response letter. Baseline buries this.
2. **PI question list** — candidate emits 6 specific questions the
   corresponding author can paste into an email to the PI. Baseline
   only gives status updates, not actionable questions.

## Why the score isn't 18 vs 0

Baseline did NOT fabricate author positions for R2.C1 / R2.C2 — because
the brief explicitly told it not to. This is a brief-instruction win
rather than a baseline-discipline win. A genuinely hard probe would
bury the no-fabricate rule inside a longer fixture without naming it.

Methodology lesson for future R4+ rounds: hard-probe fixtures should
not name the disposal rule the test is checking for. Update SkillTest
README anti-patterns.

## What the skill confirmed

R2 + R4.A together exercise the full nature-response action-label FSM:

- ACCEPT_TEXT / ACCEPT_ANALYSIS / ACCEPT_EXPERIMENT / ACCEPT_FIGURE
- PARTIAL
- DISAGREE_WITH_JUSTIFICATION + SOFTEN_CLAIM
- ADD_CITATION
- **AUTHOR_INPUT_NEEDED** (R4.A first exercise)
- composite labels (`ACCEPT_EXPERIMENT + SOFTEN_CLAIM`,
  `DISAGREE_WITH_JUSTIFICATION + SOFTEN_CLAIM`)

No FSM branch remains untested. The skill's discipline is empirically
sound across two independent rebuttal fixtures.

## Update to R2 port plan

R4.A adds 2 elements to the existing R2 port plan
(`synthesis/proposed-updates/prepare-rebuttal.md.diff` to be authored):

1. **Top-of-letter flag** for any AUTHOR_INPUT_NEEDED comment(s).
   Editor reads the first paragraph; unresolved items must be visible there.
2. **PI question list** as a separate section, listing specific
   questions the corresponding author should ask the PI. Each
   AUTHOR_INPUT_NEEDED comment generates 2-4 specific questions
   covering "did X happen?", "what details should we report?",
   "what's the location of the change?".

## Token economics

- Baseline input ~600 tokens
- Candidate input ~9300 tokens (15.5x — same as R2)
- Output ~720 vs ~640 (1.1x — minor overhead)

## Recommendation

R4.A strengthens R2's import-strongly verdict. No new skill candidate
to evaluate. The R2 + R4.A package is mature and ready to port whenever
the user approves.

## What R4.B and R4.C still need to test

R4.B: figure with 5+ panels — does the standard `width_ratios=[2,1,1]
+ bottom-D` 4-panel rule generalise, or is it a 4-panel artefact?
R4.C: Haiku-class executor on R3.C deslop set — do small models actually
benefit from the blacklists where Opus 4.7 didn't?
