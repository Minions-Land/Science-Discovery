---
round: R7
title: Writing-skill restart (CNS-first, conference-secondary)
date_created: 2026-05-17
status: draft, awaiting user approval
parent_synthesis: ../../synthesis/R6-synthesis.md
fresh_start_reason: R1–R6 tested 4 writing skills under figure/rebuttal-leaning fixtures; user requested a clean restart with CNS-grade writing-only fixtures derived from explicit pain list.
---

# R7 — Writing-Skill Restart

## Why a restart, not an extension

R1.C, R2, R3.A, R3.B, R4.x, R5.x, R6.x exercised mostly figure / rebuttal /
citation-extraction surfaces. The four "writing" skills already touched
(`nature-polishing`, `nature-response`, `nature-citation`, `nature-data`)
were probed against narrow surfaces (Chinese-flavoured paragraph, mixed-
severity rebuttal, data-availability statement, Crossref pollution). None
of them was probed against the structural-discipline failure modes the
user named in this turn:

1. Abstract / Conclusion paragraph-count, no-citation, no-numerical-detail rule.
2. Introduction vs Related Work scope split.
3. Experiment completeness (main + ablation + hyperparam + case-study + per-figure analysis).
4. LaTeX typographic discipline (`\noindent\textbf{}` paragraph headers
   only as long-paragraph summaries, list environments minimised,
   `\newcommand` model-name macro, abbreviation first-use, parenthesis
   hygiene).
5. Zero-hallucination citation under CNS-grade scrutiny.

R7 keeps R1–R6's published-skill verdicts intact (no figure work re-tested)
but treats the **writing surface as new territory**. CNS-grade probes are
load-bearing; conference-grade probes confirm portability.

## Production-zone hard rule

Same as every prior round: nothing in `synthesis/proposed-skills/` or
`synthesis/proposed-updates/` is applied to
`/Users/mjm/MinionsOS/minions/roles/writer/skills/` until the user
explicitly approves. The 15 currently shipped Writer skills (validated)
are read-only inputs to R7 — they serve as the "library context" for
Stage 0 SSL recall, and as the diff target for any update proposed in R7.

## Candidate skill list (R7)

Discovered by enumerating `find /Users/mjm/Skill -name SKILL.md`. Filtered
to writing-relevant; figure/rebuttal-only candidates already adjudicated in
R1–R6 are excluded.

| ID  | Skill | Path | Size | First impression |
|---|---|---|---|---|
| C-01 | research-paper-writing | `Research-Paper-Writing-Skills-main/research-paper-writing/` | 4.8 KB | ML/CV-leaning; reverse-outline + claim-evidence map; was tagged "pending" in R2. **Primary conference target.** |
| C-02 | nature-polishing | `nature-skills-main/skills/nature-polishing/` | 13 KB | R1.C import-strongly. Re-probed in R7 against new pain list, only on cases R1.C did not cover. |
| C-03 | scientific-writing (K-Dense) | `Awesome-.../03-K-Dense-AI-claude-scientific-skills/scientific-writing/` | 22 KB | IMRAD + reporting-guideline-heavy (CONSORT/STROBE/PRISMA). Pushes graphical abstract + lots of figures. Directly conflicts with several CNS pain rules → must A/B carefully. |
| C-04 | scientific-writing (K-Dense Writer) | `Awesome-.../04-K-Dense-AI-claude-scientific-writer/scientific-writing/` | 32 KB | Same family as C-03, plus the abstract "no labelled sections" rule + venue-template hand-off. Largest writing skill in pool. |
| C-05 | citation-management (K-Dense Writer) | `Awesome-.../04-K-Dense-AI-claude-scientific-writer/citation-management/` | 39 KB | Heavy script-driven; mandatory metadata enrichment (volume/pages/DOI). Compares against `minions/roles/writer/skills/citation-audit.md`. |
| C-06 | scientific-critical-thinking | `Awesome-.../04-K-Dense-AI-claude-scientific-writer/scientific-critical-thinking/` | TBD | claim-evidence rigor, hypothesis vs data. Touches per-figure analysis pain point. |
| C-07 | peer-review (K-Dense Writer) | `Awesome-.../04-K-Dense-AI-claude-scientific-writer/peer-review/` | 24 KB | Cross-reads with Reviewer skills; surface-only because we are testing **writer-side**, not Reviewer. Excluded from R7 unless probe specifically tests "writer drafts review-anticipating prose". |
| C-08 | academic-paper (12-agent) | `academic-research-skills-main/academic-paper/` | 32 KB | R1 explicitly skipped this for "locks the workflow"; R7 will not re-test wholesale, but mines its abstract / intro / RW sub-modes for borrow-able rules. |
| C-09 | academic-paper-reviewer | `academic-research-skills-main/academic-paper-reviewer/` | 22 KB | Reviewer-side; out of R7 writing scope. **Excluded.** |
| C-10 | rigor-reviewer | `Agent-Native-Research-Artifact-main/skills/rigor-reviewer/` | 17 KB | Same as C-09. Excluded from R7. |
| C-11 | research-manager | `Agent-Native-Research-Artifact-main/skills/research-manager/` | 16 KB | Orchestration; touches paper structure but is not section-level writing. Excluded. |
| C-12 | compiler | `Agent-Native-Research-Artifact-main/skills/compiler/` | 15 KB | Closer to LaTeX build; cross-reads with `minions/roles/writer/skills/paper-compile.md`. Held for fork-narrowly review post-R7. |
| C-13 | paper-write (ARIS) | `Awesome-.../42-wanshuiyin-ARIS/skills/paper-write/` | 19 KB | LaTeX section-by-section writer; uses outline + section-mode. Strong CNS candidate for "draft section X under discipline Y" probe. |
| C-14 | proof-writer (ARIS) | `Awesome-.../42-wanshuiyin-ARIS/skills/proof-writer/` | 7.6 KB | Theorem / lemma writer; conference-only relevance. Held. |
| C-15 | formula-derivation (ARIS) | `Awesome-.../42-wanshuiyin-ARIS/skills/formula-derivation/` | 9.3 KB | Same — held; not a CNS-prose candidate. |
| C-16 | composer (lishix520) | `Awesome-.../01-lishix520-academic-paper-skills/composer/` | TBD | Section composer; conference variant. Probe-3 candidate. |
| C-17 | strategist (lishix520) | `Awesome-.../01-lishix520-academic-paper-skills/strategist/` | TBD | Story-shaping; touches contribution bullets in Intro. |
| C-18 | stat-writing (fuhaoda) | `Awesome-.../06-fuhaoda-stats-paper-writing/stat-writing/` | TBD | Stat-paper specific; relevant for hypothesis / methods-paper probes. |
| C-19 | ml-paper-writing (Orchestra) | `Awesome-.../07-Orchestra-Research-AI-Research-SKILLs/ml-paper-writing/` | TBD | Conference-target. |
| C-20 | academic_writing (dariia-m) | `Awesome-.../27-dariia-m-my_claude_skills/academic_writing/` | TBD | Econ-leaning; deprioritised (domain mismatch with bio CNS). |
| C-21 | abstract (dariia-m) | `Awesome-.../27-dariia-m-my_claude_skills/abstract/` | TBD | Direct overlap with `minions/roles/writer/skills/abstract-writing.md`. Probe-1 candidate. |
| C-22 | paper_verification (dariia-m) | `Awesome-.../27-dariia-m-my_claude_skills/paper_verification/` | TBD | Citation/claim verification. |
| C-23 | dont-lie (dariia-m) | `Awesome-.../27-dariia-m-my_claude_skills/dont-lie/` | TBD | Anti-hallucination; paper-claim hygiene. |
| C-24 | nature-data | `nature-skills-main/skills/nature-data/` | 6.3 KB | R3.A import-strongly. Out of R7 writing-prose scope; do not re-test. |
| C-25 | nature-citation | `nature-skills-main/skills/nature-citation/` | 12 KB | R6.B Prevents real failure. Out of R7 prose scope. |
| C-26 | nature-response | `nature-skills-main/skills/nature-response/` | 6.4 KB | Out of R7 (rebuttal). |
| C-27 | research-paper-writing references | `Research-Paper-Writing-Skills-main/research-paper-writing/references/` | section guides | Loaded only when C-01 triggers. |

R7 active candidates (will run Stage 1 first per user direction):
**C-01, C-02, C-03, C-04, C-05, C-06, C-13, C-16, C-17, C-19, C-21**

Adjustments after deeper inspection:
- **C-22 (paper_verification)** is an R-script / econ replication audit skill, not a CNS-prose citation skill. Domain mismatch. **Excluded from R7.**
- **C-23 (dont-lie / anti-hallucination)** is a generic Claude-Code "always activate" guard, not paper-specific. Adds no signal vs. a properly-instructed Haiku baseline on a paper task. **Excluded from R7.**
- **C-21 (dariia-m abstract)** is econ-specific (point estimates, AER/QJE patterns). Will probe under P1 only as a domain-stress test, not under P9 (conference variant, would underperform on CNS-bio).

Total active candidates: **11**.

R7 deferred-by-scope (not re-tested but may be cross-referenced in synthesis):
C-07, C-08, C-09, C-10, C-11, C-12, C-14, C-15, C-18, C-20, C-24, C-25, C-26.

## CNS pain → probe map

Every probe states: paper type, fixture, decidable right answer, expected
failure mode in baseline, expected calibration in candidate.

### P1 — Abstract / Conclusion paragraph discipline

- **Pain:** abstract / conclusion broken into 3+ paragraphs; contains
  citations or specific numerical results or dataset names.
- **Probe (Standard, CNS):** Given a 4-paragraph draft abstract that
  contains 2 inline `\cite{}` calls, 2 specific accuracy numbers, and
  a dataset name (CIFAR-10), and given the user instruction "polish for
  *Nature Methods* submission," produce the polished abstract.
- **Decidable right answer:** ONE paragraph; ZERO `\cite{}`; numbers and
  dataset name removed or replaced with qualitative descriptors. "Here we
  show" or equivalent main-result anchor present.
- **Hard probe:** Same draft, but the source contains a borderline
  number ("a 12-fold increase") that *could* be qualitative. Tests
  restraint — does the candidate keep "12-fold" (overreach) or
  abstract to "an order-of-magnitude increase" (calibrated)?
- **Targets:** C-01, C-02, C-04, C-13, C-21 (most direct); C-03, C-16, C-17, C-19 (cross-comparison).

### P2 — Introduction vs Related Work scope

- **Pain:** Introduction discusses implementation details (specific
  optimisers, learning rates, layer counts) instead of high-level method
  classes.
- **Probe (Standard, CNS):** Draft an Introduction for a methods paper
  combining diffusion-prior with retrieval, given a brief that contains
  both high-level intuition and low-level implementation notes. Right
  answer: high-level method classes only (e.g. "diffusion-based generative
  priors" + "retrieval-augmented decoding"), NO mention of layer counts,
  optimiser settings, or hyperparameter values.
- **Decidable right answer:** Implementation-detail terms (e.g. "2-layer
  Transformer with 8 heads", "learning rate 1e-4") absent from Intro.
- **Hard probe:** Identical brief but the user prompt also says "include
  the contribution bullet list (it's a conference paper)". Tests
  CNS-vs-conference mode-switching: list is OK in conference Intro,
  not OK in Nature-style.
- **Targets:** C-01, C-02, C-13, C-16, C-17, C-19.

### P3 — Related Work depth (the inverse of P2)

- **Pain:** Related Work treated as bibliography dump with citations but
  no per-method description.
- **Probe (Standard, CNS):** Given an Introduction that mentions
  "diffusion-based priors" + "retrieval-augmented decoding" + "GAN
  baselines", draft the Related Work section. Right answer: each
  method-class paragraph names the model used, the algorithm, and the
  specific implementation properties (architecture / loss / training
  data) for the cited works.
- **Decidable right answer:** ≥ 1 sentence per method-class paragraph
  describing model + algorithm; ≥ 1 sentence describing implementation.
- **Targets:** C-01, C-13, C-16, C-19.

### P4 — Experiments completeness

- **Pain:** Main results table without ablation, hyperparameter, or
  case-study coverage; figures without per-figure analysis.
- **Probe (Standard, CNS):** Given a Methods section describing a
  3-module model (X + Y + Z) and a results.csv with main-comparison
  numbers only (no ablation), draft the Experiments section outline
  + the first results paragraph + the analysis paragraph for Figure 1.
- **Decidable right answer:** Outline must include at minimum {main,
  ablation per module + cross-ablation, hyperparameter sweep, case
  study + visualisation}. The Figure-1 analysis paragraph must compare
  against listed baselines AND explain *why* our method wins per design
  reason; not just report numbers.
- **Hard probe:** Same Methods, but the brief says "results.csv only
  contains main-comparison; ablation is not yet run". Tests restraint
  vs fabrication — does the candidate fabricate ablation numbers, or
  flag the gap with `[needs experiment]`?
- **Targets:** C-01, C-02, C-13, C-19.

### P5 — Per-figure / per-table analysis

- **Pain:** Figures and tables have captions but no analysis prose
  ("our method wins" with no reason).
- **Probe (Standard, CNS):** Given a 4-row results table (Baseline-1990
  / Baseline-2024-SOTA / Ours / Ours-no-Z) with realistic numbers, write
  the analysis paragraph.
- **Decidable right answer:** Paragraph must (a) acknowledge SOTA's
  strengths, (b) name the design reason for our improvement, (c)
  reference the no-Z column to show Z is the load-bearing module.
- **Targets:** C-01, C-02, C-06, C-13, C-19.

### P6 — LaTeX typographic discipline

- **Pain:** Overuse of `enumerate` / `itemize`; lazy `\paragraph`
  bolding; inconsistent model-name typography; bad punctuation /
  parenthesis hygiene.
- **Probe (Standard, CNS):** Given a draft Methods subsection that uses
  `\begin{itemize}` for a 4-step procedure, three lazy `\paragraph{Step
  1.}` headers, and the model name "OurNet" rendered inconsistently as
  `\texttt{OurNet}` / `\textsf{OurNet}` / plain `OurNet`, polish to CNS
  style.
- **Decidable right answer:** itemize replaced with inline numbered
  prose ("First, ...; second, ...; third, ..."); `\paragraph{}` removed
  unless the paragraph is genuinely long and the bolded title is a real
  summary; a `\newcommand{\ourmethod}{...}` macro defined and used
  consistently.
- **Hard probe:** Same draft but for a conference paper. Tests
  mode-switching: contribution bullets are OK in conference Intro;
  paragraph headers as section-summary anchors are OK in long
  conference sections.
- **Targets:** C-01, C-02, C-13. (No competitor explicitly covers
  LaTeX typography. **This is a likely new-skill gap.**)

### P7 — Abbreviation first-use discipline

- **Pain:** Full term used twice; abbreviation introduced only once with
  inconsistent later usage.
- **Probe (Standard, CNS):** Given a 5-paragraph manuscript snippet
  where "Convolutional Neural Network" appears 6 times in full and the
  abbreviation "CNN" never, polish.
- **Decidable right answer:** First occurrence: "Convolutional Neural
  Network (CNN)"; subsequent: "CNN".
- **Targets:** C-01, C-02, C-04, C-13, C-21.

### P8 — Zero-hallucination citation under CNS scrutiny

- **Pain:** Made-up DOIs / titles / author lists; citations attached to
  claims they do not actually support.
- **Probe (Standard, CNS):** Given a Discussion paragraph asserting "X
  has been shown to improve Y by 30% (Wang et al. 2022)", but the Wang
  2022 paper actually reports a 12% improvement, polish the citation
  layer.
- **Decidable right answer:** Either correct the percentage to match
  the cited source, OR replace with a `\citep{[needs verification]}`
  placeholder, OR remove the percentage. Must NOT silently keep "30%"
  with the same citation.
- **Targets:** C-05 (heavy citation-management), C-22, C-23, plus
  cross-comparison vs `minions/roles/writer/skills/citation-audit.md`.

### P9 — Conference-paper variant (mode-switch sanity check)

- **Pain:** A skill that's optimised for CNS may break a conference
  paper (which legitimately wants contribution bullets in Intro,
  paragraph-summary headers in long sections, fewer bounded-implication
  closers).
- **Probe (Standard, conf):** Given the same brief as P2 but with
  "ICML camera-ready format" instruction, draft the Introduction.
- **Decidable right answer:** Contribution bullet list present; method
  classes still high-level; implementation details still in
  Method/Experiments, not Intro.
- **Targets:** C-01, C-02, C-13, C-16, C-19. Confirms a skill is
  not over-fit to CNS prose.

### P10 — End-to-end CNS section coordination

- **Pain:** Skill might pass per-section probes but produce contradictory
  Intro vs Discussion (e.g., Intro promises mechanism X, Discussion does
  not deliver).
- **Probe (Hard, CNS):** Given Methods + Results, draft Intro + Abstract
  + Conclusion in one shot.
- **Decidable right answer:** Same main-result claim across all three;
  same scope of implication; no contradictory hedging.
- **Targets:** C-01, C-02, C-13. Multi-skill orchestration.

## Run protocol

Following `~/.claude/skills/skill-evaluator-by-metaharness/SKILL.md` and
`SkillTest/README.md` Stage-0 then Stage-1.

### Stage 0 — SSL recall

1. Build skill-index:
   - 13 R7 candidates' frontmatter `description` (first 200 chars).
   - 15 currently-shipped MinionsOS Writer skills' frontmatter as
     production distractors (the most realistic discoverability test).
   - 5 unrelated MinionsOS skills (coder, experimenter, reviewer) as
     pure noise.
2. For each of P1–P10, ask Codex GPT-5.5 (`reasoning_effort: low`,
   `sandbox: read-only`): "given probe X, name top-3 skills that should
   load." Store under `R7-writing-restart/ssl-recall/`.
3. **Recall threshold:** Pass = candidate appears in top-3 for ≥ 1
   probe where it is conceptually load-bearing. Fail = description
   needs rewriting before Stage-1 burns compute on it.

### Stage 1 — Behavioural A/B

For each (candidate, probe-it-passed-recall-on) pair:

1. Spawn two Haiku 4.5 agents in parallel, both background.
   - **BLUE (baseline):** brief only, no skill in context.
   - **RED (candidate):** brief + candidate skill text prepended.
   - Both: `≤ 350 words, decision-oriented, in Writer voice`.
2. When both return: dispatch one Codex blind judge per probe.
   - Random RED/BLUE labelling per case.
   - Verbatim brief + verbatim outputs.
   - Expected-behaviour signature in 1 sentence.
   - Strict JSON: `{winner, reasoning, skill_effect_estimate, confidence}`.
3. Save to `R7-writing-restart/case-<probe>-<skill>/{baseline.md,
   candidate.md, verdict.md, tokens.json}`.
4. Bucket per `SkillTest/README.md` rubric (Prevents real failure /
   Calibrates / Matches / Overreaches).

### Hard-probe rule

Any "Matches baseline" or "Overreaches" result on a probe must be
re-tested with the matching hard-probe variant (P1H / P2H / P4H / P6H)
before recommending skip / fix.

### Cost estimate

13 candidates × ~3 probes each (after recall filtering) ≈ 39 (RED, BLUE)
pairs ≈ 78 Haiku spawns + 39 Codex judgments. Expected:
~78 × 35 k = **~2.7 M Haiku input tokens**, ~39 × 17 k = **~660 k Codex
input tokens**. Output tokens ≈ 78 × 350 + 39 × 600 = **~50 k output**.
Wall-clock: 2-3 hours assuming batches of 10 spawns.

## Distillation policy

After all R7 verdicts:

1. Author `synthesis/R7-synthesis.md` listing per-candidate bucket.
2. Update `synthesis/what-to-import.md` / `what-to-fork.md` /
   `what-to-skip.md` with R7 rows.
3. For new gaps (P6 LaTeX typography is the main expected gap):
   draft `synthesis/proposed-skills/cns-latex-typography.md` and any
   other CNS-specific gap skills surfaced by the run.
4. For existing-skill update opportunities: draft
   `synthesis/proposed-updates/{abstract-writing,citation-audit,
   end-to-end-paper-workflow,paper-work-boundaries}.md.diff` if R7
   evidence justifies adding the user's pain rules as HARD rules.
5. Record promotion record in
   `promoted/academic-writing/R7-RECORD.md` listing
   import-strongly / fork-narrowly / skip per candidate.

**Production-zone rule still holds.** Nothing lands in
`/Users/mjm/MinionsOS/minions/roles/writer/skills/` until user
explicitly approves.

## Open question (single decision required from user)

R7 candidate set above includes both R1.C-imported `nature-polishing`
(C-02) and a re-test of it under R7's CNS-typography pain list. Two
ways to handle this:

- **Option A — Re-probe nature-polishing** under P1, P2, P5, P6, P7
  (the pain points R1.C did not cover). Generates fresh evidence;
  may surface gaps R1.C verdict missed; ~5 extra A/B pairs.
- **Option B — Trust R1.C verdict on nature-polishing**, use it only as
  a calibration anchor (i.e., compare every other candidate against
  nature-polishing as a known-good baseline). Cheaper.

R7 default = **Option A**, because the pain list is materially
different from R1.C's fixtures (typography + abbreviations + LaTeX
hygiene were not tested). User can override.
