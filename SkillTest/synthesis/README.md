# R1 Synthesis — Index

**Round:** R1 (R1.A nature-figure + R1.B scientific-figure-making + R1.C nature-polishing)
**Date:** 2026-05-16
**Cases tested:** 10 (3 + 3 + 4)
**Status:** Research-zone artefacts only. **Nothing in `proposed-skills/`
or `proposed-updates/` is applied to `/Users/mjm/MinionsOS/minions/roles/`
until the user explicitly approves.**

## Files in this directory

| File | Purpose |
|---|---|
| [`what-to-import.md`](what-to-import.md) | High-confidence ports (1 strong, 5 narrow) |
| [`what-to-fork.md`](what-to-fork.md) | Modify-before-import patterns (4 forks) |
| [`what-to-skip.md`](what-to-skip.md) | Tested and rejected patterns (6 entries) |
| `proposed-skills/cn-en-academic-polish.md` | New skill draft (R1.C) |
| `proposed-skills/figure-layout-defaults.md` | New skill draft (R1.A + R1.B) |
| `proposed-updates/academic-plotting.md.diff` | Update plan for existing skill (R1.A + R1.B) |
| `proposed-updates/abstract-writing.md.diff` | Update plan for existing skill (R1.C) |
| `proposed-updates/apply-revisions.md.diff` | Update plan for existing skill (R1.C) |
| `proposed-updates/aspect-note.md.diff` | Update plan for reviewer skill (R1.C, R2-confirmed) |
| `R3-synthesis.md` | R3 round summary |
| `R4-synthesis.md` | R4 hard-probe round summary |
| `R5-synthesis.md` | R5 pre-port validation summary |
| `R6-synthesis.md` | R6 hard-probe extension summary |
| `R-future-synthesis.md` | R-future aesthetic-exemplar paradigm validation |

## Headline numbers

| Round | Skill | Cases | Δ mean (rubric, /22) | Verdict |
|---|---|---|---|---|
| R1.A (revised) | nature-figure | 3 figure | 70% → 78% (+8 pp) | fork-narrowly |
| R1.B | scientific-figure-making | 3 figure | 70% → 76% (+6 pp) | fork-narrowly |
| R1.C | nature-polishing | 4 prose | 78% → 94% (+16 pp) | import-strongly |

## Cross-round findings

1. **Prose-discipline skills land cleanly; layout-discipline skills don't.**
   nature-polishing produced consistent gains across 4 cases. Both figure
   skills produced inconsistent gains (winning on heatmap, mixed on bar,
   *losing* on multi-panel). R1's clearest evidence is that figure-skill
   evaluation needs visual review — code-layer scoring alone gave a wildly
   wrong R1.A first-pass (47%→100%, revised to 70%→78%).
2. **Two skills tested for figures, both fail multi-panel layout.** Both
   nature-figure and scientific-figure-making nudge the runner away from
   the standard `width_ratios=[2,1,1] + bottom-spanning D` 4-panel hero
   pattern. Neither teaches it as the default. Both candidates produced
   layouts the user explicitly rejected on case-multi-panel.
3. **Content discipline is portable; layout discipline must be re-derived.**
   The rcParams + PALETTE + TwoSlopeNorm + outside-tick rules from both
   figure skills overlap and are safe to port. The mm-figsize and
   asymmetric-grid recipes are both rejected.
4. **The skill that "did less" sometimes did better.** scientific-figure-
   making's lighter rule set let the runner avoid the mm-cramming trap that
   nature-figure pushed on case-bar. "Less skill is more" applies when the
   skill's prescriptive layout rules contradict basic legibility.

## What changes for R2 / R3

Methodology updates to `SkillTest/README.md` (already applied):

- Visual inspection mandatory before scoring figure rounds.
- `constrained_layout collapsed to zero` is hard-fail, not cosmetic.
- Score by rendered artefact, not by code intent.
- Stage 0 SSL recall test should run before Stage 1 for any new skill
  whose discoverability is uncertain.

R2 candidates (queued):
- `nature-response` — rebuttal letters (test will draw on
  `proposed-updates/aspect-note.md.diff` rule)
- `nature-citation` — Nature/Science/Cell citation retrieval and export
- `nature-data` — Data Availability statements + FAIR checks
- `research-paper-writing` (ML/CV-leaning) — comparison against R1.C
  abstract / introduction findings
- `deslop` / `humanizer-academic` family — AI-trace removal at scale
  (will probably overlap with the partial-skip from R1.C)

R3 deferred candidates (skipped or low-priority): `academic-paper`
(12-agent pipeline; violates "skill should guide, not lock workflow"),
`nature-paper2ppt` (lower priority for CNS writing focus).

## Decision required from user

Before R2 starts, please confirm or revise these R1 conclusions:

1. **Port the prose-discipline rules** (cn-en-academic-polish skill,
   abstract-writing + apply-revisions + aspect-note updates) into
   MinionsOS Writer / Reviewer skills?
2. **Port the figure content-discipline rules** (academic-plotting
   update with rcParams + PALETTE + TwoSlopeNorm + outside ticks)?
3. **Port the figure layout default skill** (figure-layout-defaults
   with `width_ratios=[2,1,1] + bottom D` as 4-panel default)?
4. **Confirm R2 scope** — start with `nature-response` (highest
   complement to R1.C findings), or pick a different R2 candidate?

The drafts in `proposed-skills/` and `proposed-updates/` are concrete
proposals; the user can edit any of them before approving the port.
