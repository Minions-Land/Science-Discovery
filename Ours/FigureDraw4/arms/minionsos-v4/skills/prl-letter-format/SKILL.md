---
slug: prl-letter-format
summary: PRL Letter format pack — ≤3,750 words / ~4 pages, abstract ≤600 chars, no \section{}, ≤10–15 displayed equations (rest go to Supplemental Material), conclusion one paragraph or absorbed into closing discussion. Hard quantitative constraints; not soft style.
layer: logical
tools:
version: 1
status: active
references: latex-typography, abstract-writing, conclusion-limitation, paper-quality-contract
provenance: human + EACN-005-PRL Round 1
---

# Skill — PRL Letter Format

PRL Letters carry hard quantitative format constraints. Drafts that follow conference / journal conventions trigger an immediate format-rejection or a "shorten before review" verdict. The constraints below are quoted from EACN-005-PRL Round 1 and apply to any submission to *Physical Review Letters*.

## When to invoke

- Drafting or revising a manuscript targeted at PRL.
- Cross-venue submission where PRL is one option (apply this format only to the PRL branch).
- Trimming a longer manuscript down for PRL submission.

## The hard constraints

| Element | Constraint |
|---|---|
| Total length | ≤ 3,750 words OR ~4 journal pages including figures and references |
| Abstract | ≤ 600 characters / ~120 words, single paragraph |
| Sectioning | No `\section{}` headings. Use bold inline lead-ins: `*Introduction.—*`, `*Model.—*`, `*Results.—*`, `*Discussion.—*` |
| Displayed equations | ≤ 10–15 in main text. Intermediate steps go to Supplemental Material |
| Conclusion | One paragraph OR absorbed into the closing Discussion. Never half a page with subsections |
| Bibliography | Numbered `[1]`, `[2]` style; PRL-specific bib style file |

## Lead-in syntax

Replace every `\section{...}` with the inline pattern:

```latex
\textit{\textbf{Introduction.}}---We consider a system where…
```

Or via a custom macro:
```latex
\newcommand{\leadin}[1]{\textit{\textbf{#1.}}---}

\leadin{Introduction} We consider…
\leadin{Model} The Hamiltonian is…
\leadin{Results} We find…
\leadin{Discussion} The implication is…
```

## Equation budget management

Most theory drafts overshoot. Recipe:
1. Count displayed equations in the main text.
2. If >15, move intermediate steps (derivation chains, perturbation expansions, helper formulas) to **Supplemental Material**.
3. Keep in the main text only: the model definition, the central result, and one or two key derivation lines.
4. Cite Supplemental Material as `[S1]`, `[S2]` etc. for moved equations; reference each Supplemental section at the point the move was made.

## Abstract budget management

600 characters is roughly 4–5 sentences. Pattern:
1. Context (1 sentence): the open question.
2. Approach (1 sentence): what was done.
3. Result (1–2 sentences): the central finding with one concrete number / scaling / mechanism.
4. Implication (≤1 sentence): why it matters.

Cut adjectives, cut "we propose / we present", cut backstory.

## Procedure

1. **Length pass.** Count words; count equations; count abstract characters. Note overruns.
2. **Sectioning pass.** Replace every `\section{...}` with the lead-in pattern. Verify no orphan section markers remain.
3. **Equation pass.** Move intermediate steps to Supplemental Material; verify main-text equation count is ≤15.
4. **Abstract pass.** Tighten to ≤600 characters using the four-sentence pattern.
5. **Conclusion pass.** If the conclusion has subsections, collapse to a single paragraph or merge into Discussion.
6. **Final compile.** Verify PRL bib style, page count, and that the lead-in pattern renders correctly.

## Pitfalls

- Treating the 3,750-word limit as soft. PRL editors triage by length; over-budget triggers "shorten before review".
- Keeping `\section{...}` because "the template seems to allow it". The template allows it; PRL convention does not.
- 215-word abstract because "we have a lot to say". Cut.
- Equation budget violated by leaving derivation chains in the main text. Move to Supplemental.
- Half-page conclusion with subsections. PRL conclusion is one paragraph max.
- Treating Supplemental Material as overflow without naming what was moved. Each Supplemental entry must be referenced in the main text where the move was made.
