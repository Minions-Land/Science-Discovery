---
slug: submission-cleanup-audit
summary: Six audit categories within a week of submission — orphan figures, multiply-defined LaTeX labels, agent-internal-artifact leakage, generic figure captions, partial-integration coexistence, worktree-not-committed-at-handoff. None caught by ordinary QA; treat as a dedicated pass.
layer: logical
tools:
version: 1
status: active
references: paper-compile, citation-audit, package-submission, claim-honesty-grading, pdf-vector-layout
provenance: human + EACN-005-PRL Round 1-4 review rounds
---

# Skill — Submission Cleanup Audit

Six failure classes that survive ordinary QA, all observed in EACN-005-PRL review rounds. Each is a Reviewer-visible finding worth Minor-to-Major Revision; together they are the difference between Accept and Major-Revision verdicts.

## When to invoke

- Within a week of submission deadline.
- After a major revision — partial-integration risk is highest then.
- Whenever a reviewer flagged "this looks unfinished".

## The six categories

### 1. Orphan figures
Figures exist in `figures/` but are never `\includegraphics`'d in any `.tex`. Reviewer reads it as "the empirical evidence is incomplete."

Check:
```bash
# files referenced
grep -hroE '\\includegraphics[^{]*\{[^}]+\}' branches/writer/paper/ | grep -oE '\{[^}]+\}' | tr -d '{}' | sort -u > /tmp/used.txt
# files on disk
ls branches/writer/paper/figures/ | sort -u > /tmp/on_disk.txt
comm -13 /tmp/used.txt /tmp/on_disk.txt   # orphans
```
Either cite each orphan or delete from the repo before submission.

### 2. Multiply-defined LaTeX labels
`Label 'eq:foo' multiply defined` in `main.log`. Compiles but `\eqref` resolves to the wrong occurrence. A single such warning is enough for Minor Revision.

Fix recipe: keep main-text labels canonical; rename appendix-local duplicates with `-app` suffix (`eq:spread-bound` in main, `eq:spread-bound-app` in appendix). Verify via `grep -c "multiply defined" branches/writer/paper/build/*.log` returning 0.

### 3. Agent-internal artifact leakage
Bib entries with branch paths (`'GeometricMathematician2024-some-branch'`), agent IDs, tool slugs in citation keys, draft-only labels, `/tmp/` paths. **Must never appear in any submission.**

Check: `grep -E '(branch|agent-|/tmp/|claude-|gpt-|@.*-draft)' references/*.bib`. Also scan unused / draft `.tex` files (`make-tex.tex`, `*.draft.tex`); if any are in the repo they can leak through wildcard `\input{}`.

### 4. Generic figure captions
"Representative low-energy spectrum" / "Representative gap-versus-geometry trend" without system size, parameter choices, or source dataset / literature provenance. Reviewer-visible category even when the figure is otherwise fine.

Required caption shape: *<what>, <system size N=...>, <parameters λ=...>, <method/source: ED / DMRG bond dim χ=... / [Wang2024 Fig 3]>*.

### 5. Partial-integration coexistence
After fixing a factual error in one location (e.g. Jain K-matrix in `appendix-cs-eft.tex:96`), the old wrong formula still lives in `appendix-orbital-attachment.tex:292`. Coexistence alone is enough for Major Revision.

Audit: after every factual fix, `grep` for the *old* expression across the entire repo, not just the file you edited. Every match either gets updated or earns a comment explaining why it's a different claim.

### 6. Worktree not committed at handoff
Cleanup is in the working directory but not committed. Submission contract: handoff = clean tree + new commit beyond the last review-state commit. An uncommitted final pass is a process failure worth flagging.

Check: `git status` empty AND `git log --oneline | head` shows a handoff commit after the last review commit.

## Procedure

Run the six checks in order. Produce a one-line verdict per category (`OK` / `FIX <path:line>` / `N/A`). The audit completes only when all six are `OK`.

After fixes, re-run categories 2 and 5 (they regenerate easily): a label fix in one file can introduce a duplicate in another; a factual fix can leave a coexistence elsewhere.

## Output habit

Write verdicts to `branches/writer/paper/SUBMISSION_CLEANUP_AUDIT.md` with:
- Per-category verdict and path:line for each FIX.
- Final commit SHA after fixes.
- Mark each fix `[evidence: <log path or grep output>]`.

## Pitfalls

- Treating QA as a substitute. Standard QA checks compile cleanliness, not these six classes.
- Running once and assuming follow-up edits don't regenerate a category. Always re-run 2 + 5 after any factual fix.
- Using `git diff --name-only` instead of `grep` for partial-integration. The fix may have edited a *different* file than the original mistake lives in.
- Leaving the worktree dirty after audit fixes. Final commit must include the audit fixes themselves.
- Treating an "in-bib but never cited" warning as orphan-figure-class. That's `citation-audit` bidirectional check, not this skill.
