---
slug: prepare-rebuttal
summary: Turn a batch of reviewer feedback into a clear, evidence-backed, well-packaged response — group issues, classify response type, coordinate evidence via EACN, draft concise blocks.
layer: logical
tools: eacn3_create_task, eacn3_send_message
version: 3
status: active
supersedes:
references: citation-audit, end-to-end-paper-workflow, eacn3-mcp
provenance: human + SkillTest-R2+R4.A
---

# Skill — Prepare Rebuttal

Group issues, classify response type with explicit action labels, coordinate evidence gathering via EACN, draft concise blocks that do not promise what the team cannot deliver. Flag unresolved-author-input items at the top of the letter so the editor catches them on first read.

## When to invoke

- When a batch of reviews arrives and the rebuttal window opens.
- When camera-ready requires addressing remaining reviewer concerns (smaller scope, same discipline).

## Structure

Issue clusters (method / experiments / clarity / related work / claims scope), each ranked by severity and breadth (shared concerns = top priority). Response types per issue:

| Type | Handling |
|---|---|
| `new evidence` | Experimenter runs or Expert analyses via EACN task |
| `clarification` | Prose fix, no new experiment |
| `scope adjustment` | Concede and tighten the claim |
| `disagreement` | Rebut with citation / derivation |

Outputs under `branches/writer/paper/rebuttal/`, one file per response block. Each evidence cite marked `[derived: artifacts/exp-<id>/report.md]` or `[derived: section <N>]`.

## Action-label FSM (for explicit per-comment classification)

Every reviewer comment gets a stable ID and an action label:

| ID format | Action label | When to use |
|---|---|---|
| `R<N>.C<M>` (e.g. `R1.C2`) | `ACCEPT_TEXT` | Concession by edit |
| | `ACCEPT_ANALYSIS` | Concession by added analysis on existing data |
| | `ACCEPT_EXPERIMENT` | Concession by new experiment / new data |
| | `ACCEPT_FIGURE` | Concession by figure regeneration / addition |
| | `ADD_CITATION` | Missing-citation fix |
| | `SOFTEN_CLAIM` | Narrow scope, hedge, qualify |
| | `DISAGREE_WITH_JUSTIFICATION` | Hold the line, justify with citation / derivation |
| | `PARTIAL` | Accept part, disagree with part |
| | `AUTHOR_INPUT_NEEDED` | Author position is partial / unconfirmed |

Composite labels (`DISAGREE + SOFTEN`, `ACCEPT_EXPERIMENT + SOFTEN_CLAIM`) are allowed when one comment legitimately spans two responses.

## Procedure

1. **Ingest reviews.** Read all reviewer reports and Reviewer's consolidated summary at `artifacts/reviews/summaries/`. Do not work from individual reviews alone — the consolidated summary already dedupes and prioritizes.

2. **Assign stable IDs and action labels.** Label every reviewer comment `R<N>.C<M>`. Classify with one of the FSM action labels above (composite allowed). Do NOT label by paraphrased prose ("the third concern about GPU acceleration") — paraphrases drift and break cross-links to revisions / commits / EACN tasks.

3. **Group issues.** Cluster by topic; within each cluster rank by severity and number of reviewers. Shared concerns across reviewers = top priority.

4. **Coordinate evidence requests via EACN.** For each `ACCEPT_EXPERIMENT` or `ACCEPT_ANALYSIS` issue, open a targeted request to Experimenter or Expert with the exact question and the deadline. Do not wait on speculative experiments outside the rebuttal window.

5. **Flag AUTHOR_INPUT_NEEDED at the top of the letter.** When ANY comment is `AUTHOR_INPUT_NEEDED`, name this in the opening paragraph of the response letter so the editor catches it on first read. Do NOT bury the flag inside the per-comment section — editors triage cover letters; an unresolved point in the body is a submission-quality failure.

6. **Emit a PI question list as a separate section** for any `AUTHOR_INPUT_NEEDED` comment. 2-4 specific questions per unresolved comment that the corresponding author can paste into an email to the PI. Status updates ("R2.C1 remains unresolved until the PI confirms whether GPU acceleration was attempted") are NOT acceptable substitutes — the author needs an actionable question to send.

7. **Use `[X]` placeholder discipline.** For manuscript locations not yet recompiled with the rebuttal edits, write `[page/line/section X]` rather than fabricating specific page numbers. The placeholder gets filled at apply-revisions stage when the compiled PDF is in hand.

8. **Draft response blocks.** One per issue cluster: restate the concern in one line, state the response (with action label), cite evidence (table / figure / section / new `exp-{id}`). Reviewers skim — keep blocks short.

9. **Disagreement pattern.** For any `DISAGREE_WITH_JUSTIFICATION`, follow: acknowledge → narrow → justify (citation / derivation / experimental evidence) → soften the residual claim. A bare "we disagree because [reason]" reads as defensive; a bare acknowledgement without justification reads as capitulation.

10. **Audit honesty.** No "will do in camera-ready" promises unless the team actually can. No silent scope expansion. Material weaknesses acknowledged, not dodged.

11. **Final pass for consistency** with the paper's existing claims and with Reviewer's consolidated summary emphasis.

## Pitfalls

- Responding issue-by-issue in review order instead of grouping. Reviewers see disorganization; the area chair sees confusion.
- Labelling comments by paraphrase instead of stable `R<N>.C<M>` IDs — breaks cross-links to revisions / commits / EACN tasks.
- Using prose mood ("we agree", "has not yet confirmed") instead of explicit action labels — the editor cannot triage at a glance.
- Burying AUTHOR_INPUT_NEEDED flags inside the per-comment section. Editors triage cover letters first.
- Emitting status updates instead of actionable PI questions for unresolved comments.
- Fabricating specific page numbers (`page 12, lines 310-324`) when the manuscript hasn't been recompiled.
- Bare disagreement without acknowledgement, or bare acknowledgement without justification.
- Over-promising future work the team has no capacity for.
- Silently rewriting a claim rather than explicitly acknowledging the scope change.
