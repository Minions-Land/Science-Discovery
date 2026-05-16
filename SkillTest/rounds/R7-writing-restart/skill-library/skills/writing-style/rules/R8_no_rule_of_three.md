---
id: R8
name: no_rule_of_three
trigger:
  section: [global]
  contains_pattern: '(\w+, \w+, and \w+.*\w+, \w+, and \w+)'
---

**规则**：避免反复使用三连结构。

**触发**：检测到同一段落内多次出现 "X, Y, and Z" 模式。

**修复**：变换列举方式：
- 用两个（"X and Y"）
- 用四个
- 用 "such as X" 只举一个例子
- 改写为非列举结构

**原因**：rule-of-three 是 AI 写作的标志性模式。人类写作的列举长度更随机。
