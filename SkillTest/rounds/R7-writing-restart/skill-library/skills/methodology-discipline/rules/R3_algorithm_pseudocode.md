---
id: R3
name: algorithm_pseudocode
trigger:
  draft_section: [method, approach]
  contains_pattern: '(step 1|step 2|first.*then.*finally|pipeline|workflow)'
---

**规则**：多步流程用算法伪代码。

**触发**：检测到散文中描述多步流程。

**修复**：用 `algorithm2e` 或 `algorithmic` 环境写伪代码。散文中保留 high-level 描述，伪代码给出精确步骤。

**注意**：伪代码不是代码——用数学符号和自然语言混合，不要写 Python。
