---
slug: venue-reformat-workflow
summary: Switching venues, integrating rebuttal additions, and compressing pages — sibling-directory rule, global \cite/\citep sweep, rebuttal-content-into-appendix with plan-then-execute, page-compression by relocation. Never mutate the original tree.
layer: composite
tools:
version: 1
status: active
references: prepare-rebuttal, package-submission, apply-revisions, submission-cleanup-audit
provenance: human + Codex NeurIPS-2026 EF / ResearchEVO sessions + pingxingshixu compression session
---

# Skill — Venue Reformat Workflow

Switching from ICML to NeurIPS, integrating rebuttal-driven additions, and compressing pages all share a discipline: *don't mutate, relocate*. Original directory stays intact; new venue / new page budget lives in a sibling directory; rebuttal additions live in the appendix; page compression moves entire subsections rather than deleting prose.

## When to invoke

- Switching submissions between venues (ICML→NeurIPS, conference→journal, conference→PRL).
- Integrating rebuttal-accepted edits before camera-ready.
- Page budget exceeded; need to compress to fit.
- Author is preparing parallel submissions to differently-formatted venues.

## The four discipline rules

### 1. Sibling-directory for venue switch
Never mutate the original venue tree. Copy to a sibling directory named for the new venue:
```
~/Papers/NeurIPS 2026/ResearchEVO/        # original ICML tree (untouched)
~/Papers/NeurIPS 2026/EF/EFNEURIPS/       # NeurIPS reformat target
```
Rationale: parallel-submission safety, rollback safety, diff readability across venues.

### 2. Global cite-command sweep
NeurIPS uses `\citep{}` for parenthetical and `\citet{}` for textual; some venues use plain `\cite{}`. When switching venues, do a single global sweep, not piecemeal:
```bash
sed -i '' 's/\\cite{/\\citep{/g' **/*.tex   # ICML→NeurIPS, parenthetical default
```
Then walk the file, changing the in-line `\citet{}` cases manually. Cite-command mismatch is global by nature; don't pretend it's local.

### 3. Rebuttal additions live in the appendix
**All rebuttal-driven new content goes in the appendix; the main text stays stable across revisions.**

Why: reviewers see the same main text. Appendix additions answer specific concerns without destabilising the paper they reviewed. Camera-ready then merges or keeps the appendix structure depending on page budget.

**Plan-then-execute is mandatory** here:
1. Draft the proposal — list which rebuttal points trigger which appendix additions, with rough word counts.
2. **Stop. Send the proposal to the user. Wait for explicit approval.**
3. Only after approval, execute the additions.

This loop is stricter than ordinary edits because rebuttal-driven changes risk silent main-text drift. The user said this verbatim: *"我希望就是 rebuttal 的新增的内容，都总结道附录里面。而不是改变正文。你先做规划，给我 proposal，我拍板了之后再修改。"*

### 4. Page compression by relocation
When the main text exceeds the page budget, **move whole subsections to the appendix**, do not delete or summarise.

Pattern:
- Identify subsections that read well as standalone (Background, Extended Method, Detailed Ablation, Implementation Notes).
- Move the whole subsection text to the appendix.
- Replace it in the main text with a single sentence: *"Detailed [topic] is in Appendix [N]."*
- Update `\ref` and `\label` accordingly; check `submission-cleanup-audit.md` category 2 (multi-def labels) after the move.

Anti-pattern: trimming individual sentences across many subsections to save 1.5 pages. Reads worse, takes longer, breaks the insight-first rhythm.

## Procedure

1. **Establish target.** New venue (specify name + style file) / rebuttal (specify reviewers + accepted points) / page budget (specify pages).
2. **Choose the relevant rule.** Sibling-dir + cite sweep for venue switch; appendix-additions + plan-then-execute for rebuttal; relocation for page compression.
3. **For rebuttal: emit a proposal first.** Do not edit the manuscript until the proposal is approved.
4. **Execute the chosen rule.** Apply the global sweep, the relocation, or the appendix addition.
5. **Run `submission-cleanup-audit.md`** after the move. Category 2 (multi-def labels) and category 5 (partial integration) are highest risk.
6. **Compile and verify.** Page budget check, cite-command consistency check, label resolution check.

## Pitfalls

- Mutating the original tree because "we'll just diff later". Diffs are not version control.
- Mixed `\cite` / `\citep` after a venue switch. Reviewer notices; reads as careless.
- Rebuttal additions in the main text. Even if the addition is small, it destabilises the main-text contract with the reviewers.
- Skipping the proposal step on rebuttal incorporation. "Plan-then-execute" is non-negotiable here.
- Compressing by sentence-trimming instead of subsection-relocation. Takes longer, reads worse, leaves orphan equations and refs behind.
- Forgetting to update `\label` and `\ref` after relocation. See `submission-cleanup-audit.md` category 2.
