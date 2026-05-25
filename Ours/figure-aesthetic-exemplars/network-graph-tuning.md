# Network / graph figure tuning

**scope**: `graph-network-only` — community / graph / network archetype only. Do NOT load for stacked-bar, grouped-bar, ablation tables, or any figure where categories are proportions or counts rather than nodes-and-edges. (See [[figure-aesthetic-exemplars]] master SKILL.md "Sub-skill scope matching" for the dispatch rule.)

**Provenance**: FigureDraw2 borrow #4 — `scientific-writing-kdense` arm won the network-graph cell at 21/24 (gap +6 over the loser). Its palette mean was 2.31, the highest in the entire FigureDraw2 round. **FD3 follow-up evidence**: when this skill was loaded unconditionally for every figure type, stacked-bar regressed 19→17 (ColorBrewer Set2 was applied to a 4-class proportion bar where it doesn't fit) and network-graph itself regressed 20→16 (the 30-node, ~5-degree-mean fixture had `max_degree/min_degree ≈ 1.5`, so `node_size ∝ degree` produced visually identical bubbles, killing hierarchy). The rules below are now gated to the conditions where they actually win.

## When to apply (opt-in gate)

Apply the full rule set only when **all** of the following hold:

- Archetype is network / graph / community (nodes + edges; not bars / boxes / heatmap cells).
- `len(G.nodes) >= 20`. Below 20 nodes the hairball failure mode is unlikely; freestyle layout is usually fine and over-applying these rules looks fussy.
- The visual question is "what is the community / cluster structure?" — not "what is the path between A and B?" (path-style graphs want clearer edge labels and arrowheads — see [[figure-spec]] architecture archetype).

If `len(G.nodes) < 20`, fall back to [[figure-layout-defaults]] + [[academic-plotting]] alone. Do NOT layer this skill on top — the constants below are tuned for visual density, not for sparse small graphs.

## Defaults that prevent hairball

- `edge_alpha = 0.30`. Dial up to 0.50 only if `len(edges) < 50`.
- **`node_size`: degree-conditional, NOT unconditional proportional.** Compute `degrees = [G.degree(n) for n in G.nodes()]; ratio = max(degrees) / max(min(degrees), 1)`. Then:
  - If `ratio > 3`: scale — `node_size = [60 + 12 * d for d in degrees]`. The visual hierarchy is real and the eye can read it.
  - If `ratio <= 3` (a "flat-degree" graph): use a constant `node_size = 120`. Proportional sizing on a flat-degree graph produces near-identical bubbles, which the reader misreads as a *failed* attempt at hierarchy. A clean constant size says "degree is uniform, look at the structure instead."
  - Always state which mode you used in the caption (see Caption requirements below).
- `edge_width ∝ weight` if the edges have weights. Otherwise constant `0.6`.
- Layout: `nx.spring_layout(G, seed=PINNED_SEED, k=0.4, iterations=100)` for `len(G.nodes) <= 50`; `iterations=200` and `k=0.5` for 50–100 nodes. **Pin the seed in a script-level constant** so the figure is reproducible. `random_layout` is forbidden — it changes every render.
- Background: matplotlib default white; never grey or off-white (clutter).

## Color discipline

- Communities / clusters: use **ColorBrewer Set2** (8 colors) or **Dark2** (8 colors). They are designed for categorical-without-direction data.
- DO NOT use `tab10` — too saturated, suggests directionality the data does not have.
- DO NOT use any palette where one color is significantly brighter — readers will read it as the "important" community.
- If communities are > 8, merge the smallest two repeatedly until ≤ 8, OR switch to a continuous-blue gradient by community size. Never go to 12-color rainbow.

## Edge labels and weights

- Edge labels (text on edges) are **almost always noise**. Show edge weight via `linewidth` or `alpha`, not text.
- Exception: if the figure shows a small DAG (≤ 8 nodes) where each edge represents a named transformation, edge labels are mandatory. But that figure should probably be in [[figure-spec]] (architecture) not here.

## Layout rescue

If the spring layout produces a hairball (visual density > ~70%):

1. Try `kamada_kawai_layout` — slower but cleaner separation for medium graphs.
2. Reduce edge density first: keep only the top-k edges by weight per node, OR threshold edges by weight quantile.
3. As a last resort, switch to `circular_layout` and accept that the spatial encoding now means nothing — edges are the only signal.

## Caption requirements

Must state:
- Number of nodes and edges.
- The community detection algorithm (Louvain, Leiden, modularity-greedy).
- The pinned random seed.
- Layout algorithm used.
- The node-size mode: either "node size proportional to degree (max/min ratio = X.X)" or "constant node size (degrees flat: max/min ratio ≤ 3)".
- **A quantitative finding about the community structure (FD4 evidence: v4 dropped scientific_clarity 2 + caption_quality 2 because caption listed only layout parameters, no findings).** Pick one:
  - **Modularity Q** of the partition (Newman's Q). `nx.algorithms.community.modularity(G, communities)` for `networkx ≥ 2.6`. Q > 0.3 is "meaningful community structure"; Q > 0.5 is "well-separated".
  - **Inter/intra-community edge ratio**. State the fraction of edges that are *within* a community vs *between* communities. A high within-fraction (≥ 0.7) confirms the partition.
  - **Largest-component size + density**. If the graph has multiple connected components, name the size of the largest and its edge density.

The caption must answer "did the partition find real community structure?" — not just "what colors did we use?". A modularity Q of 0.42 in the caption is one number worth more than three sentences of layout parameters.

"Network of 30 nodes and 47 edges, colored by Louvain community (4 detected, modularity Q = 0.42). Spring-layout with seed=42, k=0.4, iterations=100. Constant node size (degrees flat: max/min ratio = 1.5). Within-community edges account for 73% of all edges (34/47), confirming meaningful cluster separation."
