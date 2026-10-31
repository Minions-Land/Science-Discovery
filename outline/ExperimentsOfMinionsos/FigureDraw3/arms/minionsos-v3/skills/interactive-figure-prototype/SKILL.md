---
slug: interactive-figure-prototype
summary: Prototype paper figures with a local interactive HTML explorer before committing to a static plot — for figures with many visual degrees of freedom.
layer: logical
tools:
version: 2
status: active
supersedes:
references: academic-plotting, figure-spec
provenance: human
---

# Skill — Interactive Figure Prototype

Small playground for figures with many visual degrees of freedom. Final submission still needs static, reproducible figure assets.

## When to invoke

- A figure has 3 or more independent visual choices to make (e.g. grouping, metric, ordering, annotation, subplot layout, color encoding) and Writer has no clear default for any of them.
- Reviewer or Expert asks for clearer visualization of an existing result.
- A dashboard-like explorer would help choose one final paper figure.

## Structure

Prototype lives at `branches/writer/paper/figures/prototypes/<slug>.html`. Controls tied to real data only — no invented values, no reinterpretation beyond Expert's evidence. Once the layout is chosen, the static plotting spec is updated or Coder is asked to produce the final asset. Provenance (data source, script path, chosen visual settings) recorded in the figure notes or caption draft.

## Procedure

1. **Name the figure decision.** Identify what is uncertain: grouping, metric selection, color, ordering, annotation, subplot layout, narrative emphasis.
2. **Locate the evidence.** Existing experiment outputs or Coder-produced figures only. Do not invent values or reinterpret results beyond Expert's evidence.
3. **Create a prototype path** at `branches/writer/paper/figures/prototypes/<slug>.html`.
4. **Expose useful controls** — toggle encodings, labels, metric views, caption variants. Keep controls tied to real data.
5. **Extract the static decision.** Once layout is chosen, update the static plotting spec or ask Coder to produce the final figure asset.
6. **Preserve provenance.** Record data source, script path, chosen visual settings in the figure notes or caption draft.
7. **Report** the prototype path, data provenance, chosen static figure direction, and any Coder handoff needed.

## Pitfalls

- Treating an interactive prototype as a submission artifact.
- Creating visual impressions not supported by the underlying data.
- Making the figure prettier while changing scientific meaning.
- Spending prototype time on routine plots that already have a clear spec.
