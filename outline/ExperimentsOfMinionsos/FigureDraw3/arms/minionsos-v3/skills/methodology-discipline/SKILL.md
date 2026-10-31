---
slug: methodology-discipline
summary: Method section — notation defined upfront, modular subsections, algorithm pseudocode, claim-evidence alignment, no repetition of Introduction motivation.
layer: logical
tools:
version: 2
status: active
supersedes:
references: end-to-end-paper-workflow
provenance: R7-evolved
---

# Skill — Methodology Discipline

The Method section is the technical core of the paper. It must be self-contained enough for reproduction: a reader with the right background should be able to reimplement the method from this section alone. The structure flows from notation setup through modular description to algorithmic specification, with every design choice traceable to an experimental verification.

## When to invoke

- Drafting or polishing the Method / Approach section.

## Setup

Define notation at the beginning, referencing `math_commands.tex`. The reader should not encounter undefined symbols when reading equations. This front-loads the cognitive cost so the technical exposition flows without interruption.

## Module structure

Organize the method into one subsection per module. Each subsection contains four elements: input, output, core formula, and design motivation. This modular structure allows the reader to understand each component independently before seeing how they compose.

For multi-step processes, provide an `algorithm2e` or `algorithmic` environment that specifies the complete procedure. Prose retains only the high-level description and intuition; the pseudocode carries the precise specification.

## Cross-references

Every design choice in the Method must have a corresponding verification in the Experiments section. If a choice cannot be verified experimentally, it should be justified theoretically or acknowledged as a heuristic.

The Method section does not restate motivation from the Introduction. When context is needed, reference the Introduction in a single sentence and move on.

## Pitfalls

- All equations packed into a single large paragraph without modular separation.
- No algorithm pseudocode, making the method non-reproducible for the reader.
- Rewriting a motivation paragraph that wastes page budget and duplicates the Introduction.
