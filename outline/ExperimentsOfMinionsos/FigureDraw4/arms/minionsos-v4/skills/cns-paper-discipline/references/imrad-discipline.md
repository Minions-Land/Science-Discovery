# IMRAD prose discipline

Provenance: scientific-writing-kdense (446-line SKILL, FigureDraw2 arm) + stat-writing-fuhaoda (179-line SKILL).

CNS-tier journals enforce IMRAD as a hard structure: **Introduction → Methods → Results → Discussion**. Nature Methods / Cell / Sci Adv allow Methods at the end of the body ("Online Methods") instead of in the middle, but IMRAD slots are the same.

## Hard rule: full-paragraph prose, no bullets in body

**The single most-violated rule in MinionsOS Writer's drafts.** CNS reviewers expect every section of the body to be flowing prose. Bullet lists are reserved for:

- Author contributions block.
- Data / code availability statement.
- Specific structured sections that the journal explicitly invites (e.g., NEJM clinical trials' "Highlights" structured abstract).

Everywhere else: bullets are wrong. Convert with this two-stage workflow:

### Two-stage outline → prose

**Stage 1 — outline file** (allowed to be bulleted, lives in `notes/outline_<section>.md`):
```
## Introduction
- Hook: prevalence of X (with cite)
- Open problem: existing method Y fails because Z
- Our contribution: 3 bullets
- Roadmap: "In this work..."
```

**Stage 2 — prose file** (the actual `sections/01_intro.tex`):
> X is a prevalent condition affecting Y million patients globally [cite]. Existing computational approaches, while accurate on benchmark Z, suffer from limitation L when deployed in setting S, leading to error rate E [cite]. Here we introduce \methodname, which addresses L by ... We demonstrate (i) ..., (ii) ..., and (iii) ... . The remainder of the manuscript is organised as follows: Section 2 ...

No intermediate bulleted draft in the .tex. The outline stays in `notes/`; the prose file is born already-prose.

## Per-section guidance

### Introduction (3-5 paragraphs)

- **Para 1**: Field-level context + significance hook. Cite review articles. End with a problem statement.
- **Para 2**: State of the art for the specific problem. Cite 5-10 most relevant prior works. End with the gap.
- **Para 3**: Our approach. Name the method (use `\methodname` macro). State the 3 contributions concretely.
- **Para 4 (optional)**: Roadmap. "Section 2 introduces..., Section 3 reports..., Section 4 discusses...". Some venues prohibit roadmap paragraphs (Nature does); check the author guide.
- **Para 5 (optional)**: Plain-language summary if the venue requires one.

### Methods (CNS often last; ML often second)

- Always reproducible-detail-first. Animal IDs, cell-line provenance, antibody catalog numbers, software versions, random seeds, hyperparameters.
- ML/CS: "Algorithm 1" pseudocode block; data preprocessing in numbered subsections; train/val/test split fully specified.
- Wet-lab: Reagents → Protocols → Data acquisition → Statistics. Each subsection 1-3 paragraphs.
- **Statistics paragraph is its own subsection.** Test name, two-tailed/one-tailed, multiple-comparison correction, software (R version), exact p-value reporting policy.

### Results (the heart — usually 4-6 figure-anchored sections)

- **One paragraph per figure or table** is a CNS norm. "Figure 2 shows ... \methodname achieves X (Δ Y) compared to baseline (cite Fig. 2). This improvement holds across all subgroups (Fig. S1)."
- Always state effect size + statistic, never just "significantly higher".
- End each results paragraph with a one-sentence interpretation, not a transition.
- **Subheadings allowed and encouraged** (Nature uses bold lead-ins; Cell uses subsection titles). Each subheading becomes the take-home claim of that block.

### Discussion (2-4 paragraphs)

- **Para 1**: Re-summarise findings in plain language (not a verbatim repeat of abstract). 3-5 sentences.
- **Para 2-3**: Implications + limitations. Limitations are mandatory — "Our study has the following limitations...".
- **Final para**: Future work (one paragraph, concrete).

## Paragraph template patterns to imitate

Three templates extracted from kdense arm's drafts that scored well in FigureDraw2 reviewer_readiness:

**Template A — Claim → Evidence → Interpretation (results paragraph)**:
> [Claim sentence: what we found.] We measured X across N subjects (M ± SD; range R). [Evidence: figure reference + key statistic.] As shown in Fig. K, methodname yields X = M ± SD vs. baseline X' = M' ± SD' (paired t-test, t = T, p = P, Cohen's d = D). [Interpretation: 1 sentence.] These results indicate that [scientific implication], consistent with [prior work or hypothesis].

**Template B — Background → Problem → Approach (intro paragraph)**:
> [Domain context with cite.] X is a [importance + scale]. [State of art with cite.] However, current approaches Y are limited by [specific limitation], particularly when [specific scenario]. [Our move.] To address this, we propose Z, which [one-line mechanism], thereby achieving [headline outcome].

**Template C — Method-statement (methods paragraph)**:
> [Method name in bold lead-in or as subheading.] We implemented \methodname using [framework / library, version]. [Inputs.] The model takes [input description] and outputs [output description]. [Training detail.] Training used [optimiser, schedule, batch, steps, hardware], with hyperparameters selected on the validation set (Table SX). [Reproducibility hook.] Code and trained checkpoints are available at [URL].

## Output-format discipline (figure of record)

**FD3 evidence**: imrad-section scored 19/24 with `typography = 2 / 3` and `vector_fidelity = 2 / 3` as the lowest dimensions. The prose was correct; the *rendered PDF* leaked rasterised LaTeX defaults — Type-3 fonts, no `\newcommand` macros for repeated entities (\methodname, \pvalue, journal abbreviations), no `pdf.fonttype` discipline on companion figures. The text-side wins are wasted if the figure-of-record fails on grader's vector / typography axes.

When the imrad-section deliverable is compiled to a single-page PDF (which is the figure-of-record for grading and for many submission systems), the prose-author MUST also enforce the compile-side discipline. Cross-skill checklist:

| Check | Source skill | What it looks like in `main.tex` |
|---|---|---|
| Type-1 fonts only (no Type-3 raster) | [[paper-compile]] §pdf-fonttype-check | Preamble: `\pdfmapfile{=pdftex.map}` and use `lmodern` / `newpxtext+newpxmath` / `mathptmx`. Verify with `pdffonts main.pdf \| grep -i "type 3"` returning nothing. |
| Macro discipline for repeated entities | [[paper-compile]] §macro-discipline-lint | `\newcommand{\methodname}{RetroDiff}` defined once, used everywhere. Lint script in [[paper-compile]] step 7. ≥ 3 macros for any non-trivial Methods section. |
| Booktabs grouping for any inline tables | [[latex-typography]] §booktabs-grouping-recipe | `\toprule` / `\midrule` / `\bottomrule` only. `\multicolumn` + `\cmidrule(lr){i-j}` for grouped headers. No `\hline`, no vertical rules. |
| Em-dash / en-dash / minus discipline | [[latex-typography]] §dash-discipline | `---` for em-dash, `--` for en-dash (number ranges), `$-$` for minus. Mixing them is the typography-axis-2 trigger. |
| Reporting-guideline anchor | [[cns-paper-discipline]]/references/reporting-guidelines.md | Methods prose names the guideline (CONSORT/STROBE/PRISMA/ARRIVE) explicitly in the first sentence and threads the relevant items through the section. |
| Vector-figure check on companion figures | [[paper-compile]] §vector-fidelity-check | Any embedded figure compiled to PDF must pass `\matplotlib.rcParams["pdf.fonttype"] = 42`, `["ps.fonttype"] = 42`, and `bbox_inches="tight"` on save. |

The author of the imrad section is responsible for *naming* these checks in the deliverable and either running them or noting that the runner has done so. A bare `main.tex` compiled to PDF without these gates is a typography-axis regression even if the prose is perfect.

## Pitfalls

- Bullet residue in `.tex`. Re-grep `\\item` in body files; flag every match.
- Generic results sentences ("OursModel performs better"). Always include effect size + statistic.
- Discussion that re-states results without interpretation. The discussion is for *meaning*, not summary.
- Limitations buried in Methods or skipped. Make them their own paragraph.
- Methods missing reproducibility detail (seed, version, hardware). Reviewers will request it; pre-empt.
