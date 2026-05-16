# Transcript — case-heatmap

## Brief

Single-panel diverging heatmap defending: "Genes in cluster B show a coordinated
shift from CTRL to TREAT, while clusters A and C remain stable." 30 genes × 8
conditions; cluster annotation as a side bar; diverging colormap centred at 0;
two-column eligible (~115 mm); editable text; sans-serif 6-pt row labels.

## Baseline run

### What I did
- `figsize=(7.0, 7.5)` (~178 mm — bigger than the 115 mm brief)
- `RdBu_r` cmap with `vmin=-vmax, vmax=vmax` (no `TwoSlopeNorm`)
- Cluster sidebar uses 3 saturated hues: `#4C72B0` blue, `#55A868` green,
  `#C44E52` red
- `colorbar(label="row-wise z-score")` rendered with default tick params
- Default font handling — DejaVu Sans, default size
- All 30 row labels rendered (every other gene name)
- `tight_layout()`, no rcParams

### Failures or shortcuts
- No `rcParams` editable-text → SVG renders text as paths (verified: 0 `<text>`
  nodes, 18 `<path>` nodes)
- Saturated 3-colour cluster bar competes with the heatmap signal — green/red
  hues clash with the diverging RdBu_r body
- No explicit centred-at-zero norm; visual zero-point relies on data symmetry
- No print/colourblind safety check on cluster colours

## Candidate run

### Skill files actually loaded (inferred)
- `nature-figure/SKILL.md` (entry)
- `references/api.md` — for the NMI pastel palette and "reserve green/red for
  gains/drops" rule (cluster bar uses `D8D8D8/3775BA/E4CCD8`, no green)
- `references/common-patterns.md` — for the diverging-heatmap pattern + outside
  tick discipline

### What changed because of the skill
- `figsize=(115/25.4, 96/25.4)` — exact mm spec from the brief
- `rcParams`: Arial / DejaVu Sans / Liberation Sans family, `svg.fonttype="none"`,
  `pdf.fonttype=42`, base font 7-pt, top/right spines off, axis line 0.8
- `TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)` — proper centred-at-zero
  diverging norm rather than relying on data symmetry
- `cmap.set_bad("white")` — explicit handling of NaN cells
- Cluster bar palette rewritten: `#D8D8D8` (cluster A, neutral grey),
  `#3775BA` (cluster B, the actual signal cluster — single-blue family
  matching the heatmap palette), `#E4CCD8` (cluster C, faint pink). The
  "reserve green/red for gains/drops" rule from `api.md` is honoured.
- Row labels: every-other gene shown at fontsize 6 (matches brief), rotation 0°
- Colourbar tick params explicit: `labelsize=6, length=2.2, width=0.6,
  direction="out"` — outside tick discipline from common-patterns
- Cluster bar y-tick `length=0` (no protruding ticks on the side bar)
- Explicit caption below axes documenting "CTRL and TREAT columns separated by
  vertical rule; left side bar denotes clusters A-C"
- `interpolation="nearest"` on `imshow` — prevents cell-edge blurring at small
  PDF sizes

### What I rejected from the skill
- Did not switch to a microscopy-style dark plate background — irrelevant for a
  z-score heatmap.
- Did not add a hero panel or reorder anything; brief is single-panel.

### Runtime notes
- Arial used; no fallback fired
- candidate run: 0.80 s (real)
- baseline already rendered earlier (~0.5 s)
