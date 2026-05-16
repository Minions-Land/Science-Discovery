# Fixture: abstract-rough

**Type:** writing — half-finished abstract
**Use in:** R1.C nature-polishing, R2 research-paper-writing
**Purpose:** Test whether the skill (a) builds the six-rung Nature ladder
(broad context → technical background → study problem → main result →
knowledge delta → general context), (b) hits an explicit "here we show"
sentence, (c) trims method detail that crowds out result.

## Source abstract (deliberately rough)

> CRISPR-Cas9 has become a widely-used tool for editing genomes in many species,
> however its delivery to the central nervous system has remained challenging
> due to the blood-brain barrier and the immunogenicity of viral vectors. To
> address this we developed a lipid nanoparticle (LNP) formulation containing a
> novel ionisable lipid (compound 14B) and a brain-targeting peptide. The
> formulation was prepared by microfluidic mixing at a flow ratio of 3:1, with
> particle size 78 nm and PDI 0.12, encapsulation efficiency 92%. We delivered
> Cas9 mRNA and a guide RNA targeting *PCSK9* to mouse brain via intravenous
> injection. We observed editing in 38% of cortical neurons at 14 days. The
> formulation was well tolerated. We think this work could enable many neurological
> applications and represents a significant advance in CNS gene editing.

## Brief for the runner

> Rewrite this 150–200-word abstract for submission to a Nature-family journal.
> Target the four-question abstract test: what was asked, how was it addressed,
> what was found, why does it matter.

## Failure modes the runner should fix

- Method detail (microfluidic 3:1, PDI 0.12) crowds the abstract; belongs in Methods
- No explicit `here we show` or equivalent
- Knowledge delta is implicit ("a significant advance" is a claim, not evidence)
- "We think" as concluding hedge — replace with bounded claim
- Closing sentence overclaims ("could enable many neurological applications")
- Six-rung ladder mostly missing the broad context rung (currently jumps to CRISPR-tooling tone, not why genome editing in CNS matters at all)

## Reference rewrite expectations

1. One opening sentence on why genome editing in the CNS matters at the field level
2. One sentence on the technical blocker (BBB / vector immunogenicity)
3. One-sentence study problem
4. Explicit "here we show" or equivalent direct verb for the main result
5. 1–2 sentences on what changed compared to prior CNS-delivery vectors
6. One closing sentence that bounds the implication (no "could enable many ...")
7. Method details kept minimal; specifics deferred to Methods section
