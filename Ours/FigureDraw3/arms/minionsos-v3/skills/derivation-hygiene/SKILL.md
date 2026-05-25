---
slug: derivation-hygiene
summary: Every load-bearing approximation must be named, scoped, and either bounded analytically or cited to its rigorous version. Cavity factorization, replica symmetry, large-N saddle, mean-field decoupling, Gaussian sums, deep-theorem invocation — each gets state, motivation, validity range.
layer: logical
tools:
version: 1
status: active
references: methodology-discipline, theoretical-justification, claim-honesty-grading
provenance: human + EACN-005-PRL Round 1
---

# Skill — Derivation Hygiene

A "self-respecting derivation" names its approximations. Reviewers caught the cavity field h_i^{(cav)} appearing without the factorization assumption being stated; they caught Gaussian sums without the (large N, bounded variance, finite higher moments) conditions; they caught the dAT-line stability not addressed; they caught Atiyah-Singer "incorrectly invoked" because the differentiable regime was unspecified. Every such omission is a derivation-hygiene failure.

## When to invoke

- Drafting Methods or Theoretical Analysis section.
- Writing an appendix containing perturbation theory, mean-field, replica, semiclassical, large-N expansions, or deep-theorem invocations.
- Reviewer flagged "the approximation regime is not stated" or "the proof has gaps".

## The hygiene rule

For every load-bearing move, the manuscript must state three things:

1. **Name** — what is the approximation called? (Cavity factorization. Replica symmetry. Large-N saddle. Mean-field decoupling. Gaussian sum approximation. Linked-cluster theorem. Adiabatic-connection argument.)
2. **Scope** — when does it hold? (T > T_c. Above the dAT line. Bounded variance + finite higher moments. Sparse coupling matrix. Smooth-deformation regime.)
3. **Validity** — bounded analytically (compute the leading correction, stability eigenvalue) OR cited to the rigorous version (Talagrand 2003 for Gaussian concentration; dAT 1978 for replica stability; Atiyah-Singer with regime; Mezard-Parisi-Virasoro for cavity).

Omitting any of the three is the failure mode.

## Worked example (PRL Round 1)

Wrong:
> "We introduce the cavity field h_i^{(cav)} and write the Bethe-Peierls equation."

Right:
> "Following the cavity method [Mezard-Parisi-Virasoro 1987], we assume that, conditional on removing site i, the neighbours of i are uncorrelated (the **factorization assumption**, valid in the high-temperature phase, equivalently above the dAT line [dAT 1978]). The cavity field h_i^{(cav)} is then well-defined, and we obtain… The breakdown of factorization below the dAT line is discussed in Sec. IV."

## Procedure

1. **Scan for moves.** Every `=`, `\approx`, `\sim`, `\to`, integration step, change of variables, large-N limit, replica trick, mean-field decoupling, semiclassical expansion, deep-theorem invocation is a candidate move.

2. **Fill three slots per move.** Name + scope + validity. If the move is exactly an algebraic identity, no slots required. If the move is approximate, asymptotic, or invokes a deep theorem, all three are mandatory.

3. **Cite the rigorous version.** For approximations that have a rigorous treatment (Talagrand-type concentration, dAT stability, semicircle law, Atiyah-Singer with manifold regularity), cite it. If you cannot cite a rigorous version, downgrade the surrounding claim to `Proposition` / `Conjecture` per `claim-honesty-grading.md`.

4. **Add a regime-of-validity remark to each theorem.** A theorem statement without a stated regime is a draft. The Atiyah-Singer invocation in PRL Round 1 was ruled "incorrectly applied" because the regime was not specified.

5. **Stability eigenvalue or leading correction.** For mean-field-class derivations, either compute the stability eigenvalue (replica saddle, Gaussian fluctuations) or cite the result that bounds it. Without one of those, the reviewer cannot tell whether the approximation is robust.

## Pitfalls

- "Standard cavity method" without naming the factorization assumption.
- Gaussian sums "by central limit" without stating variance / moment conditions.
- Mean-field decoupling without "valid above T_c" or "valid in the saddle-stable region".
- Deep-theorem invocation (Atiyah-Singer, Cobordism, Eilenberg-MacLane) without specifying the topological / differentiable regime.
- Treating "we assume X" as sufficient — the *scope* of X must be stated, not just X itself.
- Confusing the algebraic structure (which "organizes the perturbation theory") with the numerical input (which "requires external input"). See `claim-honesty-grading.md` "determined by vs tuned from".
