# Transcript — case-mixed-restrictions

## Brief (verbatim from fixture's "Brief for the runner" section ONLY — not failure-modes / reference-expectations)

> Draft a Data Availability statement and a Code Availability statement
> suitable for Nature Cardiovascular Research submission. Address each
> data source explicitly. The ECG dataset can be deposited to a public
> repository under a controlled-access route (the consortium has done
> this for prior studies on Zenodo with restricted access). The RNA-seq
> data is genuinely restricted by patient consent and must go through
> a controlled-access procedure (the institution has an established
> Data Access Committee). Public datasets need DataCite-style citations.
> Code is mostly shareable but the patent-pending peak-detection model
> needs a placeholder.

## Source manuscript context + author notes (verbatim)

> The submitted manuscript reports a multi-modal study of cardiac
> arrhythmia: (i) ECG recordings from 482 patients at three German
> hospitals (DZHK consortium ethics approval Heidelberg-2024-127);
> (ii) RNA-seq from cardiac tissue biopsies of 38 patients (subset of
> the 482); (iii) reanalysis of public data from the UK Biobank
> (application 78922) and from PhysioNet's MIMIC-IV-ECG database;
> (iv) deep-learning model weights and preprocessing code authored by
> the team; (v) a custom annotation pipeline that uses an internally
> developed peak-detection model.
>
> The journal is Nature Cardiovascular Research (Nature Portfolio).
> Submission deadline forces a Data Availability statement and
> Code Availability statement to be produced now.

> ECG的data是部分能公开，但是RNA-seq的data是restricted的因为患者
> consent restrict。Public data我们用了UK Biobank和MIMIC-IV-ECG，这些
> 我们cite一下就可以。Code我们willing to share但是custom peak-detection
> model我们想申请专利所以暂时not release。如果有人想access RNA-seq data，
> available upon reasonable request from corresponding author.

## Baseline run

### What I did

Drafted a concise Data Availability statement and Code Availability statement using only the manuscript context, author notes and runner brief. I addressed the generated ECG data, restricted RNA-seq data, reused UK Biobank and MIMIC-IV-ECG data, shareable code/model weights and the patent-pending peak-detection model.

### Failures or shortcuts

The baseline used a generic "corresponding author" access route for RNA-seq rather than routing access through the institutional Data Access Committee. It did not specify public metadata, repository manifests, data-use agreements, reviewer access or concrete DataCite fields for reused datasets. It also left the code repository and persistent identifier as future actions.

## Candidate run

### Skill files actually loaded

- SKILL.md
- references/chinese-author-alignment.md (Chinese author notes included "reasonable request" wording needing precise Nature-style conversion)
- references/statement-patterns.md (controlled-access, reused-public-data and request-based statement patterns)
- references/repository-and-identifiers.md (repository route, persistent identifier and DataCite-style dataset citation guidance)
- references/fair-metadata-checklist.md (public metadata, manifest, README, provenance and licence/access audit points)
- references/policy-principles.md (Nature-style disclosure requirements for generated, reused, restricted and code/material availability)

### What changed because of the skill

The candidate replaced vague request language with specific restriction reasons, durable access routes, review bodies, eligibility conditions and data-use agreement requirements. It mapped each dataset family to an access route, required public metadata for restricted human-participant data, and treated UK Biobank and MIMIC-IV-ECG as third-party datasets needing formal DataCite-style references.

### What I rejected from the skill

I did not use the skill's default output headings for "Repository and citation actions", "Missing information / risk flags" or "中文核对" because this case required fixed `Data Availability`, `Code Availability` and `Revision notes` sections. I also did not invent repository DOIs, accession numbers, licences, embargo dates, Data Access Committee names or dataset versions that were not present in the fixture.
