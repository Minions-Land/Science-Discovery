---
slug: paper-work-boundaries
summary: Open when about to spawn a paper-* subagent — ten-slot boundary map plus required final report sections; subagents do not auto-inherit Writer's state.
layer: scheduling
tools:
version: 2
status: active
supersedes:
references: end-to-end-paper-workflow
provenance: human
---

# Skill — Paper Work Boundaries

Boundaries to include in every Writer subagent prompt; subagents do not automatically inherit Writer's full state.

## When to invoke

Open whenever Writer is about to delegate paper work to a `paper-*` subagent — including the orchestrated path through `end-to-end-paper-workflow` and any one-off direct delegation. Detection signal: you are about to spawn a subagent whose work writes inside `branches/writer/paper/` and you need to decide which slot owns it.

## Structure

All paper work stays under `branches/writer/paper/`. Template / reference directories such as `template/` or `branches/writer/template/` are **read-only**. Existing results are inputs; do not run new experiments or invent missing evidence.

Required final report sections for every delegated paper subagent: `Completed`, `Files Changed`, `Needs Main Thread Attention`.

Cross-slot rule: work that spans two slots (e.g. a results figure that needs both numerical plotting and prose interpretation) does not give two subagents write access to the same file. Dispatch slot A first; pass A's output as **read-only context** to slot B; slot B writes the final artifact.

## Procedure

Pick the slot that matches the delegated work from the boundary map below. The mapped subagent name, its allowed scope, and the read-only constraints go into the subagent prompt verbatim, plus the required final report sections.

At the end of every delegation, verify: each subagent's `Files Changed` entries fall within its slot's allowed paths. Any cross-slot write is a boundary violation — treat it as a failed delegation rather than a completed one.

Boundary map — pick the one that matches the delegated work:

| Subagent | Scope |
|---|---|
| `paper-evidence-analyst` | Organize method facts, result numbers, comparison targets, missing evidence, open questions. Writes evidence notes only — not sections, figures, or tables. |
| `paper-literature-citation-builder` | Collect credible references, build a literature matrix, citation map, bibliography, citation gaps. Does not draft paper sections. |
| `paper-frontmatter-writer` | Title, abstract, introduction, related work — after evidence and citations are stable. |
| `paper-methods-writer` | Proposed method, formulation, architecture / module description, algorithm, method-specific implementation details. |
| `paper-results-writer` | Datasets, baselines, metrics, experimental setup, main results, ablations, error analysis, result interpretation grounded in existing outputs. |
| `paper-closing-writer` | Conclusion, compact discussion, optional limitations — after method / results are stable. |
| `paper-figure-python` | Result-grounded Python figures, plotting scripts, exports, captions. Does not reinterpret result meaning. |
| `paper-table-tex` | Result-grounded TeX tables and helper scripts with layout-safe formatting. |
| `paper-template-integrator` | Inspect template references, create / update the editable working copy under `branches/writer/paper/`, integrate sections / assets / bibliography, compile, fix layout / citation errors. |
| `paper-qa-auditor` | Final consistency across claims, numbers, citations, structure, references, figures / tables, compiled PDF readiness. Defaults to a report, not large rewrites. |

## Pitfalls

- Letting a subagent write outside its slot (e.g. `paper-figure-python` editing prose).
- Reusing `template/` for live edits instead of cloning into `branches/writer/paper/`.
- Subagents inventing missing evidence rather than reporting it under `Needs Main Thread Attention`.
