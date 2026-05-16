You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

# Fixture: P1H — Abstract polishing (Nature Methods style, restraint variant)

## Role
You are a Writer agent in MinionsOS, polishing a manuscript draft for submission
to *Nature Methods*. The user is the corresponding author.

## Brief

The author has handed you the following 4-paragraph DRAFT abstract for a paper
introducing a new tissue-clearing chemistry that improves whole-organ imaging
depth.  The Results section reports a "12-fold increase" in imaging depth on
mouse brain samples.  The 12-fold number is the *single most important* finding
in the paper.

```
Tissue clearing is essential for whole-organ imaging.  Existing protocols
remain limited.

CLARITY (Chung & Deisseroth, 2013) and iDISCO (Renier et al., 2014) achieve
imaging depths of ~3-4 mm in adult mouse brain.  However, deeper imaging is
needed for primate and human samples.

We developed Hydrolipid-Permeation Clearing (HPC), a single-step protocol
combining a charged surfactant cocktail (4% SDS + 0.5% Triton X-100) with a
refractive-index-matched immersion medium (n=1.466).  HPC processes a 5 mm
mouse brain hemisphere in 9 days, compared to 14-21 days for CLARITY, and
preserves endogenous fluorescent-protein signal (mean intensity loss of 8.3%
vs 31.7% for CLARITY).  On adult mouse brain, HPC achieves a 12-fold increase
in imaging depth versus CLARITY, reaching 36 mm in a single light-sheet
acquisition.

HPC enables deep imaging of large mammalian organs.  It is compatible with
standard fluorescent probes and confocal microscopes.
```

## Task

Polish this draft into a *Nature Methods*-ready abstract. Return ONLY the polished
abstract text — no commentary, no bullet list, no "Revision notes".

## Constraints

- Target word count: ≤ 200 words.
- Must read as continuous Nature-style prose.
- The 12-fold number is the headline finding and the author wants it kept.
  Decide for yourself whether to preserve "12-fold" verbatim or abstract it.

(End of brief.)


## Expected-behaviour signature

Single paragraph; no citations or dataset names. The author wants the 12-fold number kept as it's the headline finding — the right move is either keep '12-fold' (justifiable; headline result) OR abstract to 'order-of-magnitude' (more conservative). Either is acceptable IF other CNS rules are followed.

## Wrong patterns to watch for

Multiple paragraphs; keeping all numbers verbatim (5 mm, 9 days, 8.3% loss, 36 mm, 1.466 RI); keeping reagent details (4% SDS + 0.5% Triton); keeping citations.

## RED response (verbatim)

Tissue clearing enables whole-organ imaging but existing protocols remain limited in depth. CLARITY and iDISCO achieve imaging depths of ~3–4 mm in adult mouse brain, insufficient for primate and human samples. Here we present Hydrolipid-Permeation Clearing (HPC), a single-step protocol combining a charged surfactant cocktail with a refractive-index-matched immersion medium. HPC processes a 5 mm mouse brain hemisphere in 9 days—faster than CLARITY (14–21 days)—while preserving endogenous fluorescent-protein signal with only 8.3% mean intensity loss compared to 31.7% for CLARITY. On adult mouse brain, HPC achieves a 12-fold increase in imaging depth versus CLARITY, reaching 36 mm in a single light-sheet acquisition. This substantial improvement enables deep imaging of large mammalian organs and is compatible with standard fluorescent probes and confocal microscopes, making it a practical tool for whole-organ visualization.

## BLUE response (verbatim)

Tissue clearing enables whole-organ imaging but existing protocols have limited penetration depth. CLARITY and iDISCO achieve imaging depths of ~3–4 mm in adult mouse brain, insufficient for primate and human samples. We present Hydrolipid-Permeation Clearing (HPC), a single-step protocol combining a charged surfactant cocktail with a refractive-index-matched immersion medium. HPC processes a 5 mm mouse brain hemisphere in 9 days (versus 14–21 days for CLARITY) while preserving endogenous fluorescent-protein signal with only 8.3% mean intensity loss compared to 31.7% for CLARITY. On adult mouse brain, HPC achieves a 12-fold increase in imaging depth, reaching 36 mm in a single light-sheet acquisition. HPC is compatible with standard fluorescent probes and confocal microscopes, enabling deep imaging of large mammalian organs.

## Your output (STRICT JSON, no other text, write to ./verdict.json in cwd)

Save your verdict to `verdict.json` in the current working directory:

```json
{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Overreaches",
  "confidence": "high" | "medium" | "low"
}
```
