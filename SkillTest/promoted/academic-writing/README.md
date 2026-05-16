# Promoted — Academic Writing

Skills tested for prose polishing, abstract structure, register discipline,
Chinese-to-English translation. The strongest R1 category.

## Skills inside

### Third-party (kept as reference, not duplicated)

- **nature-polishing** — `/Users/mjm/Skill/nature-skills-main/skills/nature-polishing/`
  - Tested: R1.C (4 cases: results, intro-zh, overclaim, abstract)
  - R1.C Verdict: import-strongly (3 Calibrates + 1 Prevents real failure; 78% → 94% mean)
  - **R7 Verdict: DEMOTED — scope-restricted**
    - R7 tested 9 cases on CNS-discipline fixtures (Abstract paragraph collapse, Intro scope, LaTeX typography)
    - Result: skill won 2, lost 7, net = **−5**
    - Root cause: nature-polishing adds implementation details to Intro (350M-parameter, 50k-chain) and retains specific numbers in Abstract — both violate user's CNS rubric
    - **Decision**: nature-polishing remains valid ONLY for its R1.C-tested surfaces (Chinese-to-English polish, overclaim detection, verb taxonomy). It must NOT be used for:
      - Abstract/Conclusion structural discipline (use `abstract-discipline` from R7 skill-library instead)
      - Introduction scope control (use `introduction-discipline` instead)
      - LaTeX typography (use `latex-typography` instead)
    - The R1.C "import-strongly" verdict stands for its original scope; R7 narrows that scope.

### SkillTest drafts (authored from R1 evidence)

- **cn-en-academic-polish.md** → see `../synthesis/proposed-skills/cn-en-academic-polish.md`
  - New skill draft; covers Chinese-to-English mode (intro-zh case)

### R7 skill-library (new, replaces nature-polishing for structural discipline)

The following skills from `rounds/R7-writing-restart/skill-library/` are recommended to replace nature-polishing's structural guidance:

| Skill | Net score | Status |
|---|---|---|
| `citation-zero-hallucination` | +5 | **Promote** |
| `latex-typography` | +3 | **Promote** (rules R3, R6 validated) |
| `related-work-discipline` | +2 | **Promote** (rules R2, R3 validated) |
| `experiments-completeness` | +1 | Conditional promote (needs more data) |
| `abstract-discipline` | 0 | Neutral (rules R2, R4 validated; R1, R3 need refinement) |

### Update plans for existing MinionsOS skills

- **abstract-writing.md.diff** → see `../synthesis/proposed-updates/abstract-writing.md.diff`
- **apply-revisions.md.diff** → see `../synthesis/proposed-updates/apply-revisions.md.diff`

## Rules / patterns extracted (R1.C evidence, still valid)

| Rule | Case | What it does |
|---|---|---|
| Reconstruct logic before translating clauses | intro-zh +5 | Chinese drafts get rebuilt in publishable English order, not polished sentence-by-sentence |
| Hourglass restructure for Introduction | intro-zh +5 | gap-first → consequence → "Here, we" anchor |
| Refusal to fabricate quantification | intro-zh | Source said "substantial gain" with no numbers; candidate flagged "size of these gains should be reported in Results" instead of paraphrasing |
| Explicit "Here, we show" main-result anchor | abstract +3 | venue convention; baseline narrative formulation rejected |
| Bounded-implication closer | abstract +3 | "platform for further preclinical evaluation" not "for neurological disease" |
| Paper-type diagnosis as first move | results +2 | identify research / methods / hypothesis / algorithmic before any sentence-level edit |
| Results vs Discussion verb taxonomy | results +2 | observation verbs (was detected / increased / showed) vs interpretive verbs (may reflect / suggests / could indicate) |
| Sentence cap <= 30 words | all 4 cases | last sentence of paragraph is the most likely to overrun |
| AI-trace blacklist | all 4 cases | crucial / delve into / important to note / substantial / comprehensive / robust |
| Em-dashes <= 2 per page, never inside an English clause | all 4 cases | Chinese-influenced em-dash use is the tell |

## Recommendation (updated R7)

**Scope-restricted promotion.** nature-polishing is valid for:
- ✅ Chinese-to-English academic polish
- ✅ Overclaim detection / bounded-implication
- ✅ Verb taxonomy (Results vs Discussion)
- ✅ Sentence-level clarity (30-word cap, AI-trace blacklist)

nature-polishing must NOT be used for:
- ❌ Abstract/Conclusion structural discipline (→ use `abstract-discipline`)
- ❌ Introduction scope control (→ use `introduction-discipline`)
- ❌ LaTeX typography decisions (→ use `latex-typography`)
- ❌ Related Work organization (→ use `related-work-discipline`)

## Open questions for next round

- R7 skill-library skills need Stage 2 validation on fresh fixtures before full promotion to MinionsOS Writer
- The evolved configuration (`skill-library/_meta/evolved_config.json`) identifies 13 validated rules — these should be the priority for integration into MinionsOS Writer skills
