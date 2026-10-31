# Fixture: cns-graphical-abstract

## Task
Produce a graphical abstract for a Cell-tier submission. The paper introduces RetroDiff, a retrieval-augmented diffusion method for chemical generation. Output a single landscape figure (figure.pdf, ~1200×600 px equivalent / 2:1 aspect) suitable for the journal table-of-contents listing.

The contribution should be conveyed in ≤ 5 visual elements. Reader should grasp it in < 5 seconds without consulting the paper body.

## Inputs
- claim.json: the system name, three claims, retrieval mechanism, target chemistry. Use this as the scientific content.
- captions.json: not used for this fixture.

## Outputs (cwd)
- figure.pdf, figure.png   (the graphical abstract; landscape 2:1 aspect)
- caption.tex              (one-line graphical-abstract caption — usually a take-home statement)
- gen_figure.py            (the generation script — matplotlib + tikz + pdflatex acceptable; AI-generation route also acceptable but include a stub script that can re-render from a saved prompt)

## Hints
- Pattern: pick "workflow" / "mechanism" / "headline result" — see graphical-abstract.md guidance if your loaded skills include cns-paper-discipline.
- ≤ 4 hues, ColorBrewer or hand-picked. White background.
- Self-contained: no "see Fig. 3" cross-references.
- Font ≥ 9 pt at final size.
- One headline-finding sentence (≤ 12 words) embedded in the figure.
- This figure is graded against CNS journal expectations (Cell, Nat Commun, Sci Adv).
