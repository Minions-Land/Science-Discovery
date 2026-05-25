# Graphical abstract

Provenance: scientific-writing-kdense ("Every scientific writeup MUST include a graphical abstract"). Mandatory in Cell, Cell Reports, iScience, Cell Press journals; recommended (and increasingly enforced) in Nature, Science, NEJM.

A graphical abstract is a single visual summary of the paper. It appears before/after the text abstract on the journal page and in the table-of-contents listing. Its job is to make a busy reader who scans the TOC stop and read the paper.

## Hard requirements

- **Aspect ratio**: landscape, ~2:1 (Cell prefers 1200×600 px or 5×2.5 inches at 300 dpi). Some Nature sub-journals want square (1:1).
- **Resolution**: 300 dpi at final size for raster; vector PDF preferred when text is present.
- **No more than 5–7 visual elements** in the figure. The reader processes it in < 5 seconds.
- **Self-contained**: must be readable WITHOUT the paper. No "see Fig. 3" cross-references. Define every label inside the abstract figure.
- **Color discipline**: ≤ 4 hues, ColorBrewer or hand-picked. No rainbow.
- **Font**: same family as the body figures; ≥ 9 pt at final size.
- **No text-only**: a graphical abstract that is just a paragraph in a box is not a graphical abstract.

## Content patterns (pick one)

Three patterns cover ≈ 80% of CNS graphical abstracts. Pick the one that matches the paper's contribution.

### Pattern 1 — Workflow / pipeline

Left-to-right or top-to-bottom flow: input → method → output. Use when the paper's contribution is methodological.

```
[Sample] → [Method box (named)] → [Result figure miniature] → [Headline finding text]
```

Implementation: [[figure-spec]] archetype A (boxes-and-arrows), or [[hero-figure-prompt]] for a richer illustrated version.

### Pattern 2 — Mechanism / model

A cartoon of the biological / physical / computational mechanism the paper proposes. Used when the contribution is a *new understanding* rather than a new method.

```
[Before state diagram] → [Mechanism arrow with key molecule / equation] → [After state diagram]
```

Implementation: usually [[hero-figure-prompt]] (gpt-image-2.0 with the persistent prompt file). LaTeX TikZ as fallback.

### Pattern 3 — Headline result

A single "hero plot" — the strongest single panel from the paper, blown up and cleaned. Used when the contribution is a *quantitative finding*.

```
[Hero plot, e.g. dose-response or scaling-law] + [one-line take-home in bold]
```

Implementation: [[academic-plotting]] for the plot + [[hero-figure-prompt]] for the title overlay.

## Generation routes

### Route A — gpt-image-2.0 via hero-figure-prompt

For mechanism / pipeline / illustrated abstracts. Always go through [[hero-figure-prompt]] so the prompt is persisted as `branches/writer/paper/figures/graphical_abstract.prompt.md`. Regeneration must be possible at camera-ready time.

Baseline prompt skeleton (drop into `hero-figure-prompt`):

```
Generate a graphical abstract for a Cell Press submission.
Aspect: landscape 2:1 (1200×600 px).
Style: flat vector illustration, clean lines, scientific aesthetic.
Palette: 3-4 colors, professional pastel + one accent. White background.
Layout: <left/right OR top/bottom> flow.
Elements:
  1. <element 1, e.g. "sample preparation icon">
  2. <element 2, e.g. "compute pipeline as 3-stage block">
  3. <element 3, e.g. "dose-response curve miniature">
Text: <one-line headline finding, ≤ 12 words, sans-serif, ≥ 11 pt>.
No photorealism, no 3D shading, no decorative elements, no text outside the named labels.
```

### Route B — Illustrator / Inkscape / TikZ

For pipeline / workflow abstracts where every node label needs to match the paper exactly. Vector source committed; PDF rendered at submission time.

If TikZ:
```latex
\begin{tikzpicture}[node distance=1.4cm, every node/.style={draw, rounded corners, font=\sffamily}]
  \node (x) {Input};
  \node[right of=x, node distance=2.5cm] (m) {\methodname};
  \node[right of=m, node distance=2.5cm] (r) {Result};
  \draw[->, thick] (x) -- (m);
  \draw[->, thick] (m) -- (r);
  \node[below of=m, node distance=1cm, font=\bfseries] {Headline finding here};
\end{tikzpicture}
```

### Route C — Combine routes

Most CNS graphical abstracts mix illustrated mechanism (Route A) + a small hero plot (Route B). Generate them separately, composite in Inkscape or via [[pdf-vector-layout]].

## Anti-patterns

- Cropping figure-1 of the paper and calling it a graphical abstract. Reviewers can tell.
- Putting the abstract text *into* the graphical abstract. The two are separate elements on the journal page.
- Stock photos / clip art / royalty-free icons that don't match the paper's specific science. Either commission or generate.
- Adding decorative gradients, shadows, 3D bars. CNS aesthetic is restrained.
- Forgetting to commit the source (vector / prompt). Camera-ready almost always asks for a re-render.

## File outputs

Canonical paths under `branches/writer/paper/figures/`:

- `graphical_abstract.pdf` — the rendered figure for inclusion.
- `graphical_abstract.svg` — vector source if applicable.
- `graphical_abstract.prompt.md` — the gpt-image-2.0 prompt if Route A.
- `graphical_abstract.tex` — TikZ source if Route B.
- `graphical_abstract.png` — 300 dpi preview for slides / draft.
