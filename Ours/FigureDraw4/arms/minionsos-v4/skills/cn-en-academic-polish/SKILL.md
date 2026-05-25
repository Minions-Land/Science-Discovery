---
slug: cn-en-academic-polish
summary: Reconstruct logic before translating clauses for Chinese-influenced English; hourglass introduction order, sentence-length cap, AI-trace blacklist, stable terminology.
layer: logical
tools:
version: 2
status: active
supersedes:
references: abstract-writing, apply-revisions
provenance: SkillTest-R1.C-case-intro-zh
---

# Skill — Chinese-to-English Academic Polish

Reconstruct logic first; translate clauses second. A Chinese draft polished
clause-by-clause keeps the original sentence flow and reads as translation
to a venue editor — even when every individual sentence is grammatical
English. The job is to rebuild the argument in publishable English order,
not to clean up the surface.

## When to invoke

- The source is Chinese, or strongly Chinese-influenced English (mid-sentence
  Chinese discourse markers like "由此可见", "另一方面", "值得注意的是",
  AI-trace English vocabulary inserted between Chinese clauses, em-dashes
  used inside an English clause).
- The author is a non-native English speaker preparing a CNS-family submission
  and the existing draft preserves the Chinese flow.
- Reviewer comments mention "writing quality" or "logical flow" rather than
  specific science problems.

Do not invoke for English drafts where the issue is unclear scientific
argument; that is a [[apply-revisions]] / [[abstract-writing]] case.

## Procedure

1. **Read the source twice without writing.** Pass 1: identify what the
   author is *trying* to argue. Pass 2: identify which sentences carry the
   argument vs which are connective tissue.
2. **Diagnose paper-section type before editing.** Introduction, Methods,
   Results, Discussion, or Abstract. Each has its own move order; do not
   apply Discussion-style hedging to a Results paragraph.
3. **Rebuild logic before language.** For an Introduction:
   - Open with the gap (what's missing in the field), not a survey of what's
     done.
   - Name the consequence (what the gap blocks).
   - Anchor the contribution with "Here, we [introduce / show / report]".
   - Bound the result; refuse to assert quantification that hasn't been
     extracted from the source.
4. **Translate clauses only after logic is fixed.** Apply:
   - Sentence cap: ≤30 words per sentence. The last sentence of a paragraph
     usually overruns; check it explicitly.
   - AI-trace blacklist: remove `crucial`, `delve into`, `important to note`,
     `substantial`, `comprehensive`, `robust` (when used as filler), `seminal`.
   - Em-dashes: ≤2 per page, never inside an English clause.
   - Stable terminology: a term defined at first mention stays in the same
     form (`protein language model (PLM)` then `PLMs`, never alternating
     with `language models`, `the model`, `our framework` for the same noun).
5. **Refuse to fabricate.** If the source claims "substantial improvements
   over baselines" with no numbers, do not paraphrase as "outperforms
   existing baselines" — flag explicitly: "the size of these gains should
   be reported in the Results."
6. **Output structure:** polished prose first, then 3-5 revision notes
   bullets naming which rules drove which changes. Include a one-line
   "Diagnosed paper type / failure mode" footer when revising for a
   reviewer audience; suppress the footer for production manuscript text.

## Pitfalls

- Translating clause-by-clause from Chinese, preserving the original order.
  The result reads as a competent translation, not as a Nature-family
  introduction — exactly the failure mode this skill is meant to fix.
- "I'll fix the logic later" — if you start polishing wording before the
  logic is rebuilt, you'll over-invest in sentences that should be deleted.
- Asserting quantitative claims the source didn't quantify. The source
  saying "substantial gain" without numbers means the polished version
  must flag the missing numbers, not invent them or paraphrase past them.
- Letting `crucial` / `delve into` / `important to note` survive into the
  final draft because the surrounding sentence "looks fine."
- Mixing British / American spelling within a paragraph
  (`generalisation` next to `analyze`, `behaviour` next to `program`).
  Pick one register and apply throughout.

## Output habit

For revisions: lead with polished prose, then `Revision notes:` with 3-5
bullets that NAME the rule (`hourglass restructure`, `Chinese-to-English
mode`, `AI-trace removal`, `≤30-word cap`, `refused to fabricate
quantification`). The named-rule format is for reviewer trust, not author
ego — it lets the next reviewer or editor verify the change was rule-based,
not stylistic preference.

## Provenance

Forked from SkillTest R1.C case-intro-zh evaluation of nature-polishing.
The source skill (nature-polishing, from the Nature-skills collection)
is heavier (full SKILL.md ~10 KB + 3 references) and covers the full
section-move taxonomy; this draft narrows to the Chinese-to-English use
case which is the load-bearing benefit for MinionsOS Writer.
