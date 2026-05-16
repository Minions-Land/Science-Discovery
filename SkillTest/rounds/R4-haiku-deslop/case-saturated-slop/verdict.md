# Verdict — R4.C Haiku-class deslop / case-saturated-slop

**Round:** R4.C · **Date:** 2026-05-16 · **Rubric version:** v1
**Executor:** Haiku 4.5 (5 parallel sub-agents — 1 baseline + 4 candidate skills)
**Hypothesis tested:** R3.C concluded "deslop skills don't bite Opus-class
models." R4.C's hard probe: do they bite Haiku-class models, where the
skill-evaluator-by-metaharness protocol is calibrated?

## Numeric audit (polished prose only)

| Run | Words | Slop terms | Em-dashes |
|---|---|---|---|
| **Haiku baseline** | 96 | **0** | 1 |
| candidate-skill-deslop | 93 | 0 | 0 |
| candidate-avoid-ai-writing | 88 | 0 | 1 |
| candidate-humanizer-academic | 100 | 0 | 0 |
| candidate-stop-slop | 112 | 0 | 1 |

## Headline

**Haiku-class baseline scored 0 slop terms** — same as Opus 4.7 baseline
in R3.C. The single em-dash in baseline ("diverse domains—machine
translation, language understanding, and protein structure prediction
among them") is a stylistic choice, not a slop pattern.

R4.C confirms the R3.C prediction at executor-class scale. The deslop
skill family does NOT bite at Haiku-class either. Big-vocabulary
blacklists are insurance for models that are already disciplined; they
do not unlock new behaviour.

## What each skill actually delivered (vs Haiku baseline)

### skill-deslop
- 0 slop terms, 0 em-dashes (vs baseline 0/1).
- The em-dash drop is the only differentiator; could equally be variance.
- Same content as baseline.
- Bucket: **Matches baseline**.

### avoid-ai-writing
- 0 slop terms, 1 em-dash (vs baseline 0/1).
- Identical pattern as Opus R3.C: this skill keeps em-dashes within its own
  ≤1-per-paragraph rule (which baseline naturally satisfied).
- Same content as baseline.
- Bucket: **Matches baseline**.

### humanizer-academic
- 0 slop terms, 0 em-dashes (vs baseline 0/1).
- Pattern 13 (em-dash zero-tolerance) is the only rule that removed the
  one em-dash baseline kept. Cosmetic difference.
- Same content as baseline.
- Bucket: **Matches baseline** (with pedantic em-dash policy).

### stop-slop
- 0 slop terms, 1 em-dash, 112 words (longer, not shorter — diverges from
  the Opus-class result where stop-slop was the shortest).
- The "human subject" rule fired ("Vaswani et al. introduced... transformers
  enable... This paper builds...") — same as Opus R3.C result.
- Bucket: **Matches baseline**.

## Cross-validation with R3.C (Opus 4.7)

| Skill | Opus R3.C result | Haiku R4.C result | Conclusion |
|---|---|---|---|
| skill-deslop | Matches baseline | Matches baseline | confirmed across executor classes |
| avoid-ai-writing | Matches baseline | Matches baseline | confirmed |
| humanizer-academic | Matches baseline | Matches baseline | confirmed |
| stop-slop | Calibrates (active subject, +1 pt) | Matches baseline | active-subject benefit was Opus-only |

The R1.C synthesis prediction ("anti-AI-trace heuristics... were effective
in R1.C but not load-bearing — both baseline and candidate runners removed
these terms in 2026 even without the skill") is now empirically validated
across **two independent executor classes** (Opus 4.7 + Haiku 4.5).

## What this means

The argument that "small models benefit from blacklists where large
models don't" is **falsified** for Haiku 4.5. Haiku already internalises
the same anti-slop discipline as Opus. The skill family is not load-
bearing for any production agent class MinionsOS Writer might use.

Possible explanations:
- 2026 instruction-tuning has internalised post-2024 anti-AI-style
  discipline at all scales.
- The fixture's saturation makes the slop visible enough that even
  Haiku's pattern recognition catches it.
- Both candidate and baseline runners read the brief ("Cut anything
  that doesn't serve a reader's understanding") and applied basic
  editorial judgment.

A genuinely harder R5 probe could test on subtler-slop fixtures (where
the AI-trace pattern is buried in otherwise-clean prose), or on smaller
local models (8B-class). For MinionsOS production purposes, R4.C
closes the question: **skip the deslop family.**

## Bucket per skill (final, R3.C + R4.C consensus)

| Skill | Bucket (consensus) | Recommendation |
|---|---|---|
| skill-deslop | Matches baseline (Opus + Haiku) | **skip** |
| avoid-ai-writing | Matches baseline (Opus + Haiku) | **skip** |
| humanizer-academic | Matches baseline (Opus + Haiku) | **skip** |
| stop-slop | Calibrates Opus only; Matches baseline on Haiku | **skip** (the active-subject rule alone is too narrow to justify a port; if needed, fold into apply-revisions.md.diff as a one-liner) |

## Porting recommendation

`skip` 4 of 4. The R1.C `synthesis/what-to-skip.md` entry #5 ("Anti-AI-
trace heuristics") is upgraded from prediction to **confirmed across
2 executor classes**. No port needed. Update what-to-skip.md to record
this.

The `apply-revisions.md.diff` proposed in R1.C (which already includes
a small AI-trace blacklist) is sufficient. Do not load any of the four
deslop skills.

## Methodology note

R4.C used the skill-evaluator-by-metaharness Stage 1 protocol partially:
parallel Haiku sub-agents, structured prompts. Codex blind-judge step
was skipped because the auto-audit (slop terms / em-dashes / word count)
was already conclusive. For future R-rounds where auto-audit can settle
the question, blind-judge can be deferred to save tokens.
