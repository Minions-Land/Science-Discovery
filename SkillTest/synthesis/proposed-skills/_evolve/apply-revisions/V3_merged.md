---
slug: apply-revisions
summary: Open after rebuttal acceptance or Weak Accept / Borderline — diagnose paper type first, then edit by reviewer-traced checklist, applying the right verb register per section, re-audit citations, recompile.
layer: logical
tools:
version: 2
status: active
supersedes:
references: prepare-rebuttal, package-submission, citation-audit, paper-compile, end-to-end-paper-workflow
provenance: human + SkillTest-R1.C-merged
---

# Skill — Apply Revisions

Bridge between `prepare-rebuttal` (response packet) and `package-submission` (final bundle). Three load-bearing disciplines: (1) diagnose paper type before editing, (2) trace every edit to a reviewer-driven checklist entry, (3) match verb register to section (Results vs Discussion). Then re-audit citations and recompile.

## When to invoke

- Reviewer publishes a `Weak Accept` or `Borderline` decision and the `consolidated.md` names required revisions.
- Rebuttal is accepted and the paper moves to camera-ready status with specific reviewer-requested changes.
- Author explicitly requests a revision pass against a fixed list of reviewer concerns.

Do not invoke for speculative rewrites or "while we're at it" improvements. Only for revisions tied to a concrete published review outcome or author-approved list.

## Paper-type diagnosis (do this first)

Before any sentence-level edit, identify which paper type you are revising. The narrative logic of the right edit depends on it:

| Paper type | Narrative logic |
|---|---|
| Research | phenomenon → mechanism → significance |
| Methods | existing methods' limits → new method → fair comparison |
| Hypothesis-based | testable claim → support → boundary |
| Algorithmic / device | procedure → reliability + advantage demonstration |

A revised Discussion sentence written in research-paper voice will misfire in a methods paper. A methods-paper Results section drifting into research-paper Discussion register is the most common register-mixing failure.

## Verb register by section

| Section | Verb family | Examples |
|---|---|---|
| Results | observation verbs | `was detected`, `increased`, `decreased`, `showed`, `enabled`, `achieved`, `abolished`, `replicated` |
| Discussion | interpretive verbs | `may reflect`, `suggests`, `could indicate`, `is likely due to`, `may facilitate`, `would support`, `is consistent with` |

A paragraph that mixes registers cannot be fixed sentence-by-sentence — re-anchor it to the right section first, then polish.

## Structure

Every edit is attributable to one of:
- A specific `consolidated.md` required-revision item.
- A rebuttal promise from `branches/writer/paper/rebuttal/`.
- An author-added change with a commit message that says so.

Unattributable edits are out of scope and defer to a separate task.

Revision state lives in `branches/writer/paper/revisions/round-<n>.md` as a checklist of `{source_id, concern, change_made, files_touched, status}`. Status ∈ `pending` / `in-progress` / `done` / `deferred`. The checklist is the source of truth for "is the revision complete?" — not Writer's memory.

## Procedure

1. **Diagnose paper type** per the table above. Carry the diagnosis as the standing register for every subsequent edit.
2. **Build the checklist** from `consolidated.md` required revisions plus rebuttal response blocks. One entry per concern, all initially `pending`.
3. **Group by file target.** Sort entries by section / figure / table so one editing pass covers one file.
4. **Apply edits per entry**, marking `in-progress` on start and `done` when committed and the compile still passes.
5. **Apply verb register per section** during each edit; if the source paragraph mixes Results-observation and Discussion-interpretation verbs, re-anchor before polishing.
6. **Handle evidence-dependent edits** by opening a targeted EACN task to Experimenter or Expert per `prepare-rebuttal`'s rules. Mark the entry `pending` with a blocker note until evidence lands.
7. **Re-run `citation-audit`** after any bibliography or citation-context changes.
8. **Re-run `paper-compile`.** Verify the PDF still renders, page count still matches the venue, and no new overfull warnings appeared.
9. **Defer explicitly.** If an entry cannot be addressed in the revision window, mark `deferred` with a written justification — never silently drop it.
10. **Report** the completed `revisions/round-<n>.md` plus the recompiled PDF path. Hand off to `package-submission`.

## Output mode

- **Production output**: polished prose only.
- **Revision-coach output** (author asks for rationale): polished prose + revision notes + a one-line `Diagnosed paper type / failure mode` footer naming which rules drove the edit. The diagnosis footer never appears in production manuscript prose.

## Pitfalls

- Editing without paper-type diagnosis — sentence-level polish that fights the paper's actual genre.
- Silently widening scope: editing adjacent text because you are already in the file. Every edit must trace to a checklist entry.
- Marking an entry `done` when only the prose changed but the underlying claim / evidence did not. Reviewers check the evidence, not the wording.
- Mixing Results-tense observations into a Discussion paragraph (or vice versa). Re-anchor the paragraph to the right section before polishing.
- Deferring without justification, or deferring the same entry across two consecutive revision rounds — escalate to Expert or the author instead.
- Skipping the citation re-audit when the revision added or changed references, so `CITATION_AUDIT.md` no longer matches the bibliography.
