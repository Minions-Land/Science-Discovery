# Fixture: cns-mini-paper-end-to-end

**Type:** writing — multi-skill orchestration test
**Use in:** R5.A end-to-end multi-skill
**Purpose:** Test whether several promoted/forked skills work together when
loaded simultaneously, or whether they conflict / produce redundant outputs.

# Manuscript context (give to runner verbatim)

The user is preparing a Nature Communications submission on a CRISPR-Cas9
LNP brain-delivery platform. They give the runner a rough Chinese-influenced
English mini-paper consisting of:

(a) A rough abstract (the same `abstract-rough` fixture from R1.C).
(b) An overclaimed Discussion paragraph (the same `overclaim-paragraph`
    fixture from R1.C).
(c) A rough Data Availability statement (the same context from R3.A
    `manuscript-context`).
(d) Two reviewer comments to respond to (a subset from R2 fixture).

The user says: "Polish all four sections at once for Nature Communications
submission. Apply whatever skills you have."

# Brief for the runner

Polish all four sections (abstract, discussion paragraph, data availability,
rebuttal) for Nature Communications submission. The runner should:

1. Identify which skills apply to which section.
2. Apply each skill faithfully without redundancy (don't apply
   abstract-rules to a Discussion paragraph or to a rebuttal letter).
3. Handle the cross-section concerns:
   - Common terminology (compound 14B, PCSK9, 38% editing, etc.) stays
     stable across sections.
   - The substantively-bounded specificity rule applies in ALL four
     sections (no fabrication, no vague good-faith promises, name
     specific gaps).
4. Output should look like a coherent submission package, not a list of
   independently-polished snippets.

# Sections to polish

## (a) Abstract (rough)

CRISPR-Cas9 has become a widely-used tool for editing genomes in many
species, however its delivery to the central nervous system has remained
challenging due to the blood-brain barrier and the immunogenicity of
viral vectors. To address this we developed a lipid nanoparticle (LNP)
formulation containing a novel ionisable lipid (compound 14B) and a
brain-targeting peptide. The formulation was prepared by microfluidic
mixing at a flow ratio of 3:1, with particle size 78 nm and PDI 0.12,
encapsulation efficiency 92%. We delivered Cas9 mRNA and a guide RNA
targeting *PCSK9* to mouse brain via intravenous injection. We observed
editing in 38% of cortical neurons at 14 days. The formulation was
well tolerated. We think this work could enable many neurological
applications and represents a significant advance in CNS gene editing.

## (b) Discussion paragraph (overclaimed)

Our results clearly demonstrate that microbiome composition causes
susceptibility to inflammatory bowel disease (IBD), and we are the first
to show this. The 4.3-fold enrichment of *Faecalibacterium prausnitzii*
in healthy controls compared to IBD patients (n=82) proves that this
organism is protective. Our findings will fundamentally change how IBD
is treated, since probiotics targeting *F. prausnitzii* should now
become standard of care.

(NOTE: The Discussion paragraph is from a different study — IBD/microbiome.
This deliberately tests whether the runner correctly applies *register*
and *no-overclaim* rules without conflating the manuscript topic with
the LNP study above.)

## (c) Data Availability statement (rough Chinese-influenced English)

LNP formulation的data是部分能公开，但是动物实验的individual mouse data是
restricted的因为institutional review。Public data我们用了一个2019年的
Cas9-mRNA-injection paper的数据 (Nature 2019), 这些我们cite一下就可以。
Code我们willing to share但是compound 14B的合成路线我们想申请专利所以暂时
not release。如果有人想access individual mouse data, available upon
reasonable request from corresponding author.

## (d) Two reviewer comments to respond to

**Reviewer 1, Comment 1:**
> The 38% editing efficiency in cortical neurons is intriguing but the
> cohort is small (n=6). Please replicate in a second mouse strain with
> n≥12.

**Reviewer 1, Comment 2:**
> Compound 14B has not been chemically characterised in this manuscript
> beyond a structural diagram. Please provide ¹H-NMR, mass spectrum, and
> HPLC purity data.

Author position: accept both comments. Will replicate in C57BL/6 strain
with n=12 and add NMR / MS / HPLC to supplement.

# Failure modes the runner should fix

- Conflating the abstract topic (LNP CRISPR) with the discussion
  topic (microbiome IBD). The discussion paragraph is from a DIFFERENT
  study — runner should treat it as such.
- Applying the wrong skill to the wrong section (abstract rules to
  rebuttal, etc).
- Redundant cross-section rule application (e.g. removing AI-trace
  vocabulary 4 times instead of treating it as a global pass).
- Inventing data: fabricating page numbers, DOI for the 2019 Nature
  paper, restriction-access controller without naming it.
- Over-bloating: each section should stay concise per its own genre.
- Failing to apply the substantively-bounded specificity rule consistently
  across all four sections.

# Reference output expectations (for scoring, not shown to runner)

A passing output should:

1. Use cn-en-academic-polish (or equivalent rules) on the rough Chinese-
   influenced English (sections a and c)
2. Use abstract-writing's "Here, we show" + bounded-implication closer on
   section (a)
3. Use apply-revisions' Discussion-vs-Results verb taxonomy + boundary
   specificity on section (b)
4. Use the data-availability rules from R3.A on section (c) — named DAC,
   DataCite metadata for cited public data, code reproducibility fallback
   for patent-pending compound 14B synthesis
5. Use prepare-rebuttal's stable IDs + action labels + traceability hooks
   on section (d), including [X] placeholders for unknown line/page numbers
6. Maintain technical terminology consistently across sections
7. Not bloat — total polished output ≤700 words (each section ≤200 except
   abstract <250)
