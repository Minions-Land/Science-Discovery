---
slug: package-submission
summary: Assemble the final submission bundle — toolkit of four packaging tasks (PDF compile, source archive, supplementary, code snapshot) plus a venue checklist gate. Use any combination depending on submission type.
layer: logical
tools:
version: 3
status: active
references: paper-compile, end-to-end-paper-workflow, pdf-vector-layout
provenance: human
---

# Skill — Package Submission

Four packaging tasks available for assembling a submission bundle.
You decide which to use based on the submission type. The default sequence
below is a recommendation for full camera-ready — not a mandatory pipeline.

## When to invoke

- Final camera-ready handoff.
- Original submission package just before upload.
- Artifact-evaluation submission (code snapshot emphasis).

## The four tasks (your toolkit)

| Task | File | Use when | Skip when |
|---|---|---|---|
| **PDF Compile** | `package-submission/package-pdf-compile.md` | Any submission that includes a paper | Never — always needed |
| **Source Archive** | `package-submission/package-source-archive.md` | Venue requires `tex.zip` source upload | Venue accepts PDF-only (rare) |
| **Supplementary** | `package-submission/package-supplementary.md` | Paper has appendices in a separate document | All appendices are in the main PDF |
| **Code Snapshot** | `package-submission/package-code-snapshot.md` | Artifact evaluation, or venue requires code | No code claims in the paper |

Each task is a sibling file under `package-submission/`. Read the
relevant task file when you decide to use it. Task files are NOT
listed as standalone skills in `[Skills]` — they are progressive
disclosure reachable only after this orchestrator is chosen.

## Default recommendation (not mandatory)

For a full camera-ready submission:

1. **PDF Compile** — clean build from scratch
2. **Source Archive** — `tex.zip` that compiles standalone
3. **Supplementary** — separate PDF if venue requires it
4. **Code Snapshot** — reproducible code bundle

Then run the venue checklist gate.

## Other valid patterns

- **PDF Compile only**: Quick preprint upload to arXiv.
- **PDF Compile → Source Archive**: Standard venue submission without code.
- **PDF Compile → Code Snapshot**: Artifact-evaluation-only submission.
- **All four**: Full camera-ready with artifact evaluation.

The agent decides based on venue requirements.

## Venue checklist gate (shared)

After assembling whichever tasks apply, verify:

- Anonymous: no author info or blinding-breaking self-citations.
- Page limit: body to Conclusion (ML venues) or total including refs (IEEE).
- Fonts embedded: `pdffonts main.pdf | grep -v yes` is empty.
- File size: within venue limit (typically < 50 MB; prefer < 10 MB).

Do not mark the package ready while any checklist item fails.

## Pitfalls

- Shipping a PDF whose source does not compile on a clean machine.
- Forgetting to strip author info on anonymous submissions.
- Code snapshot that reproduces "something close" rather than the claimed numbers.

Every reproducibility claim is marked `[derived: branches/shared/exp/exp-<id>/report.md]`.
