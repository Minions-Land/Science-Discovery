# Round Notes — R6.B real-network nature-citation

**Cases:** case-real-crossref (1 case, 4 citations resolved real-time)
**Date:** 2026-05-16

## Headline

**Network exposed the failure mode R3.B couldn't see.** Crossref
query.title API has rank-1 pollution for famous paper titles
(Vaswani 2017, Devlin 2019 both hit polluted records). Baseline
that takes rank-1 at face value emits fabricated citations.
Candidate (with skill's verify-before-cite rule) catches both.

Score: 15/15 vs 8/15 (+7). Bucket UPGRADED from R3.B's "Calibrates
response" to **Prevents real failure** in network-on context.

## Recommendation upgrade

R3.B verdict: fork-narrowly.
R6.B verdict: **import-strongly** for the verify-before-cite rule.

Skill is now confirmed to be load-bearing IF the production environment
gives the Writer role real network access (which it does — WebFetch +
paper-search MCP tools are available).

The `citation-audit.md.diff` update should include a hard rule:

> Never accept Crossref query.title rank-1 result without sanity checks
> (year, container, first author). Fall back to direct DOI lookup if
> any check fails.

## Methodology learning

WebFetch domain whitelist refuses api.crossref.org. Sandbox curl
succeeds for the same URL. For future network-enabled SkillTest rounds,
use Bash + curl instead of WebFetch. Documented in this round's
transcript.md.
