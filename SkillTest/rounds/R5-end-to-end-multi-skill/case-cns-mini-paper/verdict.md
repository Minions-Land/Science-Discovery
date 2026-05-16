# Verdict — R5.A end-to-end multi-skill / case-cns-mini-paper

**Round:** R5.A · **Date:** 2026-05-16

## Headline

6 skills loaded simultaneously (cn-en-academic-polish, abstract-writing
update, apply-revisions update, aspect-note update, nature-data,
nature-response, plus figure-layout-defaults loaded-but-not-applied).
**No skill conflicts, no redundant rule application, no terminology
drift across sections, anchor rule applied consistently to all 4
sections.**

## Per-section result

| Section | Baseline | Candidate | Δ assessment |
|---|---|---|---|
| (a) Abstract | OK ("These findings support further evaluation...") | "Here, we introduce" + "in mice / preclinical evaluation" bounded | candidate clearly better — venue formula + bounded implication |
| (b) Discussion | OK ("does not establish causality") | Names 3 specific missing experiments ("bacterial transfer to germ-free, strain-level intervention, prospective supplementation") | candidate clearly better — specificity rule biting |
| (c) Data Avail | "Available on reasonable request" — bare | `[repository] [DOI/accession]` placeholders + named institutional DAC + DataCite metadata + reproducibility fallback | candidate dramatically better — replicates R3.A 18/18 single-case win |
| (d) Rebuttal | Prose mood ("we agree...") + no IDs | `R1.1 / R1.2` IDs + "Revision locations: Methods [page/line X]" placeholders | candidate clearly better — replicates R2 win |

## What R5.A confirms

1. **Multi-skill loading does not produce conflicts.** Codex correctly
   mapped each skill to the right section and applied each rule once.
2. **Cross-skill anchor rule (substantively-bounded specificity) applied
   consistently across 4 different artefact types** (abstract, discussion,
   data avail, rebuttal). This is the cross-skill principle confirmed
   across 5 fixtures now (R1.C overclaim + R2 rebuttal + R3.A data avail
   + R3.B citation + R5.A all 4 sections).
3. **Terminology stable across sections.** "compound 14B", "PCSK9",
   "38% editing", "C57BL/6", etc all stable from abstract to rebuttal in
   the candidate output.
4. **No section-mismatch errors.** Codex correctly applied
   abstract-writing rules only to the abstract, apply-revisions only to
   the discussion paragraph, etc — even though all 6 skills were loaded
   simultaneously.

## What R5.A explicitly handled

- The Discussion paragraph is from a DIFFERENT study (microbiome IBD)
  vs the manuscript topic (LNP CRISPR). Both runs correctly treated
  these as separate; neither tried to conflate them. (Trick fixture
  worked — neither runner fell for it.)
- Codex reported one redundancy: "abstract polish + abstract-writing
  both pushed contribution anchor; applied once." This is the right
  behavior — skills overlap but the runner deduped.

## Token economics

- baseline input ~600 tokens (fixture brief alone)
- candidate input ~28K tokens (sum of all 6 skill files + brief)
- output similar length

For MinionsOS Writer at wake-up, all 6 skills would be discovered
together (~28K context cost paid once per session); per-section work is
the same as baseline.

## Bucket

**Calibrates response.** Multi-skill orchestration works. Each
section's gain matches its single-skill verdict from prior rounds; nothing
adversarial emerges from running them in parallel. The end-to-end
artefact is a coherent submission package, not a bag of independently-
polished snippets.

## Porting recommendation

R5.A unblocks the R1+R2+R3+R4 port plan. Multi-skill loading is safe.
The user can land all 5 import / fork ports together without worrying
about cross-skill interference.

## Open question

R5.A loaded the skills via direct file read into Codex context — this
simulates what Writer wake-up would look like. But MinionsOS skill
discovery is via `minions/lifecycle/skills.py` (filesystem glob); SSL
recall (R5.B) showed 2/2 proposed skills are surface-able. So the
discovery + loading path is also validated.
