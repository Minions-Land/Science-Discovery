# Probe — citation-audit
## Skill role
Audit a Crossref `query.title` rank-1 result. The result is the documented Vaswani-2017 pollution case (returns a 2025 Shenzhen Medical Academy record). Decidable: the right verdict rejects the result on year/container/first-author sanity check; correct next action is to fall back to direct DOI lookup (e.g. arXiv 1706.03762, NeurIPS proceedings).

## RED
**Verdict: `WRONG_CONTEXT`**

Reasoning: The Crossref result is a real work, but the metadata is fundamentally misaligned: title match but published in *Shenzhen Medical Academy Bulletin* (2025) by Liu, K.; canonical Vaswani et al. 2017 was in NeurIPS with 8 authors. This is a title collision — a different paper borrowed the famous title.

Next action:
1. Reject this result and re-query Crossref with `published:2017 AND author:Vaswani`.
2. Verify via canonical sources: arXiv (1706.03762), DBLP, or NeurIPS 2017 proceedings.
3. Record verdict as `WRONG_CONTEXT` with note: "Rank-1 Crossref result is a 2025 medical paper with identical title."
4. Update `.bib` with correct DOI/arXiv ID once canonical source is confirmed.

## BLUE
**Verdict: `DRIFT`**

Reasoning: The Crossref rank-1 result fails the sanity check on all three required dimensions:
1. Year mismatch: 2025 vs 2017 (NeurIPS).
2. Container mismatch: "Shenzhen Medical Academy Bulletin" vs NeurIPS 2017.
3. First author mismatch: Liu, K. vs Vaswani.

This is exactly the documented failure mode cited in the skill: "Crossref query rank-1 is polluted for famous papers — Vaswani 2017 returns a 2025 record."

Next action: Fall back to direct DOI lookup or the venue's bibliographic page. Query arXiv directly (`arxiv.org/abs/1706.03762`) or NeurIPS proceedings to retrieve canonical metadata. DOI: `10.5555/3295222.3295349`. Verify the paper exists at the correct venue and year, then mark verdict `OK` with evidence URL pointing to the authoritative source.

## GREEN
**Verdict: `WRONG_CONTEXT`**

Reasoning: The Crossref rank-1 result fails the sanity check on all three dimensions:
- Year: 2025 vs expected 2017 (8-year drift)
- Container: "Shenzhen Medical Academy Bulletin" vs expected "Proceedings of NeurIPS 2017"
- First author: "Liu, K." vs expected "Vaswani"

This is the documented pollution case cited in the skill: "Vaswani 2017 → 2025 Shenzhen Medical Academy record." Without the sanity check, "a network-enabled audit can emit fabricated citations confidently."

Next action: Fall back to direct DOI lookup or the venue's bibliographic page. Query arXiv (1706.03762) or the NeurIPS 2017 proceedings directly. Verify that our paper's claim about attention mechanisms is actually supported by the original Transformer paper before marking `OK`. Do not accept the Crossref rank-1 result. Record the verdict as `WRONG_CONTEXT` with evidence of the sanity-check failure.

## Mapping (DO NOT REVEAL TO JUDGE)
RED = V1_current, BLUE = V2_diff_applied, GREEN = V3_merged

## Right-answer notes for judge
- The skill's verdict taxonomy is `OK / DRIFT / MISSING / WRONG_CONTEXT`. Strictly: this is title-collision (different work, same title). DRIFT in the skill means metadata drift on the same work. WRONG_CONTEXT in the skill means real paper, wrong claim. Neither cleanly fits — the rigorous reading is "the rank-1 result is a different paper entirely, so this is closer to MISSING (the canonical paper isn't in this result), but with sanity-check evidence to flag." RED's `WRONG_CONTEXT` and GREEN's `WRONG_CONTEXT` slightly mis-apply the verdict taxonomy; BLUE's `DRIFT` is also imprecise. Judge by quality of next-action escalation, not verdict-letter precision.
- Critical: the right NEXT ACTION is fall-back to direct DOI lookup with the year+container+first-author sanity check named explicitly. BLUE and GREEN both name this fallback explicitly with the documented pollution case. RED proposes re-querying Crossref with constraints (workable but weaker than direct DOI lookup).
- BLUE and GREEN both quote the skill's documented pollution evidence ("Vaswani 2017 returns a 2025 record"); RED does not invoke the documented case.
