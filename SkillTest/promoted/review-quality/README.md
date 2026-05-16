# Promoted — Review Quality

Skills / rules tested for criticism specificity, evidence boundaries,
and reviewer-response auditability.

## Skills inside

### Third-party (kept as reference, not duplicated)

- **nature-polishing** — `/Users/mjm/Skill/nature-skills-main/skills/nature-polishing/`
  - Discussion-section rules tested in R1.C case-overclaim are the
    review-quality contribution from this skill.
  - Verdict on the relevant rules: import-strongly (case-overclaim +4)

- **nature-response** — `/Users/mjm/Skill/nature-skills-main/skills/nature-response/`
  - Tested: R2 case-mixed-severity (1 case)
  - Verdict: **import-strongly** (15/15 vs baseline 8/15; bucket = "Prevents real failure")
  - Headline: stable comment IDs, explicit action labels, no fabrication.
    Baseline invented `page 12, lines 310-324` because the fixture lacked
    pagination — a hard reviewer-response failure mode the skill prevents.

### SkillTest drafts (authored from R1 + R2 evidence)

- **aspect-note.md.diff** -> see `../../synthesis/proposed-updates/aspect-note.md.diff`
  - R1.C case-overclaim authored; R2 case-mixed-severity confirmed
  - The "name specific missing experiment" rule fired on both fixtures,
    cross-validating across in-paper Discussion AND rebuttal letter.
  - Status: confirmed across 2 fixtures; ready to port.

### To author after R2 (placeholder)

- **prepare-rebuttal.md.diff** — update plan for
  `minions/roles/writer/skills/prepare-rebuttal.md` with R2 evidence.
  Will be drafted at `../../synthesis/proposed-updates/prepare-rebuttal.md.diff`
  once user approves moving R1 ports forward (keeping R1 / R2 synthesis
  decoupled in case the user approves them separately).

## Rules / patterns extracted

### From R1.C case-overclaim (in-paper Discussion)

| Rule | What it does |
|---|---|
| Name the specific missing experiment, not the design class | "did not include transfer experiments" beats "observational design cannot establish causation" |
| Tier the limitation by what would close it | "n >= 200 with second-site replication" beats "larger cohorts are required" |
| Mechanism downgrade discipline | "may contribute, but mechanism remains to be tested directly" beats "almost certainly through SCFA signalling" |
| Future-work specificity | "prospective and mechanistic studies" beats "future studies will address this" |

### From R2 case-mixed-severity (rebuttal letter)

| Rule | What it does |
|---|---|
| Stable comment IDs (`R<N>.C<M>` format) | enables cross-reference between submission rounds, editor tracking systems, follow-up letters |
| Explicit action labels (`ACCEPT_TEXT`, `ACCEPT_ANALYSIS`, `ACCEPT_EXPERIMENT`, `SOFTEN_CLAIM`, `DISAGREE_WITH_JUSTIFICATION`, `AUTHOR_INPUT_NEEDED`, `PARTIAL`) | turns prose mood into editor-auditable FSM; composite labels allowed where multiple actions apply (`DISAGREE_WITH_JUSTIFICATION + SOFTEN_CLAIM`, `ACCEPT_EXPERIMENT + SOFTEN_CLAIM`) |
| Traceability with `[X]` placeholders for unknown values | never invent page numbers / line numbers / figure panels — placeholder until pagination confirmed |
| Disagreement pattern: acknowledge -> narrow -> justify -> soften | R1.C3 cholesterol claim: candidate explicitly separated "not statin-magnitude-equivalent" from "mechanistically distinct CNS-only PCSK9 effect", then softened the claim instead of just defending it |

### Cross-confirmed (R1.C + R2)

The "name specific missing experiment" rule fired on both
fixture types: in-paper Discussion (R1.C case-overclaim, candidate identified
"did not include transfer experiments") AND rebuttal letter (R2
case-mixed-severity R2.C2, candidate identified "supported by the
peptide-comparison experiment"). **Cross-validated; ready to port.**

## Recommendation

`import-strongly` (after R2 cross-confirmation).

Three parallel paths into MinionsOS Reviewer + Writer skills:

1. Update `minions/roles/reviewer/skills/aspect-note.md` (or sibling) with
   the boundary-specificity rule. R1.C-authored, R2-confirmed.
2. Update `minions/roles/writer/skills/prepare-rebuttal.md` with stable
   IDs + action labels + placeholder traceability + disagreement pattern.
   R2-authored, single-case but failure modes are crisp.
3. Reviewer skills should NOT fabricate. Add as a hard rule across all
   reviewer skills: "never invent page / line / figure / supplement
   identifiers; use `[X]` placeholders when actual values unknown." This
   matches MinionsOS's existing "evidence-first EACN communication"
   convention.

## Open questions for next round

- One more rebuttal fixture with a different decision type (minor revision,
  transfer-after-review, appeal-like) would test the full action-label
  FSM, especially `AUTHOR_INPUT_NEEDED`.
- A deliberately ambiguous fixture (no clear author position) would test
  whether the skill correctly emits `AUTHOR_INPUT_NEEDED` rather than
  guessing.
- These extensions can run as R2.B / R2.C without re-testing
  nature-response from scratch.
