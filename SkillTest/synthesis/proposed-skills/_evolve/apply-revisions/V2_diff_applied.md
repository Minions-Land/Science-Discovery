---
slug: apply-revisions
summary: Open after rebuttal acceptance or a Reviewer Weak Accept / Borderline decision requiring revisions — incorporate reviewer-requested changes into the manuscript before package-submission.
layer: logical
tools:
version: 2
status: active
supersedes:
references: prepare-rebuttal, package-submission, citation-audit, paper-compile, end-to-end-paper-workflow
provenance: human + SkillTest-R1.C
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

1. **Diagnose paper type before any sentence-level edit.** Identify whether this is a research / methods / hypothesis-based / algorithmic / device paper. Different paper types require different narrative logic:
   - Research paper: phenomenon → mechanism → significance
   - Methods paper: existing methods' limits → new method → fair comparison
   - Hypothesis-based: testable claim → support → boundary
   - Algorithmic / device: procedure → reliability + advantage demonstration

   Do NOT use one narrative logic across paper types. A Discussion-tense sentence in a methods-paper Results section is the most common register-mixing failure.

2. **Build the checklist.** Read `artifacts/reviews/round-<n>/consolidated.md` required-revisions section and `branches/writer/paper/rebuttal/` response blocks. Extract one checklist entry per concern. Write the initial `revisions/round-<n>.md` with all entries `pending`.

3. **Group by file target.** Sort entries by which section / figure / table they touch, so one editing pass covers one file.

4. **Apply edits per entry.** Update the relevant `sections/*.tex`, `figures/`, `tables/`, or `bibliography`. Mark entry `in-progress` when starting, `done` when the edit is committed and the compile still passes.

5. **Apply Results vs Discussion verb taxonomy.** Results sentences use observation verbs: `was detected`, `increased`, `decreased`, `showed`, `enabled`, `achieved`, `abolished`, `replicated`. Discussion sentences use interpretive verbs: `may reflect`, `suggests`, `could indicate`, `is likely due to`, `may facilitate`, `would support`, `is consistent with`. A Results paragraph drifting into Discussion syntax (and vice versa) is a register failure that no amount of polish can fix at the sentence level — the paragraph needs to be re-anchored to the right section first.

6. **Handle evidence-dependent edits.** If an entry requires a new experimental run or analysis (rare at this stage), open a targeted EACN task to Experimenter or Expert per `prepare-rebuttal`'s rules. Mark the checklist entry `pending` with a blocker note until evidence lands.

7. **Re-run `citation-audit`** after any bibliography or citation-context changes.

8. **Re-run `paper-compile`.** Verify the PDF still renders, page count still matches the venue, and no new overfull warnings appeared.

9. **Defer explicitly.** If a reviewer-requested change cannot be made in the revision window (requires a full new experiment, conflicts with a load-bearing claim, etc.), mark the entry `deferred` with a justification — never silently drop it.

10. **Report** the completed `revisions/round-<n>.md` plus the recompiled PDF path when all entries are `done` or `deferred`. Hand off to `package-submission` for bundle assembly.

## Output mode

- **Production output**: polished prose only, ready to drop into the manuscript.
- **Revision-coach output** (when the author asks for revision rationale): polished prose + revision notes + a one-line "Diagnosed paper type / failure mode" footer naming which rules drove the edit. The diagnosis footer should NOT appear in production manuscript prose.

## Pitfalls

- Silently widening scope: editing adjacent text because you are already in the file. Every edit must trace to a checklist entry.
- Marking an entry `done` when only the prose changed but the underlying claim / evidence did not. Reviewers check the evidence, not the wording.
- Deferring without justification, or deferring the same entry across two consecutive revision rounds — that is a signal to escalate to Expert or the author, not to keep deferring.
- Skipping the citation re-audit when the revision added or changed references, so `CITATION_AUDIT.md` no longer matches the bibliography.
- Mixing Results-tense observations into a Discussion paragraph (or vice versa). Re-anchor the paragraph to the right section before polishing.
- Applying one narrative logic across paper types — a methods-paper revision needs different verb registers than a research-paper revision.
