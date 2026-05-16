# Promoted — Submission Mechanics

Skills covering the *mechanics* of submission: data availability statements,
citation retrieval and export, AI-disclosure language, repository selection.
Less about prose argument quality, more about Nature-policy compliance and
no-fabrication discipline.

## Skills inside

### Third-party (kept as reference, not duplicated)

- **nature-data** — `/Users/mjm/Skill/nature-skills-main/skills/nature-data/`
  - Tested: R3.A case-mixed-restrictions (1 case)
  - Verdict: **import-strongly** (18/18 vs baseline 8/18; bucket "Prevents real failure")
  - Headline: replaces "reasonable request" with named Data Access
    Committee + 4 review conditions; patent-pending code gets a
    reproducibility fallback; reused public data gets DataCite-style
    metadata WITHOUT fabricating identifiers.

### To author after R3.A

- **data-availability-statement.md** — new skill draft for
  `minions/roles/writer/skills/`. Will live at
  `../../synthesis/proposed-skills/data-availability-statement.md`
  once the user approves moving R3 ports forward.

## Rules / patterns extracted (R3.A evidence)

| Rule | What it does |
|---|---|
| Replace "available upon reasonable request" | Name the DAC, list review conditions (eligibility, proposed use, ethics approval, data-use agreement) |
| DataCite-style metadata for reused public data | Require creator / year / title / repository / version / DOI/accession; never fabricate values |
| Patent-pending code reproducibility fallback | Release wrappers + docs + environment + placeholder interface sufficient to reproduce all non-restricted steps |
| Restricted-data + controlled-access route specificity | Name controller, review process, conditions; do not collapse to "from corresponding author" |
| FAIR metadata coverage | Public metadata + file manifest + persistent identifier are required even when content is restricted |

## Cross-skill anchor rule (CONFIRMED across R1.C, R2, R3.A)

> **Substantively-bounded specificity, not vague good-faith promises.**

R1.C case-overclaim: "did not include transfer experiments" beats "observational design cannot establish causation."
R2 case-mixed-severity: `[X]` placeholder beats inventing `page 12, lines 310-324`.
R3.A case-mixed-restrictions: named DAC + 4 review conditions beats "reasonable request from corresponding author."

Three independent fixture types — Discussion paragraph, rebuttal letter,
data availability statement — now demand the same anchor rule. This is
the highest-confidence cross-skill principle from R1+R2+R3 so far.

## Recommendation

`import-strongly`. Plan to:

1. Author `synthesis/proposed-skills/data-availability-statement.md` covering
   the rules above (after user approves R1+R2 ports — keep R3 synthesis
   decoupled from R1+R2).
2. Add the **substantively-bounded specificity** anchor rule at the
   Writer / Reviewer common contract level (or as a top-level skill).
   Cross-skill principles should not live inside one skill file.

## Open questions for next round

- R3.B nature-citation should test whether the no-fabrication discipline
  extends to citation retrieval (predicted: yes).
- A future hard-probe fixture (international data transfer / GDPR /
  multi-IRB consent) could test the limits of the named-DAC rule.
