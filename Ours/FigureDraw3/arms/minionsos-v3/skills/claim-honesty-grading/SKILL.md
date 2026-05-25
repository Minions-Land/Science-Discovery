---
slug: claim-honesty-grading
summary: Theorem is contractual — grade as Proposition / Conjecture / Result when proof is sketchy. Distinguish "determined by framework" from "tuned from external data". Audit capability claims against actual scope; propagate fixes across abstract / intro / discussion / tables.
layer: logical
tools:
version: 1
status: active
references: theoretical-justification, paper-quality-contract, submission-cleanup-audit
provenance: human + EACN-005-PRL Round 1-2 + MinionsOS-Paper Reviewer-Shelf overclaim
---

# Skill — Claim Honesty Grading

Three failure modes survive ordinary QA: (1) hand-wave proofs labelled `Theorem`, (2) numerical inputs described as "determined by the framework", (3) capability statements that exceed what the system actually does. All three look fine sentence-by-sentence and are caught only by a dedicated grading pass.

## When to invoke

- About to label a result `\begin{theorem}` or "Theorem 1".
- About to write "α is determined by X" / "follows from Y" where Y is a framework / algebra / principle.
- Editing the Abstract, Introduction contribution bullets, Discussion, or capability comparison table.
- Reviewer flagged "you claim X but the system can't actually do that".

## The grades

| Grade | Use when |
|---|---|
| `Theorem` | Full proof in main or appendix; every step justified; assumptions stated; no missing case. |
| `Proposition` | Argument is rigorous in scope but a deep theorem invocation (linked-cluster, adiabatic-connection, Atiyah-Singer) is sketched, not proven. |
| `Conjecture` | Believed true; numerical / asymptotic evidence supports it; rigorous proof not in hand. |
| `Result` | Computed from data / DMRG / ED / fits, not derived. Report with system size and method, not as a theorem. |

If the proof has a one-sentence linked-cluster sketch and you're calling it a theorem, downgrade. The PRL Round 2 ledger explicitly demoted Theorem D.6 → Conjecture and Theorem D.7 → Proposition (Conditional Universality) for exactly this reason.

## "Determined by" vs "tuned from"

Failure pattern: *"α_i are determined by the W_{1+∞} algebra"* when α_i are obtained by numerical evaluation of sums over the Laughlin structure factor.

Rule: separate **"the algebra organizes the perturbation theory"** from **"the numerical values require external input"**. State both.

- `determined by` is reserved for *closed-form* derivation: α = f(g, β) where f is given.
- `evaluated from` / `obtained by numerical fit to` / `extracted from [dataset]` is required when the value depends on external input.

## Capability scope walk

Before sending a manuscript or comparison table, walk these four locations and check that every capability claim matches the system's actual scope:

1. Abstract claims.
2. Introduction contribution bullets.
3. Discussion / "what this enables" prose.
4. Capability comparison table (if any).

Flag any claim that would not survive a one-sentence challenge from a reviewer who has read the system implementation. Specific failure mode: Reviewer claimed "audits Shelf"; actual scope is "audits submission package" (Reviewer-Shelf overclaim, MinionsOS-Paper). The mirror failure is *underclaim*: a pillar originally called "Pluggable Skill Nodes" was renamed to "Workflow Plugin" once the actual scope (external workflow + MCP server + domain pack + skills, registered as a full EACN3 Agent) was verified to be broader than "skills".

## Propagation on fix

When a single overclaim is corrected, the same correction must propagate to every other location it appears. Coexistence is Major-Revision-class. See `submission-cleanup-audit.md` partial-integration sweep.

Recipe: after the local fix, `grep` for the *old* phrasing across the entire `branches/writer/paper/`. Every match either gets updated or earns a comment explaining why it's a different claim.

## Output habit

Mark grade choices explicitly in commit messages: `downgrade Theorem D.6 → Conjecture (linked-cluster sketch incomplete)`. Every claim adjustment carries `[derived: <evidence pointer>]` per evidence-first EACN convention.

## Pitfalls

- Treating `Theorem` as cosmetic. Reviewers grade harshly when proofs do not match the label.
- Conflating "the framework predicts X" with "X is determined by the framework alone".
- Patching one location and assuming the rest follows.
- Hedging instead of grading: "we believe the result is rigorous" is not a grade.
- Renaming a pillar without checking the new name's scope claim against implementation. "Workflow Plugin" is broader than "Skill Node" — adoption was justified only after confirming the system absorbs full workflow surfaces (MCP server + domain.md + skills + EACN3 Agent registration), not just skill files.
