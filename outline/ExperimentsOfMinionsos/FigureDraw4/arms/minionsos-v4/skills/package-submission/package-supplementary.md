---
slug: package-supplementary
summary: Assemble supplementary PDF from appendix-only content, ensuring cross-document references between main paper and supplementary resolve correctly.
layer: logical
version: 1
status: active
provenance: human
---

# Package Supplementary

Assemble `supplementary.pdf` when the venue separates appendices from the main paper.

## When to use

- Venue requires a separate supplementary document.
- Paper has appendices that exceed the main body page limit.

## Skip when

- All appendices fit within the main PDF.
- Venue does not accept separate supplementary files.

## Procedure

1. **Identify supplementary content.** Appendices, extended proofs, additional figures/tables, detailed experimental results that the main paper references but cannot include.

2. **Compile separately.** Build `supplementary.pdf` from its own `.tex` source (or a shared source with a supplementary flag).

3. **Verify cross-references.** Every "see Appendix A" or "see Supplementary Table S1" in the main paper must resolve to the correct location in `supplementary.pdf`. Every back-reference in the supplementary ("as shown in Section 3 of the main paper") must be accurate.

4. **Match formatting.** Same fonts, same figure style, same citation format as the main paper. The supplementary should look like it belongs to the same submission.

## Output

`supplementary.pdf` — self-consistent, cross-references verified, formatting matched.
