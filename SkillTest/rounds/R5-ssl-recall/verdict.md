# Verdict — R5.B SSL recall test

**Round:** R5.B · **Date:** 2026-05-16
**Method:** Stage 0 SSL recall per skill-evaluator-by-metaharness protocol.
4 probes × 35 candidate skills (33 existing MinionsOS + 2 PROPOSED).

## Per-probe result

| Probe | Top-3 picked by Haiku-router | Expected | Status |
|---|---|---|---|
| P1 cn-en polish | cn-en-academic-polish, abstract-writing, apply-revisions | cn-en-academic-polish at top-3 | **PASS** rank 1 |
| P2 figure layout | academic-plotting, figure-layout-defaults, interactive-figure-prototype | figure-layout-defaults at top-3 | **PASS** rank 2 |
| P3 rebuttal author input | prepare-rebuttal, think-then-act, unstated-premises | prepare-rebuttal at top-3 | **PASS** rank 1 |
| P4 data availability | citation-audit, paper-literature-search, package-submission | data-availability-statement (UNAUTHORED) at top-3 | **FAIL** — no skill picked correctly |

## Headline

**2/2 authored PROPOSED skills (cn-en-academic-polish, figure-layout-defaults)
are surface-able at top-3.** Their `description` fields are sufficient for
the skill router to find them at the right moment. No description rewrite
needed.

**1 unauthored gap exposed**: P4 data-availability scenario found no good
match in the existing 33-skill library. The Haiku router picked
citation-audit (verifies citations not data), paper-literature-search
(searches papers not data), and package-submission (final bundle) — none
fit. This is exactly what R3.A predicted: MinionsOS Writer needs a
dedicated data-availability-statement skill before the port can land.

## What this confirms

1. **The 2 PROPOSED skill descriptions don't need editing.** Both have
   keyword density that Haiku catches: "Chinese-influenced English",
   "hourglass introduction", "AI-trace blacklist" for cn-en-polish;
   "4-panel hero", "width_ratios", "no empty quadrants",
   "constrained_layout collapse" for figure-layout-defaults.
2. **The proposed skill set is incomplete.** Without data-availability-
   statement.md, queries about Data Availability statement writing get
   misrouted to citation/literature/submission skills. R3.A's port plan
   gap is now empirically verified at the discovery layer.
3. **Stage 0 protocol works.** Running this AFTER each new skill is
   authored (vs guessing whether descriptions are good) saves
   "loaded-but-never-used" failure mode that the original
   skill-evaluator-by-metaharness skill warns about.

## Distractor analysis

The 4-probe set was small but adversarial: each probe scenario was
specific enough to map to a few keyword matches (Nature, "delve",
"reasonable request", "PI travelling"), and the candidate library
included 33 distractors plus the targets. The router's accuracy
(2-3/3 hit on 3 of 4 probes) is reasonable for a single-shot ranking
task.

## Porting recommendation

1. The 2 PROPOSED skills are ready for SSL-recall-tested port.
2. Author `data-availability-statement.md` before the port (R3.A drafted
   the rules; just needs the SKILL.md frontmatter + structure).
3. Re-run R5.B after authoring the new skill to verify it surfaces at
   top-3 for P4-equivalent probes.

## Token economics

5 Haiku calls (1 per probe + 1 spare for any rerun) × ~30K tokens each
= ~150K tokens. Cheap compared to the figure rounds.

## Bucket

N/A — this is a Stage 0 test, not a Stage 1 behavioural A/B. Result is
recorded as **3 PASS / 1 expected-FAIL**: the failure was the test's
purpose (confirm a missing skill).

## What R5.B unblocks

Together with R5.A, R5.B is the last pre-port verification. The R1+R2+R3+R4
port plan is now:
- Validated for skill discoverability (R5.B)
- Validated for multi-skill orchestration (R5.A)
- Validated for figure-layout-defaults positive empirical win (R5.C 7-panel)

The 5 promoted skills are ready to land:
- cn-en-academic-polish (R1.C+R5.A+R5.B)
- figure-layout-defaults (R1+R4+R5.A+R5.B+R5.C)
- nature-polishing rules merged into abstract-writing.md / apply-revisions.md
- nature-response rules merged into prepare-rebuttal.md
- nature-data rules into a NEW data-availability-statement.md

Plus the cross-skill anchor rule (substantively-bounded specificity) into
common contract.
