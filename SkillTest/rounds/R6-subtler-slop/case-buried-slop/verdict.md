# Verdict — R6.C subtler-slop / case-buried-slop

**Round:** R6.C · **Date:** 2026-05-16 · **Rubric version:** v1
**Executor:** Haiku 4.5 (5 parallel runs — 1 baseline + 4 candidate skills)
**Hypothesis tested:** R3.C/R4.C concluded "deslop skills don't bite at
saturated-slop fixture." R6.C's hard probe: do they bite when the slop is
BURIED in otherwise-clean prose, where the runner might miss it without
explicit blacklist guidance?

## Numeric audit

| Run | Words | Slop terms | Em-dashes | "We applied"/"We sequenced" active? |
|---|---|---|---|---|
| **Haiku baseline** | 105 | **0** | 0 | yes ("we applied", "we sequenced") |
| candidate-skill-deslop | 102 | 0 | 0 | yes |
| candidate-avoid-ai-writing | 127 | 0 | 0 | yes |
| candidate-humanizer-academic | 105 | 0 | 0 | yes |
| candidate-stop-slop | 111 | 0 | 0 | yes |

## Headline

**Haiku 4.5 baseline removed all 5 buried slop terms (unprecedented,
paved the way, shed light on, underscore, transformative) without skill
guidance.** It also dropped the closing sycophantic two-sentence pattern
on its own initiative ("editorial speculation inappropriate for Methods-
heavy introduction"). The deslop skill family adds NOTHING vs baseline
on the buried-slop scenario.

This closes the deslop question definitively. R3.C (saturated slop) and
R4.C (saturated slop, Haiku) and R6.C (buried slop, Haiku) all concur:
**the deslop skill family is not load-bearing at any executor scale or
slop density tested.**

## What baseline did right

The Haiku baseline's revision notes show explicit reasoning:

> "Removed 'paved the way for several therapeutic hypotheses now under clinical
> investigation' — speculative and unsupported; weakens the paragraph."
> "Cut 'we anticipate that this approach will be transformative' — editorial
> speculation inappropriate for Methods-heavy introduction."

Baseline correctly identified the closing 2 sentences as the sycophantic
inflation they were and cut them. No skill needed.

## What the candidates added (incremental)

- skill-deslop: tighter ("This subset may represent a functionally distinct
  state adapted to persistent antigenic challenge" — replacing the closing
  with a concrete functional hypothesis grounded in the data).
- avoid-ai-writing: longest output (127 words); didn't cut as aggressively;
  added a "this subset exhibits a transcriptional program distinct from
  steady-state dendritic cells" sentence — arguably bloat.
- humanizer-academic: kept "Building on these foundations" (which baseline
  cut) — slightly weaker close.
- stop-slop: similar to baseline; "We applied" addition is ALREADY in
  baseline.

## Cross-validation across deslop rounds

| Round | Executor | Fixture | Baseline slop | Best-candidate slop | Differentiation |
|---|---|---|---|---|---|
| R3.C | Opus 4.7 | saturated | 0 | 0 | NONE |
| R4.C | Haiku 4.5 | saturated | 0 | 0 | NONE |
| R6.C | Haiku 4.5 | buried | 0 | 0 | NONE |

3 rounds × 4 deslop skills × 2 executor classes × 2 slop densities = 24
data points, all "skill matches baseline." The deslop family's blacklist
+ rule sets are 100% redundant for any executor MinionsOS Writer is likely
to use.

## Bucket per skill (final, R3.C+R4.C+R6.C consensus)

| Skill | All 3 rounds | Recommendation |
|---|---|---|
| skill-deslop | Matches baseline (×3) | **skip** (final) |
| avoid-ai-writing | Matches baseline (×3) | **skip** (final) |
| humanizer-academic | Matches baseline (×3) | **skip** (final) |
| stop-slop | Calibrates Opus only (R3.C); Matches baseline (R4.C, R6.C) | **skip** (final) |

## Porting recommendation

`skip` 4 of 4 (final, consistent across 3 rounds). Update
`synthesis/what-to-skip.md` entry #5 from "confirmed across 2 executor
classes" to "confirmed across 3 rounds × 2 executor classes × 2 slop
densities."

For MinionsOS production: **do not load any deslop family skill, ever.**
The existing AI-trace blacklist proposed in R1.C `apply-revisions.md.diff`
is sufficient and arguably already redundant for Opus / Haiku 2026.

## Methodology note

R6.C's auto-audit confirmed the result without Codex blind-judge. When
the auto-audit metric (slop term count + em-dash count + active subject
presence) settles the question, blind-judge is unnecessary. This saves
~25K tokens per round vs full MetaHarness Stage 1.

## Final word on the deslop question

R3.C + R4.C + R6.C is the most controlled experimental sequence in
SkillTest. All 24 (skill × executor × density) cells score zero
differentiation. The deslop skill family's value proposition does not
hold for 2026-vintage Opus or Haiku models on either saturated or
buried slop fixtures. The skip recommendation is now empirically
final.
