# Annotation — fig4-single-cell-systems-rich

**Source:** nature-skills `nature-figure` gallery. Multi-panel single-cell
systems composite (Nature Machine Intelligence vintage).

**Archetype:** Heatmap + dimension reduction + dendrogram composite. Use for
single-cell / -omics atlas figures with high-dimensional data.

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#eaeaea` | 20.6 | panel background tint |
| `#c0c0c0` | 16.3 | dendrogram strokes, gridlines |
| `#959595` | 15.0 | axis text, neutral data |
| `#eac0c0` | 4.1 | warm cmap mid (Reds family) |
| `#ea6a40` | **3.5** | **signal hot — UMAP cluster of interest, expression high** |
| `#ea9595` | 3.4 | warm cmap soft |
| `#c0eaea` | 3.4 | cool cmap mid (cyan / Blues) |
| `#6ac0c0` | 2.9 | signal cool — UMAP cluster contrast |
| `#6a6a6a` | 2.6 | dark text |
| `#ea6a6a` | 2.6 | warm cmap deep |

**Critical observation:** The figure uses a **diverging palette**
(`#ea6a40` warm vs `#6ac0c0` cool) for the UMAP / heatmap, with greys
absorbing 51%+ of pixels. The warm and cool signals are roughly
balanced (~3-4% each), and they sit at COMPLEMENTARY hue positions on
the wheel (orange-red vs blue-cyan). This is not a generic
RdBu_r — it's a hue-shifted diverging that reads warmer than RdBu_r
and feels less clinical, more "biological discovery."

## Typography

- Cluster labels: 7pt sans, positioned at cluster centroid in white-
  bordered text box for legibility against any background hue
- Heatmap row/column labels: 5.5-6pt, faded grey #959595
- Panel letters: bold 9pt, dark #404040
- Colourbar tick labels: 5.5pt, neutral grey

Cluster centroid labelling with a thin white halo is the signal
typographic move here. Without the halo, labels become unreadable
when they cross dark cluster regions.

## White space allocation

- Heatmap panel: ~50% of canvas (this is the hero in single-cell figs
  because heatmaps need many rows × columns to be legible)
- UMAP / scatter panels: ~20% each in upper-right
- Dendrogram + categorical bars: ~10% as side annotations to the heatmap
- Inter-panel gutter: very tight, almost touching, because the
  annotations are spatially LINKED (dendrogram pairs with heatmap rows;
  categorical bar pairs with heatmap columns)

## Visual rhythm

1. Heatmap hero — eye lands first; the diverging warm/cool pattern
   is the dominant visual cue
2. UMAP — secondary anchor, because clusters are coloured to MATCH
   the heatmap rows (cluster 1 in heatmap is same hue as cluster 1
   in UMAP)
3. Side annotations (dendrogram, group bars) — read AS PART OF the
   heatmap, not as separate panels

The "match cluster colours across panels" rule is the unifier — it
turns 3-4 panels into ONE coherent visual argument.

## What makes this figure work

1. **Cluster colours threaded across panels.** Cluster 1 = same hue in
   heatmap rows AND UMAP scatter. Reader doesn't have to remember;
   the colour is the index.
2. **Hue-shifted diverging cmap.** Warm `#ea6a40` instead of pure red,
   cool `#6ac0c0` instead of pure blue. Reads as biological-discovery
   palette, not the more clinical RdBu_r.
3. **Dendrogram + categorical bars as heatmap annotations, not panels.**
   They are spatially LINKED (touching) the heatmap, not gutter-
   separated. Communicates "these annotate the same data."
4. **White-haloed cluster labels.** Inline labels with a halo so they
   read against any cluster colour. Avoids "label crosses dark region
   and disappears."
5. **Heatmap centred at zero with explicit norm.** The diverging cmap
   is centred at 0 via `TwoSlopeNorm` (the rule from R1.A heatmap).
   Centre cell row is grey-white because exactly zero, not by data luck.

## Typical amateur deltas against this exemplar

- Cluster colours mismatched across panels (heatmap and UMAP use
  different palettes for the same biological clusters)
- Diverging cmap is RdBu_r literal — clinical, not warm
- Dendrogram floats as a separate panel with gutter — disconnected
  from the heatmap visually
- Cluster labels in legend block off to the side
- Heatmap data symmetric by luck rather than by `TwoSlopeNorm`
