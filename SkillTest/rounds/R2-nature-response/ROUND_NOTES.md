# Round Notes — R2 nature-response

**Cases:** case-mixed-severity (1 case)
**Date:** 2026-05-16
**Candidate skill:** `/Users/mjm/Skill/nature-skills-main/skills/nature-response/`
**Methodology:** Stage 1 only (single case, hand-loaded skill). Codex
generated baseline + candidate; main thread scored against the rebuttal
rubric (15 pts).

## Headline

Candidate **15/15** vs baseline **8/15** (+7). Bucket: Prevents real failure.

Three submission-blockers fixed by the skill:
1. Stable comment IDs (`R1.C1` vs "Reviewer 1, Comment 1:")
2. Explicit action labels (`ACCEPT_EXPERIMENT`, `DISAGREE_WITH_JUSTIFICATION
   + SOFTEN_CLAIM`, etc) vs implicit "we agree"
3. **No fabrication** (placeholder `[X]` for unknown pagination vs
   baseline inventing `page 12, lines 310-324` in R1.C3)

The fabrication failure on baseline is the hardest signal — reviewer-response
letters with invented page numbers are a hard fail at editorial review.

## Cross-validation with R1.C

R1.C case-overclaim produced the boundary-specificity rule "name the
specific missing experiment, not the design class." That rule was tagged
"tentative pending R2 confirmation" in `synthesis/proposed-updates/aspect-
note.md.diff`.

R2 confirms it. Candidate R2.C2: "frame BBB crossing as supported by
the peptide-comparison experiment rather than inferred from the targeting
design alone" — names the specific experiment. Baseline R2.C2: "revise
the mechanism language" — generic.

**The aspect-note rule is now confirmed across two independent fixtures.**
Promote from tentative to ready-to-port.

## Token economics

Single case so no aggregate; per-case:
- baseline input ~600 tokens (fixture brief alone)
- candidate input ~9300 tokens (fixture + SKILL.md + 6 references)
- output ~1700 tokens both runs
- candidate / baseline input ratio ~15.5x — heavier than R1.C
  (~10x) because nature-response loads more references

The premium is paid for action-label discipline + traceability discipline.
Worth it for any reviewer-response work where the manuscript is heading
to a CNS journal — the alternative (fabricated page numbers, vague action
mapping) is a real submission-blocker.

## Recommendation

`import-strongly`. Plan to:

### Update `minions/roles/writer/skills/prepare-rebuttal.md`

Add as hard rules:
- Stable comment IDs (`R<N>.C<M>` format)
- Explicit action labels (`ACCEPT_TEXT / ACCEPT_ANALYSIS / ACCEPT_EXPERIMENT
  / SOFTEN_CLAIM / DISAGREE_WITH_JUSTIFICATION / AUTHOR_INPUT_NEEDED /
  PARTIAL`); composite allowed
- Traceability hooks with `[X]` placeholders for unknown values; never
  fabricate
- Disagreement pattern: acknowledge -> narrow -> justify -> soften

Draft to be authored after user approves R1 ports (keep R1 / R2 synthesis
decoupled). Will live at
`synthesis/proposed-updates/prepare-rebuttal.md.diff`.

### Promote R1.C aspect-note rule

R1.C's "name specific missing experiment" rule is now confirmed by R2.
Move it from `proposed-updates/aspect-note.md.diff` (tentative) to
ready-to-port status.

## What to test next

- One more rebuttal fixture with different decision type (minor revision,
  transfer-after-review, or appeal-like) to confirm the action-label
  taxonomy covers the full FSM.
- A deliberately ambiguous fixture where author position isn't given —
  tests whether the skill correctly emits `AUTHOR_INPUT_NEEDED`.
- These can both run inside a future R2.B / R2.C without re-testing
  nature-response from scratch.
