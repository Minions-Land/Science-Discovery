---
id: R2
name: avoid_itemize
trigger:
  section: [related_work, method, experiments, conclusion]
  contains_pattern: '\\begin\{(itemize|enumerate)\}'
---

**规则**：除 Intro contribution 外，避免 itemize/enumerate。

**触发**：在 Related Work / Method / Experiments / Conclusion 检测到列表环境。

**修复**：改写为散文。列表在论文里看起来像 slide notes，不像正式学术写作。

**唯一例外**：Introduction 末尾的 contribution bullets（参见 introduction-discipline R3）。
