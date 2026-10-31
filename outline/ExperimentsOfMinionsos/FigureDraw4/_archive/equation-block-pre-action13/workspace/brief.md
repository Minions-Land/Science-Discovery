# Fixture: equation-block

## Task
Produce a single-page "derivation block" - render 3 numbered display equations with derivation chain, plus surrounding prose that cross-references them. Output as figure.pdf (a real PDF rendered by pdflatex from your equations.tex) plus figure.png raster.

The content is RetroDiff's training objective derivation:
  1. Variational lower bound (ELBO) of the diffusion model
  2. Decomposition into reconstruction + KL terms
  3. The retrieval-augmented variant (the new contribution): conditioning on retrieved exemplars

This tests both LaTeX math typesetting AND mathematical typography (align, cases, qed-style derivations, equation numbering, \eqref).

## Inputs
- claim.json: {variables, equations, prose_hints}
  variables tells you what each symbol stands for; equations are the canonical TeX source for each numbered equation.

## Outputs (cwd)
- figure.pdf, figure.png   (a single-page PDF rendered from the equations + prose)
- equations.tex            (the standalone .tex with the three numbered equations + prose)
- caption.tex              (the LaTeX caption)
- gen_figure.py            (calls pdflatex)

## Hints
- Use align or align* environments; number equations with \label{eq:...}.
- Cross-reference with \eqref{eq:...}.
- Variables should be italic (default LaTeX behaviour); operators (log, KL) upright.
- Use \mathbb{E}, \mathcal{L}, \mathrm{KL} for stylistic distinctions.
- The prose between equations should describe the derivation step, not just say "by Jensen".
