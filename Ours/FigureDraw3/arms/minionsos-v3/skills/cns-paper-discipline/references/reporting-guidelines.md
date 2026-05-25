# Reporting guidelines (CONSORT / STROBE / PRISMA / ARRIVE / MIAME / COREQ)

Provenance: scientific-writing-kdense lists these as "reporting guidelines that fit the study type". CNS-tier journals enforce them at submission — manuscripts without the matching checklist are returned at the editorial-screening stage.

## Decision: which guideline

| Study type | Guideline | Items | When required |
|---|---|---|---|
| Randomised controlled trial | **CONSORT 2010** | 25 | Mandatory: NEJM, JAMA, Lancet, BMJ, Cell journals reporting RCTs. |
| Observational cohort / case-control / cross-sectional | **STROBE** | 22 | Mandatory: Lancet, BMJ; recommended: Nat Commun, Cell Reports for clinical/cohort studies. |
| Systematic review / meta-analysis | **PRISMA 2020** | 27 | Mandatory in all CNS sub-journals for any review claiming "systematic". |
| Animal preclinical study | **ARRIVE 2.0** | 21 (Essential 10 + Recommended 11) | Mandatory: Nature, all sub-journals; required by 1000+ journals via ICLAS. |
| Microarray / transcriptomic | **MIAME** | 6 categories | Required by Nat Methods, Cell, Science for any expression-array study. |
| Qualitative research | **COREQ** | 32 | NEJM, Lancet, BMJ qualitative pieces. |
| Diagnostic accuracy | **STARD 2015** | 30 | NEJM, Lancet, JAMA, Radiology. |
| Computational reproducibility | NEURIPS / ICML reproducibility checklist + project's own | varies | Top ML venues now require explicit reproducibility statement. Nature has a separate "Reporting Summary" for CS submissions. |

If in doubt, ask the user. Picking the wrong checklist is worse than admitting uncertainty.

## Where the checklist items go in the manuscript

Different guidelines distribute their items across different sections; the manuscript must satisfy each item *somewhere*, and the cover-letter / supplementary checklist file states *where*.

### CONSORT skeleton (RCT)

| Item | Section | Critical content |
|---|---|---|
| 1a/1b — Title + abstract | Abstract | "Randomised" appears in title; structured abstract per CONSORT-A. |
| 2a/2b — Background + objectives | Introduction | Cite scientific rationale + specific hypothesis. |
| 3-7 — Trial design | Methods | Design type (parallel, crossover, factorial), allocation ratio, important changes after start. |
| 8-10 — Randomisation | Methods | Sequence generation method, allocation concealment, who enrolled / assigned. |
| 11 — Blinding | Methods | Who was blinded (participants, providers, outcome assessors). "Open-label" is also a valid answer. |
| 12 — Statistical methods | Methods | Primary analysis, subgroup, missing-data approach. |
| 13-19 — Results | Results | **Flow diagram is mandatory** — render via [[figure-spec]] sankey. Baseline data table. Numbers analysed. |
| 20-21 — Discussion | Discussion | Limitations, generalisability. |
| 22-25 — Other | End-matter | Registration number (NCT...), protocol availability, funding. |

### STROBE skeleton (observational)

| Slot | Section | Content |
|---|---|---|
| Title + abstract | Abstract | Indicate study design ("cross-sectional", "case-control", "cohort"). |
| Background, objectives | Introduction | Pre-specified hypotheses. |
| Setting, participants, variables, data sources, bias, study size, statistical methods | Methods | Each its own subsection or paragraph. "Bias" paragraph is non-optional. |
| Participant flow, descriptive data, outcome data, main results, other analyses | Results | Flow diagram shows numbers at each stage of inclusion. |
| Key results, limitations, interpretation, generalisability | Discussion | Limitations is mandatory. |
| Funding, conflicts | End-matter | |

### PRISMA 2020 skeleton (systematic review)

| Slot | Section | Content |
|---|---|---|
| Title | "Systematic review" or "meta-analysis" in title. | |
| Abstract | PRISMA-A 12-item structured abstract. | |
| Methods | Eligibility criteria, information sources, search strategy (full string in supplement), selection process, data extraction, risk of bias, summary measures, synthesis methods. | |
| Results | **Flow diagram (PRISMA 2020) is mandatory**: identification → screening → eligibility → included. Render via [[figure-spec]] sankey-or-arrows. |
| Discussion | Strengths and limitations of the evidence + of the review. | |
| Other | Protocol registration (PROSPERO ID), funding, code/data availability. | |

### ARRIVE 2.0 — Essential 10

The "Essential 10" items must be in every animal-study Methods section, even in CNS papers where Methods is short:

1. Study design (groups, sample size, statistical units).
2. Sample size justification.
3. Inclusion / exclusion criteria.
4. Randomisation method.
5. Blinding.
6. Outcome measures.
7. Statistical methods.
8. Experimental animals (species, strain, sex, weight, age).
9. Experimental procedures (timing, where, who).
10. Results (descriptive + inferential statistics).

## How to use this in a Writer workflow

1. **Identify study type → pick guideline.** Save the chosen checklist as `notes/<guideline>_checklist.md`.
2. **For every item, set status: PASS / TODO / N/A.** Initially all are TODO.
3. **As sections are drafted, flip items to PASS and link to the .tex line that satisfies it.** Use comments like `% [STROBE-7] bias addressed:` for traceability.
4. **At [[paper-compile]] time, dump the checklist to `compile.log`.** The macro-discipline lint and the checklist audit run together.
5. **Submission package includes the filled checklist as a supplementary file.** Most journals require this verbatim.

## Pitfalls

- Picking a checklist for the wrong study type. Ask the user; do not guess.
- Filling the checklist after the manuscript is done. Reverse-fitting often forces a rewrite of Methods. Pick the guideline at outline time.
- Reporting effect size without confidence interval (CONSORT-17, STROBE-16). "Mean difference 4.2 (95% CI 2.1 to 6.3)" — both numbers, always.
- Skipping the flow diagram when the guideline requires one. CONSORT, STROBE, and PRISMA all have mandatory flow diagrams.
- Forgetting protocol registration (CONSORT-23, PRISMA-24, NCT/PROSPERO ID). Auto-rejection trigger.
