---
slug: make-latex-model
summary: Scaffold a clean LaTeX paper project under branches/writer/paper/ matching the target venue's style — minimal, compilable skeleton ready for prose.
layer: logical
tools:
version: 2
status: active
supersedes:
references: paper-compile, end-to-end-paper-workflow
provenance: human
---

# Skill — Make LaTeX Model

Minimal, compilable skeleton with the correct venue style, section layout matching venue norms, and the conventions `paper-compile` and `citation-audit` rely on.

## When to invoke

- At the start of a paper-writing phase, before any section drafting.
- When switching venue — re-scaffold, do not patch the old one.

## Structure

Directory layout under `branches/writer/paper/`:

```
main.tex     sections/     figures/     tables/     references/     notes/     build/
```

`main.tex` is the only entry point; sections are `\input{sections/NN_<name>.tex}` files, two-digit prefixed so lexical order = document order. Citation command matches venue: `natbib` (`\citep` / `\citet`) for ML / NLP / CV venues; numeric `\cite{}` for IEEE. Each section file starts with a `% [VERIFY]` marker list of outstanding claims.

## Procedure

1. **Identify the venue.** ICLR / NeurIPS / ICML / CVPR / ACL / AAAI / IEEE journal / IEEE conf. Fetch the official style file from the venue page; do not reuse an old copy without checking the year.
2. **Create the layout** under `branches/writer/paper/` with the structure above.
3. **Seed sections** matching venue norms: abstract, introduction, related work, method, experiments, conclusion, (ethics / reproducibility / limitations where required). Each starts with `% [VERIFY]` list.
4. **Wire citations.** Pick the citation command matching venue (`natbib` for ML / NLP / CV; numeric `\cite{}` for IEEE). Create `references/references.bib`.
5. **Add preamble hygiene.** `\usepackage{cleveref}` + `\crefname` for custom theorem envs; `hyperref` loaded last; `microtype`; `booktabs` for tables. The style file's own conventions (font, margins) are not overridden.
6. **Verify compile.** Run `paper-compile` on the empty skeleton. Must produce a valid PDF with no undefined refs before any real content is added.
7. **Announce on EACN** the venue, style file version / source, section layout, and that the empty skeleton compiles. Venue facts marked `[derived: venue page <URL> @ <ts>]`.

## Pitfalls

- Copy-pasting last year's style file. Venue rules drift; always pull the current one.
- Mixing citation styles (`\citep` in one section, `\cite` in another). Pick one per venue and lock it.
- Letting `main.tex` grow beyond preamble + `\input` lines. Content belongs in `sections/`.
