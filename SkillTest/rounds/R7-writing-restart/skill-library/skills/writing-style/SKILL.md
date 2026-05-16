---
name: writing-style
description: 去除 AI 翻译腔 / AI 写作腔，确保学术散文自然、精准、无冗余。适用于全文所有 section。
triggers:
  - "去翻译腔"
  - "de-AI"
  - "polish style"
  - "润色风格"
  - task == polish
outputs: 自然、精准的学术英文散文
scope:
  section: [global]
  paper_type: [CNS, conference]
---

# Writing Style — 去 AI 腔 / 去翻译腔

| 规则 | 要求 |
|---|---|
| R1 禁用 AI 高频词 | delve, pivotal, landscape, tapestry, underscore, noteworthy, intriguingly, harness, leverage (as verb), utilize |
| R2 去冗余开头 | 删除 "It is worth noting that" / "Importantly," / "Notably," / "In this section, we…" |
| R3 去翻译腔 | 避免中文直译结构：「With the development of…」「plays an important role」「has attracted wide attention」 |
| R4 主语动词紧邻 | subject 和 verb 之间不要插入长定语从句 |
| R5 旧信息在前 | 每句话：familiar context first → new information later |
| R6 动词代替名词化 | "perform an analysis" → "analyze"；"make a comparison" → "compare" |
| R7 不要连续 This/We 开头 | 连续两句不要都以 "This" 或 "We" 开头 |
| R8 避免 rule-of-three | 不要反复出现 "X, Y, and Z" 的三连结构 |
| R9 具体名词 | "this result" → "this ablation" / "this theorem" / "the 30× speedup" |

详细规则见 `rules/`。
