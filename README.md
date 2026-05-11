<div align="center">

# Science-Discovery

### A curated collection of Claude Code skills for the academic research lifecycle

<p>
From literature search to figure production, from rebuttal to reviewer simulation —
eight upstream snapshots assembled into one actionable stack, plus a full survey of the
benchmark landscape and a student-ready research proposal.
</p>

<p>
  <a href="https://github.com/Minions-Land/Science-Discovery">
    <img src="https://img.shields.io/badge/GitHub-Minions--Land%2FScience--Discovery-181717?logo=github" alt="GitHub"/>
  </a>
  <img src="https://img.shields.io/badge/sub--repos-8-c24619" alt="8 sub-repos"/>
  <img src="https://img.shields.io/badge/skills-25%2B-0a6cbd" alt="25+ skills"/>
  <img src="https://img.shields.io/badge/benchmarks%20surveyed-29-1f7a4c" alt="29 benchmarks"/>
  <img src="https://img.shields.io/badge/license-heterogeneous-6b4ca7" alt="heterogeneous licenses"/>
</p>

<p>
  <a href="./research-report.html">
    <img src="https://img.shields.io/badge/📄%20Open%20Research%20Report-Survey%20%2B%20Proposal-c24619?style=for-the-badge" alt="Open Research Report"/>
  </a>
</p>

<sub>Click the button above to open the full research report &amp; proposal in your browser.</sub>

</div>

---

## What this is

This repository is **not a single product**. It is a reading list made executable — eight
independently-sourced upstream snapshots, each covering one slice of the academic workflow,
kept side by side so an AI agent (or a new collaborator) can reach into any of them from one
place. A consolidated HTML artifact, [`research-report.html`](./research-report.html),
stitches the pieces together with an ecosystem survey, a benchmark map, and a 12-week
student proposal.

> **Who it is for** — researchers who use Claude Code / Cursor / Codex to draft papers,
> run experiments, and respond to reviewers, and students who want a structured way to
> enter AI-for-science research.

## The eight sub-repos

| Directory                                    | What it delivers                                                          | Upstream                                                                                             | License     |
| -------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------- |
| `academic-research-skills-main/`             | 4-skill research pipeline (deep-research → paper → reviewer → pipeline)   | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)          | CC BY-NC 4.0 |
| `RebuttalStudio-master/`                     | Electron editor for conference rebuttals; 5 stages × 4 venue templates    | [runtsang/RebuttalStudio](https://github.com/runtsang/RebuttalStudio)                                | MIT         |
| `figures4papers-main/`                       | 9 published-grade matplotlib figure references (Nature MI / ICML / NeurIPS) | [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers)                        | —           |
| `nature-skills-main/`                        | 6 skills for Nature-style writing, figures, citations, data, response, PPT | [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)                              | MIT         |
| `Research-Paper-Writing-Skills-main/`        | Prof. Peng Sida's writing methodology, packaged as a skill                | [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | MIT         |
| `awesome-ai-research-writing-main/`          | Prompt templates from MSRA / ByteDance Seed / Shanghai AI Lab researchers | [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing)          | —           |
| `Awesome-Agent-Skills-for-Empirical-Research-main/` | Stanford REAP × CoPaper.AI meta-list: 119 repos, 23,000+ skills | [brycewang-stanford/Awesome-Agent-Skills-for-Empirical-Research](https://github.com/brycewang-stanford/Awesome-Agent-Skills-for-Empirical-Research) | CC BY-SA 4.0 |
| `Agent-Native-Research-Artifact-main/`       | ARA protocol + 3 skills (compiler, research-manager, rigor-reviewer)       | [Orchestra-Research/Agent-Native-Research-Artifact](https://github.com/Orchestra-Research/Agent-Native-Research-Artifact) · [arXiv 2604.24658](https://arxiv.org/abs/2604.24658) | MIT         |

Together they cover **idea → literature → writing → figures → reviewer response → rebuttal →
artifact packaging**. `research-report.html` is the map of how they connect, plus which parts
are missing and worth building next.

## Quick start

### 1. Read the report first

```bash
open research-report.html        # macOS
# or: xdg-open research-report.html      # Linux
# or: start research-report.html         # Windows
```

Two halves, readable in either order:

- **Part I · Survey** — what we already have, the broader skill ecosystem, 29 benchmarks across every step of the research lifecycle, and a deep dive on the 2026-04 ARA paper.
- **Part II · Proposal** — four research tracks for students, environment scripts, a 12-week roadmap, and evaluation rubric.

### 2. Wire the skills into your agent

```bash
mkdir -p ~/.claude/skills

# academic-research-skills (four skills)
for s in deep-research academic-paper academic-paper-reviewer academic-pipeline; do
  ln -sfn "$(pwd)/academic-research-skills-main/skills/$s" ~/.claude/skills/$s
done

# nature-skills (six)
for s in nature-figure nature-polishing nature-citation nature-data nature-response nature-paper2ppt; do
  ln -sfn "$(pwd)/nature-skills-main/skills/$s" ~/.claude/skills/$s
done

# figures4papers + research-paper-writing
ln -sfn "$(pwd)/figures4papers-main/scientific-figure-making"                ~/.claude/skills/scientific-figure-making
ln -sfn "$(pwd)/Research-Paper-Writing-Skills-main/research-paper-writing"   ~/.claude/skills/research-paper-writing

# ARA (three skills) — or use the official installer: npx @orchestra-research/ara-skills install --all
for s in compiler research-manager rigor-reviewer; do
  ln -sfn "$(pwd)/Agent-Native-Research-Artifact-main/skills/$s" ~/.claude/skills/$s
done
```

### 3. Run the standalone app (optional)

```bash
cd RebuttalStudio-master && npm install && npm start
```

For commands scoped to individual sub-repos (Python lints, figure scripts, etc.), see
[`CLAUDE.md`](./CLAUDE.md).

## Layout

```
Science-Discovery/
├── research-report.html                           # ← start here
├── README.md                                      # this file
├── CLAUDE.md                                      # guidance for Claude Code / agents
├── AGENTS.md                                      # mirror of CLAUDE.md for other agents
├── academic-research-skills-main/                 # 4 skills · 25 modes
├── RebuttalStudio-master/                         # Electron app + stage templates
├── figures4papers-main/                           # matplotlib reference library
├── nature-skills-main/                            # 6 Nature-style skills
├── Research-Paper-Writing-Skills-main/            # Peng Sida's method
├── awesome-ai-research-writing-main/              # Chinese prompt templates
├── Awesome-Agent-Skills-for-Empirical-Research-main/   # 119-repo meta-list
└── Agent-Native-Research-Artifact-main/           # ARA protocol + 3 skills
```

## On the shoulders of

All substantial code and content comes from upstream authors. We redistribute snapshots for
convenience and interoperability; each sub-directory retains its original author, license,
and `README.md`. Please cite the corresponding upstream work (and the ARA paper,
[arXiv:2604.24658](https://arxiv.org/abs/2604.24658), if you build on §4 of the report) when
you publish results.

## Contributing

Bug fixes, new skill suggestions, and pull requests to `research-report.html` (typos, new
benchmarks, improved diagrams) are welcome. Because sub-repositories are upstream snapshots,
issues inside them should be filed with the original maintainer — open an issue here only for
items that affect the top level (`README.md` · `CLAUDE.md` · `AGENTS.md` · `research-report.html`).

## License

The collection itself is made available under the most restrictive inherited term
(**CC BY-NC 4.0**, from `academic-research-skills-main`). Each sub-repository keeps its own
license — see the table above and the individual `LICENSE` files before redistributing.
