# Round Notes — R1.C nature-polishing

**Cases:** case-results, case-intro-zh, case-overclaim, case-abstract
**Date:** 2026-05-16
**Candidate skill:** `/Users/mjm/Skill/nature-skills-main/skills/nature-polishing/`
**Methodology:** Stage 1 only (single skill, hand-loaded). Codex generated
both baseline and candidate prose for 4 fixtures; main thread scored against
the rubric. Unlike R1.A, no rendering step — text is the artefact, side-by-side
read is the visual inspection.

## Aggregate scores

| Case | Baseline / 22 | Candidate / 22 | Δ | Bucket |
|---|---|---|---|---|
| case-results | 18 / 22 | 20 / 22 | +2 | Calibrates response |
| case-intro-zh | 16 / 22 | 21 / 22 | +5 | Prevents real failure |
| case-overclaim | 17 / 22 | 21 / 22 | +4 | Calibrates response |
| case-abstract | 18 / 22 | 21 / 22 | +3 | Calibrates response |
| **Mean (normalised /22)** | **78%** | **94%** | **+16 pp** |

Compared to R1.A's revised +8 pp, R1.C lands a stronger and more consistent
gain. The skill's prose discipline holds up where the figure skill's layout
discipline didn't.

## Where the candidate consistently beat baseline

1. **Paper-type diagnosis as a first move.** Every candidate output appended
   an explicit "Diagnosed paper type / failure mode" block. This isn't fluff
   — it's the skill's first rule ("identify the paper type before editing")
   emitted as evidence, and it shows up in editing decisions: case-results
   stayed in Results-tense discipline; case-intro-zh applied Chinese-to-English
   reconstruction; case-overclaim explicitly named claim-without-evidence as the
   failure; case-abstract called out method-detail crowding.
2. **Boundary specificity in Discussion-class prose.** case-overclaim is the
   sharpest example. Baseline says "do not support a clinical recommendation";
   candidate names the specific missing experiment ("did not include transfer
   experiments"). Reviewer-proof.
3. **Refusal to fabricate quantification.** case-intro-zh's source claim
   "substantial improvements over baselines" had no numbers. Baseline silently
   re-asserted "outperforms existing baselines." Candidate flagged "the size of
   these gains should be reported in the Results" — refused the lazy fabrication.
4. **Formal anchors at venue-required positions.** case-abstract's "Here, we
   show" is essentially a Nature-family abstract convention. Baseline used a
   narrative verb; candidate used the formula.
5. **Hourglass restructure on Chinese-influenced prose.** case-intro-zh:
   baseline preserved the original Chinese draft order; candidate flipped to
   gap-first → consequence → "Here, we" — load-bearing for Chinese-author labs
   targeting CNS journals.

## Where the candidate didn't help (or hurt)

1. **Verbosity.** Candidate prose is systematically 25–50% longer than
   baseline (case-overclaim 175 vs 130 words; case-abstract 196 vs 146).
   For Discussion paragraphs the boundary detail is worth it; for tight
   abstracts (200-word limit) the candidate flirts with the cap.
2. **Diagnosis footer adds output bloat.** Useful as evidence the skill
   loaded, less useful as final manuscript prose. Skill should let the runner
   suppress it for production output.
3. **No-or-minimal AI-trace difference.** Baseline runner already removed
   crucial / delve into / important to note / substantial. Em-dash count was
   0 in both. The skill's anti-AI rules are a "you'd already get this in 2026
   from any competent academic editor" — they're insurance, not transformative.

## Token economics

Same shape as R1.A: candidate input ~10× baseline because the SKILL.md is
~10 KB. Output ~25–35% longer for the diagnosis + revision-notes footer.
Production cost: paid once at Writer wake-up if the skill lives in
`minions/roles/writer/skills/`, then per-paragraph marginal is identical.

## Recommendation

`import-strongly`. Three independent components are portable wins, and
together they upgrade existing MinionsOS Writer skills:

### Update `minions/roles/writer/skills/abstract-writing.md`

- Add **explicit "Here, we show" anchor** as a hard rule for the main-result rung
  of the six-rung ladder.
- Add **bounded-implication closer** rule: implications must name the species,
  scope, and system actually tested ("a platform for further preclinical
  evaluation" — not "for neurological disease").

### Add new skill `minions/roles/writer/skills/cn-en-academic-polish.md`

Covers Chinese-to-English mode: reconstruct logic before translating clauses;
explicit gap-first hourglass; AI-trace vocabulary blacklist; British vs American
discipline; ≤30-word sentence cap. The intro-zh case is the proof this matters.

### Update `minions/roles/writer/skills/apply-revisions.md`

- Add **Results-vs-Discussion verb taxonomy**: list the past-tense observation
  verbs (was detected, increased, showed, enabled, achieved) and the
  interpretive verbs (may reflect, suggests, could indicate, is likely due to,
  may facilitate) as a hard register rule.
- Add **paper-type diagnosis as a first-move rule**: identify research vs methods
  vs hypothesis-based paper before any sentence-level edit. The candidate's
  diagnosis footer is the evidence this works.

### Update existing rebuttal / review skills

- The "name the specific missing experiment, not just the experimental
  design class" rule from case-overclaim should port into reviewer skills as
  a quality criterion for their generated criticism.

## Open questions for next round

- The "Here, we show" anchor and bounded-implication closer should be tested
  against `research-paper-writing` (R2) which has its own ML-leaning abstract
  guidance. If the rules conflict, ML-style and Nature-style may need
  separate skill files.
- The "diagnose paper type first" rule shouldn't be expensive to add but
  needs verification: does it survive the SSL recall test? (Stage 0 deferred.)
- For Chinese-author cases, the candidate caught the AI-trace vocabulary
  baseline already removed. Does this hold up if the source has more
  Chinese influence (full Chinese drafts vs the partly-bilingual fixture)?
  Plan a harder probe in R3.
