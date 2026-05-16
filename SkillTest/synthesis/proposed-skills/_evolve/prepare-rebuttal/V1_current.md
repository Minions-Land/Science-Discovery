---
slug: prepare-rebuttal
summary: Turn a batch of reviewer feedback into a clear, evidence-backed, well-packaged response — group issues, classify response type, coordinate evidence via EACN, draft concise blocks.
layer: logical
tools: eacn3_create_task, eacn3_send_message
version: 2
status: active
supersedes:
references: citation-audit, end-to-end-paper-workflow, eacn3-mcp
provenance: human
---

# Skill — Prepare Rebuttal

Group issues, classify response type, coordinate evidence gathering via EACN, draft concise blocks that do not promise what the team cannot deliver.

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

## Procedure

1. **Ingest reviews.** Read all reviewer reports and Reviewer's consolidated summary at `artifacts/reviews/summaries/`. Do not work from individual reviews alone — the consolidated summary already dedupes and prioritizes.
2. **Group issues.** Cluster by topic; within each cluster rank by severity and number of reviewers. Shared concerns across reviewers = top priority.
3. **Classify response type per issue** per the table above.
4. **Coordinate evidence requests via EACN.** For each `new evidence` issue, open a targeted request to Experimenter or Expert with the exact question and the deadline. Do not wait on speculative experiments outside the rebuttal window.
5. **Draft response blocks.** One per issue cluster: restate the concern in one line, state the response, cite evidence (table / figure / section / new `exp-{id}`). Reviewers skim — keep blocks short.
6. **Audit honesty.** No "will do in camera-ready" promises unless the team actually can. No silent scope expansion. Material weaknesses acknowledged, not dodged.
7. **Final pass for consistency** with the paper's existing claims and with Reviewer's consolidated summary emphasis.

## Pitfalls

- Responding issue-by-issue in review order instead of grouping. Reviewers see disorganization; the area chair sees confusion.
- Over-promising future work the team has no capacity for.
- Silently rewriting a claim rather than explicitly acknowledging the scope change.
