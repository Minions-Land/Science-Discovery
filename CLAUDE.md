# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

`/Users/mjm/Skill` is **not a single project** — it is a local collection of **eight independently-sourced upstream repositories** (downloaded zip snapshots, hence the `-master` / `-main` suffixes), all of which deliver **Claude Code / agent skills for academic research workflows**. Each subdirectory has its own lifecycle, license, tooling, and README. The top level adds one integrated artifact, `research-report.html` — a Part I survey + Part II student proposal that stitches the eight snapshots into one narrative and maps them onto the public benchmark landscape.

The public presence of this collection lives at [github.com/Minions-Land/Science-Discovery](https://github.com/Minions-Land/Science-Discovery). The top-level `README.md` is the reader-facing entry point and contains a button that opens `research-report.html`.

When the user asks for "build" / "test" / "lint", always first identify **which subdirectory** they mean. The right command depends entirely on the sub-repo.

## Top-level artifacts

| File | Role |
|---|---|
| `research-report.html` | Single-file HTML report (≈80 KB, 16 sections). Part I surveys the local stack + ecosystem + 29 benchmarks + ARA; Part II is a 12-week student proposal with 4 tracks. Update this whenever a sub-repo changes materially or a new important benchmark/paper appears. |
| `README.md` | Public-facing landing; short, links prominently to `research-report.html`. |
| `CLAUDE.md` | This file — agent guidance. |
| `AGENTS.md` | Mirror of `CLAUDE.md` for other coding agents (Codex / Cursor / Gemini CLI). Keep in sync. |

## The eight sub-repos

| Directory | Kind | Primary artifact | Language / runtime |
|---|---|---|---|
| `academic-research-skills-main/` | Claude Code plugin (4 skills, 25 modes, full pipeline) | `skills/{deep-research,academic-paper,academic-paper-reviewer,academic-pipeline}/SKILL.md` | Python (CI lints); Markdown skill content |
| `RebuttalStudio-master/` | Electron desktop app for conference rebuttals | `src/main/main.js` entry; bundled `skills/` for polish/stage1/stage2 | Node.js / Electron |
| `figures4papers-main/` | Scientific figure skill + per-paper plotting scripts | `scientific-figure-making/SKILL.md` + `figure_*/plot_*.py` | Python (matplotlib) |
| `nature-skills-main/` | Skill bundle for Nature-style writing / figures / citations / rebuttals / paper→PPT | `skills/nature-*/SKILL.md` | Markdown; Python where referenced |
| `Research-Paper-Writing-Skills-main/` | Single skill `research-paper-writing/` adapting Peng Sida's notes | `research-paper-writing/SKILL.md` + `references/` | Markdown |
| `awesome-ai-research-writing-main/` | Curated list (README-only) with Chinese research-writing prompt templates | `README.md` | — |
| `Awesome-Agent-Skills-for-Empirical-Research-main/` | Stanford REAP × CoPaper.AI meta-list: 119 repos / 23,000+ skills indexed by research stage | `README.md` + `README-en.md` + `docs/01..10-*.md` + vendored `skills/00–49/` | Markdown; some Python / Stata / R for the `00.*-Full-empirical-analysis-skill_*` siblings |
| `Agent-Native-Research-Artifact-main/` | ARA protocol + 3 skills (compiler, research-manager, rigor-reviewer); arXiv 2604.24658 | `skills/{compiler,research-manager,rigor-reviewer}/SKILL.md` + `packages/ara-skills/` npm installer | Markdown skill content; Node.js installer |

## Commands (scoped per sub-repo)

Always `cd` into the target sub-repo first.

### `academic-research-skills-main/`
Python-based CI lints, no build step. Run from repo root:

```bash
pip install -r requirements-dev.txt        # pyyaml + jsonschema[format]>=4.17 — REQUIRED
python3 scripts/check_spec_consistency.py  # main spec lint
python3 scripts/check_version_consistency.py
PYTHONPATH=. python3 -m unittest scripts.test_check_sprint_contract -v   # single lint's unit tests
PYTHONPATH=. python3 -m unittest discover scripts -v                     # all unit tests
```

Gotcha: without `requirements-dev.txt` installed, `test_check_sprint_contract` (71 tests) reports **67 errors + 1 failure** that all trace to `ModuleNotFoundError: jsonschema`. Don't debug the tests — install deps first.

The full CI matrix (≈20 checks: `check_*.py` + their `test_check_*.py`) lives in `.github/workflows/spec-consistency.yml`, with a separate pytest workflow for `scripts/adapters/tests/`. Inspect that workflow to reproduce CI locally. Many checks require `PYTHONPATH=.` or `PYTHONPATH=scripts` — copy the invocation from the workflow rather than guessing.

### `RebuttalStudio-master/`

```bash
npm install
npm start          # launches Electron app (src/main/main.js)
```
No tests, linters, or build scripts are configured beyond these. Dependencies: electron, marked, dompurify, html-to-docx.

The portable parts of this sub-repo — independent of the Electron shell — are in `skills/` (stage1, stage2, stage4, stage5, polish, document-memory, utility) and `templates/` (ICLR/ICML/ARR/NeurIPS JSON configs, `final_remarks_tokenseek.md`). If importing content into another agent system, those are the units to copy, not the Electron app.

### `figures4papers-main/`
No package manager config. Each `figure_*/` is a self-contained plotting project run with plain Python + matplotlib:

```bash
cd figure_CellSpliceNet && python plot_comparison.py   # writes to figures/
```
The skill itself (`scientific-figure-making/SKILL.md`) is documentation — no build.

Gotcha: many `figure_*/data/` directories are **empty in this snapshot** (`.npz` / `.csv` inputs weren't included). Scripts are high-quality reference patterns but not runnable out of the box — verify the data dir has content before trying to execute.

### `Agent-Native-Research-Artifact-main/`
No local build. Skills are Markdown and ship with an npm installer:

```bash
# Official installer — auto-detects Claude Code / Cursor / Gemini CLI / Codex / Hermes
npx @orchestra-research/ara-skills install --all

# Or install one skill into a specific agent
npx @orchestra-research/ara-skills install --skill compiler --agent claude-code
```

Direct symlink works too (see `README.md` quick start). The three skills are invoked as `/compiler <path>`, `/research-manager`, `/rigor-reviewer <artifact_dir>`. Their local specs live in `skills/{compiler,research-manager,rigor-reviewer}/SKILL.md`. `packages/ara-skills/` holds the installer source — do not edit it without syncing upstream.

When citing ARA, use the BibTeX block in its root `README.md` (arXiv 2604.24658, Liu et al. 2026).

### Documentation-only sub-repos
`nature-skills-main/`, `Research-Paper-Writing-Skills-main/`, `awesome-ai-research-writing-main/`, and `Awesome-Agent-Skills-for-Empirical-Research-main/` have no build/test commands. Changes are to Markdown only. Validate by reading the skill's own README for its install instructions (mostly `cp -R` or `ln -s` into `~/.claude/skills/`).

## Architecture — how the pieces fit

The sub-repos cover **different stages of an academic paper's lifecycle** and can be composed even though they ship separately:

```
idea → deep-research ─┐
                      ├─ academic-pipeline ──→ final paper + AI self-reflection
idea → plan paper  ──→ academic-paper ──→ academic-paper-reviewer ──→ revision
                                                │
       figure work:     figures4papers / nature-figure
       style polish:    nature-polishing
       citations:       nature-citation
       data stmt:       nature-data
       rebuttal:        RebuttalStudio + nature-response
       slides:          nature-paper2ppt
       artifact pack:   Agent-Native-Research-Artifact (compiler → logic/src/trace/evidence)
       epistemic review: Agent-Native-Research-Artifact (rigor-reviewer, Seal Level 2)
```

Three architectural ideas recur and are worth knowing before editing:

1. **Skill-as-directory** convention. Every skill ships as a folder containing `SKILL.md` (YAML frontmatter + workflow), optional `references/*.md`, and sometimes `scripts/`. Claude Code auto-discovers skills at `~/.claude/skills/<name>/SKILL.md` (global) or `<project>/.claude/skills/<name>/SKILL.md` (project). Install is copy or symlink; there is no package format shared across these repos except where `academic-research-skills-main` adds Claude Code **plugin** packaging (`.claude-plugin/plugin.json`, `commands/ars-*.md`, `hooks/hooks.json`, `agents/*.md` as symlinks into `deep-research/agents/`), and `Agent-Native-Research-Artifact-main` ships a multi-agent **npm installer** (`@orchestra-research/ara-skills`) that follows the [Agent Skills open standard](https://agentskills.io/specification).

2. **Material Passport handoff schema** (`academic-research-skills-main/shared/handoff_schemas.md`, Schema 9+). Artifacts pass between agents/stages as structured ledgers, not free-form prose. `shared/contracts/` + `shared/sprint_contract.schema.json` define the JSON-Schema gates; lint scripts enforce them. When editing anything under `academic-research-skills-main/`, assume schema changes require corresponding `scripts/check_*.py` and test updates.

3. **ARA four-layer protocol** (`Agent-Native-Research-Artifact-main/README.md`). Recasts a paper as a machine-executable package with `logic/` (claims / concepts / experiments), `src/` (configs / environment / code), `trace/exploration_tree.yaml` (research DAG, **including dead ends**), and `evidence/` (raw tables / figures). Cross-layer forensic bindings thread claims → experiments → evidence; provenance tags (`user` / `ai-suggested` / `ai-executed` / `user-revised`) distinguish human-confirmed facts from AI inferences. Conceptually compatible with Material Passport: both are structured artifact contracts, which makes interop between the two schemas an interesting research direction (see `research-report.html` §4.5).

## Sub-repo nuances that affect editing

- **`academic-research-skills-main/` has its own nested `CLAUDE.md`** at `.claude/CLAUDE.md`. It contains authoritative per-version changelog context (v3.0 → v3.7.0) and routing rules between the four skills. Read it before making non-trivial changes inside that sub-repo; don't duplicate its content here. `MODE_REGISTRY.md` is the single source of truth for all 25 modes — update it first when adding/renaming modes.
- **License heterogeneity**: `academic-research-skills-main` is **CC BY-NC 4.0**; `Research-Paper-Writing-Skills-main`, `RebuttalStudio-master`, `nature-skills-main`, and `Agent-Native-Research-Artifact-main` are MIT; `Awesome-Agent-Skills-for-Empirical-Research-main` is CC BY-SA 4.0; `figures4papers-main` and `awesome-ai-research-writing-main` have no explicit LICENSE file. Don't copy content between sub-repos without checking.
- **`figures4papers-main` style contract**: scripts must call `apply_publication_style()` / `finalize_figure()` from the skill's API (`scientific-figure-making/references/api.md`) and export both `.png` and `.pdf`. `nature-figure` additionally mandates three specific rcParams (Arial family, `svg.fonttype='none'`) and `.svg` as primary export.
- **`nature-polishing` README ↔ SKILL drift.** The sub-repo README advertises "≤30-word sentences" and "British English mandatory" as the skill's headline rules; the shipped `skills/nature-polishing/SKILL.md` (currently v5.0.2) has been rewritten around paper-type classification + reader-question sequencing + Academic Phrasebank phrase families, and **does not enforce the 30-word rule anywhere in its content or references**. When editing or citing this skill, read the actual SKILL.md, not the top-level README.
- **`Agent-Native-Research-Artifact-main/` is upstream-active**. The npm package `@orchestra-research/ara-skills` is the authoritative distribution; our snapshot may lag behind. For anything beyond reading/understanding, prefer the official installer. When the paper (arXiv 2604.24658) cites empirical numbers (PaperBench 72.4 → 93.7%, RE-Bench 57.4 → 64.4%), treat them as the version-of-record — we reproduce them in `research-report.html` §4.4.
- **`Awesome-Agent-Skills-for-Empirical-Research-main/` is a meta-list with vendored skills**. `docs/01..10-*.md` is the research-stage index; `skills/00–49/` are vendored copies of the listed skills (with `00 / 00.1 / 00.2 / 00.3` being Python / Stata / R siblings of the same 8-step empirical pipeline). The repository itself passed a 52/52 security scan (see `SECURITY-SCAN-REPORT.md`), which is why we trust the vendored copies without re-auditing.
- Each sub-repo is a **snapshot**, not a git checkout. There is no `git pull` to update — re-download from upstream.

## When asked to "install a skill"

Default install path for Claude Code globally:
```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/<skill-dir>" ~/.claude/skills/<skill-dir>   # or cp -R for copy-based
```
`academic-research-skills-main` additionally supports plugin install via `/plugin marketplace add ...` then `/plugin install academic-research-skills` — see that sub-repo's `QUICKSTART.md`. `Agent-Native-Research-Artifact-main` supports `npx @orchestra-research/ara-skills install --all`, which auto-detects Claude Code / Cursor / Gemini CLI / Codex / Hermes.

For the curated one-shot that wires the whole stack in, see the "Quick start" section of the top-level `README.md`.

## When asked to "update the research report"

`research-report.html` is a single self-contained file (inline CSS + inline JS; no build). Edit in place. Things that typically trigger an update:

- New sub-repo added / removed at the top level → update the section §1 / §2 tables and the README.
- A benchmark you've cited rolls a new SOTA or new version → update §3.
- A new relevant arXiv paper on agent-native research, skill composition, or AI-for-science evaluation appears → consider promoting it to §4 the way ARA is currently featured.
- A track / timeline / rubric change in how we collaborate with students → update §9–§13.

Always re-verify numbers against their source when touching them: GitHub stars via `api.github.com/repos/<owner>/<repo>`, benchmark metadata via `api.openalex.org/works?search=<title>`. Both are reachable from this environment's local shell; the agent-side `WebSearch` / `WebFetch` are typically blocked, so prefer `curl` from `Bash`.
