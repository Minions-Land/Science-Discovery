# Round Notes — R3.B nature-citation

**Cases:** case-mixed-claims (1 case)
**Date:** 2026-05-16
**Candidate skill:** `/Users/mjm/Skill/nature-skills-main/skills/nature-citation/`

## Headline

Candidate **13/15** vs baseline **9/15** (+4). Bucket: Calibrates response.

This is the first R1+R2+R3 round where baseline performed strongly on
the primary risk dimension (no-fabrication). Both runs used `[needs
verification]` placeholders without prompting, suggesting that when
the runner is disciplined enough to flag uncertainty, the skill's main
contribution shifts from "safety" to "structure."

## Three structural improvements

1. Stable claim IDs (`S001-S008`)
2. Scope filtering with conditional acceptance ("scVelo scope unresolved";
   "Science-family in-scope only if directly tests SCFA")
3. Support grading status tag (metadata-only / background / primary-source /
   scope-unresolved / out-of-scope)

## What the skill did NOT deliver

The skill's high-leverage feature is its `nature_citation.py` Crossref
script for retrieving real DOIs. SkillTest is no-network by design;
candidate correctly didn't call the script. But this means the
no-network candidate is essentially a "structural overlay" on what an
attentive baseline runner would produce.

For MinionsOS Writer, this matters: if the Writer role has network
access (Crossref via WebFetch or paper-search MCP tools), the skill's
script-driven mode is high-value. If it doesn't, the structural rules
alone are worth porting but the value is incremental.

## Cross-validation with R3.A

R3.A confirmed: "name the specific access controller; placeholder for
unknown identifiers." R3.B confirms the same anchor in citation context:
"`[needs verification]` placeholder for unknown DOIs / volumes /
pages." The cross-skill anchor rule **substantively-bounded specificity,
not vague good-faith promises** is now confirmed across 4 fixtures
(R1.C overclaim + R2 rebuttal + R3.A data availability + R3.B citation
candidates).

## Token economics

- baseline input ~600 tokens
- candidate input ~6500 tokens (~11x)
- output ~330 tokens both (similar)

Lighter premium than R3.A. The script-aware references are smaller than
nature-data's policy + repository references.

## Recommendation

`fork-narrowly`. Plan to update existing
`minions/roles/writer/skills/citation-audit.md` with stable IDs +
scope filtering + support grading. Skip the Crossref script (network-
dependent; venue-specific) and the journal-scope hardcoded list (R1
imported-paper-skill-catalog already covers domain assumptions).

Draft delta for proposed-updates: `citation-audit.md.diff`.

## What to test next in R3.C

- skill-deslop, avoid-ai-writing, humanizer-academic, stop-slop comparison.
- Build one fixture: a paragraph with deliberate AI-trace vocabulary.
- Test all 4 candidates against it (one round, 4 candidates × 1 fixture).
- Hypothesis from R1.C: AI-trace blacklists are insurance, not
  transformative; sentence-level deslop tools should produce diminishing
  returns vs each other and vs an Opus / GPT-class baseline.
