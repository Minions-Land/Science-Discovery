# Fixture: imrad-section

## Task
Given the bullet-pointed outline of one paper section (Methods) for a Cell-tier observational cohort study on liver fibrosis, expand it into full-paragraph prose suitable for direct inclusion in main.tex. STROBE reporting guideline applies.

The outline is intentionally bulleted so the test is whether the agent does the two-stage outline → prose conversion (no bullets in body) and whether STROBE items are mapped to specific sentences.

## Inputs
- outline.md: the bulleted outline of the Methods section.
- claim.json: study type + sample size + key statistical method.

## Outputs (cwd)
- figure.pdf, figure.png  (a single-page PDF rendering of the prose Methods section, compiled from main.tex via pdflatex; acts as the figure of record for grading)
- main.tex                (the full-prose Methods section — 3-5 paragraphs, no bullets, full STROBE coverage)
- caption.tex             (a one-sentence figure caption stating the section / venue / STROBE items covered)
- gen_figure.py           (the script that compiled main.tex to figure.pdf)

## Hints
- Two-stage rule: outline.md is allowed to be bulleted (it is the input). main.tex MUST be flowing prose, no `\item`, no bullet lists.
- STROBE items 4-12 are the Methods scope (study design, setting, participants, variables, data sources, bias, study size, statistical methods). Each must be addressed in the prose.
- Paragraph templates: Claim → Evidence → Interpretation; Method-statement (named subsection or bold lead-in).
- This figure is graded as much for prose quality as for compilability. Grader will check: paragraph structure, STROBE item coverage, full-prose discipline, reproducibility detail (seed / version / hardware where applicable for the cohort study's analytics pipeline).
