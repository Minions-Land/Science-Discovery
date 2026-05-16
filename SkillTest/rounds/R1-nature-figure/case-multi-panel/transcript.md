# Transcript — case-multi-panel

## Brief

Four-panel composite defending: "Compound X is more potent and selective than
Compound Y, validated across pharmacology (A), structural prediction (B), in
vivo cytokine response (C), and cell-resolution genotype rescue (D)."

Required panels: A (hero, ~50% width) dose-response; B scatter w/ unity line;
C time course of 3 biomarkers; D bar by genotype with overlaid dots.
Two-column width (~180 mm), one page tall. Hero panel ~2× area of others;
unified palette across panels; sans-serif Arial 7-pt body, 8-pt panel labels;
source-data hooks per panel.

## Baseline run

### What I did
- `figsize=(11, 7)` (~280 mm — big, but no hero geometry: 2×3 grid with
  width_ratios=[2,1,1] and ax_d full-width spanning the bottom)
- Default matplotlib palette via `prop_cycle` for compounds, biomarkers,
  genotypes — three different palette systems across the four panels
- Panel A: dose-response with `errorbar` markers and dashed `axvline` at EC50
  (no fill_between CI band; brief asked for CI)
- Panel B: scatter + dashed `unity` line (good); group colours from default
  cycle
- Panel C: errorbar lines, default colours
- Panel D: `ax_d.bar(...)` + overlaid scatter for replicates; significance
  marker via `ax.plot([x1, x1, x2, x2], [y, y+0.015, y+0.015, y], 'k', lw=1)`
- `tight_layout()`, no rcParams

### Failures or shortcuts
- No `rcParams` editable text → SVG svg has 0 `<text>` nodes / 63 `<path>`
  nodes (text rasterised)
- Three different palettes across panels (default cycle compounds, default
  cycle biomarkers, default cycle genotypes) — violates "unified family" rule
- No fill_between CI band on panel A despite the brief asking
- No source-data caption hooks
- Panel ratios make A roughly the same area as B+C combined; not the
  dominant hero the brief asked for

## Candidate run

### Skill files actually loaded (inferred)
- `nature-figure/SKILL.md`
- `references/figure-contract.md` — for the archetype + hero-panel rule
- `references/api.md` — for the unified PALETTE dict
- `references/common-patterns.md` — for asymmetric multi-panel layouts and
  fill_between CI patterns

### What changed because of the skill
- `figsize=(180/25.4, 128/25.4)` — exact 180 mm × 128 mm (two-column page-tall)
- `rcParams` block: Arial / DejaVu Sans, `svg.fonttype="none"`, `pdf.fonttype=42`,
  base 7-pt, top/right spines off, axes 0.8, legend frame off
- **Hero panel geometry redesigned**: `gridspec(3, 4, ...)` with panel A at
  `gs[0:2, 0:2]` (taking the full left half × upper 2/3) — actually 4× the
  area of any other panel. Panel B at `[0,2]`, C at `[0,3]`, D at `[1:, 2:]`.
  This is the asymmetric hero layout from `common-patterns.md`.
- **Unified PALETTE dict** at the top: `signal`, `signal_soft`, `neutral`,
  `neutral_light`, `accent`, `accent_dark`, `black` — ALL panels draw from this
  one dict. CompoundX = signal blue, CompoundY = neutral grey, kinase = signal
  soft, GPCR = accent pink, IL6/TNFa/IL10 use signal/accent-dark/neutral, WT/Het/KO
  bars + replicate dots in the same hierarchy.
- Panel A: dose-response now has fill_between 95% CI band (alpha=0.16),
  EC50 vertical guides plus inline numerical EC50 labels per compound, log-x
  axis, single legend with shortened handle
- Panel B: per-group regression slope text annotation at fixed transAxes
  positions (skill rule: "annotate slope in panel rather than relying on caption")
- Panel C: errorbar lines for each biomarker, unified palette, shared y-axis
- Panel D: bar with edge stroke + per-replicate dots in white-fill /
  black-edge (so they read on top of bars), pairwise significance
  vs WT
- Panel labels (a/b/c/d) at fixed transAxes `(-0.14, 1.08)` — uniform offset,
  fontsize 8, bold
- Tick discipline applied uniformly: `direction="out", length=2.5, width=0.7`
- `bbox_inches="tight"` and 600 dpi PNG export

### What I rejected from the skill
- Did not switch to dark image-plate styling (no microscopy in this brief)
- Did not adopt direct labelling for panel A — legend is needed because
  CompoundX vs CompoundY is the central comparison and must be unambiguous
- Did not condense panel D into a strip below the others — the brief
  recommended either "bottom strip" or "right column"; chose right column
  to keep the hero/subordinate hierarchy cleaner

### Runtime notes
- Arial used; no fallback
- candidate run: 1.51 s (real)
- baseline run earlier: ~1.0 s
