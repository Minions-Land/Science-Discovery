---
slug: package-code-snapshot
summary: Prepare a reproducible code snapshot with exact reproduction commands, dependency lockfile, and pointers to experiment artifacts for every claimed result.
layer: logical
version: 1
status: active
provenance: human
---

# Package Code Snapshot

Prepare a code bundle that reproduces the paper's claimed results.

## When to use

- Artifact evaluation submission.
- Venue requires code alongside the paper.
- Paper makes reproducibility claims that need backing.

## Skip when

- No code claims in the paper.
- Pure theoretical / survey paper with no experiments.

## Procedure

1. **Write `README.md`** with exact reproduction commands. Not "run the experiments" — the specific commands, in order, that produce each reported number.

2. **Include dependency lockfile.** `requirements.txt`, `uv.lock`, `environment.yml`, or equivalent. Pin versions exactly.

3. **Pointer to experiment artifacts.** For each reported number (table, figure), include a pointer: `[derived: branches/shared/exp/exp-<id>/report.md]`. The reader must be able to trace any claim to its source data.

4. **Scrub paths and secrets.** No absolute paths, no API keys, no institutional hostnames. Replace with placeholders and document them in the README.

5. **Include license.** MIT, Apache-2.0, or whatever the project uses.

6. **Verify reproduction.** Run the commands yourself (or dispatch to Coder) in a clean environment. If numbers don't match the paper exactly, either fix the snapshot or honestly document the gap.

## Output

Code snapshot directory with: `README.md`, lockfile, source code, license, and experiment pointers. Every claimed result is traceable.
