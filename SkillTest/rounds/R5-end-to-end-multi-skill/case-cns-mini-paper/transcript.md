# Transcript — case-cns-mini-paper

## Brief (verbatim brief section only)

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

## Source sections (verbatim)

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

## Baseline run

### What I did per section

- Abstract: Polished for Nature Communications style without loading skills; preserved supplied particle size, PDI, encapsulation efficiency, *PCSK9*, 38% editing and mouse context.
- Discussion paragraph: Treated as a separate IBD/microbiome study; softened causal, novelty and clinical claims.
- Data/Code Availability: Converted mixed Chinese-English notes into concise availability statements without inventing identifiers.
- Response: Drafted a short point-by-point acceptance response to both reviewer comments.

### Failures or shortcuts (anything you skipped)

- Did not add a formal data access committee route or DataCite metadata placeholders.
- Did not use stable reviewer IDs, action labels or manuscript-location placeholders.
- Kept the response concise but less traceable than a Nature response package.

## Candidate run

### Skill files actually loaded (full list)

- `/Users/mjm/Skill/SkillTest/synthesis/proposed-skills/cn-en-academic-polish.md`
- `/Users/mjm/Skill/SkillTest/synthesis/proposed-skills/figure-layout-defaults.md`
- `/Users/mjm/Skill/SkillTest/synthesis/proposed-updates/abstract-writing.md.diff`
- `/Users/mjm/Skill/SkillTest/synthesis/proposed-updates/apply-revisions.md.diff`
- `/Users/mjm/Skill/SkillTest/synthesis/proposed-updates/aspect-note.md.diff`
- `/Users/mjm/Skill/nature-skills-main/skills/nature-data/SKILL.md`
- `/Users/mjm/Skill/nature-skills-main/skills/nature-data/references/chinese-author-alignment.md`
- `/Users/mjm/Skill/nature-skills-main/skills/nature-data/references/statement-patterns.md`
- `/Users/mjm/Skill/nature-skills-main/skills/nature-response/SKILL.md`
- `/Users/mjm/Skill/nature-skills-main/skills/nature-response/references/action-mapping.md`
- `/Users/mjm/Skill/nature-skills-main/skills/nature-response/references/response-structure.md`

### Per-section skill mapping (which skill drove which decisions)

- Abstract: `cn-en-academic-polish` rebuilt the argument order and stabilized terminology; `abstract-writing.md.diff` supplied the "Here, we introduce" anchor and mouse-bounded closer.
- Discussion: `apply-revisions.md.diff` drove paper-type diagnosis and Discussion-register verbs; `aspect-note.md.diff` drove the named missing experiments.
- Data/Code Availability: `nature-data` drove dataset-to-route mapping, controlled-access wording, DataCite placeholders, and separation of data from code/material restrictions.
- Response to Reviewers: `nature-response` drove stable IDs, preserved comments, cooperative tone, action specificity and visible placeholders for unknown locations.

### Cross-section coordination (terminology consistency, anchor rule application)

- Kept `compound 14B`, `LNP`, `*PCSK9*`, `38% editing`, `cortical neurons`, `C57BL/6`, and `n=12` stable across relevant sections.
- Did not import CRISPR/LNP terminology into the IBD discussion.
- Applied bounded specificity globally: mouse-only scope in the abstract, named missing experiments in the discussion, explicit access-route placeholders in availability, and `[X]` placeholders rather than fabricated line numbers in the response.

### Conflicts or redundancies encountered

- `cn-en-academic-polish` and `abstract-writing.md.diff` both encourage a contribution anchor; this was applied once as "Here, we introduce".
- `nature-data` and `nature-response` both forbid fabricated identifiers or line numbers; this was handled as one global anti-fabrication rule.
- `figure-layout-defaults` was irrelevant for prose and was not applied.

### What was rejected from any skill

- Rejected the `cn-en-academic-polish` habit of adding revision notes after polished prose because the case required the fixed output structure.
- Rejected the full `nature-data` audit sections and full `nature-response` tracker/checklist to keep the polished prose within the requested budget.
- Rejected any line numbers, accession numbers, repository names, dataset DOI, or 2019 Nature paper metadata not supplied by the fixture.
