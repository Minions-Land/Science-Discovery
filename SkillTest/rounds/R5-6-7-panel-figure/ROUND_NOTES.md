# Round Notes — R5.C 6/7-panel figure (layout default extension)

**Cases:** case-6panel, case-7panel
**Date:** 2026-05-16
**Candidate skill:** `figure-layout-defaults.md` (SkillTest-authored,
                     distilled from R1.A + R1.B + R4.B negative evidence)

## Headline

**6-panel: Matches baseline (skill inert at this panel count).**
**7-panel: Calibrates / lower-Prevents (+10, user grades candidate
80-90/100 vs baseline 60/100).**

R5.C 7-panel is the first SkillTest figure round where a candidate skill
cleanly beats baseline on the rendered artefact (user-confirmed visual
review). The figure-layout-defaults skill is now empirically positive,
not just defensively negative.

## Cross-validation across all figure rounds

| Panel count | Tested skills | Best result |
|---|---|---|
| 1 (single) | nature-figure, scientific-figure-making | Calibrates (heatmap), Overreaches partial (bar at tight figsize) |
| 4 | nature-figure, scientific-figure-making | Overreaches (both) |
| 5 | nature-figure, scientific-figure-making | Overreaches (both) |
| 6 | figure-layout-defaults | Matches baseline (Codex finds the right grid naturally) |
| **7** | **figure-layout-defaults** | **Calibrates (+10, clean visual win)** |

The skill's value scales with panel count COMPLEXITY, not panel count
linearly. At 4 and 5 panels existing third-party skills fail because
they push the runner away from the natural good grid. At 6 panels Codex
finds the natural good grid without help. At 7 panels Codex needs the
skill's explicit "designate 4-cell hero + contiguous remainder + no
over-stretching" rules to avoid forcing G into a too-small bottom slot.

## What R5.C closes

The figure-layout-defaults skill (SkillTest-authored from R1 + R4
evidence) is now upgraded:

- R1+R4 evidence: defensive negative — port to fix nature-figure and
  scientific-figure-making's bad multi-panel patterns.
- R5.C 7-panel evidence: positive empirical — the skill's rules
  genuinely produce a better-rendered artefact than naive baseline.

Port recommendation: **import-strongly** (was fork-narrowly).

## What R5.C did NOT change

- R5.C 6-panel showed the skill is INERT at that count (Codex naive
  default IS the skill's recommendation). Not a problem; just note that
  the skill saves work mostly at 4/5/7+ panels, not at 6.
- The skill's content discipline (rcParams, palette, editable text) is
  unchanged from R1.A/R1.B/R4.B verdicts.

## Token economics

6-panel: ~9000 input tokens for skill load (figure-layout-defaults ~9 KB).
7-panel: same.
Outputs similar length to baseline. Skill premium is paid once when the
runner reads the skill; per-figure marginal cost is unchanged.

For MinionsOS Writer: load this skill at wake-up; it costs ~9K tokens
of context once, saves submission-blocker level layout failures on 4/5/7+
panel composites.

## What R5 has now confirmed end-to-end

- **R5.A** end-to-end multi-skill: 6 skills loaded simultaneously, no
  conflicts, no redundancy, substantively-bounded specificity applied
  consistently across 4 sections.
- **R5.B** SSL recall: 2/2 PROPOSED skills (cn-en-academic-polish,
  figure-layout-defaults) correctly recalled at top-3. Plus a real gap
  found: data-availability-statement skill is missing — 4 distractor
  skills picked instead — confirms the R3.A finding that this needs
  authoring before the port.
- **R5.C** layout extension: 7-panel positive empirical win for figure-
  layout-defaults (clean +10).

R5 closes. SkillTest project R1+R2+R3+R4+R5 = 5 rounds × 18 sub-rounds
× 14 cases. Port plan is mature.

## Open questions for R6+

The "designate 4-cell hero + contiguous remainder" rule was tested up to
7 panels. Beyond 7 panels (8+ panel composites) is plausibly within scope
for very dense Nature Methods / Cell Reports submissions; the rule may
need extension. Could be R6 if the user wants to push further; otherwise
the skill is mature for typical CNS submission load (≤7 panels).

The data-availability-statement skill is the one remaining "todo" — R3.A
showed it should exist and R5.B confirmed it's not surface-able from
existing skill descriptions. To be authored after the user approves
R1+R2+R3+R4+R5 ports.
