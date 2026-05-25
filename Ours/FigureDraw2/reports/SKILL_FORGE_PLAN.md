# Skill-Forge Plan — FigureDraw2 → MinionsOS

**Date**: 2026-05-25  
**Driver**: FigureDraw2 §VII borrow-list (8 items + 2 anti-patterns) — grader-validated against 144 cells.  
**Constraint**: 渐进式;CNS 优先 > ML 次之;sub-skill 模式按需展开。

## 一句话方针

现有 12 个 writer SKILL **没有一个要被替换或删除**。所有 forge 都是 **(a) Edit 注入新规则到现有 SKILL** + **(b) 新建 sub-skill 当 reference 索引** + **(c) 新建 1 个 CNS-tier 上层 SKILL**(因为 awesome 库暴露的 CNS 期刊纪律是 MinionsOS 完全空缺的能力)。

## Forge 动作清单

### 动作 1 — 新建顶层 SKILL: `cns-paper-discipline.md`

**Why**: scientific-writing-kdense 的 IMRAD + 报告指南(CONSORT/STROBE/PRISMA/ARRIVE)+ 必出 graphical abstract 三件事,在 MinionsOS 现有 36 个 SKILL 里完全没有。这是 Cell/Nature/Science 期刊的硬要求,MinionsOS 想做 CNS-tier 论文必须补这一课。

**Source**: scientific-writing-kdense (446 行) + stat-writing-fuhaoda 的 reporting guideline 索引。

**位置**: `minions/roles/writer/skills/cns-paper-discipline.md`

**结构**: 顶层 SKILL,引用 3 个 sub-skill 文件(IMRAD / reporting-guideline / graphical-abstract)。

---

### 动作 2 — 新建 sub-skill 索引: `figure-chart-atlas/`

**Why**: awesome-writing-prompts 的「19 种学术图表库」清单是 MinionsOS 的 `academic-plotting` 当前缺的具体硬规则(我们只有 chart-type-from-data-shape 一行)。

**Source**: awesome-writing-prompts 的「实验绘图推荐」prompt + nature-figure 的 chart-atlas。

**位置**: `minions/roles/writer/skills/figure-chart-atlas/SKILL.md` + `references/19-archetypes.md` + `references/scale-rescue.md`(断裂轴/对数/归一化)。

**关系**: `academic-plotting.md` 的 "chart-type-from-data-shape" 表换成 "see [[figure-chart-atlas]]"。

---

### 动作 3 — Edit `academic-plotting.md`: 加 caption checklist 段

**Borrow #2** — awesome-writing-prompts arm 的 reviewer_readiness 维度第一(2.29)。

**新增**: 「caption checklist」一节: (1) 一句话「读者第一眼应看到什么」;(2) bold take-home 数字;(3) 解释每种视觉编码。这是 caption.tex 退出前的强制 lint。

---

### 动作 4 — Edit `latex-typography.md`: 加 booktabs 分组 idiom

**Borrow #3** — composer-lishix 在 latex-table 拿 21(arm 第一),用了 `\multicolumn{4}{c}{baselines}` 分组。

**新增**: 「booktabs 分组习惯」一节: 当 methods 自然分成 baseline/ours 两组时,用 `\multicolumn` + `\cmidrule(lr){i-j}` 横向分组;within-1-std overlap 时同时 bold。

---

### 动作 5 — Edit `figure-spec.md`: 加 sankey/flow template

**Borrow #5** — stat-writing-fuhaoda 在 sankey 拿 18(arm 第一,gap +8 over latex-document)。

**新增**: 在 figure-spec 的 archetypes 列表里加 "flow / sankey" template,定义 nodes/links 的 spec 格式 + source-color 一致性规则。

---

### 动作 6 — Edit `paper-compile.md`: 加 macro-discipline lint check

**Anti-pattern #2** — 7 个非-minionsos arm 都能编译但 macro 数 ≤ 3。MinionsOS 应该把这条做成 paper-compile 退出前的强制 check,而不是依赖 Sonnet 自觉。

**新增**: 在 paper-compile.md 的 "Procedure" 第 7 步前加一步 "macro-discipline lint":扫 main.tex,如果某个名字硬编码 ≥ 3 次且未定义为 `\newcommand`,fail compile 并报错列出违规位置。

---

### 动作 7 — Edit `figure-aesthetic-exemplars/SKILL.md`: 加 ML-paper gallery 子集

**Borrow #1** — ml-paper-writing arm 在 grouped-bar / line-errband / 4panel-hero / roc-prc 4 类拿冠军,67 行 SKILL + 真实论文 demo。MinionsOS 在 figures4papers 实验里也吃过这亏。

**新增**: `figure-aesthetic-exemplars/gallery/ml-paper-grouped-bar.py` 等 4 个 reference scripts(从 ml-paper-writing 的 references/ 抽出来);SKILL.md 里加一节 "ML-paper idioms":log-y CI 阴影 alpha ≤ 0.25、legend 右下角 inset、legend 不带 frame。

---

### 动作 8 — Edit `figure-aesthetic-exemplars/SKILL.md`: 加 network-graph 调参

**Borrow #4** — scientific-writing-kdense 在 network-graph 拿冠军(21),palette 平均 2.31 全场第一。

**新增**: "network/graph 调参清单": (1) edge alpha 默认 0.3;(2) node size ∝ degree;(3) community 用 ColorBrewer Set2;(4) spring layout 而不是 random。

---

### 动作 9 — 新建 sub-skill: `caption-revision.md`

**Borrow #6** — academic-paper-imbad 的 12-agent pipeline 在 caption 写作上有 "draft → reviewer-pass → revise" 痕迹;MinionsOS 是 single-pass。

**位置**: `minions/roles/writer/skills/caption-revision.md`

**功能**: 强制一次 "模拟 Reviewer 提一个尖锐 feedback → revise" 循环。被 `academic-plotting` 和 `cns-paper-discipline` 双向引用。

---

### 动作 10 — Edit `academic-plotting.md` 的 description: 强化 "When not to load"

**Anti-pattern #1** — latex-document arm 的 SKILL.md 描述太宽泛,paper-page cell 失败。

**新增**: 在 `academic-plotting.md` frontmatter 的 description 后追加 "When not to load" 段:不画 architecture / pipeline 图(去 figure-spec)、不出整篇 paper(去 paper-compile)、不画 hero(去 hero-figure-prompt)。这是给 agent 的明确路由信号。

---

## 不做的事(明确剔除)

- **不去抄 stat-writing-fuhaoda 的 task-routing 范式整体进 MinionsOS**:MinionsOS 现有 36 个 writer SKILL 已经是分散索引(每 SKILL 一个 task),再叠一层 router 反而冗余。只借 sankey/flow template 一项。
- **不动 hero-figure-prompt / pdf-vector-layout / submission-cleanup-audit**:这三个是 MinionsOS 上一轮已经胜出的 SKILL,grader evidence 没有 actionable 信号。保持不动。
- **不抄 deslop / humanizer 反 AI 化 SKILL**:MinionsOS 的 cn-en-academic-polish 已经覆盖,且这次实验没测「去 AI 味」轴。

## 渐进式纪律

- **每动一个 SKILL,先 Read → Edit 一段(≤50 行)→ 立即可逆**。不一口气重写。
- **每个 Edit 都在 frontmatter `version` 字段 +1**,加 `provenance: human + FigureDraw2-evidence` 行。
- **每个新建 SKILL 都从 ≤3KB 种子 Write 开始**,不一次写满。
- 完成后写 `CHANGELOG_skill-forge_figdraw2.md` 列具体改了什么。
