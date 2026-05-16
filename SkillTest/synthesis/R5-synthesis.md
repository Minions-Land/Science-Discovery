# R5 Synthesis (Pre-Port Validation Round)

**Round:** R5 (R5.A end-to-end + R5.B SSL recall + R5.C 6/7-panel figure)
**Date:** 2026-05-16
**Status:** Research-zone artefacts. Nothing in `proposed-skills/` or
`proposed-updates/` is applied to MinionsOS until the user explicitly
approves. R5 is the last validation round before the user-decision gate
on landing R1+R2+R3+R4 ports.

## Summary

| Sub-round | Tested | Result |
|---|---|---|
| R5.A | Multi-skill orchestration (6 skills × 4 sections) | **No conflicts, no redundancy, anchor rule consistent across sections** |
| R5.B | Stage 0 SSL recall for 2 PROPOSED skills | **2/2 PASS** + 1 expected-FAIL exposing data-availability gap |
| R5.C | figure-layout-defaults at 6 + 7 panels | **6-panel: Matches baseline (skill inert) · 7-panel: Calibrates +10 (FIRST clean win for any tested figure skill)** |

## Three load-bearing R5 findings

### 1. Multi-skill loading is safe

R5.A loaded 6 skills simultaneously into Codex context and ran them
against a 4-section mini-paper fixture (abstract / discussion / data
availability / rebuttal). Each skill applied to its right section; no
section-mismatch errors; no redundant rule application; cross-section
terminology stable. **The R1+R2+R3+R4 port plan does not produce skill
collisions in practice.**

### 2. PROPOSED skill descriptions are discoverable

R5.B Stage 0 test showed both authored PROPOSED skills surface at
top-3 for their target scenarios. cn-en-academic-polish ranks #1
for the Chinese-influenced polish probe; figure-layout-defaults ranks
#2 for the 4-panel figure probe (academic-plotting picked up #1, also
acceptable). **The descriptions don't need rewriting.**

The expected failure on P4 (data availability) confirmed R3.A: a new
`data-availability-statement.md` skill needs authoring before the port,
because no existing skill fills this slot.

### 3. figure-layout-defaults is now empirically positive

R5.C 7-panel test produced the first clean win for any candidate figure
skill in SkillTest history. User: "candidate 无论是从颜色还是排版上，都
完全胜过了 baseline ... 几乎完美." Score: 22/22 vs 12/22 (+10 points).

The skill was originally drafted in R1 synthesis as a defensive patch
against nature-figure / scientific-figure-making's multi-panel failure
mode. R5.C 7-panel confirms it as positive empirical: when the runner
needs to solve hierarchy + grid simultaneously at high panel counts,
the skill's "designate 4-cell hero + contiguous remainder + no over-
stretching" rules genuinely produce a better artefact.

Port priority for figure-layout-defaults: **upgraded from fork-narrowly
to import-strongly**.

## Cross-skill anchor rule, now confirmed across 5 fixtures

> **Substantively-bounded specificity, not vague good-faith promises.**

| Round | Fixture | Manifestation |
|---|---|---|
| R1.C | overclaim Discussion | "did not include transfer experiments" beats "observational design cannot establish causation" |
| R2 | mixed-severity rebuttal | `[X]` placeholder beats inventing `page 12, lines 310-324` |
| R3.A | data-availability with mixed restrictions | named DAC + 4 review conditions beats "available upon reasonable request" |
| R3.B | citation candidates with no network | `[needs verification]` placeholder beats fabricated DOIs |
| **R5.A** | **end-to-end mini-paper** | **all 4 sections honour the rule simultaneously** |

This is the highest-confidence portable principle from SkillTest. It
should land at the MinionsOS common contract level (`minions/roles/SYSTEM.md`
evidence-first section), not buried inside any single skill.

## What R5 unblocks

The full R1+R2+R3+R4 port plan is now validated across:

- Behavioural A/B (R1+R2+R3+R4 individual rounds)
- Multi-skill orchestration (R5.A)
- Skill discoverability (R5.B)
- Empirical positive figure-layout-defaults result (R5.C 7-panel)

**The user can now land the port with high confidence.** The plan:

| Skill | Port Action | Source |
|---|---|---|
| nature-polishing rules | Merge into existing `abstract-writing.md` + `apply-revisions.md` (R1.C diffs) | R1.C |
| nature-response rules | Merge into existing `prepare-rebuttal.md` (R2 + R4.A diffs) | R2 + R4.A |
| nature-data rules | New skill `data-availability-statement.md` | R3.A |
| nature-figure / scientific-figure-making content rules | Merge into `academic-plotting.md` (R1+R4 diff) | R1.A + R1.B + R4.B |
| **NEW**: cn-en-academic-polish | New skill | R1.C |
| **NEW**: figure-layout-defaults | New skill | R1+R4+R5.C |
| **ELEVATE**: substantively-bounded specificity | Add to common contract / `roles/SYSTEM.md` evidence-first section | R1.C+R2+R3.A+R3.B+R5.A |
| deslop family | Skip (R3.C+R4.C: confirmed not needed at any executor class) | R3.C+R4.C |

## What R5 did NOT need to test

- Real-network nature-citation: deferred (Codex sandbox no Crossref).
- 8+ panel figure: extension; can be R6 if needed.
- Subtler-slop fixtures: extension; deslop family already SKIP-confirmed.

## R5+ open questions

- **Author data-availability-statement.md** before final port. Should
  draft from R3.A rules; R5.B confirms it has a real discoverability
  gap.
- **Re-run R5.B** with the new data-availability skill to confirm P4
  routes to it correctly.
- **R6+** could test 8+ panel composites if MinionsOS needs them.

## Recommendation

Land the R1-R5 port plan. The 5 rounds + 18 sub-rounds + 14 cases of
evidence are mature. The user has reviewed every figure visually and
every prose section structurally. No further validation is required
unless the user wants to extend coverage to genuinely new domains
(e.g. statistics / methods writing / figure narration in supplementary).
