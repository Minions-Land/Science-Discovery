# Round Notes — R3.C deslop-comparison

**Cases:** case-saturated-slop (1 fixture × 4 candidates + 1 baseline)
**Date:** 2026-05-16
**Candidate skills (4):**
- skill-deslop (`/Users/mjm/Skill/Awesome-Agent-Skills.../45-stephenturner-skill-deslop/`)
- avoid-ai-writing (`/Users/mjm/Skill/Awesome-Agent-Skills.../47-conorbronsdon-avoid-ai-writing/`)
- humanizer-academic (`/Users/mjm/Skill/Awesome-Agent-Skills.../44-matsuikentaro1-humanizer_academic/`)
- stop-slop (`/Users/mjm/Skill/Awesome-Agent-Skills.../46-hardikpandya-stop-slop/`)

## Headline

**5 polished outputs (1 baseline + 4 candidates) all score 0 slop terms,
0 em-dashes, words within 77-95.** Opus 4.7 (May 2026) handles the
saturated-slop fixture as cleanly as the candidates. The R1.C prediction
that AI-trace blacklists are insurance-not-transformative is empirically
confirmed.

## Per-skill bucket

| Skill | Bucket | Recommendation |
|---|---|---|
| skill-deslop | Matches baseline | skip |
| avoid-ai-writing | Matches baseline | skip |
| humanizer-academic | Matches baseline | skip |
| stop-slop | Calibrates response (active-subject rule, +1 pt) | fork-narrowly |

## What the round taught

1. **Big-vocabulary blacklists are load-bearing only for older / smaller
   models.** Opus 4.7 already internalises every entry in the union of
   these 4 skills' blacklists. Loading any of them adds 130-504 lines of
   context for output that is byte-equivalent to baseline.
2. **Active-voice / human-subject rule is the one outlier.** stop-slop's
   "Researchers use attention mechanisms..." vs baseline's "Attention
   mechanisms are central..." is the single content-level differentiator.
   Marginal but real.
3. **Skill-load cost is not justified by skill effect on this dimension.**
   For MinionsOS Writer (Opus / Sonnet class), sentence-level deslop is
   handled internally; no port needed.
4. **For Haiku-class subagents, the picture might differ.** A future
   round (R4?) could re-test these 4 skills on Haiku to see if the
   blacklists genuinely bite for smaller models.

## Token economics

5 runs × 1 fixture each. Per-skill input premium:
- skill-deslop: ~7x baseline
- avoid-ai-writing: ~14x baseline (huge SKILL.md)
- humanizer-academic: ~15x baseline (heaviest)
- stop-slop: ~3x baseline (lightest)

Output similar across all 5 (90-95 words, except stop-slop 77).

The cost-effectiveness ratio is worst for the heaviest skills
(humanizer-academic, avoid-ai-writing) which produce zero differentiation
from baseline. stop-slop's lightness + marginal active-subject win
makes it the best of a weak set.

## Recommendation

`skip` 3 of 4. `fork-narrowly` for stop-slop's active-subject rule
only — and even that is marginal. Update
`synthesis/what-to-skip.md` entry #5 to upgrade from prediction to
confirmed.

For MinionsOS Writer port plan: do nothing on the deslop family.
The existing `apply-revisions.md` AI-trace blacklist (proposed in R1.C)
is sufficient.

## What to test next

R3 is closing. Open questions for future rounds:

- Do these blacklist skills bite on Haiku-class subagents? Test with
  MetaHarness-style A/B pairs (haiku × 2 + codex blind judge) per the
  skill-evaluator-by-metaharness protocol.
- Are there OTHER non-blacklist AI-trace patterns worth testing?
  (Hedging frequency, cliche metaphor detection, repetitive structure
  detection.) Could be R4 fixtures.
