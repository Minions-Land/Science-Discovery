---
id: R2
name: remove_filler_openings
trigger:
  section: [global]
  contains_pattern: '(It is worth noting|Importantly,|Notably,|It should be noted|In this section, we|As mentioned earlier)'
---

**规则**：删除冗余开头。

**触发**：检测到 filler phrases。

**修复**：直接删除，让句子从实质内容开始。

**示例**：
- ❌ "It is worth noting that our method achieves…"
- ✅ "Our method achieves…"
- ❌ "In this section, we describe our approach."
- ✅ （直接开始描述，不需要 meta-commentary）
