---
slug: cns-paper-discipline
summary: Cell / Nature / Science / NEJM submission discipline — IMRAD structure, reporting guidelines (CONSORT/STROBE/PRISMA/ARRIVE), mandatory graphical abstract, full-paragraph prose (no bullets in body), and venue-specific submission shape. New top-level skill, prioritised over generic academic-plotting/latex-typography for CNS-tier targets.
layer: logical
tools:
version: 1
status: active
supersedes:
references: academic-plotting, latex-typography, paper-compile, hero-figure-prompt, abstract-writing, conclusion-limitation, methodology-discipline, related-work-discipline, caption-revision
provenance: FigureDraw2-evidence (synthesized from scientific-writing-kdense + stat-writing-fuhaoda; new top-level skill — fills MinionsOS's CNS-coverage gap surfaced in v2 grader)
---

# Skill — CNS Paper Discipline

MinionsOS's existing writer skills target ML / NeurIPS norms by default. **Cell, Nature, Science, NEJM and their sub-journals add hard requirements that those skills don't enforce**:

- IMRAD structure with full-paragraph prose (no bullet lists in body — the kdense arm's #1 rule, 446 lines of skill).
- Mandatory **graphical abstract** plus 1-2 additional schematic figures.
- A reporting guideline that fits the study type (CONSORT for trials, STROBE for observational, PRISMA for reviews, ARRIVE for animal, MIAME for microarray, COREQ for qualitative).
- Specific abstract length budgets (Nature: 150-200 words; Cell: 150 words; Science: 125 words main + structured 200-word "editor's summary").
- Hard rule: "results lead, methods last" (Nature inverts the IMRAD body order — methods at end).
- Author contributions, data availability, and code availability statements are mandatory and audited.

MinionsOS hadn't covered any of these explicitly. This skill is the index — full guidance lives in three sub-skill reference files.

## When to invoke

- Target venue is Nature / Cell / Science (or any sub-journal: Nat Commun, Nat Methods, Cell Reports, Sci Adv, etc.).
- Target venue is NEJM, JAMA, Lancet, BMJ.
- Target venue is a journal that lists CONSORT / STROBE / PRISMA / ARRIVE in its author guidelines.
- User explicitly says "this is for a CNS submission" or "this is wet-lab / clinical / observational".

## When NOT to invoke (route to ML-tier instead)

- NeurIPS / ICML / ICLR / ACL / CVPR — load [[ml-paper-writing-conventions]] (see plan §next-round) or just [[academic-plotting]] + [[latex-typography]].
- arXiv preprint without a target journal — usually ML-tier conventions are fine; defer this skill until venue is decided.
- Workshop paper, short paper, extended abstract — too short for IMRAD / graphical abstract.
- Internal report, technical memo, lab note — overkill.

## Three sub-skills

| Sub-skill | File | Purpose |
|---|---|---|
| IMRAD prose discipline | `references/imrad-discipline.md` | Full-paragraph rule, IMRAD slot-by-slot guidance, paragraph-template patterns, the "two-stage outline → prose" workflow |
| Reporting guidelines | `references/reporting-guidelines.md` | CONSORT / STROBE / PRISMA / ARRIVE / MIAME / COREQ — when to use which, the checklist items, where they go in the manuscript |
| Graphical abstract | `references/graphical-abstract.md` | Mandatory figure spec, generation routes (gpt-image-2.0 / Illustrator / TikZ), aspect ratio, content discipline |

Open the relevant sub-skill when starting a section. The full file count is small; do not preload all three.

## Procedure

1. **Confirm the venue and study type** in one sentence. "Nat Commun submission, observational cohort study, n=2400."
2. **Pick the reporting guideline** from `references/reporting-guidelines.md` based on study type. The 32-item STROBE checklist (or CONSORT-25, PRISMA-27, ARRIVE-21) becomes the contract for what the manuscript must contain.
3. **Outline the IMRAD body** following `references/imrad-discipline.md`. Two-stage rule: outlines first (bullets allowed in the outline file), then prose conversion (no bullets in main.tex body).
4. **Plan the graphical abstract** using `references/graphical-abstract.md` early. CNS submission portals reject manuscripts that lack one. Generate via [[hero-figure-prompt]] in parallel with prose drafting; do not leave it for the last day.
5. **Hand off to existing skills for downstream**: figures via [[academic-plotting]] / [[figure-spec]] / [[figure-chart-atlas]], LaTeX via [[latex-typography]] / [[paper-compile]] / [[make-latex-model]], polish via [[caption-revision]] / [[submission-cleanup-audit]].
6. **Audit**: after compile, the reporting-guideline checklist must be re-walked end-to-end. Append the checklist item-by-item to `compile.log` with PASS / TODO / N/A — TODO items block submission.

## Pitfalls

- Treating IMRAD as flexible. CNS reviewers actually do reject papers that put methods between intro and results.
- Skipping the graphical abstract. "We'll add it later" → it's at submission deadline, half-rendered, and the paper looks unfinished.
- Picking a reporting guideline by guesswork. If you're not sure whether STROBE vs CONSORT applies, ask the user — the wrong checklist makes the manuscript fail external audit.
- Bullet lists in the body. Common bug from MinionsOS Writer when running fast — every bullet must become a sentence. The kdense arm spent 446 lines on this rule for a reason.
- Forgetting Author Contributions / Data Availability / Code Availability statements. These are auto-rejection items at most CNS sub-journals.
- Using ML-tier formatting (numbered citations, narrow margins, double-column) on a Nature submission. Different houses, different shapes.

## Related

- [[hero-figure-prompt]] — the graphical abstract is best generated through this skill.
- [[caption-revision]] — every figure caption in a CNS submission goes through one revision pass.
- [[abstract-writing]] — venue-specific abstract budgets are enforced here.
- [[submission-cleanup-audit]] — final check before package upload.
