---
name: citation-zero-hallucination
description: 引用必须真实：不编造 BibTeX、不把作者记忆中的"~12%"当成已验证数字、不凭空加引用。
triggers:
  - "citation"
  - "引用"
  - "bib"
  - task in [draft, polish]
  - contains_pattern: '\[VERIFY\]|~\d+%|approximately \d+'
outputs: 零幻觉的引用和数字
scope:
  section: [global]
  paper_type: [CNS, conference]
---

# Citation Zero-Hallucination

| 规则 | 要求 |
|---|---|
| R1 不编造 BibTeX | 引用必须来自 DBLP / CrossRef / 用户提供的 .bib；找不到标 `[VERIFY]` |
| R2 不编造数字 | 如果数据还没跑，用 `[INSERT VALUE]` 占位符，不要编一个 |
| R3 不把暗示当事实 | 作者说"大概 12%"→ 不能写成"12%"；要么验证，要么用定性描述 |
| R4 引用格式一致 | ML 会议用 `\citep{}`/`\citet{}`；IEEE 用 `\cite{}`；不混用 |
| R5 只引用已 cite 的 | references.bib 只含实际 `\cite` 过的条目 |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=15)

| 指标 | 值 |
|---|---|
| Skill 胜 | 7 |
| 平局 | 6 |
| Baseline 胜 | 2 |
| **净分** | **+5** |

**进化算法推荐**：
- 保留（validated）：R1, R2, R4, R3
- 停用/修改（anti-validated）：无
