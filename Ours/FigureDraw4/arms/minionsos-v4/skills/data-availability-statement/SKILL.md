---
slug: data-availability-statement
summary: Write Nature-policy-compliant Data Availability and Code Availability statements — replace "available upon reasonable request" with named DAC + review conditions; require DataCite-style metadata for reused public data; provide reproducibility fallback for patent-pending or restricted code.
layer: logical
tools:
version: 2
status: active
supersedes:
references: paper-literature-search, citation-audit, package-submission
provenance: SkillTest-R3.A-case-mixed-restrictions
---

# Skill — Data Availability Statement

`available upon reasonable request` is a submission-quality failure for
Nature-family venues. Replace it with substantively-bounded specificity:
who reviews requests, on what conditions, returning what artefact, in
what time. Same discipline applies to Code Availability when patents,
licensing, or proprietary tooling block a clean public release.

## When to invoke

- Drafting or revising a `Data Availability` or `Code Availability`
  paragraph for a Nature-family submission, camera-ready, or revision.
- The author hands over a Chinese-influenced draft that says "available
  on reasonable request" or "from the corresponding author" with no
  named controller, no review process, and no DataCite metadata.
- Reviewer flags vague data-sharing language and the rebuttal needs a
  policy-compliant rewrite.
- Code is patent-pending or proprietary and the team is about to write
  "code will not be released" — this skill produces the reproducibility
  fallback that Nature's policy actually expects.

Do not invoke for non-Nature venues with their own (looser) policy
unless the author asks for the higher bar.

## Procedure

1. **Inventory the data assets.** List every dataset by class:
   `(class, identifier_or_status, restriction, controller)`. Classes:
   - **Generated data, shareable**: where will it go (Zenodo / GEO / SRA / Figshare); what identifier or accession will be assigned; is it reserved or already minted?
   - **Generated data, restricted**: why (consent / IRB / commercial / national security); who owns the access decision; what review process do requesters go through?
   - **Reused public data**: what is the original citation; do you have the DataCite-style metadata (creator, year, title, repository, version or access date, persistent identifier)?
   - **Reused restricted data**: who owns redistribution rights; can you cite the original DAC instead of brokering access yourself?

2. **Replace "reasonable request" with a named DAC + review conditions.**
   For any restricted-access dataset, the statement names:
   - The institutional Data Access Committee (or equivalent named body) that reviews requests.
   - The review conditions (typical: researcher eligibility, proposed use, ethics approval at the requester's institution, data-use agreement signature).
   - The expected turnaround if known.
   The statement does NOT promise unconditional access, and does NOT bury the access route in "from the corresponding author" prose.

3. **DataCite-style citation discipline for public data.** For any
   reused public dataset, the statement names the required fields
   without fabricating values: `[creator] · [year] · [title] · [repository]
   · [version OR access date] · [persistent identifier — DOI / accession]`.
   If a field is genuinely unknown, mark it `[needs verification]`
   rather than inventing a plausible-looking DOI.

4. **Code Availability is a separate paragraph.** Do not bundle code
   into Data Availability. Code Availability covers:
   - Where code lives (GitHub / Zenodo / institutional repo) at the time
     of acceptance.
   - License (MIT / GPL / Apache / proprietary).
   - Software environment (env file / Dockerfile / conda env / requirements).
   - Reproducibility scope: which figures / tables / experiments the
     released code reproduces.

5. **Patent-pending or proprietary code: write the fallback.** If the
   full code cannot be released because a patent is pending or a
   license restricts redistribution, the statement must NOT say "will
   not be released." It must commit to:
   - Runnable wrappers, documentation, environment files.
   - A placeholder interface sufficient to reproduce all
     non-restricted preprocessing and analysis steps.
   - Time horizon for full release (after patent grant, after embargo,
     etc.) if known.
   The reproducibility scope is the load-bearing claim — Nature's
   policy is "you can withhold the secret sauce; you cannot withhold
   reproducibility of the figures."

6. **No fabrication.** Do not invent DOIs, accession numbers, repository
   names, ethics approval IDs, DAC contact addresses, or grant numbers.
   Use the value the source provides verbatim, mark `[needs verification]`
   when the source is silent, and flag the gap to the author.

## Output

Two paragraphs (Data Availability + Code Availability) in the venue's
exact prose register, ready for direct insertion into the manuscript.
Plus a 3-5 bullet list of revision notes naming which rules drove which
changes (`named DAC instead of reasonable-request`, `DataCite-style fields
required for [dataset]`, `patent-pending fallback added`, `flagged
[dataset] for missing DOI`).

If the author explicitly asks for a single combined paragraph (some
venues), still keep the two concerns mentally separate while drafting,
then merge with a sentence-level transition.

## Pitfalls

- "Available from the corresponding author on reasonable request"
  with no named controller, no conditions, no review process. This is
  the failure mode this skill exists to fix.
- Inventing a Zenodo DOI / SRA accession because the structure of a
  real one is well-known. The reviewer or production editor will check.
- Treating patent-pending code as a hard "will not be released" — Nature's
  reproducibility policy actually allows this if the fallback is
  authored correctly. Skipping the fallback is a submission-quality
  failure.
- Mixing Data Availability into Code Availability or vice versa.
  They have different policy obligations; keep them separate.
- Letting Chinese-influenced register survive: a draft that says
  "we will provide upon reasonable request" (a literal carry-over from the
  source Chinese phrasing) → fail. Chinese-author Writers should run this
  skill with [[cn-en-academic-polish]] when the source draft is
  Chinese-flavoured.

## Output habit

Lead with the two clean paragraphs (Data + Code). Then `Revision notes:`
with named-rule bullets. Mark any `[needs verification]` placeholders so
the next pass (author / Reviewer) can verify or fill.

## Provenance

Forked from SkillTest R3.A `case-mixed-restrictions` evaluation of
nature-data (from the Nature-skills collection).
Largest single-case Δ in SkillTest history (18/18 vs 8/18 baseline) on a
Nature-family fixture mixing patient ECG + RNA-seq + public data + patent-
pending code. R5.A multi-skill orchestration confirmed the skill applies
to its right section without conflict with `abstract-writing`,
`apply-revisions`, `prepare-rebuttal`, or `citation-audit`.
