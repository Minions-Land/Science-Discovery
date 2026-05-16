---
id: R1
name: banned_ai_words
trigger:
  section: [global]
  contains_pattern: '\b(delve|pivotal|landscape|tapestry|underscore|noteworthy|intriguingly|harness|leverage|utilize|multifaceted|paradigm shift|holistic)\b'
---

**规则**：禁用 AI 高频词。

**触发**：检测到 AI 写作标志词。

**替换建议**：
- delve → examine / explore / investigate
- pivotal → important / key / central
- landscape → field / area / domain
- harness → use / apply
- leverage → use / exploit
- utilize → use
- multifaceted → complex / varied
- paradigm shift → change / advance

**原则**：如果一个词在 ChatGPT 输出里出现频率是人类写作的 10×，就不要用。
