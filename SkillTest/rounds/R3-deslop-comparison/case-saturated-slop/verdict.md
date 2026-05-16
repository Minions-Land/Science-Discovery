# Verdict — deslop-comparison / case-saturated-slop

**Round:** R3.C · **Date:** 2026-05-16 · **Rubric version:** v1
**Scope:** 1 fixture × 4 candidate skills (skill-deslop, avoid-ai-writing,
humanizer-academic, stop-slop) + 1 baseline

## Headline

**All 5 outputs scored identically on AI-trace removal:** zero slop terms,
zero em-dashes, all words within 77-95. Baseline (no skill loaded, Opus
4.7 in 2026) handled the saturated-AI-slop fixture as cleanly as the
candidates. The skills are insurance, not transformation.

## Numeric score

| Run | Polished words | Slop terms | Em-dashes | Score (writing /22) |
|---|---|---|---|---|
| baseline | 94 | 0 | 0 | **18/22** |
| candidate-avoid-ai-writing | 95 | 0 | 0 | 18/22 |
| candidate-humanizer-academic | 94 | 0 | 0 | 18/22 |
| candidate-skill-deslop | 90 | 0 | 0 | 18/22 |
| candidate-stop-slop | 77 | 0 | 0 | **19/22** (+1 for active-subject rule) |

## What each skill actually delivered (vs baseline)

### skill-deslop
- Identical scope of removal vs baseline (delve / tapestry / plethora /
  paved the way / transformative — all gone in both).
- Verbose revision notes name the rule numbers ("Deslop Rule 1, Rule 3,
  Rule 4, Rule 7") — useful as audit trail, not as content delta.
- **Bucket: Matches baseline.**

### avoid-ai-writing
- Identical scope of removal vs baseline. Tiered vocabulary rules
  (Tier 1 / Tier 2) are restated in revision notes but produce same
  output as baseline.
- The 480-line SKILL.md is mostly an exhaustive vocabulary blacklist
  that Opus 4.7 already implements internally.
- **Bucket: Matches baseline.**

### humanizer-academic
- Identical scope of removal. "Pattern 13" through "Pattern 18" cited
  in revision notes; output content same as baseline.
- 504-line SKILL.md is the heaviest of the four; output is the most
  formal-academic-sounding ("provided evidence about how transformer
  models process information") but has same anti-slop net effect.
- **Bucket: Matches baseline.**

### stop-slop
- **The one differentiated candidate.** 77 words vs ~94 elsewhere — most
  aggressive cuts.
- Adds an explicit subject ("Researchers use attention mechanisms...")
  where baseline uses "Attention mechanisms are central..." — this is
  Rule 3-equivalent (active voice + human subject) which the other
  three skills don't enforce as hard.
- **Bucket: Calibrates response.** Mildly tighter prose than baseline.

## What the skill set as a whole delivered

The skill set's value across 4 candidates × 1 fixture = 5 polished outputs:

- **AI-trace removal:** all 4 candidates and baseline scored 0. No skill
  uniquely removed slop terms baseline left in.
- **Em-dash removal:** all 4 candidates and baseline scored 0. No skill
  uniquely cut em-dashes baseline kept.
- **Sentence rhythm:** all 5 outputs have similar rhythm (5-6 sentences
  averaging 18-22 words). No skill uniquely varied length more than
  baseline.
- **Active voice / human subject:** stop-slop alone enforced this. +1
  pt vs the others.

## Cross-validation with R1.C

R1.C predicted (in `synthesis/what-to-skip.md`): "AI-trace blacklists
are insurance, not transformative — both baseline and candidate runners
removed these terms in 2026 even without the skill."

R3.C confirms with controlled evidence: 4 different blacklist-style
skills, on a saturated-slop fixture, produce output indistinguishable
from baseline on the trace-removal dimension.

## Bucket per skill

| Skill | Bucket | Reason |
|---|---|---|
| skill-deslop | Matches baseline | Same removal scope; rule labels are audit-only value |
| avoid-ai-writing | Matches baseline | 480 lines of vocabulary blacklist that Opus 4.7 internalises |
| humanizer-academic | Matches baseline | 504 lines, heaviest skill; output identical to baseline content |
| stop-slop | Calibrates response | Active-subject rule is the one differentiator; +1 pt at most |

## Porting recommendation

`skip` for skill-deslop / avoid-ai-writing / humanizer-academic.

`fork-narrowly` for stop-slop **only the active-subject rule**:
> When a sentence's subject is abstract ("Attention mechanisms are central
> ...", "The mechanism scales..."), consider rewriting with a human or
> entity subject ("Researchers use attention mechanisms ...", "Transformers
> scale ...") if the result reads more directly. Don't enforce when the
> abstract subject is genuinely the topic.

Even this rule is marginal — stop-slop's output is 77 words, baseline is
94, but baseline reads slightly more natural for an academic paper.

The bigger lesson is that **for Opus-class models in 2026, sentence-level
deslop tools are not load-bearing for MinionsOS Writer**. They were
load-bearing in 2023-2024 when smaller models genuinely produced
"crucial / important to note / paves the way" reflexively. They are no
longer.

For older / cheaper / smaller models in MinionsOS subagent contexts,
these blacklists may still bite. Worth re-testing on Haiku-class
specifically before final reject.

## Provenance

R3.C was structured to test the prediction from R1.C
`what-to-skip.md` entry #5: "Anti-AI-trace heuristics ... were effective
in R1.C but not load-bearing — both baseline and candidate runners
removed these terms in 2026 even without the skill." R3.C confirms with
4 independent blacklist skills × 1 saturated fixture = no skill
materially differentiates from baseline on the trace-removal dimension.

The prediction is now empirically validated. `what-to-skip.md` entry
#5 stands.
