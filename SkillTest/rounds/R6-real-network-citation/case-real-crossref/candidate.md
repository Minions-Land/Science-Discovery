## Citation 1: Vaswani et al. 2017 ("Attention Is All You Need")

The Crossref `query.title=Attention+Is+All+You+Need` query returned anomalous
records:
- rank 1: DOI `10.65215/r5bs2d54`, publisher "Shenzhen Medical Academy of
  Research and Translation", year 2025 — **NOT the original NeurIPS 2017
  paper.** Likely a third-party Crossref record using the famous title.
- rank 2: similar issue.

Verified citation (manual cross-check):

- Title: "Attention Is All You Need"
- Authors: Vaswani A, Shazeer N, Parmar N, et al.
- Year: 2017
- Venue: Advances in Neural Information Processing Systems (NeurIPS) 30
- arXiv preprint: 1706.03762
- arXiv DOI: 10.48550/arXiv.1706.03762 [needs verification — this DOI
  is not currently registered in Crossref under that exact form;
  arxiv self-registered DOI may not appear via api.crossref.org]
- Conference proceedings DOI: [needs verification — NeurIPS 2017
  proceedings did not register per-paper DOIs through Crossref]

**Recommendation:** cite as NeurIPS 2017 conference paper. If a DOI is
required by the venue, use the arXiv preprint identifier with explicit
"preprint" tag, NOT the spurious Crossref record.

## Citation 2: Devlin et al. 2019 BERT

The Crossref `query.title=BERT+Pre-training+Deep+Bidirectional+Transformers`
query returned anomalous rank-1 records (a 2014 Museum Education paper).

Verified citation (direct DOI lookup):

- DOI: 10.18653/v1/N19-1423
- Title: "BERT: Pre-training of Deep Bidirectional Transformers for Language
  Understanding"
- Authors: Devlin J, Chang MW, Lee K, Toutanova K
- Year: 2019
- Venue: Proceedings of the 2019 Conference of the North American Chapter of
  the Association for Computational Linguistics (NAACL-HLT 2019)

**Verified via direct DOI fetch.** Container-title in Crossref reads
"Proceedings of the 2019 Conference of the North"; full pagination needs
verification from the Anthology record.

## Citation 3: Jumper et al. 2021 AlphaFold

Crossref query.title returned the correct rank-1 record (no anomaly).

- DOI: 10.1038/s41586-021-03819-2
- Title: "Highly accurate protein structure prediction with AlphaFold"
- Authors: Jumper J, Evans R, Pritzel A, et al.
- Year: 2021
- Journal: Nature
- Volume: 596
- Issue: 7873
- Pages: 583-589

**All metadata verified via Crossref.**

## Citation 4: Jinek et al. 2012 CRISPR

Crossref query.title returned the correct rank-1 record (no anomaly).

- DOI: 10.1126/science.1225829
- Title: "A Programmable Dual-RNA-Guided DNA Endonuclease in Adaptive
  Bacterial Immunity"
- Authors: Jinek M, Chylinski K, Fonfara I, Hauer M, Doudna JA, Charpentier E
- Year: 2012
- Journal: Science
- Volume: 337
- Issue: 6096
- Pages: 816-821

**All metadata verified via Crossref.**

## Revision notes

- Applied nature-citation discipline: query Crossref by title, but DO NOT
  accept rank-1 result without sanity checks (year matches expected,
  container is the right journal/conference, first author matches).
- Citations 1 and 2 hit a real Crossref-pollution failure mode: the
  popular title "Attention Is All You Need" has been registered by an
  unrelated 2025 medical record; "BERT: Pre-training of Deep Bidirectional
  Transformers" matched a 2014 museum education paper as rank 1.
- Citations 3 and 4 returned clean Crossref records — these are the
  trusted-rank-1 cases.
- Used direct DOI lookup (`https://api.crossref.org/works/<DOI>`) to
  verify Devlin BERT NAACL 2019 record (10.18653/v1/N19-1423).
- Vaswani 2017 has no clean Crossref-published-conference DOI; flag as
  preprint-only and recommend NeurIPS 30 (2017) citation with arXiv
  identifier as supplementary.
