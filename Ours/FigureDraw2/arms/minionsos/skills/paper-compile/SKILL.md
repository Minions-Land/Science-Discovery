---
slug: paper-compile
summary: Compile the LaTeX paper cleanly — run latexmk, fix the small auto-fixable errors, iterate at most 3 attempts, verify submission-shaped output.
layer: logical
tools:
version: 2
status: active
supersedes:
references: make-latex-model, package-submission
provenance: human
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
7. **Post-compile checks.** PDF exists and > 100 KB; no `??` or `[?]` in output; page count within venue limit (ML: main body to end of Conclusion; IEEE: total including refs); fonts embedded (`pdffonts main.pdf | grep -v yes` is empty).

Keep `compile.log` on disk. Page-count claims marked `[derived: pdfinfo @ <ts>]`.

## Pitfalls

- Suppressing warnings by editing the log-reading script instead of the source. The warnings are the point.
- Auto-deleting `\usepackage` lines to clear errors — often removes load-bearing macros.
- Counting pages including references on a venue that excludes them (or vice versa). Re-check the venue rule.
