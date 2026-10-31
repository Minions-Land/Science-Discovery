# Next Skill-Forge Plan — based on FigureDraw3 evidence

**Date**: 2026-05-25  
**Driver**: FigureDraw3 self-eval (single-arm minionsos-v3 vs FD2 minionsos anchor) — 19 figures + 1 paper-page, 19 grader scores.

## 上轮成绩

- Common-17 平均: **18.71 → 21.18 (+2.47, +13.2%)**
- typography: 1.53 → 2.42 (+0.89) ★
- vector_fidelity: 1.59 → 2.47 (+0.88) ★
- palette: 2.06 → 2.68 (+0.62)
- paper-page macros: 6 → 8
- 5 个 fig_type 拿满分 24/24 (grouped-bar / scatter-fit / forest-plot / heatmap-class)
- 新加的 cns-graphical-abstract 22/24 (categorical 验证 cns-paper-discipline SKILL 生效)

## 下轮要修的 3 个 regression

| fig_type | v2 | v3 | Δ | 根因猜测 |
|---|---:|---:|---:|---|
| stacked-bar | 19 | 17 | **-2** | `network-graph-tuning` 的 ColorBrewer Set2 规则被 agent 错位应用到 stacked-bar(stacked-bar 4-class proportion 不属于 community,但规则太硬被泛化)|
| volcano | 23 | 19 | **-4** | `caption-revision` 的 "reviewer-pass" 让 agent 加了过多注释,稀释了 volcano 的视觉密度;也可能是 `figure-chart-atlas/19-archetypes.md` 中 "annotate top-5" 写得太宽泛 |
| network-graph | 20 | 16 | **-4** | `network-graph-tuning.md` 的 spring layout 默认不对 30-node 完全展开;node-size ∝ degree 在 5-degree 平均图里看不出层级 |

这是 "rule injection 后的 reward hacking":agent 严格遵守新规则,但偏离了上一轮 grader 喜欢的版本。

## 下轮 Skill-Forge 动作清单

### Action 1 — `figure-aesthetic-exemplars/network-graph-tuning.md` 加 opt-in gate

现状: 规则不分场景,无脑应用。
改: 在文件头加 "When to apply" 段:**仅 N >= 20 nodes 时强制**。N < 20 时建议保持上一版的 freestyle。同时把 `node_size ∝ degree` 改为 `if max_degree / min_degree > 3: scale; else: constant`。

### Action 2 — `figure-aesthetic-exemplars/SKILL.md` 加 "scope" 字段

stacked-bar 不是 community 图但被 ColorBrewer 规则套用。修法: 在每个 sub-skill ref 文件头加 `scope:` 字段(`scope: graph-network-only` / `scope: ml-paper-only`),master SKILL 在加载子 ref 前先 match scope。

### Action 3 — 在 `figure-chart-atlas/references/19-archetypes.md` 中 volcano 段加 "annotate restraint" 规则

现状: 写 "annotate top-5 by neg_log10_p magnitude"。  
改: "annotate top-3 to top-5 only IF the points are visually well-separated; if cluster-y, annotate the 3 most-extreme of each direction (3 up, 3 down) and skip the rest." 加一条 "never annotate more than 10 points on a volcano".

### Action 4 — 给 `caption-revision.md` 加 "don't over-annotate figures" 反例

`caption-revision` 的 reviewer-pass 倾向于让 agent 给图加更多 inline annotation。补一条: caption 的 reviewer-pass 不应改图,只改 caption 文字。If reviewer-pass 想加 in-figure annotation, escalate to academic-plotting instead of doing it inline.

### Action 5 — 加 regression-core 评测集合

这是元层面的工具改进(不是 SKILL 改动): 在 `evals/` 下加一个 "regression-core" 5-cell 子集 (stacked-bar / volcano / network-graph / 4panel-hero / sankey),每次 Skill-Forge 后必须先跑这 5 个,任意一个跌幅 >= 3 就标记 SKILL 改动需要再修订。

### Action 6 — `imrad-section` 19/24 偏低,具体补强 imrad-discipline.md

FD3 的 imrad-section 拿了 19/24,typography 2 / vector_fidelity 2 是最低维度。证据指向:agent 出的 LaTeX 渲染没用 `pdf.fonttype` 等 figure 级别的 vector discipline。修法: `imrad-discipline.md` 末尾加一段 "output-format discipline" 指向 `paper-compile` + `latex-typography` 的 vector + macro 检查清单。

### Action 7 — Sub-skill 模式扩展

下一步把 `cns-paper-discipline/` 拆细: 现在 3 个 reference (imrad / reporting / graphical-abstract) 已经成型,但 `imrad-discipline.md` 单文件 ~150 行,继续注入 evidence 会过载。下一轮按 venue 拆: `imrad-cell.md` / `imrad-nature.md` / `imrad-nejm.md`(每个 venue 实际有不同的 IMRAD 顺序和长度约束)。Master `imrad-discipline.md` 退化为索引 + 通用规则。

## 可选: 新 fig_type 想测的方向

- `extended-data-figure` — Nature sub-journal 的 extended data figure(不在主体的补充图;有不同的 caption 长度限制)
- `multi-panel-CNS` — 实测一个 6-panel hero figure 是否 minionsos 还能稳住 layout
- `response-letter` — Reviewer response letter,测 `prepare-rebuttal` SKILL

## Forge 节奏建议

按用户的 "渐进式纰漏" 要求:每轮 Forge 最多改 2-3 个 SKILL,不一口气把所有 borrow 全注入。本轮(FD3 → FD4)聚焦于 **修 3 个 regression**(Action 1-4),evals 工具(Action 5),imrad 加强(Action 6)。Sub-skill 拆细(Action 7) 留给 FD5。
