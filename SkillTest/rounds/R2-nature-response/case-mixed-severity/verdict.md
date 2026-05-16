# Verdict — nature-response / case-mixed-severity

**Round:** R2 · **Date:** 2026-05-16 · **Rubric version:** v1 (rebuttal /15)

## Numeric score

| Dim | Baseline | Candidate | Δ | Notes |
|---|---|---|---|---|
| Comment ID + classification | 1/3 | 3/3 | +2 | baseline uses "Reviewer 1, Comment 1:" as ID (long, not cross-referenceable); candidate uses `R1.C1` style stable IDs |
| Action mapping | 1/3 | 3/3 | +2 | baseline tags responses implicitly ("we agree", "partially agree"); candidate uses explicit labels: `ACCEPT_EXPERIMENT`, `ACCEPT_ANALYSIS`, `PARTIAL`, `DISAGREE_WITH_JUSTIFICATION`, `SOFTEN_CLAIM` (with composite labels where multiple actions apply) |
| Traceability to manuscript | 0/3 | 3/3 | +3 | **baseline fabricated page 12 lines 310-324 in R1.C3** (the fixture provided no pagination — these numbers are invented). Candidate uses `page [X], lines [Y-Z]` placeholders with explicit note "marked as placeholders until the revised manuscript is paginated" |
| Tone | 2/2 | 2/2 | 0 | both cooperative; both acknowledge before disagreeing |
| Completeness | 4/4 | 4/4 | 0 | both reply to all 5 comments; both handle the disagreement (R1.C3) on scientific grounds |
| **Total** | **8/15** | **15/15** | **+7** | |

## What the skill actually delivered

Three load-bearing changes, in increasing severity:

1. **Stable comment IDs.** Baseline's "Reviewer 1, Comment 1:" prose
   prefix can't be cross-referenced from a spreadsheet, an editor's
   tracking system, or a follow-up letter. Candidate's `R1.C1` ID is
   the convention used by every CNS revision system and lets editors
   diff between submission rounds.

2. **Action labels.** Baseline tags each response by mood ("we agree",
   "we partially agree", "we respectfully disagree"). Candidate uses
   explicit labels (`ACCEPT_EXPERIMENT`, `PARTIAL`, `DISAGREE_WITH_JUSTIFICATION`,
   `SOFTEN_CLAIM`) that map to a finite-state machine an editor can audit.
   Candidate also uses composite labels where multiple actions apply
   simultaneously (R1.C3 = `DISAGREE_WITH_JUSTIFICATION + SOFTEN_CLAIM`;
   R2.C2 = `ACCEPT_EXPERIMENT + SOFTEN_CLAIM`) — baseline misses both
   composites.

3. **No fabrication.** Baseline R1.C3 invented `page 12, lines 310-324`.
   The fixture gave no pagination. This is a hard failure mode for
   reviewer-response writing — fabricated traceability hooks defeat the
   point of traceability. Candidate uses `page [X], lines [Y-Z]`
   placeholders with explicit note that they will be filled at final
   pagination.

## What the skill missed

Nothing material on this case. The candidate's response to R2.C2 is
particularly clean: it accepts the experiment AND softens the
mechanism claim until that experiment lands ("frame BBB crossing as
supported by the peptide-comparison experiment rather than inferred
from the targeting design alone"). Baseline says "revise the mechanism
language" — vague, the editor can't verify.

## Visual / textual inspection

- Word counts: baseline 458, candidate 462 — almost identical. The
  skill's contribution is structural, not verbose.
- Both letters are addressed to the editor with cooperative tone.
- Both correctly handle the only disagreement (R1.C3 cholesterol
  effect): acknowledge magnitude is not statin-equivalent, justify
  on mechanistic-distinctness grounds.

## Token cost

See `tokens.json`. nature-response is the heaviest skill in R1+R2 by
far: SKILL.md ~6 KB + ~6 references avg ~5 KB each = ~36 KB / ~9000
input-token premium. Output similar length to baseline.

## Bucket

**Prevents real failure.** Three independent submission-blockers fixed:
unstable comment IDs (no cross-reference possible), implicit action
mapping (editor can't audit), fabricated page numbers. Each is the kind
of thing that would draw editor pushback on resubmission. The skill
turns a competent prose reply into an editor-auditable verification
document.

## Cross-validation with R1.C aspect-note rule

R1.C case-overclaim produced the rule "name the specific missing
experiment, not the design class" — flagged in
`synthesis/proposed-updates/aspect-note.md.diff` as a tentative port
needing R2 confirmation. R2 evidence:

- Candidate R2.C2 says "frame BBB crossing as supported by the
  peptide-comparison experiment" — names the specific experiment
  that would close the boundary. This MATCHES R1.C's aspect-note
  rule.
- Baseline R2.C2 says "revise the mechanism language" — generic.

The R1.C aspect-note rule is now confirmed across two independent
fixtures (R1.C case-overclaim Discussion paragraph + R2 case-mixed-
severity rebuttal letter). Promote the rule from "tentative pending
R2" to "confirmed; ready to port."

## Porting recommendation

`import-as-is`. nature-response delivers on its core promise on this
case: turn a free-prose response into a structured editor-auditable
document. Three components portable into MinionsOS Writer:

### Update or new skill: `prepare-rebuttal.md` (Writer)

Add hard rules:
- **Stable comment IDs** in `R<N>.C<M>` format (or equivalent)
- **Action labels**: `ACCEPT_TEXT / ACCEPT_ANALYSIS / ACCEPT_EXPERIMENT
  / SOFTEN_CLAIM / DISAGREE_WITH_JUSTIFICATION / AUTHOR_INPUT_NEEDED /
  PARTIAL`. Composite labels allowed when multiple actions apply.
- **Traceability hooks**: every reply names section / page / line /
  figure / supplement. **Use `[X]` placeholders when actual values
  unknown**; never invent.
- **Disagreement pattern**: acknowledge concern, name what you agree
  with, narrow the disagreement, give scientific justification,
  soften the claim.

Draft delta: `synthesis/proposed-updates/prepare-rebuttal.md.diff`
(to be authored after the user approves R1 ports — keeps R1 / R2
synthesis decoupled).

## Open questions for the next round

- Single-case verdict, but the failure modes (fabrication, vague action
  mapping) are crisp enough that I think one strong case + R1.C
  cross-confirmation is enough evidence. Consider testing one more
  case (different decision type — minor revision only, or transfer-
  after-review) before declaring full import.
- The "AUTHOR_INPUT_NEEDED" action label didn't fire in this case
  because the brief gave a clear author position. A future fixture
  with deliberately unclear author position would test this branch.
