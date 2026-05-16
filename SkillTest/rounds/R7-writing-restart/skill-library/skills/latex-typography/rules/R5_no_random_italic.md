---
id: R5
name: no_random_italic
trigger:
  section: [global]
  contains_pattern: '\\textit\{(very|highly|significantly|important|key|novel)'
---

**规则**：不要乱用斜体。

**触发**：检测到对强调词的斜体。

**修复**：删除斜体。斜体只用于：
- 数学变量（$x$, $\theta$）
- 外文术语（*in vivo*, *a priori*）
- 书名/期刊名

**注意**：如果你觉得需要斜体来强调，说明句子本身写得不够有力——重写句子。
