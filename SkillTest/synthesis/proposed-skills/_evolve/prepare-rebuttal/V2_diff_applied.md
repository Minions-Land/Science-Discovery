---
slug: prepare-rebuttal
summary: Turn a batch of reviewer feedback into a clear, evidence-backed, well-packaged response — stable comment IDs, explicit action-label FSM, coordinate evidence via EACN, top-of-letter AUTHOR_INPUT_NEEDED flag, PI question list, [X] placeholder discipline.
layer: logical
tools: eacn3_create_task, eacn3_send_message
version: 3
status: active
supersedes:
references: citation-audit, end-to-end-paper-workflow, eacn3-mcp
provenance: human + SkillTest-R2+R4.A
---

# Skill — Prepare Rebuttal

Group issues, classify with an explicit action-label FSM, coordinate evidence via EACN, draft concise blocks. Two top-of-letter rules ensure the editor never has to dig: (1) unresolved author-input flagged in the opening paragraph; (2) PI questions in a separate dedicated section.

## When to invoke

- When a batch of reviews arrives and the rebuttal window opens.
- When camera-ready requires addressing remaining reviewer concerns (smaller scope, same discipline).

## Issue clusters and response types

Issue clusters (method / experiments / clarity / related work / claims scope), each ranked by severity and breadth (shared concerns = top priority). Response types:

| Type | Handling |
|---|---|
| `new evidence` | Experimenter runs or Expert analyses via EACN task |
| `clarification` | Prose fix, no new experiment |
| `scope adjustment` | Concede and tighten the claim |
| `disagreement` | Rebut with citation / derivation |

## Action-label FSM (per comment)

Every comment gets a stable ID `R<N>.C<M>` and one action label (composite allowed):

`ACCEPT_TEXT` · `ACCEPT_ANALYSIS` · `ACCEPT_EXPERIMENT` · `ACCEPT_FIGURE` · `ADD_CITATION` · `SOFTEN_CLAIM` · `DISAGREE_WITH_JUSTIFICATION` · `PARTIAL` · `AUTHOR_INPUT_NEEDED`

Outputs under `branches/writer/paper/rebuttal/`, one file per response block. Each evidence cite marked `[derived: artifacts/exp-<id>/report.md]` or `[derived: section <N>]`.

## Procedure

1. **Ingest reviews.** Read all reviewer reports and Reviewer's consolidated summary at `artifacts/reviews/summaries/`. Do not work from individual reviews alone — the consolidated summary already dedupes and prioritizes.

2. **Label every comment.** Assign stable `R<N>.C<M>` IDs and explicit action labels (NOT paraphrased prose, NOT prose mood like "we agree"). Use these IDs in the response letter, the revisions checklist, EACN tasks, and commit messages.

3. **Group issues.** Cluster by topic; within each cluster rank by severity and number of reviewers. Shared concerns across reviewers = top priority.

4. **Coordinate evidence requests via EACN.** For each `ACCEPT_EXPERIMENT` or `ACCEPT_ANALYSIS` issue, open a targeted request to Experimenter or Expert with the exact question and the deadline.

5. **Flag AUTHOR_INPUT_NEEDED at the top of the letter.** If ANY comment carries this label, name it in the opening paragraph of the response letter. Editors triage cover letters; burying the flag in the per-comment section is a submission-quality failure.

6. **Emit a PI question list as a separate section** for every `AUTHOR_INPUT_NEEDED`. 2-4 specific questions the author can paste into an email to the PI. Status updates ("remains unresolved until the PI confirms…") are not substitutes for an actionable question.

7. **Use `[X]` placeholder discipline** for manuscript locations the rebuttal author cannot verify at draft time. Don't fabricate `page 12, lines 310-324` — fill the placeholder at the apply-revisions stage when the compiled PDF is in hand.

8. **Draft response blocks.** One per issue cluster: restate the concern in one line, state the response (with action label), cite evidence (table / figure / section / new `exp-{id}`). Keep blocks short — reviewers skim.

9. **Disagreement pattern.** For `DISAGREE_WITH_JUSTIFICATION`: acknowledge in the reviewer's framing → narrow to a specific sub-claim → justify with citation / derivation / experimental evidence → soften the residual claim if justification is partial. Bare "we disagree" is defensive; bare acknowledgement is capitulation.

10. **Audit honesty.** No "will do in camera-ready" promises unless the team actually can. No silent scope expansion. Material weaknesses acknowledged, not dodged.

11. **Final pass for consistency** with the paper's existing claims and with Reviewer's consolidated summary emphasis.

## Pitfalls

- Responding issue-by-issue in review order instead of grouping. Reviewers see disorganization; the area chair sees confusion.
- Labelling comments by paraphrase instead of stable `R<N>.C<M>` IDs.
- Using prose mood ("we agree", "has not yet confirmed") instead of explicit FSM action labels.
- Burying `AUTHOR_INPUT_NEEDED` inside the per-comment section instead of flagging at the top of the cover letter.
- Emitting status updates instead of actionable PI questions for unresolved comments.
- Fabricating specific page / line numbers when the manuscript hasn't been recompiled with the rebuttal edits.
- Bare disagreement without acknowledgement, or bare acknowledgement without justification.
- Over-promising future work the team has no capacity for.
- Silently rewriting a claim rather than explicitly acknowledging the scope change.
