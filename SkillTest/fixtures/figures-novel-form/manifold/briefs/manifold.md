# Figure brief: manifold — single-cell trajectory

**Type:** figure — single-panel (or 2-panel max) manifold visualisation
**Use in:** R-future-3 Task 1 manifold-form validation
**Data:** `../data/manifold-cells.csv` (1000 cells × 6 columns:
cell_id, x, y, cluster {progenitor / intermediate / terminal_A / terminal_B},
pseudotime, gene_marker_pct)

## Scientific claim the figure must defend

> Cells differentiate from a progenitor cluster through an intermediate
> trajectory toward two terminal fates (A and B). The bifurcation occurs
> midway along the pseudotime axis, and gene_marker_pct increases
> monotonically with pseudotime in terminal A but plateaus in terminal B.

## Required content

The data has natural 2D geometric structure with:
- 4 clusters
- A trajectory (pseudotime gradient) from progenitor through intermediate
  to two terminal fates
- A continuous expression value (gene_marker_pct) that varies along the
  trajectory

## Style requirements

- Single panel preferred (or 2-panel max if showing trajectory + marker
  expression separately)
- Two-column width OK (~120-180 mm)
- Editable text in SVG, sans-serif Arial 7-pt body
- The figure must communicate the **trajectory and bifurcation visually**.
  Clusters with same colour are NOT enough — the geometric structure
  itself must be the visual subject.

## Failure modes the runner should fix

- **Reaching for PCA scatter coloured by cluster.** Loses the trajectory
  + branch information; hard to read.
- **Defaulting to bar chart of cluster sizes** + separate violin of
  marker_pct per cluster. Loses ALL the geometric structure.
- **Heatmap of cluster × pseudotime bins.** Discretises continuous
  pseudotime; loses the trajectory shape.
- **Default matplotlib `tab10` palette** for clusters. Multi-hue
  distinct hues; violates Principle 1 (色调一致性).
- **Saturated colours** at full alpha for cluster fills. Violates
  Principle 2; obscures background context.

## Reference rewrite expectations (for scoring)

A passing rewrite should:

1. Pick a **manifold visualisation** as the primary form (not bar / line /
   heatmap)
2. Show the trajectory shape (curve from progenitor through intermediate
   to bifurcation point and onward to terminal_A / terminal_B)
3. Use a single hue family (e.g. blue, with saturation gradient OR
   distinct cluster hues all within the cool family)
4. Encode pseudotime via colour gradient OR via plotting order (so it
   visually flows)
5. Annotate the bifurcation point and terminal fates inline (not in a
   separate legend block)
6. Apply Principle 2 (饱和度淡): cluster fills at ~50-70% saturation
7. Apply Principle 5 (form novelty): the geometric STRUCTURE of the
   data is the visual subject

## R-future-3 hypothesis

If candidate (figure-aesthetic-exemplars skill loaded, including the
diffusion_swiss_roll exemplar's annotation card) picks a manifold form
while baseline picks PCA-scatter or bar/violin, the skill demonstrably
encodes the form-novelty axis — not just colour discipline.
