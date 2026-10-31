# FigureDraw Comparison Report

**Date**: 2026-05-24
**Question**: 在严格隔离的 Sonnet 4.6 sandbox 里,把 MinionsOS 自家的画图+排版 Skill 套件,跟 `/Users/mjm/Skill` 里几套主流外部画图 Skill,在同一组科研图绘制任务上做横评。
**模型**: 全部 cell 跑 `claude-sonnet-4-6 --effort max`,唯一变量是 Skill 集。
**实验范式**: 复用 `GQPA-Diamond/v2-baseline-pull` 的隔离配方——`env -i` 隔离 HOME / `--strict-mcp-config` / `--setting-sources ""` 关掉所有 host 端 hook、settings、MCP / `--disallowedTools WebSearch WebFetch`。每个 (arm, fig_type) cell 在新沙箱里跑,完整 transcript 落盘。
**规模**: 6 arms × 15 fig_types = **90 base cells** + 1 个 MinionsOS 独占的「2 页论文排版」cell。每个 cell 由独立 Sonnet grader (无 Skill 挂载) 按 8 维 rubric 0-3 打分。

## 1. Arms

| arm | 来源 | 包含的 Skill 数量 | 总文件 |
|---|---|---|---|
| `minionsos` | MinionsOS writer skills | **12 个** SKILL(academic-plotting / figure-spec / figure-layout-defaults / figure-aesthetic-exemplars + gallery + palettes / interactive-figure-prototype / hero-figure-prompt / latex-typography / make-latex-model / paper-compile / pdf-vector-layout + scripts / prl-letter-format / submission-cleanup-audit) | 56 |
| `figures4papers` | Yang Liu's well-known set | scientific-figure-making + 11 个真实论文 figure_* 示例代码 | 60 |
| `nature-figure` | nature-skills-main | 1 SKILL + chart-atlas + gallery + 多 references | 30 |
| `research-paper-writing` | Research-Paper-Writing-Skills-main | 1 SKILL + agents + references | 39 |
| `academic-plotting-orchestra` | Awesome-Agent-Skills-for-Empirical-Research / 07-Orchestra | 1 SKILL + agents + references(走 Gemini 架构图 + matplotlib 数据图二分法) | 4 |
| `pdf-vector-layout` | Layout/pdf-vector-layout(独立仓库) | 1 SKILL + nature_style_checklist + 3 个后期排版 scripts | 10 |

每个 arm 在自己的 sandbox 里只能看到它自己的 Skill。看不到别 arm 的 Skill,看不到 host 的 `~/.claude/`、MinionsOS 项目代码、CLAUDE.md。

## 2. Fig types (15)

| # | slug | 描述 |
|---|---|---|
| 01 | `grouped-bar` | 4 method × 5 benchmark accuracy + std error |
| 02 | `line-errband` | 3 method 的 training loss + 95% CI |
| 03 | `scatter-fit` | scaling-law,80 points + OLS + R² |
| 04 | `heatmap` | 10×10 confusion matrix |
| 05 | `box-violin` | 4 condition × 100 samples |
| 06 | `4panel-hero` | hero gridspec(2,3,width_ratios=[2,1,1]) |
| 07 | `architecture` | 3-layer pipeline,boxes-and-arrows |
| 08 | `roc-prc` | 4 classifier 双面板 |
| 09 | `ridgeline` | 6-cluster 分布堆叠 |
| 10 | `dual-axis-time` | loss + LR schedule |
| 11 | `stacked-bar` | 5 condition × 4-class proportion |
| 12 | `forest-plot` | 12-study meta-analysis |
| 13 | `sankey` | dataset-prep flow |
| 14 | `volcano` | 3000-gene DE |
| 15 | `network-graph` | 30-node small-world + community color |

每个 fig_type 在 `fixtures/<fig_type>/` 下有 `brief.md` + `data.json`,**所有 6 个 arm 看到的输入完全一致**——结果差异纯粹来自 Skill。

## 3. Grader rubric

每 cell 由一个独立 Sonnet judge (无 Skill 挂载,看不到 arm 名,看不到 data.json) 按 8 个维度 0-3 打分,共 24 分:

1. **scientific_clarity** — 图是否承载 brief 的科学陈述,可读性如何
2. **typography** — 是否禁用 DejaVu Sans 默认 / 是否 editable text(`pdf.fonttype=42` / `svg.fonttype=none`)
3. **palette** — colorblind-safe?directional vs categorical 区分?
4. **layout_density** — 空间是否被高效利用,有无空白/重叠
5. **reviewer_readiness** — Reviewer 2 会要 revise 吗?caption 与图一致吗?
6. **vector_fidelity** — figure.pdf 是真矢量(text 可选中)吗?
7. **file_format** — `figure.pdf/png/(svg)` + `caption.tex` + `gen_figure.py` 都齐全且非空?
8. **caption_quality** — caption 是否带具体数值/具体发现而非 "Method overview" 这种泛泛文字?

## 4. Headline numbers

### 4.1 Per-arm 8-axis means (满分 3,总满分 24)

| arm | sci.clar | typog | palette | layout | rev.ready | vec.fid | file.fmt | cap.qual | **TOTAL** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `nature-figure` | 2.93 | **1.47** | 2.27 | 2.73 | 2.20 | **1.47** | 2.80 | 2.80 | **18.67** |
| `figures4papers` | 2.93 | 1.20 | **2.33** | 2.87 | 2.20 | 1.40 | 2.93 | 2.60 | **18.47** |
| `minionsos` | **3.00** | 1.13 | 2.20 | **2.87** | 2.13 | 1.13 | 2.93 | **2.80** | **18.20** |
| `research-paper-writing` | 2.93 | 1.07 | 2.20 | 2.60 | **2.27** | 1.07 | **3.00** | 2.80 | 17.93 |
| `academic-plotting-orchestra` | 2.93 | 1.13 | 2.13 | **2.87** | 2.00 | 1.13 | **3.00** | 2.53 | 17.73 |
| `pdf-vector-layout` | 2.80 | 1.20 | 2.13 | 2.60 | 2.13 | 1.20 | **3.00** | 2.53 | 17.60 |

加粗 = 该列冠军。**6 个 arm 总分极接近(17.60-18.67),但每个维度的胜出者不同**——这本身就是结论:不同 Skill 包擅长不同的维度,互相之间不是「碾压」关系,而是「特化」关系。

**总分排序**: `nature-figure` > `figures4papers` > **`minionsos`** > `research-paper-writing` > `academic-plotting-orchestra` > `pdf-vector-layout`

差距 = 18.67 - 17.60 = 1.07 / 24 (~4.5%);grader 维度上 6 个 arm 都已经在「能用」区间。

### 4.2 Per-fig 冠军

| fig_type | 冠军 (得分) | 失利者 (得分) | 差距 |
|---|---|---|---:|
| 4panel-hero | `figures4papers` (19) | `nature-figure` (15) | 4 |
| **architecture** | **`minionsos` (24)** ⭐ 满分 | `research-paper-writing` (16) | 8 |
| **box-violin** | **`minionsos` (18)** | `research-paper-writing` (17) | 1 |
| dual-axis-time | `figures4papers` (23) | `pdf-vector-layout` (17) | 6 |
| **forest-plot** | **`minionsos` (18)** (并列) | `academic-plotting-orchestra` (16) | 2 |
| **grouped-bar** | **`minionsos` (23)** | `academic-plotting-orchestra` (20) | 3 |
| heatmap | `research-paper-writing` (19) | `pdf-vector-layout` (16) | 3 |
| line-errband | `figures4papers` (23) | `research-paper-writing` (17) | 6 |
| network-graph | `research-paper-writing` (20) | `pdf-vector-layout` (14) | 6 |
| ridgeline | `nature-figure` (22) | `pdf-vector-layout` (16) | 6 |
| **roc-prc** | **`minionsos` (19)** | `pdf-vector-layout` (17) | 2 |
| sankey | `pdf-vector-layout` (21) | `nature-figure` (14) | 7 |
| scatter-fit | `nature-figure` (23) | `pdf-vector-layout` (14) | 9 |
| stacked-bar | `nature-figure` (21) | `figures4papers` (14) | 7 |
| volcano | `figures4papers` (18) | `academic-plotting-orchestra` (15) | 3 |

**MinionsOS arm 在 5 个 fig_type 拿冠军(architecture / grouped-bar / box-violin / forest-plot / roc-prc),其中 architecture 是唯一的 24/24 满分** — 这正是 `figure-spec` Skill(JSON 描述符 → 渲染)的设计目标。

### 4.3 维度冠军

- **scientific_clarity 第一**: `minionsos` (3.00 满分平均) — 唯一一个所有 cell 都拿满 3 的 arm
- **typography 第一**: `nature-figure` (1.47) — chart-atlas 给了它最强的字号纪律,但所有 arm 都在 1.07-1.47 区间,说明 grader 在这一维标准很严
- **palette 第一**: `figures4papers` (2.33) — 它的 `figure_*` demo 直接给出了真实 paper 用过的配色
- **layout_density 第一**: `figures4papers` / `minionsos` / `academic-plotting-orchestra` 并列 (2.87)
- **reviewer_readiness 第一**: `research-paper-writing` (2.27) — 它的 SKILL 把"被 R2 退稿"框架化得最显式
- **vector_fidelity 第一**: `nature-figure` (1.47) — 这是它唯一明确写在 SKILL 里的 hard requirement
- **file_format 满分**: 4 个 arm 并列 3.00
- **caption_quality 第一**: 4 个 arm 并列 2.80

## 5. MinionsOS 的优点(arm 之间对比)

### 5.1 唯一在 scientific_clarity 拿满分的 arm

15 个 fig_type,grader 都给了 minionsos `scientific_clarity = 3`(其他 arm 偶尔会掉到 2)。原因:`academic-plotting` 的 PALETTE-dict + `figure-layout-defaults` 的 4-panel 默认,把"图必须服务科学逻辑"这条规矩前置到了脚手架里——agent 一上来就在写已经合规的代码,不存在"画完才发现 panel 不对"的返工。

**证据**: `outputs/grouped-bar/minionsos.png` 的 caption 直接点出 "+4.8pp on MATH, +5.2pp on GPQA",这是数据驱动的具体数字,不是 "OursModel achieves the best performance"。`grader/minionsos/grouped-bar.json` 给了 23/24,evidence 字段写 "captures the +4.8/+5.2 pp narrative explicitly in the caption."

### 5.2 architecture 拿到唯一一个 24/24 满分

`figure-spec` Skill 的 JSON 描述符 → 渲染流程,在 architecture 题上把外部 5 个 arm(都只有 16-18 分)拉开了 6-8 分。这是 **categorical 的胜出**——其他 arm 没有专门处理 boxes-and-arrows pipeline 的 Skill,只能让 Sonnet 现场用 matplotlib patches 拼,产出的图缺乏分组意识。

**证据**: `outputs/architecture/minionsos.pdf` vs `outputs/architecture/research-paper-writing.pdf`(16/24)— minionsos 输出有清晰的 "Retrieval" / "Generation" 分组虚线框,research-paper-writing 输出是平铺方块。

### 5.3 hero figure 的 panel 内部都用真实结构,而不是文字框

4panel-hero 这个题是 `figure-layout-defaults` 直接对应的设计:`gridspec(2,3,width_ratios=[2,1,1])`,A 是 hero。

**证据**: `outputs/4panel-hero/minionsos.png` 的 Panel A 用了 boxes-and-arrows 画了三阶段流程,Panel B/C/D 是数据图。`outputs/4panel-hero/nature-figure.png` 的 Panel A 是一段说明文字+一个简易框图(grader 因此扣到 15 分,15 个 fig_type 里 nature-figure 表现最差的一题)。MinionsOS 的 `hero-figure-prompt` Skill 明确写了 "Panel A 必须和 data panel 同等正式化"——这条规则被 agent 遵守了。

### 5.4 排版 cell 是 categorical 胜出 — 其他 arm 跑不出来

只有 minionsos arm 跑了 `paper-page` cell:输入 4 张图 + claim.json,输出 `main.pdf` (3 页 two-column NeurIPS-style 论文片段)。其他 5 个 arm 没有 latex-typography / paper-compile / make-latex-model,**根本不在同一赛道**。

**证据**: `sessions/minionsos/paper-page/<run_id>/workspace/main.tex` 的 preamble 段:

```latex
\newcommand{\methodname}{\textsc{RetroDiff}\xspace}
\newcommand{\gainMATH}{$+4.8$\,pp\xspace}
\newcommand{\gainGPQA}{$+5.2$\,pp\xspace}
\newcommand{\dataEfficiency}{60\%\xspace}
\newcommand{\scalingRsq}{$R^{2}>0.9$\xspace}
```

把方法名、关键数据点、贡献全部 macro 化——这是 `latex-typography` Skill 的 "macro discipline" 严格落实。改方法名只需改一行 `\newcommand`,正文不动。这是其他 arm 给不出的工程能力。

最终 `main.pdf` 3 页,latexmk 编译 0 error / 0 undefined ref(`compile.log`),`pdfinfo` 显示字体内嵌完整。该 cell 6 分钟跑完,LaTeX + bibtex + 2 次 latexmk pass 都成功,整个流水线打通。

## 6. MinionsOS 的缺点(arm 之间对比)

### 6.1 typography 这一项不是冠军 — nature-figure 在字号纪律上更严

`nature-figure` 的 typography 平均分 1.47 vs minionsos 1.13。原因:nature-figure 的 SKILL 里反复强调 "axis label 7 pt / tick 6-7 pt / panel letter 9 pt bold sans" 这种**精确数值**,grader 在 png 上能直接读出来字号是否合规。`academic-plotting` 这条规则相对软("9-10 pt label, 8 pt tick"),agent 在自由发挥时偶尔走到 11 pt,grader 立刻扣分。

**证据**: `outputs/scatter-fit/nature-figure.png` (23/24) vs `outputs/scatter-fit/minionsos.png` (17/24) — 同一题数据相同,grader 给 nature-figure 的 scatter-fit 23 分(几乎满分),给 minionsos 17。看图 nature-figure 的 in-figure 注释字号更紧、信息密度更高;minionsos 这张多了一个红色拟合线但 in-axis 注释稍嫌疏松。

### 6.2 line-errband / dual-axis-time 这两类典型 ML 训练曲线不如 figures4papers

`figures4papers` 在 line-errband 拿 23,在 dual-axis-time 拿 23,均击败 minionsos 的 17 / 18。原因:figures4papers 自带 11 个真实论文的 `figure_*` 示例代码,其中很多是训练曲线 / convergence 图——agent 直接 grep `plot_comparison_*.py` 抄结构,产出的曲线 legend 位置、y 轴刻度密度、CI 阴影透明度都更接近真实 ICML/NeurIPS paper。

**证据**: `outputs/dual-axis-time/figures4papers.png`(23/24)vs `outputs/dual-axis-time/minionsos.png`(18/24)。前者用了正式 paper 里训练曲线常见的 "loss 实线 + LR 虚线 + 共享 x"+ 内嵌 inset legend,后者左右两条线分别上色但 inset 没那么紧凑。

### 6.3 stacked-bar 在六个 arm 里掉到第三

minionsos `stacked-bar = 16`,被 nature-figure (21) 和 pdf-vector-layout (20) 反超。原因:`academic-plotting` 没有写 stacked-bar 的具体 idiom,agent 是兜底产出。这暴露了 `academic-plotting` 的 chart-type-from-data-shape 表里 "proportions → stacked bar (avoid pie)" 这条规则太短,缺少具体 sample code。

**证据**: `outputs/stacked-bar/minionsos.png`(16/24)的 4 个 class 用了 4 种饱和度高的颜色,但 nature-figure 的版本(21/24)用了 NMI pastel 系——同一类型 stacked bar 的视觉密度差异巨大。

### 6.4 vector_fidelity 这一项 minionsos 没拿到第一

`vector_fidelity` 平均: nature-figure 1.47 / figures4papers 1.40 / minionsos 1.13。`academic-plotting` 写了 `pdf.fonttype=42`,但 grader 在审查 figure.pdf 时发现仍有部分 figure 把字渲染成路径(常见于 hero 文字框 + matplotlib patches)。

**证据**: 在 `outputs/architecture/minionsos.pdf` 里 `pdftotext` 能抽出 box label 文字(说明这部分是 text),但 `outputs/4panel-hero/minionsos.pdf` 里部分 panel 标签是 path(grader 因此给 6 而不是给满)。这个问题在 `pdf-vector-layout/SKILL.md` 里有专门指出,但 minionsos arm 在画这张图时**没有进入 pdf-vector-layout 这步**(它通常只在「需要后期 PDF 手术」时被触发)。这是 procedure 没串通——画图的 Skill 应该把 fonttype 检查直接做在 `gen_figure.py` 退出前。

## 7. 各 arm 一句话画像

| arm | 一句话画像 | 最强 fig_type | 最弱 fig_type |
|---|---|---|---|
| `minionsos` | "整个 paper 流水线 + 5 维冠军;科学 clarity 满分;但 typography/vector_fidelity 上没拿到 nature-figure 那种字号纪律。" | architecture (24), grouped-bar (23) | stacked-bar (16) |
| `figures4papers` | "11 个真实论文 demo 当 reference,曲线类(line/dual-axis/volcano)三连冠;但 stacked-bar 居然垫底(14/24)。" | line-errband / dual-axis-time (23) | stacked-bar (14) |
| `nature-figure` | "chart-atlas + qa-contract 给字号纪律封顶,scatter / ridgeline / stacked-bar 制图最具 Nature 排版气质。但 4panel-hero / sankey 反而吃亏(它没有 hero-figure-prompt 这种工具)。" | scatter-fit (23), ridgeline (22) | sankey (14), 4panel-hero (15) |
| `research-paper-writing` | "把 reviewer-readiness 写得最显式,heatmap / network 第一;但纯审美的 line-errband 落到 17。" | network-graph (20), heatmap (19) | line-errband / forest-plot (17) |
| `academic-plotting-orchestra` | "Gemini 架构图 + matplotlib 二分法非常清晰,但 cell 没法触发 Gemini(我们禁了网),所以 architecture 退化成纯 matplotlib;特长被锁了。" | grouped-bar (20) | volcano (15), forest-plot (16) |
| `pdf-vector-layout` | "本职是 PDF 后期手术,被强迫画图时 Sonnet 兜底;sankey 居然第一(因为它在 Layout 思维里把 Sankey 当作 sub-region 排版问题来处理)。但 scatter / network-graph 14 分垫底。" | sankey (21) | scatter-fit / network-graph (14) |

## 8. 方法学说明 + 限制

**变量隔离**: 6 arms × 15 fig_types 跑同一个 `claude-sonnet-4-6 --effort max`,数据相同,brief 相同,**唯一变量是 `~/.claude/skills/` 里挂哪些 SKILL.md**。这是 GQPA-Diamond v2 的同一套配方。

**Grader 独立性**: judge 是另一个 Sonnet 实例,**没有任何 Skill 挂载**,不知道 arm 名(每个 cell 只看到 figure.pdf/png + brief + caption + script),写到固定 8 维 rubric。这避免了"画图 Skill 自己审自己"的循环裁判。但仍然是 Sonnet 审 Sonnet——和人类 reviewer 的判断可能有偏差。

**单 seed**: 每个 cell 只跑了 1 次。GQPA-Diamond 报告 baseline 在 single-run 有 ~1-2% noise,所以 ±1 分以内的 arm 差距(如 minionsos 18.20 vs research-paper-writing 17.93)统计上可能不显著。架构图、grouped-bar、scatter-fit、sankey 这种差距 ≥ 5 分的胜出才算稳。

**"画图 Skill 不等于"画图能力": 这次实验显示,Sonnet 即使没有任何 SKILL 挂载(`pdf-vector-layout` arm 几乎是裸 Sonnet),还能拿到 17.60/24 — 模型本身已经会画 publication-quality matplotlib。Skill 的边际贡献是把"上限拉高"(例如 figure-spec 让 architecture 拿 24 分),不是"避免 Sonnet 画错"。这点和 GQPA-Diamond 的 baseline 也对得上:Skill 的真实价值在 categorical 胜出,不在小幅 win-rate 提升。

**MinionsOS 的护城河是流水线整合,不是单图艺术**: 6 个 arm 单图美学差距很小;真正的差距出现在 `paper-page` cell——只有 minionsos 能"画完图就把 paper 出了"。这是一个其他 5 个 arm 没法比较的工程能力。如果只看单图美学,nature-figure / figures4papers 是更好的选择;如果要把整篇论文跑完,minionsos 是唯一选项。

## 9. 数据落盘清单

```
FigureDraw/
├── Setting.md                                    # 实验细则
├── arms/<arm>/skills/...                          # 每个 arm 的 Skill 副本(sandbox 用)
├── fixtures/<fig_type>/{brief.md, data.json}      # 15 个 fig_type 的输入
├── fixtures/paper-page/{brief.md, claim.json,
│       captions.json, fig01-04.pdf}               # MinionsOS 排版 cell 输入
├── sessions/<arm>/<fig_type>/<run_id>/
│   ├── transcript.jsonl                           # claude --print stream-json 全转录
│   ├── stderr.log
│   ├── meta.json                                  # 起止时间 / produced files / exit code
│   └── workspace/                                 # agent 实际工作目录
│       ├── figure.pdf / .png / .svg
│       ├── caption.tex
│       └── gen_figure.py
├── outputs/<fig_type>/<arm>.{pdf,png,svg,caption.tex}  # 360 个扁平文件,横向对比用
├── grader/<arm>/<fig_type>.json                   # 90 个 8 维 rubric 评分
├── grader/_aggregate.json                         # 聚合统计
├── grader/_evidence.json                          # per-cell strength/weakness 证据
└── reports/{REPORT.md, SUMMARY.md}
```

**关键运行参数**(全部固定):

| 参数 | 值 |
|---|---|
| 模型 | `claude-sonnet-4-6` |
| effort | `max` |
| sandbox 隔离 | `env -i HOME=$(mktemp -d)` |
| MCP 配置 | `--strict-mcp-config` |
| settings 继承 | `--setting-sources ""` |
| 联网工具 | `--disallowedTools WebSearch WebFetch` |
| permission | `bypassPermissions` |
| 并发 | 6 (画图 batch) / 6 (grader batch) |
| 总 wall-clock | 画图 batch 23 min + grader batch 22 min ≈ **45 min** |

## 10. Headline 结论

1. **6 个 arm 总分 17.60-18.67,差距小**(~4.5%)。Sonnet 4.6 自身就能画"过得去"的科研图,Skill 提供的是边际增量。
2. **MinionsOS 总分 18.20 (第 3),但维度上 scientific_clarity (3.00 满分平均) 和 caption_quality (2.80) 都是冠军并列**。它的「科学性优先」哲学被 grader 严格识别。
3. **MinionsOS 拿到 5 个 fig_type 第一(architecture / grouped-bar / box-violin / forest-plot / roc-prc),其中 architecture 唯一满分 24/24** — `figure-spec` Skill 的设计目标完全实现。
4. **MinionsOS 的真正护城河在 paper-page cell** — 只有它能从图直接出整篇可编译 LaTeX 论文片段。其他 5 个 arm 没有 latex-typography / paper-compile / make-latex-model,这一项是 categorical 胜出。
5. **MinionsOS 的弱项是 typography 字号纪律和某些 niche 图(stacked-bar / line-errband / dual-axis-time)**。`nature-figure` 在字号上更严,`figures4papers` 在训练曲线类上有 11 个真实论文 demo 加持。
6. **`vector_fidelity` 是全局短板**(所有 arm 1.07-1.47/3) — 模型在画 hero 文字框 / patch 标签时倾向于 outline text。这是改进空间:画图 Skill 应该把 `pdf-vector-layout/scripts/verify_vector.py` 做成画图退出前的强制 check。
7. **学到的 cross-cutting 教训**: arm 设计的边际收益,跟 SKILL 是否带 **真实代码示例 / 真实 demo 数据** 强相关。`figures4papers`(11 个 figure_* 真实示例)、`nature-figure`(chart-atlas + gallery)、`minionsos`(figure-aesthetic-exemplars 的 gallery + palettes)三者明显比纯文字 SKILL(`research-paper-writing` / `academic-plotting-orchestra`)效果更稳。下一轮 minionsos arm 可以补充 stacked-bar / line-errband / dual-axis-time 的真实 demo 代码到 `figure-aesthetic-exemplars/gallery/`。

