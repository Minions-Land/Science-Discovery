---
slug: figure-spec
summary: Structured FigureSpec format for formal architecture / workflow / pipeline / sankey-flow figures — JSON description (canvas, nodes, edges, groups, links) is source of truth, rendered SVG/PDF is byte-stable from the spec.
layer: logical
tools:
version: 3
status: active
supersedes:
references: academic-plotting
provenance: human + FigureDraw2-evidence (borrow #5 sankey/flow archetype)
---

# Skill — Figure Spec

Spec is the source of truth; the rendered SVG / PDF is built from it and regenerates byte-stable from the same spec.

## When to invoke

- Any formal architecture / method-overview / pipeline figure for a venue submission.
- Sankey / data-flow / cohort-flow diagrams (where the proportion / volume of flow matters).
- When a reviewer asks "how does X connect to Y?" and the answer needs a canonical diagram.

Do **not** use for data plots (→ `academic-plotting`) or informal illustrations.

## Two archetypes, one spec

### Archetype A — Architecture / pipeline (boxes + arrows)

Four blocks:

- `canvas`: `{width, height}` — single-col ~500×350, two-col ~900×500, tall topology ~700×700.
- `nodes`: list of `{id, label, x, y, shape, fill, stroke}`. Positions explicit; no auto-layout magic.
- `edges`: list of `{source, target, style, label}`; `style` ∈ `solid` (data flow), `dashed` (control / feedback), `gray` (secondary).
- `groups`: optional `{label, node_ids, fill, stroke}` for named regions.

### Archetype B — Sankey / flow (FigureDraw2 borrow #5 — stat-writing-fuhaoda arm; sankey 冠军 18/24)

Three blocks:

- `canvas`: `{width, height}` — typical 600×360 for a 3-stage flow.
- `nodes`: list of `{id, label, stage, color}`. **Stage** is an integer (0, 1, 2, ...) controlling left-right ordering. Auto-layout decides y; spec only fixes stage.
- `links`: list of `{source, target, value, color?}`. The `value` field is the flow magnitude (count, count rate, or proportion).

Discipline rules specific to sankey:

- **Source-color consistency**: every outflow from a single source node uses the same color. The reader should be able to track "where did source X's volume go" by following one color across the figure. This is what set stat-writing-fuhaoda apart in FigureDraw2 — the inferior arms used per-link colors and the figure became unreadable.
- **Stage labels at top**: "Stage 1: Raw" / "Stage 2: Filtered" / "Stage 3: Train/Val/Test" as a header row above the canvas, in 8 pt sans.
- **Numerical labels on every link**: the value of each flow either inline at link midpoint or in a side legend. A sankey without numbers is a decoration, not evidence.
- **No crossing links if avoidable**: if two stage transitions force crossings, swap one node's vertical order to minimize them. Manual stage-internal y-order overrides auto-layout.

### Spec example — sankey

```json
{
  "archetype": "sankey",
  "canvas": {"width": 620, "height": 360},
  "nodes": [
    {"id": "raw",      "label": "Raw (n=1120)",     "stage": 0, "color": "#4F6B8A"},
    {"id": "clean",    "label": "Cleaned",          "stage": 1, "color": "#5C8A8A"},
    {"id": "reject",   "label": "Rejected",         "stage": 1, "color": "#A85A4A"},
    {"id": "train",    "label": "Train (n=600)",    "stage": 2, "color": "#5C8A8A"},
    {"id": "val",      "label": "Val (n=120)",      "stage": 2, "color": "#5C8A8A"},
    {"id": "test",     "label": "Test (n=100)",     "stage": 2, "color": "#5C8A8A"}
  ],
  "links": [
    {"source": "raw",   "target": "clean",  "value": 1000},
    {"source": "raw",   "target": "reject", "value": 120},
    {"source": "clean", "target": "train",  "value": 600},
    {"source": "clean", "target": "val",    "value": 120},
    {"source": "clean", "target": "test",   "value": 100}
  ]
}
```

Note how every outflow from `raw` would be colored by the source `raw`'s color; every outflow from `clean` by `clean`'s color. The renderer enforces this — do not override per link unless explicitly justified.

Spec and rendered figure live side-by-side under `branches/writer/paper/figures/` (e.g. `fig_overview.json` + `fig_overview.pdf`). Spec includes a provenance comment: which paper section, which claim, last regeneration date.

## Procedure

1. **Decide which archetype** — boxes-and-arrows (A) vs. flow-with-volume (B). If unsure, the test: "do the link widths carry quantitative meaning?" → yes is sankey.
2. **Draft the spec** with the blocks above.
3. **Name labels exactly as they appear in the paper.** The spec is also a glossary check — label drift between figure and prose is a common review smell.
4. **Render deterministically** via a JSON → SVG renderer (e.g. `tools/figure_renderer.py` if present in `branches/writer/tools/`). Commit both spec and rendered SVG / PDF.
5. **Iterate on the spec, not the SVG.** Never hand-edit the rendered SVG for structural changes; edit the spec and re-render. Hand-edit only for final visual polish that will not regenerate.
6. **Include the provenance comment** in the spec file: paper section, supported claim, date of last regeneration.

## Pitfalls

- Letting a diagram tool auto-layout architecture nodes. Spatial arrangement carries meaning; specify it.
- Drifting labels between figure and prose. Lock label text in the spec.
- Hand-editing SVG to patch the spec's mistakes — breaks regeneration and future edits.
- Sankey with per-link colors instead of source-color consistency (FigureDraw2 latex-document arm 10/24 vs stat-writing-fuhaoda 18/24 — same data, color discipline alone caused the gap).
- Sankey without numerical link labels — decorative, not evidence.
- Crossing links that could be avoided by swapping one node's vertical order.
