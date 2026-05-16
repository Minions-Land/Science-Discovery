---
slug: apply-revisions
summary: Open after rebuttal acceptance or a Reviewer Weak Accept / Borderline decision requiring revisions — incorporate reviewer-requested changes into the manuscript before package-submission.
layer: logical
tools:
version: 1
status: active
supersedes:
references: prepare-rebuttal, package-submission, citation-audit, paper-compile, end-to-end-paper-workflow
provenance: human
---

# Skill — Apply Revisions

Bridge between `prepare-rebuttal` (which produces the response packet) and `package-submission` (which builds the final bundle). Covers the revision *work* — edit sections, update figures and tables, extend analyses, re-audit citations, recompile.

## When to invoke

- Reviewer publishes a `Weak Accept` or `Borderline` decision and the `consolidated.md` names required revisions.
- Rebuttal is accepted and the paper moves to camera-ready status with specific reviewer-requested changes.
- Author explicitly requests a revision pass against a fixed list of reviewer concerns.

Do not invoke this skill for speculative rewrites or for "while we're at it" improvements. Only for revisions tied to a concrete published review outcome or author-approved list.

## Structure

Revisions are traced to their source. Every edit is attributable to one of: (a) a specific `consolidated.md` required-revision item, (b) a rebuttal promise from `branches/writer/paper/rebuttal/`, (c) an author-added change with a commit message that says so. Unattributable edits are out of scope and defer to a separate task.

Revision state lives in `branches/writer/paper/revisions/round-<n>.md` — a checklist of `{source_id, concern, change_made, files_touched, status}`. Status ∈ `pending` / `in-progress` / `done` / `deferred`. The checklist is the source of truth for "is the revision complete?" — not Writer's memory.

## Procedure

1. **Build the checklist.** Read `artifacts/reviews/round-<n>/consolidated.md` required-revisions section and `branches/writer/paper/rebuttal/` response blocks. Extract one checklist entry per concern. Write the initial `revisions/round-<n>.md` with all entries `pending`.
2. **Group by file target.** Sort entries by which section / figure / table they touch, so one editing pass covers one file.
3. **Apply edits per entry.** Update the relevant `sections/*.tex`, `figures/`, `tables/`, or `bibliography`. Mark entry `in-progress` when starting, `done` when the edit is committed and the compile still passes.
4. **Handle evidence-dependent edits.** If an entry requires a new experimental run or analysis (rare at this stage), open a targeted EACN task to Experimenter or Expert per `prepare-rebuttal`'s rules. Mark the checklist entry `pending` with a blocker note until evidence lands.
5. **Re-run `citation-audit`** after any bibliography or citation-context changes.
6. **Re-run `paper-compile`.** Verify the PDF still renders, page count still matches the venue, and no new overfull warnings appeared.
7. **Defer explicitly.** If a reviewer-requested change cannot be made in the revision window (requires a full new experiment, conflicts with a load-bearing claim, etc.), mark the entry `deferred` with a justification — never silently drop it.
8. **Report** the completed `revisions/round-<n>.md` plus the recompiled PDF path when all entries are `done` or `deferred`. Hand off to `package-submission` for bundle assembly.

## Pitfalls

- Silently widening scope: editing adjacent text because you are already in the file. Every edit must trace to a checklist entry.
- Marking an entry `done` when only the prose changed but the underlying claim / evidence did not. Reviewers check the evidence, not the wording.
- Deferring without justification, or deferring the same entry across two consecutive revision rounds — that is a signal to escalate to Expert or the author, not to keep deferring.
- Skipping the citation re-audit when the revision added or changed references, so `CITATION_AUDIT.md` no longer matches the bibliography.
