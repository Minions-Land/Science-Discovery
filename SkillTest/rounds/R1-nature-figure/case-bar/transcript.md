# Transcript — case-bar

## Brief

(quoted from `/Users/mjm/Skill/SkillTest/fixtures/figures/briefs/bar-ablation.md`)

> Single-panel grouped bar chart defending the claim:
> "Removing component C from our framework hurts performance more than removing
> component A or B, indicating that C carries the dominant inductive bias."
> Three datasets × four methods (Full / -A / -B / -C); error bars ±1 SD over
> n=5 seeds; dashed external-baseline line per dataset; `*` / `**` significance
> markers for Full vs −C only; single-column width (~85 mm); editable text;
> sans-serif 7-pt body; direct-or-non-overlapping legend; y-axis 0–1.

## Baseline run

### What I did
- `figsize=(6.0, 4.0)` (default inches — about 152 mm wide; ~80% bigger than the
  brief's single-column ask)
- Default matplotlib palette via `ax.bar(..., label=...)` cycling through
  the prop_cycle (blue/orange/green/red — saturated, not unified)
- Default font family (matplotlib default `DejaVu Sans` at default 10-pt)
- No `rcParams` for editable text, no `pdf.fonttype=42`, no `svg.fonttype=none`
- Default tight_layout
- Significance markers above Full vs -C with a horizontal connector
- Error-bar definition stuffed into a tiny in-axes text box at the bottom-left
  (`fontsize=8`)
- Welch's t-test for sig markers (`stats.ttest_ind(equal_var=False)`)

### Failures or shortcuts
- No `rcParams` editable-text setup → SVG text is rendered as paths in some
  matplotlib versions
- Saturated 4-colour palette fights itself; no unified method-family colouring
- Legend rendered with frame, default position (`upper right`) — risk of
  overlapping the highest bar in Dataset-3
- Caption-style note placed *inside* the plot axes; reduces effective plotting
  area and uses default font size
- Figure 152 mm vs brief's ~85 mm → text-to-data ratio off-spec

## Candidate run

### Skill files actually loaded (inferred from script structure + rcParams)
- `nature-figure/SKILL.md` — the entry skill itself
- `references/api.md` — for the `PALETTE` block referenced as the "NMI pastel"
  family (script imports `Patch` and uses a single-blue family with hatches)
- `references/common-patterns.md` — for the print-safe bar pattern (alpha-graded
  single-hue family + hatch differentiation, top legend, captioned bottom strip)

### What changed because of the skill
- `figsize` switched to `(85/25.4, 58/25.4)` — exact single-column mm spec
- `rcParams`: `font.family=sans-serif`, `font.sans-serif=[Arial, DejaVu Sans, ...]`,
  `svg.fonttype="none"` (editable text in SVG), `pdf.fonttype=42` (TrueType in
  PDF), `font.size=7`, top/right spines off, axis linewidth 0.8, legend frame off
- Palette: **single-hue blue family** (`BASE_BLUE = (0.216, 0.459, 0.729)`) with
  alpha gradient (1.0 / 0.68 / 0.46 / 0.26) plus hatch pattern (`""`, `//`,
  `\\`, `..`) — print-safe, colourblind-safe, and degenerates correctly to
  greyscale. This is the "unified method family" rule from the skill.
- Edge `linewidth=0.55` on bars (skill-grade thin strokes); error-bar
  `elinewidth=0.65, capthick=0.65, capsize=2.0`
- Significance marker line `lw=0.65` and lowered fontsize (7) for tightness
- Legend moved to `bbox_to_anchor=(0.5, 1.18)` *above* the axes (single row,
  `ncol=4`) — keeps legend out of the plotting area, no overlap
- Caption shifted *outside* the plotting area (`transform=ax.transAxes`,
  `0.0, -0.26`) at fontsize 5.8
- `dpi=600` for PNG export (skill quotes 600 as Nature minimum); SVG and PDF
  exported alongside
- `bbox_inches="tight"` on `savefig`

### What I rejected from the skill
- Did not switch to dark image-plate styling (skill mentions it for
  microscopy/volume rendering only — not relevant for ablation bars).
- Did not use direct labelling (the brief explicitly allowed legend); the
  candidate kept the legend but placed it above-axes per common-patterns.
- Did not add a *hero panel* concept — this is a single-panel figure by
  brief, so hierarchy is moot.

### Runtime notes
- Both Arial and DejaVu Sans installed; Arial is preferred and was used.
  (`font_manager.fontManager.ttflist` confirms `Arial` resident in the conda env.)
- Constrained_layout warning fired once on the first candidate save: "axes
  sizes collapsed to zero. Try making figure larger or Axes decorations
  smaller." — cosmetic; the figure rendered correctly because `bbox_inches="tight"`
  recomputed extents on save. **This is a real signal the skill's mm-precision
  layout is tight against matplotlib's caption + legend padding** — flag for
  future fork: candidate should leave a touch more vertical headroom or move
  the legend to inside-axes for very small figures.
- candidate run wall time: 1.42 s (real)
- baseline run wall time: previously rendered, ~0.7 s based on earlier run
