---
slug: citation-audit
summary: Verify every \cite{...} is a real work, correctly attributed, and used in a context the cited paper actually supports — three-layer check (existence, metadata, context); never trust Crossref query.title rank-1 without sanity check (year + container + first author).
layer: logical
tools:
version: 3
status: active
supersedes:
references: paper-literature-search, end-to-end-paper-workflow
provenance: human + SkillTest-R3.B+R6.B
---

# Skill — Citation Audit

Every bib entry checked at three layers: the work **exists**, the **metadata** matches canonical sources, the **context** in our sentence is something the cited paper actually establishes.

## When to invoke

- Once before any submission, rebuttal, or camera-ready.
- When Reviewer flags a suspect citation in `artifacts/reviews/`.
- When adding a batch of new citations late in the writing cycle.

Run after the draft is stable and numeric claims have been audited; before final compile for submission. Running too early wastes lookups on placeholder text.

This is the **Writer-side full pre-submission sweep**. Ethics independently runs sampled audits via `ethics/citation-authenticity-audit` over both the `.bib` and Reviewer-cited prior work and pings via EACN — that is oversight, not a substitute for this sweep.

## Structure

Per-entry verdict ∈ `OK` / `DRIFT` / `MISSING` / `WRONG_CONTEXT`. Outputs:

- `branches/writer/paper/CITATION_AUDIT.md` (human-readable per-entry list with verdict, evidence URL, sentence).
- `branches/writer/paper/CITATION_AUDIT.json` (machine: `{key, status, evidence_url, notes}` per entry).

Verification sources: arXiv, DBLP, ACL Anthology, OpenReview, publisher venue page, DOI resolver. Aggregator pages (ResearchGate, Academia.edu, Semantic Scholar surface, Google Scholar snippets) are NOT canonical.

## Procedure

1. **Gate timing** — after draft stable and numeric audit done; before final compile.
2. **Extract `(key, context)` pairs.** For every `\cite{...}` in `branches/writer/paper/`, record key, file, line, full surrounding sentence. Build inverse index (bib entry → cite sites).
3. **Verify existence.** For each entry, resolve arXiv ID / DOI / venue URL via web search. Unresolvable → emit `[needs verification]` placeholder rather than fabricating; mark verdict `MISSING`.
4. **Verify metadata.** Compare authors, year, title, venue against canonical sources. Mismatch → `DRIFT`. Watch for arXiv v1 vs conference version title drift and year off-by-one on preprint-to-accepted transitions.
5. **Apply Crossref rank-1 sanity check.** When using Crossref `query.title` to resolve a citation, NEVER accept rank-1 without verifying all three:
   - **Year** matches the year the paper was actually published.
   - **Container** matches the expected journal / conference name.
   - **First author family name** matches the canonical first author.

   If ANY check fails, fall back to direct DOI lookup (e.g. `10.18653/v1/N19-1423` for BERT) or to the venue's own bibliographic page. Crossref query rank-1 is documented to be polluted for famous papers — Vaswani 2017 returns a 2025 record, Devlin 2019 returns a 2014 unrelated paper.
6. **Verify context.** Does the cited paper actually support what our sentence claims? Wrong-context (real paper, wrong claim) is the most dangerous class. Flag `WRONG_CONTEXT` with a one-line explanation.
7. **Record verdicts** in `CITATION_AUDIT.md` and `CITATION_AUDIT.json`. Every non-`OK` entry marked `[derived: web lookup <URL> @ <ts>]`.

## Pitfalls

- Pattern-matching from memory. Every verdict cites a fresh web source.
- Trusting Crossref `query.title` rank-1 because it's the top result. Famous-paper title collisions are a documented failure mode; always run the sanity check.
- Auto-"fixing" by swapping in a different paper without rechecking the context.
- Treating existence as sufficient — wrong-context is the failure mode that survives naïve audits.
- Citing arXiv preprint title when the accepted-version DOI exists with different metadata.
- Using ResearchGate or Google Scholar snippet text as canonical — they are aggregators, not authoritative sources.
