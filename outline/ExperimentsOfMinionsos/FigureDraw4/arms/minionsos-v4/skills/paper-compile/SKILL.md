---
slug: paper-compile
summary: Compile the LaTeX paper cleanly — run latexmk, fix the small auto-fixable errors, iterate at most 3 attempts, verify submission-shaped output. Macro-discipline lint added in v3.
layer: logical
tools:
version: 3
status: active
supersedes:
references: make-latex-model, package-submission, latex-typography
provenance: human + FigureDraw2-evidence (anti-pattern #2 macro discipline gap)
---

# Skill — Paper Compile

Clean compile, log-driven diagnosis, bounded iteration, submission-shape checks.

## When to invoke

- Before handing a draft to Reviewer or Expert for feedback.
- Before any camera-ready package.
- When `[VERIFY]` markers, `?` refs, or "Overfull \\hbox" warnings are present in the source or the last `compile.log`.

## Structure

The compilation cycle is log-driven: `latexmk` end-to-end, read `compile.log` carefully, auto-fix the small safe class (missing packages, broken refs, stale paths), escalate anything requiring scientific judgment. Iterate at most 3 attempts; every attempt must change at least one concrete source line identified from the log. The final report is compact: status, PDF path, page counts, errors fixed with line refs, warnings remaining, undefined ref / citation counts.

## Procedure

1. **Verify prerequisites.** `which pdflatex latexmk bibtex`. Ensure `branches/writer/paper/main.tex`, `*.bib`, `sections/`, and `figures/` exist. Fail fast with a clear error if not.
2. **Clean build.** In `branches/writer/paper/`: `latexmk -C` then `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex 2>&1 | tee compile.log`.
3. **Diagnose from the log, not from guesses.** Common auto-fixable: missing `.sty` (install or remove), undefined `\ref` / `\cite` (fix label / key), missing figure files (check extension), BibTeX syntax nits. Do **not** silently delete user content to make errors disappear.
4. **Iterate at most 3 attempts.** Each attempt must change at least one concrete source line from the log; no blind recompiles.
5. **Scan for overfull hboxes** (`grep "Overfull \\\\hbox" compile.log`). Fix table / equation overflows per `SYSTEM.md` table layout rules (`\resizebox`, orientation pivot, `\small`). Minor paragraph overflows (< 5 pt) may be ignored.
6. **Detect stale section files.** For every `sections/*.tex`, grep `main.tex` for its basename; warn on any unreferenced file.
7. **Macro-discipline lint (FigureDraw2 anti-pattern #2).** Before declaring success, scan the body for hard-coded names that should be `\newcommand` macros. Concretely: collect every Title-Case identifier of length ≥ 4 that appears ≥ 3 times in `sections/*.tex` AND does not match a `\newcommand{\name}` in `main.tex` preamble. Warn (not fail-by-default — Reviewer-bench evidence will tell us when to harden) for each violation, e.g. `Method-A appears 7× in body but is not macro-defined; consider \newcommand{\methodA}{Method-A\xspace}`. The bar set by FigureDraw2 was: minionsos paper-page used 6 macros while every external arm used ≤ 3. The lint output ends up in `compile.log` so future audits can verify the rule fired. Implementation hint: `python branches/writer/tools/macro_lint.py main.tex` if the helper exists; otherwise inline `grep -oE '\\b[A-Z][a-zA-Z0-9-]{3,}\\b' sections/*.tex | sort | uniq -c | awk '$1 >= 3'` and cross-check against `grep '\\newcommand' main.tex`.
8. **Post-compile checks.** PDF exists and > 100 KB; no `??` or `[?]` in output; page count within venue limit (ML: main body to end of Conclusion; IEEE: total including refs); fonts embedded (`pdffonts main.pdf | grep -v yes` is empty).
9. **Standalone-figure page-trim discipline (FD4 evidence: equation-block lost layout_density 3→2 because letter-size paper had 47% blank space below the derivation block).** When the deliverable is a *single-page LaTeX-rendered figure* (equation block, IMRAD prose section, single derivation), the page must be trimmed to content height. Two tools:
   - **Inline geometry**: `\usepackage[paperwidth=8.5in,paperheight=Hin,margin=0.75in]{geometry}` where `H` is set to actual content height. Iterate: build → measure content → re-emit with right `paperheight`. Sometimes the cleanest path is to use `standalone` document-class instead of `article`.
   - **`pdfcrop` post-build**: `pdfcrop --margins '24 24 24 24' figure.pdf figure.pdf` (re-overwrites the cropped PDF in place). Available wherever pdflatex is. Run as a final compile step for any figure-of-record PDF where the body content is < 70% of the chosen page size.
   
   The check: `pdfinfo figure.pdf | grep "Page size"` — if the height is the default 11.0in for letter-size and the content fills < 70% (estimate visually or by counting non-white pixels in the rasterised PNG), trim. A figure-of-record PDF that is 50% blank space ships a layout_density-2 score even when the prose / equations are perfect.

Keep `compile.log` on disk. Page-count claims marked `[derived: pdfinfo @ <ts>]`.

## Pitfalls

- Suppressing warnings by editing the log-reading script instead of the source. The warnings are the point.
- Auto-deleting `\usepackage` lines to clear errors — often removes load-bearing macros.
- Counting pages including references on a venue that excludes them (or vice versa). Re-check the venue rule.
