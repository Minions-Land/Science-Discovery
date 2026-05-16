# Annotation — atlas-network-matrix

**Source:** nature-skills `nature-figure/assets/chart-atlas/atlas-10-network-matrix.png`.
Atlas illustration of the network + adjacency-matrix combo form.

**Archetype:** Hybrid composite — network nodes + edges + matrix in one
visual. Use when relationships between entities are the message.

**User grade (R-future-2):** "非常漂亮，虽然稍微有点看不懂，但视觉效果
极佳. 不过总体的热力图配色有点丑，用了红色和一种奇怪的湖水绿，这个配色
不太行."

## Extracted palette

| Hex | % | Role |
|---|---|---|
| `#95c0c0` | 14.8 | teal (network node face) |
| `#409595` | 14.3 | dark teal (network edges) |
| `#6ac0c0` | 8.4 | mid teal |
| `#c0c0c0` | 7.7 | grey (axis chrome) |
| **`#c04040`** | **7.1** | **signal red — flagged by user as bad pairing with teal** |
| `#6a9595` | 5.6 | dark teal mid |
| `#6a95c0` | 5.1 | accent blue |
| `#eaeaea` | 10.2 | background |
| `#959595` | 4.4 | text |

## What works (network half)

1. **Teal-family monochromatic for the network.** Nodes, edges, and
   labels all sit on the cyan-teal axis. Reads as ONE coherent network
   visual, not "blue nodes + red edges + green labels."
2. **Edge weight by stroke alpha, not hue.** Edge importance is encoded
   by alpha not by colour change — keeps the hue family pure.
3. **Node size by degree.** A common convention but executed cleanly
   here — no jitter, no stroke flashes.
4. **Labels at bezier-controlled offsets.** Labels don't overlap edges
   because they're placed on perpendicular offsets from each node.

## What does NOT work (matrix half — user-flagged)

1. **Red `#c04040` paired with teal `#95c0c0`.** Direct red-vs-teal
   complementary on a small heatmap reads as "ugly" — too high
   contrast, too saturated, no neutral buffer.

   **Fix:** for matrix-as-summary in a network composite, use single-
   hue diverging within the network's family (deep teal `#154040` to
   pale teal `#c0eaea` via TwoSlopeNorm at 0). NOT red-vs-teal.

2. **Matrix occupies 30% of canvas but information density is low.**
   The matrix is summarising the network; could be 50% smaller and
   still readable. Principle 3 (effective display area) violation.

## What makes this beyond-human (when palette is fixed)

The network half achieves:
- Nodes + edges + labels in coordinated teal-family
- Visual hierarchy via stroke weight + node size only
- No competing axis chrome — the network IS the visual

A human matplotlib networkx plotter typically:
- Uses default Spring layout that overlaps nodes
- Default node colour is azure / blue / yellow per group — multi-hue
- Edge colour is black — clashes with coloured nodes
- Includes axis ticks (irrelevant for a network plot)

The exemplar removes axis chrome and keeps only the network as the
visual subject.

## Recommended use

Re-render this figure with the matrix half in single-hue teal diverging
to remove the user-flagged "ugly red+teal" issue. Then it would be
a clean exemplar.
