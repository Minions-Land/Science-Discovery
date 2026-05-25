# FigureDraw — One-Page Summary

**Setup**: 6 arms × 15 fig_types × Sonnet 4.6 --effort max,sandboxed via env -i + `--strict-mcp-config` + `--setting-sources ""` + `--disallowedTools WebSearch WebFetch`,完整复用 GQPA-Diamond v2-baseline-pull 范式。每个 cell 由独立 Sonnet judge 按 8 维 0-3 rubric 打分。**90 + 1 paper-page cell,wall-clock ≈ 45 min**。

## 总分排名 (满分 24)

| arm | total | 强项 |
|---|---:|---|
| nature-figure | 18.67 | typography (1.47), vector_fidelity (1.47);scatter / ridgeline / stacked-bar 制图 |
| figures4papers | 18.47 | palette (2.33);line-errband / dual-axis-time (23 满分级别) |
| **minionsos** | **18.20** | **scientific_clarity (3.00 满分平均) + 5 个 fig_type 冠军** |
| research-paper-writing | 17.93 | reviewer_readiness (2.27);heatmap / network |
| academic-plotting-orchestra | 17.73 | layout_density (2.87) |
| pdf-vector-layout | 17.60 | sankey 因 layout 思维出乎意料拿了第一 (21) |

差距 = 1.07 / 24,~4.5%。Sonnet 自身画图就行,Skill 是边际增益。

## MinionsOS 的胜出点

1. **architecture 满分 24/24** — `figure-spec` Skill (JSON 描述符 → 渲染) 唯一拿满
2. **5 个 fig_type 冠军**: architecture / grouped-bar / box-violin / forest-plot / roc-prc
3. **scientific_clarity 唯一全部满分的 arm** (15/15 cell 都 3 分)
4. **唯一能跑 paper-page cell 的 arm** — 输入 4 张图 → 输出 3 页 two-column LaTeX 论文。其他 5 个 arm categorical 跑不出来。`\methodname / \gainMATH / \dataEfficiency / \scalingRsq` 全 macro 化,latexmk 0 error。

## MinionsOS 的弱项

1. **typography 字号纪律不及 nature-figure** (1.13 vs 1.47) — `academic-plotting` 的字号规则 ("9-10 pt") 太软,要写成具体值
2. **训练曲线类输给 figures4papers**: line-errband 17 vs 23, dual-axis-time 18 vs 23 — figures4papers 有 11 个真实论文 demo,minionsos 缺这一类 gallery 案例
3. **stacked-bar 16 (六个 arm 第三)** — `academic-plotting` 没写 stacked-bar idiom,agent 兜底
4. **vector_fidelity 1.13** — hero 文字框 / patch label 仍有 outline text。`pdf-vector-layout/scripts/verify_vector.py` 没被强制做成画图退出前的 check

## 一句话结论

**单图美学差距不大,MinionsOS 真护城河是「图 → 论文」整条流水线**。如果只要单张漂亮的论文图,nature-figure 和 figures4papers 是更省事的选择;如果要一条龙跑完整篇 paper,只有 MinionsOS 能做。

