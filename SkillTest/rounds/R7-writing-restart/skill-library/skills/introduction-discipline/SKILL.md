---
name: introduction-discipline
description: 撰写或润色论文 Introduction 时，确保只写背景 + 方法类描述（不写实现细节），末尾带 contribution itemize，4–6 段 hourglass 结构。
triggers:
  - "写 introduction"
  - "draft intro"
  - "润色引言"
  - draft_section == intro
outputs: 符合 CNS/conference 规范的 Introduction section
scope:
  section: [introduction]
  paper_type: [CNS, conference]
---

# Introduction Discipline

Introduction 的核心职责是**背景 + 动机 + 方法类概述 + contribution**。

| 规则 | 要求 |
|---|---|
| R1 无实现细节 | 参数量、优化器、索引结构等属于 Method，不放 Intro |
| R2 方法类描述 | 只在「类」层面描述：a learned diffusion prior / retrieval-augmented decoding |
| R3 Contribution itemize | Intro 末尾 2–4 条 noun-phrase bullets（唯一允许 itemize 的地方） |
| R4 段落结构 | 4–6 段 hourglass：broad → gap → approach → contribution → (optional roadmap) |
| R5 Why-not 分析 | 必须说清楚 prior work 为什么不够（不只是"没人做过"） |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=28)

| 指标 | 值 |
|---|---|
| Skill 胜 | 8 |
| 平局 | 0 |
| Baseline 胜 | 20 |
| **净分** | **-12** |

**进化算法推荐**：
- 保留（validated）：无
- 停用/修改（anti-validated）：R3, R4, _general, R1, R2
