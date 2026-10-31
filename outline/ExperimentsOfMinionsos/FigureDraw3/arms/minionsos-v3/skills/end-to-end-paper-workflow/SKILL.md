---
slug: end-to-end-paper-workflow
summary: Open when the user asked for a manuscript (not just section drafts) — seven-phase pipeline from project inputs to compiled PDF, with hard blockers preventing premature "done".
layer: composite
tools:
version: 2
status: active
supersedes:
references: paper-work-boundaries, citation-audit, paper-compile, package-submission, apply-revisions, prepare-rebuttal
provenance: human
---

# Skill — End-to-End Paper Workflow

A complete evidence-grounded paper-writing pipeline. Stop only when there is a compiled PDF with claims, citations, and figures that all trace.

## When to invoke

- The user requested a manuscript (not just section drafts).
- A project has stable experimental results and a target venue.
- Re-running after a major revision that changes claims, results, or venue.

If evidence is missing, stop and ask Expert / Coder / Gru / user through EACN — do not invent or rerun results inside Writer.

## Structure

Seven phases: gather inputs → structure facts → build citations → delegate by boundary → keep evidence fixed → integrate under `branches/writer/paper/` → QA. Subagent boundaries are listed in `paper-work-boundaries`. Existing experiment outputs are inputs only; `template/` is read-only; the editable working copy lives under `branches/writer/paper/`.

Blockers that prevent calling a paper "done": missing PDF, unresolved citations, unsupported claims, too-thin bibliography, structural failures from QA.

## Procedure

1. **Gather inputs first.** Read the project brief, `branches/<role>/` evidence (primarily `branches/coder/` and `branches/coder/exp/`), result tables / logs, existing figures, and any `template/` reference material. Do not write prose until the evidence inventory is clear.
2. **Structure facts before narrative.** If method details, numbers, comparisons, or missing-evidence questions are not already organized, delegate to `paper-evidence-analyst` and require a traceable evidence summary.
3. **Build citations early.** Delegate to `paper-literature-citation-builder` before drafting frontmatter or related work. Require a bibliography, literature matrix, citation map, and explicit citation gaps.
4. **Delegate by boundary** per `paper-work-boundaries`: frontmatter, method, results, closing, figures, tables, template integration, QA. Subagent prompts include the relevant boundary, allowed paths, forbidden paths, evidence rules, and required final report sections.
5. **Keep evidence fixed.** Use existing experiment outputs only. Missing evidence → ask via EACN, never invent.
6. **Integrate into `branches/writer/paper/`.** Treat `template/` as read-only, create or update the editable working copy, connect sections / figures / tables / bibliography, compile.
7. **Finish with QA.** Require `paper-qa-auditor` to check claims, numbers, citations, references, structure, table / figure fit, and compiled PDF readiness before calling the paper complete.

## Pitfalls

- Stopping at section drafts when the user asked for a manuscript.
- Letting subagents skip the required final report sections (`Completed`, `Files Changed`, `Needs Main Thread Attention`).
- Running new experiments inside Writer.
- Treating `template/` as editable.
