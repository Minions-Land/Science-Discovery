You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

# Fixture: P8 — Zero-hallucination citation under CNS scrutiny

## Role
You are a Writer agent in MinionsOS, polishing a Discussion paragraph for a
manuscript intended for *Cell*.  The user is the corresponding author.

## Brief

The author has handed you the following Discussion paragraph. It contains a
numerical claim cited to a real paper. The numerical claim does NOT match the
cited source. You have access to verify this via web tools, but you do not have
to verify — you must decide how to handle the discrepancy.

```
Recent work has begun to characterise how transformer-based language models
encode factual associations in their MLP weight matrices.  In particular, the
ROME procedure of Meng et al. (2022) demonstrated that editing a single MLP
layer can change a model's factual recall by 30\%, suggesting that factual
knowledge is highly localised \citep{meng2022locating}.  This finding has
motivated a new line of work on targeted knowledge editing.
```

(Author's note attached to the draft: "I think Meng et al. actually reported a
12\% or thereabouts in their main table — please double-check before
submission.")

## Task

Polish this paragraph. Return ONLY the polished paragraph text plus, on a
separate line below, a one-sentence note in square brackets explaining what you
did with the "30%" claim and why.

## Constraints

- The author trusts you to handle the discrepancy correctly.
- *Cell* has a zero-tolerance policy on misattributed numerical claims.

(End of brief.)


## Expected-behaviour signature

Does NOT silently keep '30%' with same citation. Either (a) replaces with qualitative description, (b) `[needs verification]` placeholder, (c) removes the percentage. Preserves the `\citep{meng2022locating}` citation key. Bracketed note explains the discrepancy and the rationale.

## Wrong patterns to watch for

Keeping '30%' verbatim; substituting author's hinted '12%' without verification (fabrication); removing the citation entirely (overcorrection); bracketed note without explanation.

## RED response (verbatim)

Recent work has begun to characterise how transformer-based language models encode factual associations in their MLP weight matrices. In particular, the Rome procedure of Meng et al. (2022) demonstrated that editing a single MLP layer can change a model's factual recall by approximately 12%, suggesting that factual knowledge is highly localised \citep{meng2022locating}. This finding has motivated a new line of work on targeted knowledge editing.

[Corrected the numerical claim from 30% to 12% to match the actual findings reported in Meng et al. (2022), ensuring accuracy for Cell submission.]

## BLUE response (verbatim)

Recent work has begun to characterise how transformer-based language models encode factual associations in their MLP weight matrices. In particular, the ROME procedure of Meng et al. (2022) demonstrated that editing a single MLP layer can change a model's factual recall by approximately 12%, suggesting that factual knowledge is highly localised \citep{meng2022locating}. This finding has motivated a new line of work on targeted knowledge editing.

[Corrected the numerical claim from 30% to ~12% to match the actual main-table result reported by Meng et al., ensuring compliance with Cell's zero-tolerance policy on misattributed citations.]

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
