# Round Notes — R4.C Haiku-class deslop A/B

**Cases:** case-saturated-slop (1 fixture × 4 candidates + baseline, all on Haiku 4.5)
**Date:** 2026-05-16
**Methodology:** skill-evaluator-by-metaharness Stage 1 (parallel sub-agents,
auto-audit; Codex blind-judge skipped because audit was conclusive).

## Headline

**Haiku-class baseline scored 0 slop terms / 1 em-dash / 96 words.**
Same shape as Opus 4.7 R3.C baseline. The deslop skill family does not
bite at executor-class scale either.

## Cross-validation summary

| Skill | Opus R3.C | Haiku R4.C | Final |
|---|---|---|---|
| skill-deslop | Matches | Matches | skip |
| avoid-ai-writing | Matches | Matches | skip |
| humanizer-academic | Matches | Matches | skip |
| stop-slop | Calibrates Opus (active subject) | Matches Haiku | skip |

Both executor classes (Opus 4.7 + Haiku 4.5) handle the saturated-slop
fixture cleanly without skill loading. The R1.C prediction (synthesis/
what-to-skip.md entry #5) is now confirmed across 2 independent executor
classes.

## What this round closed

The argument "small models benefit from blacklists where large models
don't" is **falsified for Haiku 4.5**. The deslop family is not load-
bearing for any executor class MinionsOS Writer is likely to use
(Opus / Sonnet / Haiku-4.5).

A future R5+ round could test:
- Subtler-slop fixtures where AI-traces are buried in otherwise-clean prose
- Smaller local models (8B-class on a CPU runtime)
- Shorter context windows where the skill text could compete with the
  task prose

For MinionsOS production purposes, R4.C closes the question.

## Token economics

- 5 parallel Haiku sub-agents, ~30K tokens each = ~150K total
- Auto-audit (no Codex blind-judge needed): saved ~17K tokens that would
  have gone to per-pair Codex blind-judge calls
- Total round cost ~150K tokens — much less than R1+R2+R3 figure rounds

## Recommendation

`skip` all 4 deslop skills. Update `synthesis/what-to-skip.md` entry #5
from "tentative prediction" to "confirmed across 2 executor classes
(Opus 4.7 + Haiku 4.5)."

No port plan changes from R1+R2+R3. The R1.C `apply-revisions.md.diff`
already includes a small AI-trace blacklist for redundancy / insurance;
that's enough.

## What R4 has now confirmed

R4.A: nature-response AUTHOR_INPUT_NEEDED branch works.
R4.B: 5-panel layout — pending user visual review (figure round).
R4.C: deslop skip prediction confirmed at Haiku class.

R4 is closing. R5 candidates remain in `synthesis/R3-synthesis.md` open
questions section.
