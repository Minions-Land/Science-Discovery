---
slug: related-work-discipline
summary: Related Work organized by method class (not paper-by-paper survey); each paragraph contains model + algorithm + implementation + connection to this work. Minimum 1 full page.
layer: logical
tools:
version: 2
status: active
supersedes:
references: paper-literature-search, end-to-end-paper-workflow
provenance: R7-evolved
---

# Skill — Related Work Discipline

Related Work is the only section where specific method details belong — model architectures, algorithmic choices, implementation strategies. Its purpose is not to survey the literature but to build an argument: here is what exists, here is why it falls short, and here is where our work fits. The section is organized by method class, not by paper.

## When to invoke

- Drafting or polishing the Related Work section.
- Checking whether Related Work is too short or poorly organized.

## Organization

Each paragraph covers one method class. Within that paragraph, present the three elements that define the class: model, algorithm, and implementation approach. Close the paragraph by explaining why this class of methods is insufficient and how the present work differs.

This structure means every paragraph earns its place — the reader understands not just what prior work did, but why it motivates the current contribution.

## Scope and format

Conference papers require at least 1 full page of Related Work (3–4 substantive paragraphs). Short Related Work sections are a common reviewer complaint and signal insufficient engagement with the field.

Cover both classic foundational methods and recent state-of-the-art. The section is entirely prose — do not use itemize or enumerate.

## Pitfalls

- Paper-by-paper enumeration ("[1] proposed X. [2] extended X to Y.") — this is a list, not an argument.
- Covering only recent SOTA without discussing classic methods.
- Paragraphs ending without connecting to this work (reader does not understand why the paragraph exists).
