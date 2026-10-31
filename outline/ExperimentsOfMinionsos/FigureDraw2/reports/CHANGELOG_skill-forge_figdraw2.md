# Skill-Forge Changelog — FigureDraw2 → MinionsOS Writer

**Date**: 2026-05-25  
**Trigger**: User goal — "对所有评比过的 Baselines 进行一次究极的 Skill-Forge,CNS 优先 > ML 次之,渐进式注入,sub-skill 模式按需展开。"  
**Driver evidence**: FigureDraw1 (90 cells) + FigureDraw2 (144 cells), grader-validated. See `outline/ExperimentsOfMinionsos/FigureDraw2/reports/REPORT.html` §VII for the borrow-list and `SKILL_FORGE_PLAN.md` for the planning spreadsheet.

## Summary

10 changes touched **8 SKILL files** + **2 new sub-skill folders**. All edits are **purely additive** — no MinionsOS Writer SKILL was deleted or renamed. CNS-tier coverage (Cell / Nature / Science) added as a new top-level skill with three sub-skills, since FigureDraw2 surfaced this as MinionsOS's biggest coverage gap relative to scientific-writing-kdense (446-line CNS-targeted SKILL).

All touched SKILLs bumped `version` and added `provenance: + FigureDraw2-evidence (...)` lines. No behavioural validation has been run yet — the natural next step is a FigureDraw3 round to confirm the borrows produce a measurable lift.

## Per-file changelog

### Changed (8 SKILLs)

| File | Version | What was added | Borrow source |
|---|---|---|---|
| `academic-plotting.md` | v3 → v4 | (1) "When NOT to load" routing block; (2) Caption checklist (4-item); (3) ML-paper idioms section pointing to new sub-skill; (4) Network-graph idioms section pointing to new sub-skill | Borrow #2 (awesome-writing-prompts arm reviewer_readiness 2.29 #1), Borrow #4 (kdense network-graph 21/24), Anti-pattern #1 (latex-document arm misroute) |
| `latex-typography.md` | v3 → v4 | Booktabs grouping recipe (`\multicolumn` + `\cmidrule`) for benchmark tables, with within-1-σ overlap rule | Borrow #3 (composer-lishix arm latex-table 21/24) |
| `figure-spec.md` | v2 → v3 | (1) Two-archetype split: "A: architecture" + "B: sankey/flow"; (2) Sankey spec format with source-color discipline; (3) Stage-label + numerical-label requirements | Borrow #5 (stat-writing-fuhaoda sankey 18/24, gap +8) |
| `paper-compile.md` | v2 → v3 | New step 7 "Macro-discipline lint" — scan body for hardcoded names appearing ≥3 times that lack `\newcommand` definitions, warn into `compile.log`. The macro discipline gap was the single sharpest categorical win in FigureDraw2 (minionsos 6 macros vs 1-3 for every other arm). | Anti-pattern #2 (universal awesome-arm gap) |
| `figure-aesthetic-exemplars/SKILL.md` | v1-draft → v2-active | Promoted from "DRAFT — SkillTest research zone" to active; added references to two new sub-skill files | Borrow #1, Borrow #4 |

### New (2 sub-skill folders + 1 standalone + supporting files)

| File | Type | Purpose |
|---|---|---|
| `caption-revision.md` | Standalone SKILL | Single-pass "simulate Reviewer 2 → revise" loop for figure / table / abstract captions. Adds the cheap revision pass that academic-paper-imbad's 12-agent pipeline gave for free. |
| `figure-aesthetic-exemplars/ml-paper-idioms.md` | Sub-skill reference | Training-curve / ablation / ROC-PRC / dual-axis idioms imitating ml-paper-writing arm's wins. |
| `figure-aesthetic-exemplars/network-graph-tuning.md` | Sub-skill reference | Hairball-prevention defaults (edge alpha, node size ∝ degree, ColorBrewer Set2/Dark2, pinned-seed spring layout). |
| `figure-chart-atlas/SKILL.md` | New top-level SKILL | Pre-plotting decision skill; 19-archetype catalog index, hands off to academic-plotting after archetype is chosen. |
| `figure-chart-atlas/references/19-archetypes.md` | Reference | Per-archetype: when / when not / route / pitfall. Synthesised from awesome-writing-prompts "实验绘图推荐" prompt. |
| `figure-chart-atlas/references/scale-rescue.md` | Reference | Decision tree for broken-axis vs log vs normalisation when data spans > 1 order of magnitude. |
| `cns-paper-discipline/SKILL.md` | New top-level SKILL | Cell / Nature / Science / NEJM submission discipline; index pointing to three sub-skills. **MinionsOS's first CNS-tier explicit coverage** (FigureDraw2 surfaced this gap). |
| `cns-paper-discipline/references/imrad-discipline.md` | Reference | Full-paragraph prose rule (no bullets in body), per-section guidance, three reusable paragraph templates. |
| `cns-paper-discipline/references/reporting-guidelines.md` | Reference | CONSORT/STROBE/PRISMA/ARRIVE/MIAME/COREQ/STARD decision matrix + per-checklist skeleton. |
| `cns-paper-discipline/references/graphical-abstract.md` | Reference | Mandatory-figure spec, 3 content patterns (workflow/mechanism/headline), 3 generation routes (gpt-image-2.0/TikZ/composite). |

### Not touched (deliberate)

- `hero-figure-prompt.md`, `pdf-vector-layout.md` (folder + .md), `submission-cleanup-audit.md` — already grader-strong in FigureDraw1; no actionable signal in FigureDraw2.
- `cn-en-academic-polish.md` — covers the awesome "去 AI 味" prompts; FigureDraw didn't test this axis.
- `prl-letter-format.md`, `make-latex-model.md` — venue-specific and project-init scope; orthogonal to figure/typography evidence.
- The other 28 writer SKILLs (`abstract-writing`, `methodology-discipline`, `derivation-hygiene`, `experiments-completeness`, etc.) — out of FigureDraw2 scope; future Skill-Forge rounds may cite them as reference targets but no evidence-driven changes today.

## Tier separation (CNS vs ML)

The forge naturally surfaced a **two-tier split**:

- **CNS-tier** (new): `cns-paper-discipline/` is the umbrella when target is Cell/Nature/Science/NEJM/Lancet/etc. Loads IMRAD, reporting-guideline, graphical-abstract sub-skills.
- **ML-tier** (existing): `academic-plotting.md` + `latex-typography.md` + `figure-aesthetic-exemplars/ml-paper-idioms.md` is the implicit set for NeurIPS/ICML/ICLR/ACL/CVPR.

Both tiers share the universal layer: `figure-chart-atlas` (archetype picker), `figure-spec` (architecture / sankey), `caption-revision` (Reviewer-2 single-pass), `paper-compile` (macro lint).

This structure mirrors how scientific-writing-kdense and ml-paper-writing differ in the Awesome library — they targeted different venues with the same modeling backbone. MinionsOS now has explicit coverage for both.

## Validation status

- **Form**: All edited SKILLs follow MinionsOS frontmatter conventions; provenance lines added; cross-references via `[[skill-name]]` updated where new sub-skills are referenced.
- **Behavior**: NOT YET VALIDATED. Plan is to run FigureDraw3 with the same harness, this time:
  - 8 arms in v2 + minionsos-v3 (this round's writer skills) = 9 arms
  - 17 fig_types unchanged + paper-page (per arm) unchanged
  - 2 new fig_types: `cns-graphical-abstract` (tests cns-paper-discipline) + `imrad-section` (tests imrad-discipline rules)
  - Headline metric: does minionsos-v3 close the 0.47 ml-paper-writing gap on grouped-bar / line-errband / 4panel-hero / roc-prc, AND does it claim a new gap on cns-graphical-abstract / imrad-section?
- **Reward-hacking watch**: macro-lint can be over-zealous (false positives on field terms like "Transformer" or "PyTorch" that legitimately don't need macros). The FigureDraw3 grader should explicitly score "is the macro lint output sensible?" so we can tune the heuristic before hardening from warn → fail.

## Files for follow-up

- `outline/ExperimentsOfMinionsos/FigureDraw2/reports/SKILL_FORGE_PLAN.md` — the absorption planning doc.
- `outline/ExperimentsOfMinionsos/FigureDraw2/reports/REPORT.html` §VII — original borrow-list with grader evidence.
- `outline/ExperimentsOfMinionsos/FigureDraw/reports/REPORT.html` — merged v1+v2 report (overall narrative).
- Memory entry: `~/.claude/projects/-Users-mjm-MinionsOS/memory/project_figuredraw_experiment.md` — pointer for future sessions.

## Next round (FigureDraw3) hypothesis

If the borrows are absorbed correctly, minionsos-v3 should:
1. Match or beat ml-paper-writing on the 4 ML-curve fig_types (current gap 5-6 points). Driver: ml-paper-idioms.md.
2. Stay #1 on architecture / equation-block / heatmap / volcano / stacked-bar (current wins).
3. Add a new categorical win on `cns-graphical-abstract` and `imrad-section` (no other arm has these capabilities; should be 22+/24).
4. Keep paper-page macro count at 6+ (already #1; macro-lint should make this robust to refactor).
5. Pick up 1-2 points on caption_quality / reviewer_readiness via caption-revision pass.

If any of these regresses, that's the signal to refine the borrow rule, not back it out.
