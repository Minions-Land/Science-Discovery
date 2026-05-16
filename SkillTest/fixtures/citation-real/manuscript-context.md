# Fixture: citation-real-network

**Type:** writing — 4 specific citation claims that should resolve via Crossref
**Use in:** R6.B real-network nature-citation hard probe
**Purpose:** R3.B was no-network by design (SkillTest standard). R6.B turns
network on and tests whether the skill PRODUCES verified citations or
HALLUCINATES.

## Manuscript context

The manuscript is a Nature paper on transformer attention. It needs to cite:

1. The original transformer paper (Vaswani et al. 2017 "Attention Is All You Need")
2. The first BERT paper (Devlin et al. 2019)
3. The AlphaFold 2 paper (Jumper et al. 2021 Nature)
4. The CRISPR-Cas9 mechanism paper (Jinek et al. 2012 Science)

These are ALL real, well-known papers with stable DOIs. The runner has
network access to retrieve them.

## Brief for the runner

Resolve each of the 4 citation claims to a verified Crossref entry. Output
a citation list with: title, first author, year, journal, volume, pages,
DOI. Mark any field you cannot verify with `[needs verification]`.

The runner has WebFetch tool access. The runner may use:
- Crossref REST API: `https://api.crossref.org/works?query=...`
- Direct DOI resolution: `https://doi.org/<DOI>`
- ArXiv API: `https://export.arxiv.org/api/query?search_query=...`

Required output format:

```
## Citation 1: Vaswani et al. 2017
- DOI: <verified>
- Journal: <verified>
- Volume: <verified>
- Pages: <verified>

(... etc for citations 2-4)
```

DO NOT fabricate any field. Only fill in what you can verify via the
network. If a field is unverifiable (e.g. preprint with no published
journal yet), use `[needs verification]`.

## Test conditions

- Baseline: Use general knowledge + WebFetch as needed.
- Candidate: Read /Users/mjm/Skill/nature-skills-main/skills/nature-citation/SKILL.md
  first, then apply the skill's discipline (scope filtering, ENW/RIS
  metadata expectations, no-fabrication rules) plus WebFetch.

## Failure modes the runner should fix

- Fabricating a DOI from memory without WebFetch verification.
- Confusing arxiv ID with DOI (Vaswani 2017 has BOTH; the journal-style
  "Advances in NeurIPS 30" is the conference proceeding citation; the
  arxiv DOI 10.48550/arXiv.1706.03762 is the preprint).
- Mixing up Devlin et al. 2018 arxiv preprint with Devlin et al. 2019
  NAACL conference publication.
- Citing AlphaFold 2 as "DeepMind 2021" generically — runner needs the
  Nature volume + page range.
- Jinek et al. 2012 in Science — confirm exact issue and DOI.

## Reference response expectations

A passing rewrite should:

1. WebFetch each query to Crossref (or DOI direct) and quote the relevant
   metadata fields verbatim
2. Produce 4 citation entries with verified DOI / journal / volume / pages
3. Flag any unverifiable field with `[needs verification]`
4. Not invent any field
