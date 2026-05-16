# Round Notes — R5.B SSL recall test

**Cases:** 4 probes × 35 candidate skills
**Date:** 2026-05-16

## Headline

Stage 0 SSL recall: 3 PASS / 1 expected-FAIL.

- 2 authored PROPOSED skills (cn-en-academic-polish, figure-layout-defaults)
  are surface-able at top-3 — no description rewrite needed.
- 1 gap exposed: data-availability-statement skill is missing; existing
  library has no good fit for Data Availability writing scenario.

## What the round confirmed

R3.A's prediction "MinionsOS Writer needs a dedicated data-availability
skill" is now confirmed at the discovery layer. Without authoring this
skill, P4-equivalent queries route to citation-audit / paper-literature-
search / package-submission — all wrong matches.

## Bucket

N/A (Stage 0 test). Functional outcome: 2 PROPOSED skills validated for
discoverability; 1 missing skill flagged for authoring before port.

## Recommendation

Author `data-availability-statement.md` from R3.A's rules before final
port to MinionsOS. Re-run R5.B with the new skill to verify P4 surfaces
correctly.
