## Data Availability

The ECG recordings generated from 482 patients at the three participating German hospitals will be deposited in Zenodo as a restricted-access record before publication, with public metadata, a file manifest and access conditions linked to DZHK consortium ethics approval Heidelberg-2024-127. Qualified researchers may request access through the repository or consortium-controlled access route, subject to ethics approval and a data-use agreement.

The RNA-seq data from cardiac tissue biopsies of 38 patients are not publicly available because participant consent does not permit open redistribution. Requests should be submitted to the institutional Data Access Committee, which will review researcher eligibility, proposed use, ethics approval and data-use agreement requirements. Public metadata and analysis-ready summary/source data should be deposited with the controlled-access record where consent permits.

This study also reanalysed third-party public datasets from UK Biobank, used under application 78922, and PhysioNet's MIMIC-IV-ECG database. These datasets remain available from their original repositories under their respective access terms and should be cited in the reference list using DataCite-style dataset citations with creator, year, dataset title, repository, version or release where applicable, and DOI/accession or stable identifier.

## Code Availability

Preprocessing scripts, analysis code and shareable deep-learning model weights will be archived in a public software repository with a versioned release and persistent identifier before publication. The internally developed peak-detection model used in the custom annotation pipeline is patent pending and is not available at submission; the release should include runnable wrappers, documentation, environment files and a placeholder interface sufficient to reproduce all non-restricted preprocessing and analysis steps.

## Revision notes

- Used the skill rule that "available upon reasonable request" is weak unless the restriction, access body, eligibility and conditions are explicit.
- Applied the controlled-access human-data pattern separately to ECG and RNA-seq rather than merging all patient data.
- Followed repository/identifier guidance by requiring durable records, public metadata, manifests and persistent identifiers without inventing DOIs.
- Applied the reused-public-data rule by requiring DataCite-style citations for UK Biobank and MIMIC-IV-ECG instead of merely naming them.
- Kept code separate from data and used the policy rule that commercial or patent restrictions must be disclosed with a reproducibility-preserving fallback.
