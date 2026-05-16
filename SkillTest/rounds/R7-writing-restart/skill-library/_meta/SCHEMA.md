# Skill Library Schema (R7) — 渐进式披露 / progressive disclosure

两层结构：

```
skill-library/
├── _meta/
│   ├── SCHEMA.md           # this file
│   └── index.json          # all top-level skills + their descriptions
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md        # 主文件，~150 词，包含 description + trigger + 规则清单
│       └── rules/
│           ├── R1_xxx.md   # 子规则细节，按需展开
│           └── R2_xxx.md
```

## 顶层 skill 列表（草案）

| skill | scope | 子规则数（估计）|
|---|---|---|
| `abstract-discipline` | Abstract / Conclusion 段落规范 | 4 |
| `introduction-discipline` | Introduction 内容与结构 | 4 |
| `related-work-discipline` | Related Work 组织 | 3 |
| `experiments-completeness` | 主实验/消融/超参/案例分析 | 4 |
| `latex-typography` | 宏定义、列表、加粗、`\paragraph{}` | 5 |
| `abbreviation-discipline` | 全称/简写规范 | 2 |
| `citation-zero-hallucination` | 引用真实性、无编造数字 | 3 |

## SKILL.md frontmatter（机器可读 description）

```yaml
---
name: abstract-discipline
description: 适用于撰写或润色论文 Abstract / Conclusion 时，确保单段、无引用、无具体数字、无数据集名。
scope:
  section: [abstract, conclusion]
  paper_type: [CNS, conference]   # CNS=Nature/Cell/Science 类；conference=NeurIPS/ICLR/ICML/CVPR
  task: [polish, draft]
triggers:
  any_of:
    - draft_section: abstract
    - draft_section: conclusion
rules:
  - id: R1
    name: single_paragraph
    summary: "段落数必须为 1"
  - id: R2
    name: no_citations
    summary: "不可包含 \\cite/\\citep/\\citet"
  - id: R3
    name: no_specific_numbers
    summary: "具体数字（TM-score、F1、fold-change）改为定性描述"
  - id: R4
    name: no_dataset_names
    summary: "具体数据集名（CIFAR-10、CASP15、PDB）改为类别名"
fitness:                  # 由 evaluator pipeline 填充
  cases_won: []
  cases_lost: []
  net_score: null
---
```

## 子规则文件（rules/Rx_xxx.md）

短小，~50–100 词，包含：
- 一句话规则
- 触发条件（具体 regex / pattern）
- 输出转换（如何修复）
- 例外（参考 USER_WRITING_RUBRIC）

## Trigger grammar（v1）

- `draft_section: <abstract|intro|related_work|method|experiments|conclusion|global>`
- `paragraph_count: "<op><n>"`
- `contains_pattern: <regex>`
- `paper_type: <CNS|conference|both>`
- `task: <polish|draft|review>`

## 渐进式披露 / progressive disclosure

- Stage 1（路由）：读 `SKILL.md` frontmatter 决定是否激活该 skill。
- Stage 2（执行）：按需读取 `rules/Rx_*.md` 的具体细节。
- 模型可以一次只看 SKILL.md（轻量），需要展开某条 rule 时再读。
- 这避免了把每条 atomic 抬升成顶层 skill 时的「碎片化」。

## 合并 / 冲突规则

- **同 skill 内冲突**：在 SKILL.md 的 rules 列表显式列出 `conflict_with`，由 USER_WRITING_RUBRIC 仲裁。
- **跨 skill 冲突**：典型例子 — `latex-typography` 的「避免 itemize」与 `introduction-discipline` 的「contribution itemize 在 Intro 末尾」。后者在 introduction-discipline 内部声明 example 例外。
- **合并**：两个 skill 的 scope.section 与 trigger 重合度 ≥80% → 合并为一个 skill，保留各自子规则。
