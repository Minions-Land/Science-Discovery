---
id: R4
name: subject_verb_proximity
trigger:
  section: [global]
  task: [polish]
---

**规则**：主语和动词紧邻。

**要求**：subject 和 verb 之间不要插入长定语从句或插入语。

**示例**：
- ❌ "The method, which was proposed by Smith et al. (2023) and later extended by Jones et al. (2024) to handle multi-modal inputs, achieves state-of-the-art results."
- ✅ "The method achieves state-of-the-art results. Originally proposed by Smith et al. (2023), it was later extended by Jones et al. (2024) to handle multi-modal inputs."

**原则**：读者不应该在找到动词之前忘记主语是什么。
