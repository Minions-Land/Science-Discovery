---
id: R3
name: no_hint_as_fact
trigger:
  section: [global]
  contains_pattern: '(~\d+%|approximately \d+|about \d+|roughly \d+)'
---

**规则**：不把暗示当事实。

**触发**：检测到近似数字表述。

**场景**：作者在 notes 里写"大概 12%"或"~30%"→ 不能直接写成 "12%" 或 "30%"。

**修复选项**：
1. 验证后写精确值
2. 用定性描述（"a substantial fraction"）
3. 用占位符 + 注释（`[needs verification: author estimates ~12%]`）

**原因**：Cell/Nature 对数字的零容忍政策——一个未验证的数字可以导致 retraction。
