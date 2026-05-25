---
所有产物都在 ./FigureDraw/ 这个文件夹下分门归类
---

# FigureDraw 实验细则

## 目标

把 MinionsOS 自家所有画图 + 排版 Skill 与 `/Users/mjm/Skill` 里几套主流外部画图 Skill,在「同一组科研图绘制任务」上做严格对照,留下证据,写报告。

## 0. 阶段优先级

先把 6 个 arm × 15 个 fig_type = 90 个 cell 全部跑完(Sonnet baseline),再加上 1 个 MinionsOS 独占的「mock 论文 2 页排版 cell」,共 91 cells。所有 cell 跑完后再做独立 grader + 报告。

## 1. Arms (6)

| arm slug | mount | 含什么 |
|---|---|---|
| `minionsos` | MinionsOS writer skills 全部 | academic-plotting / figure-spec / figure-layout-defaults / figure-aesthetic-exemplars(含 gallery + palettes)/ interactive-figure-prototype / hero-figure-prompt / latex-typography / make-latex-model / paper-compile / pdf-vector-layout / prl-letter-format / submission-cleanup-audit |
| `figures4papers` | `/Users/mjm/Skill/figures4papers-main/` | scientific-figure-making/SKILL.md + references + 11 个真实论文 figure_* 示例 |
| `nature-figure` | `/Users/mjm/Skill/nature-skills-main/skills/nature-figure/` | SKILL.md + references(api/design-theory/figure-contract/qa-contract/...)+ chart-atlas + gallery |
| `scientific-figure-making` | `/Users/mjm/Skill/scientific-agent-skills-main/skills/scientific-figure-making/` | SKILL.md + references |
| `academic-plotting-orchestra` | `/Users/mjm/Skill/Awesome-Agent-Skills-for-Empirical-Research-main/skills/07-Orchestra-Research-AI-Research-SKILLs/academic-plotting/` | SKILL.md + agents + references(走 Gemini 架构图 + matplotlib 数据图二分法) |
| `pdf-vector-layout` | `/Users/mjm/Skill/Layout/pdf-vector-layout/` | SKILL.md + nature_style_checklist + scripts(move/merge/verify)— 主打后期排版,画图能力空 |

每个 arm 在自己 sandbox 内只能看到它自己的 Skill;不能看到别 arm 的 Skill,也看不到 `~/.claude/`、MinionsOS 项目代码、CLAUDE.md。

## 2. Sandbox 约束

完全照抄 GQPA-Diamond v2:

- `env -i HOME=$(mktemp -d)` 隔离 HOME;sandbox 里只放 `.claude/skills/<arm-skill>` 和工作目录。
- `--strict-mcp-config --setting-sources ""`:不继承 user/project setting,不挂任何 MCP 默认配置,关掉所有 MinionsOS hook(reel_capture / large_file_guard / edit_failure_rescue / bg_keepalive_nudge)。
- `--disallowedTools WebSearch WebFetch`:禁联网。
- `--model claude-sonnet-4-6 --effort max`:全 arm 同模型同 effort,唯一变量是 Skill。
- `--no-session-persistence --permission-mode bypassPermissions`。
- `--add-dir <fixture>` 加载本 cell 的 data + brief 目录,不让 agent 看到 ground truth / 别 arm 输出。
- 完整 stream-json transcript 落盘 + stderr 落盘。

## 3. Fig type taxonomy (15)

每个 fig_type 都有 `fixtures/<fig_type>/data.json` + `brief.md`,所有 arm 看到的输入完全相同。

| # | slug | 描述 | 数据来源 |
|---|---|---|---|
| 01 | `grouped-bar` | 4 method × 5 benchmark 的准确率,带 std error | mock numeric |
| 02 | `line-errband` | 3 method 的 training loss vs steps,带 95% CI | mock numeric |
| 03 | `scatter-fit` | scaling law 风格,~80 points,带 OLS + R² | mock numeric |
| 04 | `heatmap` | 10×10 confusion matrix,行/列标签 | mock numeric |
| 05 | `box-violin` | 4 condition × N≈100 distribution | mock numeric |
| 06 | `4panel-hero` | A=method overview, B=ablation bar, C=trend, D=heatmap | mock numeric |
| 07 | `architecture` | 3-layer pipeline,boxes-and-arrows | brief 描述 |
| 08 | `roc-prc` | binary classifier,4 method 的 ROC + PRC 双面板 | mock numeric |
| 09 | `ridgeline` | 6 cluster 的 expression distribution | mock numeric |
| 10 | `dual-axis-time` | training loss + LR schedule,共享 x | mock numeric |
| 11 | `stacked-bar` | 5 condition 的 4-class proportion | mock numeric |
| 12 | `forest-plot` | meta-analysis 风格,12 study,带 CI | mock numeric |
| 13 | `sankey` | 3 stage 的 flow diagram,5 source × 4 mid × 3 sink | brief + data |
| 14 | `volcano` | DE genes,X=log2FC, Y=−log10(pval),~3000 点 | mock numeric |
| 15 | `network-graph` | 30-node small-world,带社区染色 | mock numeric |

## 4. MinionsOS 独占 cell

| slug | 描述 |
|---|---|
| `paper-page` | 给一篇 mock paper 的 abstract + 1 method section + 选 4 张已生成的图,用 latex-typography + paper-compile + pdf-vector-layout 出 2-3 页 PDF。验证 macro-driven 命名、figure caption 一致性、cross-ref、pdf-vector-layout 后期收尾。 |

## 5. 落盘结构

```
FigureDraw/
├── Setting.md
├── arms/<arm>/
│   ├── README.md            # arm 描述 + 挂载内容
│   └── skills/              # 该 arm 的 Skill 副本(实际 sandbox 用 --add-dir 挂)
├── fixtures/<fig_type>/
│   ├── brief.md
│   └── data.json
├── scripts/
│   ├── run_cell.sh
│   ├── grade_cell.py
│   └── batch_run.sh
├── sessions/<arm>/<fig_type>/<run_id>/
│   ├── transcript.jsonl
│   ├── stderr.log
│   ├── meta.json
│   └── workspace/           # agent 的输出 (figure.pdf/png/svg + caption.tex + 任何 .py)
├── outputs/<fig_type>/<arm>.pdf  (+png +svg)        # 复制到一个扁平目录便于横向对比
├── grader/<arm>/<fig_type>.json
└── reports/
    ├── REPORT.md
    └── SUMMARY.md
```

## 6. 评分

每 cell 跑完后,由独立 Sonnet grader (无 Skill 挂载) 按固定 rubric 给分,8 维:
- scientific clarity / typography / palette discipline / layout density / reviewer-readiness / vector fidelity / file-format hygiene (pdf+png+svg)/ caption quality

每维 0-3 分,grader 必须把每个分数挂到具体证据 (transcript 行号 + 图文件细节)。grader 看不到 arm 名,只看到 figure 文件 + caption + 该 fig_type 的 brief。

## 7. 模型

`claude-sonnet-4-6 --effort max`,全部 arm + grader 都是它。唯一变量:Skill。
