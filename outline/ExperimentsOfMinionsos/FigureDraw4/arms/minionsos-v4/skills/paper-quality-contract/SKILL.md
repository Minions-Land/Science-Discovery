---
slug: paper-quality-contract
summary: Six postures the user enforces on every paper — claim honesty, derivation hygiene, insight-first paragraph rhythm, naming-as-correctness, submission cleanup, venue reformat. Toolkit, not a sequential pipeline; pick the posture(s) the failure mode calls for.
layer: composite
tools:
version: 1
status: active
references: claim-honesty-grading, submission-cleanup-audit, derivation-hygiene, insight-first-paragraph, venue-reformat-workflow, prl-letter-format, hero-figure-prompt, latex-typography, citation-audit
provenance: human + Causality-Paper / MinionsOS-Paper / LLM-Survey / NeurIPS-2026 / EACN-005-PRL / ZheMa-Proposal review rounds
---

# Skill — Paper Quality Contract

The user's de-facto quality bar across every paper, distilled from review rounds on multiple manuscripts. Every posture below corresponds to a specific failure mode the user has flagged across sessions. This is the *quality* layer, orthogonal to `end-to-end-paper-workflow` (the pipeline) and `paper-work-boundaries` (the scheduling).

## When to consider this skill

- About to write or revise a substantive section.
- Reviewer or self-review caught a quality issue and you need to know which sub-skill to open.
- A draft has just been integrated and is heading into submission cleanup.

Skip when the work is a typo fix, a single-line patch, or a non-content commit.

## The six postures (toolkit)

| Posture | Sub-skill | Use when |
|---|---|---|
| **Claim honesty** | `claim-honesty-grading.md` | About to write `\begin{theorem}`, "determined by [framework]", or any capability claim. Grade `Theorem` / `Proposition` / `Conjecture` / `Result` honestly. |
| **Derivation hygiene** | `derivation-hygiene.md` | Method or appendix uses an approximation (cavity factorization, large-N limit, mean-field decoupling) — name it, scope it, bound or cite it. |
| **Insight-first paragraph** | `insight-first-paragraph.md` | Drafting a technical subsection — open with "the core insight is X", then formula+ref+implication. Anti-textbook-recap. |
| **Naming as correctness** | `latex-typography.md` (macro discipline + propagate-on-rename) | Picking a method / pillar / component name. Names bind method to object, never single generic word. |
| **Submission cleanup** | `submission-cleanup-audit.md` | Within a week of submission: orphan figures, multi-def labels, agent-artifact leakage, generic captions, partial-integration coexistence. |
| **Venue reformat** | `venue-reformat-workflow.md` | ICML→NeurIPS, conference→PRL, rebuttal incorporation, page-budget pressure. Sibling directory + cite sweep + rebuttal→appendix. |
| **Hero figure** | `hero-figure-prompt.md` | Figure 1 / illustration / method-overview hero — gpt-image-2.0, Times + LaTeX fonts, persisted prompt, Nature panel structure. |

For PRL specifically also open `prl-letter-format.md` (≤3,750 words, ≤600-char abstract, no `\section`, ≤15 displayed equations).

## Hard rules (override convenience)

These apply globally; sub-skills enforce them, but the contract is non-negotiable:

1. **No fake citations, no invented bibkeys.** Web search → reverse-lookup `references/*.bib` → cite if entry exists, else add entry first. Inventing a key is a fireable offense. See `citation-audit.md` bidirectional check.
2. **No engineering details in the body.** Paths, version numbers, code identifiers, git branch names, agent IDs go to the appendix. Body stays scientific.
3. **No checkmark / half-checkmark capability tables.** Replace ✓/½/✗ with per-feature explicit content (numbers, scopes, names). See `latex-typography.md`.
4. **Don't compile the PDF unless asked.** Edit `.tex`; the user runs `latexmk`. QA-readiness check is the only exception.
5. **Cross-section propagation on every fix.** A correction to one location must propagate to abstract / intro / discussion / capability table / every appendix. Coexistence of corrected and uncorrected is Major-Revision-class.
6. **Generic anything is fluff.** No "Common Development Tasks", no "Tips for Development", no "we propose a novel framework that…", no lettered enumerations `(a)…(b)…(c)…` in body prose, no single-line contribution bullets.
7. **Names bind method to object.** Not "Memory" but "Tri-Layer Memory (Draft/Book/Shelf)". Not "Reflection" but "Two-Tier Reflection (Ethics + Reviewer)". A name that doesn't bind a method is a renaming opportunity.

## How this composes with existing skills

Existing skills cover most procedural surfaces (`abstract-writing`, `introduction-discipline`, `methodology-discipline`, `theoretical-justification`, `experiments-completeness`, `package-submission`, `apply-revisions`, `prepare-rebuttal`, `paper-compile`, `figure-spec`, `academic-plotting`). This contract layer adds the *quality bar* those skills must clear and the *audit categories* the user expects an agent to catch on its own.

When a sub-skill conflicts with the contract, the contract wins. When existing skills already encode contract rules (`abstract-writing` requires single paragraph; `latex-typography` requires `\newcommand` macros), they are the canonical source — read them, don't re-derive.

## Pitfalls

- Treating the contract as a checklist or sequential pipeline. The postures are à la carte.
- Skipping `claim-honesty-grading.md` when promoting to `\begin{theorem}`. The label is contractual.
- Skipping `submission-cleanup-audit.md` because "QA already passed". QA does not check orphan figures, multi-def labels, agent-artifact leakage, or partial integration unless explicitly told to.
- Polishing prose on a draft that hasn't passed insight-first rhythm. You will polish the wrong layer.
- Renaming a pillar without running propagate-on-rename across abstract / intro / discussion / tables / figures.
