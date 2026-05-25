# Methods (outline — convert to prose)

## Study design
- prospective observational cohort, 3-center (Beijing, Shanghai, Guangzhou)
- recruitment 2018-2022
- follow-up median 3.4y (IQR 2.6-4.1)
- ethics: institutional approval at all 3 centers; written informed consent

## Participants
- inclusion: biopsy-confirmed MASLD, age ≥18, no concurrent HBV/HCV
- exclusion: alcohol > 30 g/day (men) / 20 g/day (women); cancer Hx; pregnancy
- baseline n=2412; loss to follow-up 425 (17.6%)
- final analytic n=1987

## Variables
- exposure: baseline non-invasive scores (FIB-4, NFS, APRI, transient elastography)
- primary outcome: ≥1 stage progression on 2nd biopsy at follow-up (METAVIR scoring, central re-read for 20% sample)
- covariates: age, sex, BMI, diabetes, alcohol intake, baseline fibrosis stage

## Data sources / measurement
- laboratory variables from 3-center harmonized lab protocols
- biopsy: central pathology re-read for 20% sample to assess inter-rater reliability (Cohen κ=0.78)
- elastography: standardized FibroScan protocol per manufacturer guidelines

## Bias
- healthy-volunteer bias from refusal to undergo follow-up biopsy → IPW sensitivity
- inter-center misclassification → central re-read
- residual confounding from diet → E-value sensitivity

## Study size
- pre-specified power: 80% to detect HR=1.5 with α=0.05, assuming 30% progression rate over 3y → n=1800 needed; recruited 2412 to allow loss to follow-up

## Statistical methods
- primary: Cox proportional hazards with time-varying covariates
- adjusted: age, sex, BMI, diabetes, alcohol intake, baseline fibrosis stage
- missing data: multiple imputation, 10 iterations
- sensitivity: E-value for unmeasured confounding, complete-case analysis
- software: R 4.3.1, survival 3.5-7, mice 3.16.0
- α: two-tailed p<0.05; Bonferroni for the 3 secondary endpoints
