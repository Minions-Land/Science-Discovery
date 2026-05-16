# Fixture: data-availability-mixed-restrictions

**Type:** writing — Data Availability statement for a manuscript with
public, restricted, and ambiguous data sources
**Use in:** R3.A nature-data
**Purpose:** Test whether the skill (a) maps every result-supporting dataset
to a durable access route, (b) handles restricted clinical data with
proper restriction reason / controller / review route, (c) flags vague
"reasonable request" wording as the failure mode it is, (d) cites public
datasets with DataCite-style metadata.

## Manuscript context (give to runner verbatim)

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

## Author notes (rough Chinese-influenced English, give verbatim)

> ECG的data是部分能公开，但是RNA-seq的data是restricted的因为患者
> consent restrict。Public data我们用了UK Biobank和MIMIC-IV-ECG，这些
> 我们cite一下就可以。Code我们willing to share但是custom peak-detection
> model我们想申请专利所以暂时not release。如果有人想access RNA-seq data，
> available upon reasonable request from corresponding author.

## Brief for the runner

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

## Failure modes the runner should fix

- "Available upon reasonable request from the corresponding author" —
  Nature flags this as inadequate; needs replacement with a controlled-
  access procedure naming the controller, review route, and conditions.
- Generic "the data are public" without DataCite metadata
  (creator, title, repository, year, identifier) for the public datasets.
- Lumping all data into one statement; each source should map to its
  own access route.
- Code statement that just says "available on GitHub" with no DOI /
  release tag / archived snapshot.
- Patent-pending code: needs proper "withheld pending IP review" wording
  with stated review timeline, not "not released" with no timeline.
- Mixing English and Chinese-style hedging ("我们willing to share" must
  be reconstructed into the English Data Availability convention).

## Reference statement expectations (for scoring, not shown to runner)

A passing rewrite should:

1. Map every dataset to a durable identifier or controlled-access route
2. Replace "reasonable request" wording with a named DAC + access route
3. Cite UK Biobank and MIMIC-IV-ECG with DataCite-style citations
   (creator, title, year, repository, DOI/identifier)
4. Use Code Availability section explicitly with version/DOI for
   shareable code; placeholder with reason + IP review timeline for
   patent-pending code
5. Be split into clearly labelled sections (Data Availability, Code
   Availability) per Nature submission norms
