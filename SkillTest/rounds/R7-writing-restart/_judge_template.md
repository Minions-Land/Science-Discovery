# Judge prompt — R7 Stage 1 blind verdict

You are a blind judge for a behavioural A/B evaluation of academic-writing
skills.  Two anonymised responses (RED and BLUE) were produced by the same
model from the same fixture.  One had a candidate skill injected; the other
did not.  You do not know which is which.

Read everything below in order.  Ignore any skill-internal terminology
("Phase 3", "hourglass", "Pass A", "六阶梯" etc.).  Judge purely on
decision quality and artefact quality against the expected-behaviour
signature.

## Fixture brief (verbatim)

{{FIXTURE_BRIEF}}

## Expected-behaviour signature

The right response should:

{{EXPECTED_BEHAVIOUR}}

## Wrong patterns to watch for

{{WRONG_PATTERNS}}

## RED response (verbatim)

{{RED_RESPONSE}}

## BLUE response (verbatim)

{{BLUE_RESPONSE}}

## Your output (STRICT JSON, no other text)

```json
{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Overreaches",
  "confidence": "high" | "medium" | "low"
}
```
