---
name: abbreviation-discipline
description: 全称/简写规范：第一次出现用"全称（简写）"，之后统一用简写。
triggers:
  - "简写规范"
  - "abbreviation"
  - task == polish
  - contains_pattern: repeated full form after first definition
outputs: 规范化的简写使用
scope:
  section: [global]
  paper_type: [CNS, conference]
---

# Abbreviation Discipline

| 规则 | 要求 |
|---|---|
| R1 首次全称+括号简写 | 第一次出现：`Convolutional Neural Network (CNN)` |
| R2 之后只用简写 | 后续全部用 `CNN`，不再写全称 |
| R3 每个 section 独立 | Abstract 里定义过的简写，在 Intro 第一次出现时要重新定义（因为有些读者只看某个 section） |
| R4 不要过度缩写 | 只缩写出现 ≥3 次的术语；只出现 1–2 次的直接写全称 |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=9)

| 指标 | 值 |
|---|---|
| Skill 胜 | 3 |
| 平局 | 0 |
| Baseline 胜 | 6 |
| **净分** | **-3** |

**进化算法推荐**：
- 保留（validated）：无
- 停用/修改（anti-validated）：R1, R2
