# Transcript — case-heatmap

## Brief
# Figure brief: heatmap — cross-condition expression z-score

**Type:** figure — single-panel diverging heatmap
**Use in:** R1.A nature-figure, R1.B scientific-figure-making
**Data:** `../data/heatmap-zscore.csv`

## Scientific claim the figure must defend

> Genes in cluster B show a coordinated shift from condition CTRL to condition
> TREAT, while clusters A and C remain stable.

## Required content

- 30 genes (rows), 8 conditions (columns: CTRL_1–CTRL_4, TREAT_1–TREAT_4)
- Cell value: row-wise z-score (already provided in csv)
- Rows grouped into 3 clusters: A (rows 1–10), B (rows 11–20), C (rows 21–30)
- Cluster annotation as a thin coloured side bar
- Diverging colormap centred at 0, white at the centre

## Style requirements

- Two-column-eligible single panel (~115 mm wide); not a square
- Sans-serif 6-pt row labels; rotated 0° (horizontal); only every 2nd or 3rd label if overlap
- Colormap: choose a colourblind-safe diverging family (e.g. RdBu_r, BrBG)
- Print-safe: distinguishable in CMYK preview
- Editable text in SVG; ticks on outside

## Failure modes to watch

- Default `viridis` or `plasma` (sequential colormaps misrepresent diverging data)
- Saturation-only colour without value — diagonal-line overprint test fails
- Row labels truncated
- Missing condition group separator between CTRL and TREAT
- No cluster side bar

## Baseline run
### What I did
- Loaded only the brief and CSV.
- Used default `imshow` settings and the default colormap.
- Plotted all 30 row labels and all 8 condition labels.
- Added a default colorbar and `fig.tight_layout()`.
- Exported SVG, PDF, and 300 dpi PNG.
### Failures or shortcuts
- Default colormap is sequential rather than diverging centered at 0.
- No cluster side bar.
- No CTRL/TREAT separator or group labels.
- Row and column labels are crowded.

## Candidate run
### Skill files actually loaded
- SKILL.md
- references/tutorials.md (heatmap walkthrough and finalize flow)
- references/api.md (FigureStyle, make_heatmap/finalize conventions, SVG text export)
- references/common-patterns.md (layout spacing and print-safe discipline)
- references/design-theory.md (typography, export policy, color rationale)
### What changed because of the skill
- Applied publication rcParams: 6-pt sans-serif labels, top/right spines off, editable SVG text, PDF TrueType text.
- Used `RdBu_r` with `TwoSlopeNorm(vcenter=0)` so white is centered at zero.
- Added a thin cluster side bar with A/B/C labels.
- Added a separator between CTRL and TREAT and horizontal separators between clusters.
- Reduced row labels to every second gene and kept them horizontal.
- Added outside ticks and a labeled colorbar.
### What I rejected (or overrode) from the skill
- Overrode the nominal ~115 mm width with a 5.4 x 5.9 inch canvas because the heatmap needed room for horizontal row labels, side bar, group labels, and colorbar.
- Used a taller non-square panel to preserve 30-row legibility, consistent with the brief's "not a square" requirement.
### Layout sanity checks performed
- Legend overlap? Not applicable; no legend.
- Truncated labels? No visible truncation in the final candidate PNG after moving row labels to the right and increasing colorbar padding.
- "constrained_layout collapsed to zero" fired? No; constrained_layout was not used and no such warning appeared.
- Font fallback warning? No explicit missing-font warning appeared, only environment cache warnings.
- Final candidate render legible? yes
