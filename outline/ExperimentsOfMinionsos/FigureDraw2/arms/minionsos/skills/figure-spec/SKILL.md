---
slug: figure-spec
summary: Structured FigureSpec format for formal architecture / workflow / pipeline figures — JSON description (canvas, nodes, edges, groups) is source of truth, rendered SVG/PDF is byte-stable from the spec.
layer: logical
tools:
version: 2
status: active
supersedes:
references: academic-plotting
provenance: human
---

# Skill — Figure Spec

Spec is the source of truth; the rendered SVG / PDF is built from it and regenerates byte-stable from the same spec.

## When to invoke

- Any formal architecture / method-overview / pipeline figure for a venue submission.
- When a reviewer asks "how does X connect to Y?" and the answer needs a canonical diagram.

Do **not** use for data plots (→ `academic-plotting`) or informal illustrations.

## Structure

The spec has four blocks:

- `canvas`: `{width, height}` — single-col ~500×350, two-col ~900×500, tall topology ~700×700.
- `nodes`: list of `{id, label, x, y, shape, fill, stroke}`. Positions explicit; no auto-layout magic.
- `edges`: list of `{source, target, style, label}`; `style` ∈ `solid` (data flow), `dashed` (control / feedback), `gray` (secondary).
- `groups`: optional `{label, node_ids, fill, stroke}` for named regions.

Spec and rendered figure live side-by-side under `branches/writer/paper/figures/` (e.g. `fig_overview.json` + `fig_overview.pdf`). Spec includes a provenance comment: which paper section, which claim, last regeneration date.

## Procedure

1. **Decide when to spec** (formal architecture / method / pipeline only).
2. **Draft the spec** with the four blocks above.
3. **Name labels exactly as they appear in the paper.** The spec is also a glossary check — label drift between figure and prose is a common review smell.
4. **Render deterministically** via a JSON → SVG renderer (e.g. `tools/figure_renderer.py` if present in `branches/writer/tools/`). Commit both spec and rendered SVG / PDF.
5. **Iterate on the spec, not the SVG.** Never hand-edit the rendered SVG for structural changes; edit the spec and re-render. Hand-edit only for final visual polish that will not regenerate.
6. **Include the provenance comment** in the spec file: paper section, supported claim, date of last regeneration.

## Pitfalls

- Letting a diagram tool auto-layout. Spatial arrangement carries meaning; specify it.
- Drifting labels between figure and prose. Lock label text in the spec.
- Hand-editing SVG to patch the spec's mistakes — breaks regeneration and future edits.
