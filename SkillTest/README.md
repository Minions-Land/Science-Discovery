# SkillTest — CNS Skill Library Evaluation

Long-running benchmark for CNS-grade writing / figure / rebuttal skills.
Every round produces real artefacts (rewritten prose, rendered SVG/PDF) plus
token usage, so the evidence stays auditable years later.

## Goals

1. **Decide what to port into MinionsOS.** Each round closes with a row in
   `synthesis/what-to-import.md`, `what-to-fork.md`, or `what-to-skip.md`.
2. **Stand up a long-term benchmark.** Fixtures + rubric are frozen baselines.
   Future skills test against the same inputs and rubric.

## Layout

```
SkillTest/
├── README.md                # this file
├── fixtures/                # shared inputs (writing / figures / rebuttal)
├── rounds/                  # one folder per (round, candidate skill)
│   └── R<N>-<skill-slug>/
│       ├── case-<name>/
│       │   ├── baseline.{ext}
│       │   ├── candidate.{ext}
│       │   ├── transcript.md
│       │   ├── tokens.json
│       │   └── verdict.md
│       └── ROUND_NOTES.md
├── synthesis/               # cross-round conclusions
└── templates/               # verdict / tokens / round-notes templates
```

## Method

The method is two-stage, MetaHarness-aligned, with one extension for figure
fixtures: we keep real artefacts and a numeric rubric on top of the blind
verdict, because vector quality and information architecture cannot be judged
from text alone.

### Stage 0 — SSL recall (must run first for any new skill)

Behavioural evidence is moot if the skill is never picked. Before running any
A/B, check whether the candidate's `description` / `summary` makes it
discoverable at the right moment.

1. Collect the frontmatter `description` (or first 200 chars of the summary)
   from every skill in the candidate's library plus 10–15 distractor skills
   (writer / coder / reviewer skills from MinionsOS make good distractors).
2. Show the descriptors to a fresh model and ask: "given probe X, name the top
   3 skills that should load." (probe X is the fixture brief.)
3. Pass = candidate is in top 3 for its intended probe; **fix the description
   first** if it isn't. Running Stage 1 on a non-recallable skill is wasted compute.

Skip Stage 0 only when (a) we are hand-loading a single skill for an isolated
test (R1.A / R1.C — fine) or (b) we already verified recall in a prior run.

### Stage 1 — behavioural A/B with real artefacts

For each `(skill, fixture)` pair:

1. **Baseline (BLUE in judge prompt).** Clean Codex/Claude session, no skill
   context, only the fixture brief. Record the artefact (rewritten prose,
   rendered SVG/PDF) byte-for-byte.
2. **Candidate (RED in judge prompt).** Same brief, same model, same params;
   only the candidate skill's `SKILL.md` (and references it auto-pulls) is
   prepended as system context.
3. **Token capture.** Both runs save `{input, output, cached, total, wall_time}`
   into `tokens.json`.
4. **Visual inspection (figure rounds only — mandatory).** Render both artefacts
   to PNG (or load the SVG directly) and view them in a browser via Playwright.
   Don't trust code review and Codex's verbal description alone — open the file
   and look. Record observations:
   - Palette: are the colours actually colourblind-safe in the rendered output, or
     just declared so in code? Look for adjacent muddy hues, near-greys mistaken
     for accents, gain-vs-loss signals reading the same.
   - Text: overlapping labels, truncated tick marks, legend covering data, fonts
     falling back to a default that the script didn't ask for.
   - Caption-vs-figure consistency: does the figure actually defend the claim
     stated in the brief? Are panel labels (a/b/c/d) where the caption says they are?
     Does the dashed baseline line in panel A actually appear?
   - Geometry: aspect ratio reasonable for the journal column; hero panel actually
     dominant; whitespace not collapsing or exploding around panels.

   Any visual finding that contradicts the code's intent goes into `verdict.md`
   under "What the skill missed or hurt" — code that *says* the right thing but
   *renders* wrong is a failure mode the rubric needs to catch.
5. **Numeric rubric.** Fill `verdict.md` against the rubric below — both runs.
   Score before reading the blind verdict; the rubric is *what the runner
   thinks*, the blind verdict is *what an external judge thinks*.
6. **Blind judgement.** Pass both artefacts to a Codex judge with random
   RED / BLUE labels (so Codex can't fingerprint by position), the verbatim
   brief, the expected-behaviour signature, and the instruction "ignore
   skill-internal terminology — judge by decision quality and artefact
   quality". Output: `{winner, reasoning, skill_effect_estimate, confidence}`.
7. **Bucket.** Classify into one of:

   | Bucket | Meaning |
   |---|---|
   | **Prevents real failure** | Without skill, baseline produces a wrong artefact (e.g. truncates y-axis, fabricates DOI, mixes Results + Discussion tense). |
   | **Calibrates response** | Both reach roughly the right artefact; candidate is better defended (specific n, hedging scaled to evidence, palette unified). |
   | **Matches baseline** | No measurable difference. Re-test with a hard probe before recommending deletion. |
   | **Overreaches** | Candidate is *worse* than baseline (e.g. forces a layout the brief did not ask for, edits content the user did not flag). |

8. **Hard probe (optional, but used on any "Matches baseline" skill).** A second
   fixture variant where the skill's rule is non-obvious — borderline overclaim,
   ambiguous archetype, partial information. Catches skills whose value is in
   restraint, not action.

9. **Round notes.** After all cases in the round, write `ROUND_NOTES.md`
   with the per-case rubric scores, the per-case bucket, and the porting
   recommendation.

## Rubrics (frozen — do not edit per round)

### Writing rubric (22 pts)

| Dim | Pts | What earns the points |
|---|---|---|
| Argument clarity / paper-type fit | 4 | Identifies paper type; section logic matches it |
| Hedging calibration | 3 | demonstrate / suggest / may scaled to evidence |
| Sentence rhythm | 3 | ≤30 words; no 5 adjacent paragraphs of identical length |
| AI-trace removal | 3 | No "delve into / crucial / it is important to note"; ≤2 em-dashes/page |
| Claim-evidence completeness | 4 | Every load-bearing claim traceable to data or citation |
| Citation hygiene | 3 | DOI present where available; no second-hand citations passed off as primary |
| House style consistency | 2 | British / American not mixed; terminology stable |

### Figure rubric (22 pts)

| Dim | Pts | What earns the points |
|---|---|---|
| Information architecture / non-redundant panels | 4 | Each panel answers a unique question |
| Visual hierarchy / hero panel | 3 | One panel dominates; others subordinate |
| Palette discipline | 3 | Unified method palette; colourblind-safe |
| Typography & export | 3 | sans-serif (Arial), `svg.fonttype=none`, editable text |
| Statistical annotation | 3 | n, error bar definition, significance markers |
| Reproducibility | 3 | Code runs end-to-end; source data present |
| Review readiness | 3 | Legend self-contained; not dependent on prose |

### Rebuttal rubric (15 pts)

| Dim | Pts | What earns the points |
|---|---|---|
| Comment ID + classification | 3 | Stable ID; type tag (claim / experiment / framing / scope) |
| Action mapping | 3 | ACCEPT / SOFTEN / DISAGREE / AUTHOR_INPUT_NEEDED tag |
| Traceability to manuscript | 3 | Cites section, page, line, figure, or supplement |
| Tone | 2 | Cooperative; disagrees only on scientific grounds |
| Completeness | 4 | Every comment receives a reply or unresolved flag |

## Skill index

Each skill tested gets one row here. Status: `pending` / `R<N>` / `imported` / `forked` / `skipped`.

| Skill | Path | Round | Status |
|---|---|---|---|
| nature-figure | `Skill/nature-skills-main/skills/nature-figure/` | R1.A | **fork-narrowly** (R1.A revised: 2 of 3 cases overreached visually; port content-discipline rules but reject mm-precision figsize and asymmetric L-grid hero) |
| scientific-figure-making | `Skill/figures4papers-main/scientific-figure-making/` | R1.B | **fork-narrowly** (R1.B complete: +5 / +6 / -2 across 3 cases; case-multi-panel **lost** to baseline; same multi-panel failure mode as R1.A nature-figure) |
| nature-polishing | `Skill/nature-skills-main/skills/nature-polishing/` | R1.C | **import-strongly** (R1.C complete: +5 / +4 / +3 / +2 across 4 cases; one "prevents real failure" + 3 "calibrates"; port plan in `rounds/R1-nature-polishing/ROUND_NOTES.md`) |
| nature-response | `Skill/nature-skills-main/skills/nature-response/` | R2 | **import-strongly** (R2 case-mixed-severity: 15/15 vs baseline 8/15; bucket "Prevents real failure"; stable IDs + action labels + no fabrication) |
| nature-citation | `Skill/nature-skills-main/skills/nature-citation/` | R3.B | **fork-narrowly** (R3.B 13/15 vs 9/15; "Calibrates"; structural overlay on no-network baseline; same anchor rule as R3.A — no fabrication) |
| nature-data | `Skill/nature-skills-main/skills/nature-data/` | R3.A | **import-strongly** (R3.A 18/18 vs 8/18; "Prevents real failure"; named DAC + DataCite + code repro fallback; confirms substantively-bounded specificity rule) |
| research-paper-writing | `Skill/Research-Paper-Writing-Skills-main/research-paper-writing/` | R2 | pending |
| skill-deslop | `Skill/Awesome-Agent-Skills.../skills/45-stephenturner-skill-deslop/` | R3.C | **skip** (Matches baseline; Opus 4.7 already removes blacklist terms) |
| avoid-ai-writing | `Skill/Awesome-Agent-Skills.../skills/47-conorbronsdon-avoid-ai-writing/` | R3.C | **skip** (Matches baseline) |
| humanizer-academic | `Skill/Awesome-Agent-Skills.../skills/44-matsuikentaro1-humanizer_academic/` | R3.C | **skip** (Matches baseline) |

## Anti-patterns (don't drift into these)

- Editing the rubric after seeing the candidate's output. Freeze the rubric per round.
- Letting the runner know it's an evaluation. Both baseline and candidate get the
  same instruction surface; only the system context differs.
- Importing a skill into MinionsOS just because it scored well on one fixture.
  Three or more cases or a strong R2 confirmation before porting.
- Fabricating fixture data. If a fixture cites a paper, the citation has to be real.
- **Skipping Stage 0 for unfamiliar skills.** A skill can win every Stage-1 A/B
  and still never load in production if its `description` doesn't surface it.
- **A/B in alphabetical order** (A always before B) — Codex fingerprints by
  position. Always randomise to RED/BLUE per case.
- **Treating "Matches baseline" as a delete recommendation.** Re-run with a
  hard probe; standard probes underestimate skill value 30–50% of the time.
- **Letting skill vocabulary leak into RED.** If the candidate emits "Phase 3"
  or "六阶梯" verbatim, redact before judging or instruct Codex to ignore
  skill-internal terminology.
- **Running this on Sonnet-class agents only.** MetaHarness is calibrated for
  Haiku-class executors; Sonnet alone often does what skills prescribe and
  differences vanish in the noise. For figure tasks where the executor is the
  same class as the production target (Codex / Sonnet / Opus), keep the
  rubric — it catches things blind A/B won't.
- **Scoring figure cases by code-layer evidence alone (R1.A lesson).** rcParams
  set correctly, palette dict present, gridspec asymmetric → all true does
  not imply rendered figure is submittable. Visual inspection of the rendered
  artefact is mandatory, not optional. If multimodal image read is unavailable
  in the runner's session, generate side-by-side Playwright screenshots and
  have the user / a separate visual judge confirm before scoring.
- **Treating `constrained_layout collapsed to zero` as cosmetic (R1.A lesson).**
  It is not. It means the rendered figure is cramped beyond legibility even
  if `bbox_inches="tight"` recovers a saved file. Re-render at larger figsize
  or fail the case.
- **Modifying production skill libraries during evaluation (hard rule).**
  Port recommendations live in `SkillTest/synthesis/proposed-skills/` and
  in each round's `verdict.md` / `ROUND_NOTES.md`. They are NOT applied to
  `/Users/mjm/MinionsOS/minions/roles/` (or any other production library)
  until the user explicitly approves. SkillTest is the research zone;
  MinionsOS is the production zone. Cross-pollination only happens by
  explicit user decision, never as a side effect of a round verdict.
