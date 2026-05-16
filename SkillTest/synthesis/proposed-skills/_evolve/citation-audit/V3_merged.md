---
slug: citation-audit
summary: Verify every \cite{...} at three layers — existence (with Crossref rank-1 sanity check), metadata, context. Wrong-context is the most dangerous failure class; Crossref query.title rank-1 is polluted for famous papers and requires year+container+first-author verification.
layer: logical
tools:
version: 3
status: active
supersedes:
references: paper-literature-search, end-to-end-paper-workflow
provenance: human + SkillTest-R3.B+R6.B-merged
---

# Skill — Citation Audit

Three-layer check on every bib entry: the work **exists** (with rank-1 sanity check), the **metadata** matches canonical sources, the **context** in our sentence is something the cited paper actually establishes. Wrong-context is the failure class that survives naïve audits; Crossref rank-1 trust is the failure class that produces fabrications at scale.

## When to invoke

- Once before any submission, rebuttal, or camera-ready.
- When Reviewer flags a suspect citation in `artifacts/reviews/`.
- When adding a batch of new citations late in the writing cycle.

Run after the draft is stable and numeric claims have been audited; before final compile for submission. Running too early wastes lookups on placeholder text.

This is the **Writer-side full pre-submission sweep**. Ethics independently runs sampled audits via `ethics/citation-authenticity-audit` over both the `.bib` and Reviewer-cited prior work and pings via EACN — that is oversight, not a substitute for this sweep.

## Verdict per entry

`OK` / `DRIFT` / `MISSING` / `WRONG_CONTEXT`. Outputs:

- `branches/writer/paper/CITATION_AUDIT.md` (human-readable per-entry list with verdict, evidence URL, sentence).
- `branches/writer/paper/CITATION_AUDIT.json` (machine: `{key, status, evidence_url, notes}` per entry).

## Canonical vs aggregator sources

| Canonical (use these) | Aggregator (NOT canonical) |
|---|---|
| DOI resolver `https://doi.org/<DOI>` | ResearchGate |
| Publisher venue page | Academia.edu |
| arXiv (preprints only — verify accepted-version DOI separately) | Semantic Scholar surface page |
| DBLP (CS conferences) | Google Scholar snippet |
| ACL Anthology | — |
| OpenReview | — |

## Procedure

1. **Gate timing** — after draft stable and numeric audit done; before final compile.

2. **Extract `(key, context)` pairs.** For every `\cite{...}` in `branches/writer/paper/`, record key, file, line, full surrounding sentence. Build inverse index (bib entry → cite sites).

3. **Verify existence.** Resolve arXiv ID / DOI / venue URL via web search. If unresolvable, emit `[needs verification]` rather than fabricating; mark verdict `MISSING` and pass to next round / author.

4. **Apply Crossref rank-1 sanity check.** When resolving via Crossref `query.title`, NEVER accept rank-1 verbatim. Verify all three:
   - **Year**: matches the year the paper was actually published.
   - **Container**: matches the expected journal / conference name.
   - **First author family name**: matches the canonical first author.

   If ANY check fails, fall back to direct DOI lookup (e.g. `10.18653/v1/N19-1423` for BERT) or to the venue's own bibliographic page. Documented pollution: Vaswani 2017 → 2025 Shenzhen Medical Academy record; Devlin 2019 → 2014 Journal of Museum Education paper. Without the sanity check, a network-enabled audit can emit fabricated citations confidently.

5. **Verify metadata.** Compare authors, year, title, venue against canonical sources. Mismatch → `DRIFT`. Watch:
   - arXiv v1 vs accepted-conference-version title drift.
   - Year off-by-one on preprint-to-accepted transitions.
   - Venue / proceedings name changes between submission and publication.

6. **Verify context.** Does the cited paper actually support what our sentence claims? Wrong-context (real paper, wrong claim) is the most dangerous class — it survives existence + metadata checks. Flag `WRONG_CONTEXT` with a one-line explanation of the gap.

7. **Record verdicts** in `CITATION_AUDIT.md` and `CITATION_AUDIT.json`. Every non-`OK` entry marked `[derived: web lookup <URL> @ <ts>]`.

## Pitfalls

- Pattern-matching from memory. Every verdict cites a fresh web source.
- **Crossref rank-1 trust** without sanity check. Famous-paper title collisions are a documented failure mode that produces confident fabrications.
- Auto-"fixing" by swapping in a different paper without rechecking the context.
- Treating existence as sufficient — wrong-context survives naïve audits.
- Citing arXiv preprint title when the accepted-version DOI exists with different metadata.
- Using aggregator pages (ResearchGate, Google Scholar) as canonical sources.
- Treating `MISSING` as a hard failure that demands removal. The right move is `[needs verification]` placeholder, then escalate to author or next-pass reviewer.
