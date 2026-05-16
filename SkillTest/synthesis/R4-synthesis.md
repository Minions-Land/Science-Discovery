# R4 Synthesis (Hard-Probe Round)

**Round:** R4 (R4.A minor-revision rebuttal + R4.B 5-panel figure + R4.C Haiku-class deslop)
**Date:** 2026-05-16
**Status:** Research-zone artefacts only. Nothing in `proposed-skills/` or
`proposed-updates/` is applied to MinionsOS until the user explicitly approves.

## Summary

R4 is the hard-probe round: each sub-round explicitly tries to break a
prediction or extend a finding from R1-R3.

| Sub-round | Skill | Hypothesis tested | Result |
|---|---|---|---|
| R4.A | nature-response | AUTHOR_INPUT_NEEDED branch of action FSM works on under-specified author position | **CONFIRMED** + 2 new port elements (top-of-letter flag, PI question list) |
| R4.B | nature-figure + scientific-figure-making | 4-panel asymmetric-grid failure is 4-panel-specific or generalises | **GENERALISES** — same failure at 5 panels; figure-layout-defaults extended with 5-panel default |
| R4.C | 4 deslop skills (Haiku class) | Small models benefit from blacklists where Opus 4.7 didn't | **FALSIFIED** — Haiku 4.5 baseline as clean as Opus baseline; skip 4 of 4 |

## Three load-bearing R4 findings

### 1. nature-response covers AUTHOR_INPUT_NEEDED + 2 new rules

R4.A confirmed candidate emits `AUTHOR_INPUT_NEEDED` correctly when 2 of
4 reviewer comments lack author position. Two skill-specific wins
discovered:

- **Top-of-letter flag** — candidate names unresolved comments in the
  opening paragraph of the response letter (visible to editor on first
  read). Baseline buries this.
- **PI question list** — candidate emits a separate section with 6
  specific questions the corresponding author can paste into an email
  to the PI. Baseline gives status updates only.

Update R2 port plan: add these two elements to the proposed
`prepare-rebuttal.md` update.

The full nature-response action FSM is now empirically exercised across
R2 + R4.A: ACCEPT_TEXT, ACCEPT_ANALYSIS, ACCEPT_EXPERIMENT, ACCEPT_FIGURE,
ADD_CITATION, PARTIAL, SOFTEN_CLAIM, DISAGREE_WITH_JUSTIFICATION,
AUTHOR_INPUT_NEEDED, plus composite labels. No FSM branch untested.

### 2. Figure asymmetric-grid failure is structural, not 4-panel-specific

R4.B confirmed both nature-figure and scientific-figure-making produce
worse 5-panel layouts than baseline matplotlib-default. The 5-panel
baseline used `gridspec(3, 3)` with `ax_a=gs[0:2,0:2]`; user called
this "无敌好看且非常准确" — same pattern as 4-panel `[2,1,1]+bottom-D`.

**The figure-layout-defaults skill (SkillTest-authored) is now
extended:**
- 4-panel default: `gridspec(2, 3, width_ratios=[2,1,1], height_ratios=[1.4, 1])`
- 5-panel default: `gridspec(3, 3)` with hero=`gs[0:2, 0:2]`
- 6+ panel principle: 4-cell hero + contiguous subordinate remainder, no
  empty cells, no over-stretching

Both skills' content discipline (rcParams, PALETTE, TwoSlopeNorm,
outside ticks) is still portable. Both skills' multi-panel layout
patterns remain rejected.

### 3. Deslop skills definitively skipped (2-executor-class confirmation)

R4.C ran the same fixture as R3.C on Haiku 4.5 (instead of Opus 4.7).
All 5 outputs (1 baseline + 4 candidates) scored 0 slop terms. The
"smaller models benefit from blacklists" hypothesis is falsified.

R1.C `synthesis/what-to-skip.md` entry #5 is upgraded from prediction
to confirmed across 2 executor classes (Opus 4.7 + Haiku 4.5).

## What R4 did NOT change

- R3.A nature-data: still import-strongly. R4 didn't re-test it.
- R3.B nature-citation: still fork-narrowly. R4 didn't extend it.
- R1.C nature-polishing: still import-strongly. R4 didn't re-test it.
- R1.A / R1.B figure content discipline: still fork-narrowly portable.

## What R5+ could test

R3-synthesis.md "what to test next" section listed candidates that R4
addressed only partially:

- ✓ **Hard-probe rebuttal** (R4.A done — AUTHOR_INPUT_NEEDED branch)
- ✓ **5-panel figure** (R4.B done — asymmetric grid still fails)
- ✓ **Haiku-class deslop** (R4.C done — skip confirmed at scale)
- ✗ Real-network nature-citation (skipped — Codex sandbox no Crossref)
- ✗ End-to-end multi-skill (deferred to R5)

R5 candidates:

1. **End-to-end paper writing**: combine ported skills (nature-polishing
   + nature-figure rcParams + nature-data + nature-response) on a single
   fixture; test cross-skill orchestration; check for skill-discovery
   conflicts.
2. **6-panel and 7-panel figures**: extend the figure-layout-defaults
   skill to higher panel counts; verify the "designate 4-cell hero +
   contiguous remainder" generalisation.
3. **Subtler-slop fixtures**: AI-trace patterns buried in otherwise-clean
   prose. Could the deslop family bite on harder cases? (Probably not,
   but worth one round before final close.)
4. **Stage 0 SSL recall test for the 5 proposed skills**: before the
   user lands ports, verify that each proposed skill's `description`
   makes it discoverable from MinionsOS Writer's full library at the
   right moment. Per skill-evaluator-by-metaharness protocol.

## Decision required from user

R4 doesn't change the R1+R2+R3 port plan substantively; it adds:
- 2 new rules to the R2 nature-response port (top-of-letter flag, PI
  question list)
- 5-panel default to the figure-layout-defaults skill
- Final closure on deslop family (skip)

R4 confirms the existing port plan is sound. The drafts in `proposed-
skills/` and `proposed-updates/` are ready when the user wants to
land them.

Recommended next move:
- Either: land R1+R2+R3+R4 ports together (single coherent push), OR
- Run R5 (end-to-end multi-skill orchestration) before landing, to
  catch cross-skill conflicts.

The R5 cost is one round (~30 min); the value is catching skill-
discovery / SSL-recall conflicts before MinionsOS production. Worth it
unless the user wants to ship now.
