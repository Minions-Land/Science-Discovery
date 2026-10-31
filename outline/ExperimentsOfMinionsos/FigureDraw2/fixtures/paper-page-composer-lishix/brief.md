# Fixture: paper-page (MinionsOS-only)

## Task
Produce a 2-3 page submission-shaped LaTeX paper section that REFERENCES four already-produced figures (which I will provide in this directory as `fig01.pdf` ... `fig04.pdf`). The paper should:

- Have a title, abstract (~150 words), and TWO sections (Method + Results).
- Use macro-driven naming: \newcommand{\methodname}{...} for the method name.
- \includegraphics{fig01} ... \includegraphics{fig04} with full \caption referencing the data shown.
- Use \Cref/\cref or \ref consistently across sections.
- Compile cleanly with `pdflatex` (or `latexmk`) -- main.pdf must exist.
- Run a final pdf-vector-layout pass on main.pdf if the produced PDF needs spacing tightening.

## Inputs
- fig01.pdf, fig02.pdf, fig03.pdf, fig04.pdf  (four figures provided)
- captions.json: {fig01: "...", fig02: "...", fig03: "...", fig04: "..."} (the caption text for each)
- claim.json:    the scientific story this section needs to tell, with a method name and 3 hard claims

## Outputs (cwd)
- main.tex, main.pdf
- references.bib (small; you may use only the cite keys present in claim.json)
- compile.log
- (optional) main_polished.pdf if pdf-vector-layout was applied

## Hints
- Apply latex-typography (macro discipline, no hard-coded names).
- Apply paper-compile (clean log, no undefined refs, fonts embedded).
- Apply submission-cleanup-audit on the final PDF.
- Apply pdf-vector-layout if there's a layout issue worth surgery (note in compile.log if you applied it).
- 2 pages target; 3 pages OK.
